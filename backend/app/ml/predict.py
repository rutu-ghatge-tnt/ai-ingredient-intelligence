# app/ml/predict.py

"""Prediction: use LightGBM if available, else graph-overlap baseline"""

import os, pickle
from typing import List, Dict, Any, Tuple
import networkx as nx
from app.config import MODEL_PATH
from app.logic.queries import branded_candidates_from_inci, score_candidates_by_overlap
from app.ml.features import branded_feature_vector

_MODEL = None

def _load_model():
    global _MODEL
    if _MODEL is not None: return _MODEL
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f: _MODEL = pickle.load(f)
    return _MODEL

def predict_branded_for_inci(G: nx.MultiDiGraph, query_inci_nodes: List[tuple], top_k: int = 10) -> List[Dict[str, Any]]:
    candidates = branded_candidates_from_inci(G, query_inci_nodes)
    if not candidates: return []

    model = _load_model()
    if model is None:
        scored = score_candidates_by_overlap(G, query_inci_nodes, candidates)[:top_k]
        return [{"node": b, "score": s, "features": meta} for (b, s, meta) in scored]

    X, nodes, feats_list = [], [], []
    for b in candidates:
        feats = branded_feature_vector(G, query_inci_nodes, b)
        X.append([feats["overlap_count"], feats["branded_inci_total"], feats["supplier_degree"], feats["func_degree"], feats["chem_degree"]])
        nodes.append(b); feats_list.append(feats)

    try:
        y = model.predict_proba(X)[:, 1]
    except Exception:
        y = model.predict(X)

    scored = sorted(zip(nodes, y, feats_list), key=lambda t: t[1], reverse=True)[:top_k]
    return [{"node": n, "score": float(s), "features": f} for (n, s, f) in scored]
