# app/ml/metrics.py

"""
Ranking metrics used for this problem:
- MAP@K    : Mean Average Precision at K
- NDCG@K   : Normalized Discounted Cumulative Gain at K
- Recall@K : Fraction of true positives retrieved in top-K

All functions operate on per-query lists then average.
"""

from typing import List, Set
import math

def average_precision_at_k(pred_ids: List[str], true_ids: Set[str], k: int) -> float:
    """AP@K for a single query."""
    if not true_ids:
        return 0.0
    hits, score = 0, 0.0
    for i, pid in enumerate(pred_ids[:k], start=1):
        if pid in true_ids:
            hits += 1
            score += hits / i
    return score / min(len(true_ids), k)

def mean_average_precision_at_k(batch_preds: List[List[str]], batch_truths: List[Set[str]], k: int) -> float:
    """MAP@K across queries."""
    scores = [average_precision_at_k(p, t, k) for p, t in zip(batch_preds, batch_truths)]
    return float(sum(scores) / max(len(scores), 1))

def ndcg_at_k(pred_ids: List[str], true_ids: Set[str], k: int) -> float:
    """Binary relevance NDCG@K for a single query."""
    def dcg(items: List[str]) -> float:
        s = 0.0
        for i, pid in enumerate(items[:k], start=1):
            rel = 1.0 if pid in true_ids else 0.0
            if rel:
                s += (2**rel - 1) / math.log2(i + 1)
        return s

    ideal = dcg(list(true_ids))  # ideal ranking puts all relevant first
    if ideal == 0.0:
        return 0.0
    return dcg(pred_ids) / ideal

def mean_ndcg_at_k(batch_preds: List[List[str]], batch_truths: List[Set[str]], k: int) -> float:
    scores = [ndcg_at_k(p, t, k) for p, t in zip(batch_preds, batch_truths)]
    return float(sum(scores) / max(len(scores), 1))

def recall_at_k(pred_ids: List[str], true_ids: Set[str], k: int) -> float:
    """Recall@K for a single query."""
    if not true_ids:
        return 0.0
    hits = sum(1 for pid in pred_ids[:k] if pid in true_ids)
    return hits / len(true_ids)

def mean_recall_at_k(batch_preds: List[List[str]], batch_truths: List[Set[str]], k: int) -> float:
    scores = [recall_at_k(p, t, k) for p, t in zip(batch_preds, batch_truths)]
    return float(sum(scores) / max(len(scores), 1))
