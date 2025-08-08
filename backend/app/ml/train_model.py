# app/ml/train_model.py

"""End-to-end training with LightGBM (CatBoost optional) + type-safe scoring."""

import argparse
import os
import pickle
from typing import List, Dict, Any, Tuple, Set

import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score

from lightgbm import LGBMClassifier
try:
    from catboost import CatBoostClassifier
    _CATBOOST_AVAILABLE = True
except Exception:
    _CATBOOST_AVAILABLE = False

from app.config import MODEL_PATH
from app.db.sync_mongodb import sync_db         # <-- sync (PyMongo) DB for training
from app.logic.graph_builder import build_graph
from app.ml.features import branded_feature_vector
from app.ml.dataset import build_dataset
from app.ml.metrics import (
    mean_average_precision_at_k,
    mean_ndcg_at_k,
    mean_recall_at_k,
)


# ---------- coercion helper ----------
def _scores_from_model(model, X) -> np.ndarray:
    """
    Return a 1-D float64 numpy array of scores for the positive class,
    regardless of estimator return type.
    """
    try:
        proba = model.predict_proba(X)
    except Exception:
        proba = model.predict(X)

    # Coerce to dense float64 ndarray
    try:
        import scipy.sparse as sp  # optional dependency
        if sp.issparse(proba):
            proba = proba.toarray()
    except Exception:
        pass

    arr = np.asarray(proba)
    if arr.ndim == 2:
        if arr.shape[1] >= 2:
            arr = arr[:, 1]
        else:
            arr = arr[:, 0]
    return np.asarray(arr, dtype=np.float64)


# ---------- model trainers ----------
def train_lightgbm(X: np.ndarray, y: np.ndarray):
    model = LGBMClassifier(
        objective="binary",
        n_estimators=800,
        learning_rate=0.05,
        num_leaves=63,
        max_depth=-1,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=1e-3,
        reg_lambda=1e-2,
    )
    pos = max(int(y.sum()), 1)
    neg = max(int((y == 0).sum()), 1)
    model.set_params(scale_pos_weight=neg / pos)
    model.fit(X, y)
    return model


def train_catboost(X: np.ndarray, y: np.ndarray):
    if not _CATBOOST_AVAILABLE:
        raise RuntimeError("CatBoost not installed. pip install catboost")
    model = CatBoostClassifier(
        loss_function="Logloss",
        iterations=1000,
        learning_rate=0.05,
        depth=6,
        l2_leaf_reg=3.0,
        random_seed=42,
        verbose=False,
        auto_class_weights="Balanced",
    )
    model.fit(X, y)
    return model


# ---------- feature vectorization / eval ----------
def _vectorize_features(G, samples: List[Dict[str, Any]]):
    X, y, branded_ids, query_inci_ids_per_sample = [], [], [], []
    for s in samples:
        bnode = ("branded", s["branded_id"])
        qnodes = [("inci", i) for i in s["query_inci_ids"]]
        feats = branded_feature_vector(G, qnodes, bnode)
        X.append([
            float(feats["overlap_count"]),
            float(feats["branded_inci_total"]),
            float(feats["supplier_degree"]),
            float(feats["func_degree"]),
            float(feats["chem_degree"]),
        ])
        y.append(int(s["label"]))
        branded_ids.append(s["branded_id"])
        query_inci_ids_per_sample.append(s["query_inci_ids"])
    return np.array(X, dtype=np.float64), np.array(y, dtype=np.int32), branded_ids, query_inci_ids_per_sample


def _group_ids_for_cv(query_inci_ids_per_sample: List[List[str]]) -> np.ndarray:
    keys = ["|".join(sorted(q)) for q in query_inci_ids_per_sample]
    uniq = {k: i for i, k in enumerate(sorted(set(keys)))}
    return np.array([uniq[k] for k in keys], dtype=np.int32)


