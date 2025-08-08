# app/logic/queries.py

"""Small helpers on the graph (used by predictors)"""

from typing import Iterable, List, Tuple, Dict
import networkx as nx

def branded_candidates_from_inci(G: nx.MultiDiGraph, inci_nodes: Iterable[tuple]) -> List[tuple]:
    out = set()
    for inode in inci_nodes:
        if inode not in G: continue
        for _, b, d in G.out_edges(inode, data=True):
            if d.get("type") == "contains":
                out.add(b)
    return list(out)

def score_candidates_by_overlap(G: nx.MultiDiGraph, query_inci: Iterable[tuple], branded_nodes: Iterable[tuple]) -> List[Tuple[tuple, float, Dict]]:
    qset = set(query_inci)
    scored = []
    for b in branded_nodes:
        branded_inci = {src for src, dst, d in G.in_edges(b, data=True) if d.get("type") == "contains"}
        if not branded_inci: continue
        overlap = len(qset & branded_inci)
        score = overlap / max(len(branded_inci), 1)
        scored.append((b, float(score), {"overlap": overlap, "branded_inci_count": len(branded_inci)}))
    return sorted(scored, key=lambda t: t[1], reverse=True)
