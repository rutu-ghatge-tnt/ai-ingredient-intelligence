# app/ml/dataset.py

"""
Training data builder.

Expected label source (you can rename/adjust):
- Collection: 'formulations'
- Doc schema (example):
  {
    _id: ObjectId(...),
    name: "Day Cream X",
    inci_ids: [ "64f...a1", "64f...b2", ... ],          # INCI ids used in the formulation
    branded_true_ids: [ "65a...9c", "65b...10", ... ],  # Branded ingredient ids truly used
    # optional:
    created_at, split: "train"|"valid"|"test"
  }

We build (query, candidate) pairs:
- Query = set of INCI for a formulation
- Candidates = all branded nodes reachable from any query INCI (graph neighbors)
- Label = 1 if candidate in branded_true_ids else 0

Hard negatives: candidates not in truth but near in graph. Optionally add random negatives.
"""

from typing import Dict, List, Tuple, Iterable, Set
import random
from pymongo.collection import Collection
import networkx as nx

from app.logic.graph_builder import _node_id
from app.logic.queries import branded_candidates_from_inci

def _strid(x) -> str:
    return str(x)

def _inci_nodes_from_ids(G: nx.MultiDiGraph, inci_ids: Iterable[str]) -> List[tuple]:
    return [_node_id("inci", _strid(i)) for i in inci_ids if (_node_id("inci", _strid(i)) in G)]

def build_pairs_for_doc(
    G: nx.MultiDiGraph,
    doc: Dict,
    negative_multiplier: float = 1.0,
) -> Tuple[List[Dict], Set[str]]:
    """
    Build training pairs for one formulation document.
    Returns (pairs, true_set).
    Each pair -> { 'branded_id': str, 'label': 0/1, 'query_inci_ids': [str] }
    """
    query_inci_ids: List[str] = [ _strid(i) for i in (doc.get("inci_ids") or []) ]
    true_branded_ids: Set[str] = set(_strid(i) for i in (doc.get("branded_true_ids") or []))

    if not query_inci_ids:
        return [], set()

    query_inci_nodes = _inci_nodes_from_ids(G, query_inci_ids)

    # Graph candidate set (nearby branded via 'contains')
    candidates_nodes = set(branded_candidates_from_inci(G, query_inci_nodes))
    candidates_ids = [ node_id for (_kind, node_id) in candidates_nodes ]

    # Split positives/negatives
    pos_ids = [bid for bid in candidates_ids if bid in true_branded_ids]
    neg_ids = [bid for bid in candidates_ids if bid not in true_branded_ids]

    # Downsample negatives to control class balance
    neg_keep = int(len(pos_ids) * negative_multiplier) if negative_multiplier > 0 else len(neg_ids)
    if neg_keep > 0 and len(neg_ids) > neg_keep:
        random.shuffle(neg_ids)
        neg_ids = neg_ids[:neg_keep]

    pairs = []
    for bid in pos_ids:
        pairs.append({
            "branded_id": bid,
            "label": 1,
            "query_inci_ids": query_inci_ids,
        })
    for bid in neg_ids:
        pairs.append({
            "branded_id": bid,
            "label": 0,
            "query_inci_ids": query_inci_ids,
        })

    return pairs, true_branded_ids

def fetch_split(formulations_col: Collection, split: str | None):
    """Fetch docs for a split; if split is None, fetch all."""
    q = {} if split is None else {"split": split}
    return list(formulations_col.find(q, {"_id": 1, "inci_ids": 1, "branded_true_ids": 1}))

def build_dataset(
    G: nx.MultiDiGraph,
    formulations_col: Collection,
    split: str | None,
    negative_multiplier: float = 2.0,
) -> Tuple[List[Dict], List[Set[str]]]:
    """
    Build dataset for a split.
    Returns:
      samples: [{ branded_id, label, query_inci_ids }]
      truths:  [ set(true_branded_ids) per doc ] (aligned to queries order)
    """
    docs = fetch_split(formulations_col, split)
    samples: List[Dict] = []
    truths: List[Set[str]] = []

    for doc in docs:
        pairs, true_set = build_pairs_for_doc(G, doc, negative_multiplier=negative_multiplier)
        if not pairs:
            continue
        samples.extend(pairs)
        truths.append(true_set)

    return samples, truths