def _rank_eval_from_raw_scores(
    branded_ids: List[str],
    query_inci_ids_per_sample: List[List[str]],
    y_true: np.ndarray,
    y_prob: np.ndarray,
    k_values=(3, 5, 10),
) -> Dict[str, float]:
    # regroup by query key
    by_query: Dict[str, List[Tuple[str, float, int]]] = {}
    for bid, qids, yt, yp in zip(branded_ids, query_inci_ids_per_sample, y_true, y_prob):
        qkey = "|".join(sorted(qids))
        by_query.setdefault(qkey, []).append((bid, float(yp), int(yt)))

    preds_lists: List[List[str]] = []
    truths_sets: List[Set[str]] = []
    for rows in by_query.values():
        rows.sort(key=lambda t: t[1], reverse=True)
        preds = [bid for (bid, score, label) in rows]
        truth = {bid for (bid, score, label) in rows if label == 1}
        preds_lists.append(preds)
        truths_sets.append(truth)

    out: Dict[str, float] = {}
    for k in k_values:
        out[f"MAP@{k}"] = float(mean_average_precision_at_k(preds_lists, truths_sets, k))
        out[f"NDCG@{k}"] = float(mean_ndcg_at_k(preds_lists, truths_sets, k))
        out[f"Recall@{k}"] = float(mean_recall_at_k(preds_lists, truths_sets, k))
    return out


# ---------- main ----------
def main(args):
    # Build/load graph (await inside sync script)
    G = __import__("asyncio").get_event_loop().run_until_complete(
        build_graph(force=args.force_rebuild)
    )

    # Use **sync** collection for dataset building
    formulations_col = sync_db["formulations"]

    # Build dataset
    samples, _truths = build_dataset(
        G,
        formulations_col,
        split=None if args.split == "None" else args.split,
        negative_multiplier=args.neg_mult,
    )
    if not samples:
        print("No training samples found. Populate 'formulations' collection and retry.")
        return

    # Features
    X, y, branded_ids, query_inci_ids_per_sample = _vectorize_features(G, samples)

    # CV sanity (group by query to avoid leakage)
    groups = _group_ids_for_cv(query_inci_ids_per_sample)
    n_splits = max(min(5, len(set(groups))), 2)
    gkf = GroupKFold(n_splits=n_splits)

    cv_aucs: list[float] = []
    for fold, (tr, va) in enumerate(gkf.split(X, y, groups), start=1):
        Xtr, Xva = X[tr], X[va]
        ytr, yva = y[tr], y[va]
        model = train_lightgbm(Xtr, ytr) if args.model == "lgbm" else train_catboost(Xtr, ytr)
        yprob = _scores_from_model(model, Xva)                     # float64
        auc = float(roc_auc_score(yva.astype(int), yprob))         # cast to Python float
        cv_aucs.append(auc)
        print(f"[Fold {fold}] ROC-AUC: {auc:.4f}")

    if cv_aucs:
        auc_mean = float(np.mean(cv_aucs))
        auc_std = float(np.std(cv_aucs))
        print(f"CV AUC mean: {auc_mean:.4f}  std: {auc_std:.4f}")

    # Fit final model on all data
    model = train_lightgbm(X, y) if args.model == "lgbm" else train_catboost(X, y)

    # Train-set ranking proxy (visibility)
    yprob_all = _scores_from_model(model, X)
    rank_scores = _rank_eval_from_raw_scores(
        branded_ids,
        query_inci_ids_per_sample,
        y_true=y,
        y_prob=yprob_all,
        k_values=(3, 5, 10),
    )
    print("Ranking metrics (train/all):", {k: float(round(v, 4)) for k, v in rank_scores.items()})

    # Save model
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="lgbm", choices=["lgbm", "catboost"])
    parser.add_argument("--split", type=str, default="train", help='Use "train" or "None" for all docs')
    parser.add_argument("--valid_split", type=str, default="valid")  # reserved if you add a separate valid set
    parser.add_argument("--neg_mult", type=float, default=2.0)
    parser.add_argument("--force_rebuild", action="store_true")
    args = parser.parse_args()
    main(args)
