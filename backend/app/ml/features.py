# app/ml/features.py

"""Feature vectors for ML scoring (no starred-unpack to keep Pylance happy)."""

from typing import Iterable, Dict, Any, Set, Tuple
import networkx as nx


def _incoming_inci(G: nx.MultiDiGraph, branded_node: Tuple[str, str]) -> Set[Tuple[str, str]]:
    """
    Return the set of INCI nodes that connect to the given branded node
    via edges of type 'contains'.
    """
    inci_nodes: Set[Tuple[str, str]] = set()
    for src, dst, data in G.in_edges(branded_node, data=True):
        # src is a node like ("inci", "<id>")
        if data.get("type") == "contains":
            inci_nodes.add(src)
    return inci_nodes


def _out_degree_by_type(G: nx.MultiDiGraph, node: Tuple[str, str], edge_type: str) -> int:
    """
    Count outgoing edges of a given type from 'node'.
    """
    count = 0
    for _src, _dst, data in G.out_edges(node, data=True):
        if data.get("type") == edge_type:
            count += 1
    return count


def branded_feature_vector(
    G: nx.MultiDiGraph,
    query_inci_nodes: Iterable[Tuple[str, str]],
    branded_node: Tuple[str, str],
) -> Dict[str, Any]:
    """
    Compute simple structural features for a branded candidate given a query:
      - overlap_count:    |query_inci ∩ branded_inci|
      - branded_inci_total
      - supplier_degree:  # of 'supplied_by' edges
      - func_degree:      # of 'has_function' edges
      - chem_degree:      # of 'has_class' edges
    """
    qset = set(query_inci_nodes)

    branded_inci = _incoming_inci(G, branded_node)
    supplier_deg = _out_degree_by_type(G, branded_node, "supplied_by")
    func_deg = _out_degree_by_type(G, branded_node, "has_function")
    chem_deg = _out_degree_by_type(G, branded_node, "has_class")

    return {
        "overlap_count": len(qset.intersection(branded_inci)),
        "branded_inci_total": len(branded_inci),
        "supplier_degree": supplier_deg,
        "func_degree": func_deg,
        "chem_degree": chem_deg,
    }
