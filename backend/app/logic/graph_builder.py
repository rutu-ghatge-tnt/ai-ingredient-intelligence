# app/logic/graph_builder.py

"""Build + cache NetworkX graph from Mongo"""

from typing import Optional, Dict
import asyncio
import networkx as nx
from app.db.collections import (
    branded_ingredients_col, inci_col, suppliers_col,
    functional_categories_col, chemical_classes_col
)

_GRAPH: Optional[nx.MultiDiGraph] = None

def _node_id(kind: str, sid) -> tuple[str, str]:
    return (kind, str(sid))

async def _index(col, proj: Dict | None = None) -> Dict[str, dict]:
    docs = await col.find({}, proj or {}).to_list(None)
    return {str(d["_id"]): d for d in docs}

async def build_graph(force: bool = False) -> nx.MultiDiGraph:
    global _GRAPH
    if _GRAPH is not None and not force:
        return _GRAPH

    G = nx.MultiDiGraph()

    inci_map, branded_map, sup_map, func_map, chem_map = await asyncio.gather(
        _index(inci_col, {"_id": 1, "inciName": 1}),
        _index(branded_ingredients_col),
        _index(suppliers_col, {"_id": 1, "supplierName": 1}),
        _index(functional_categories_col),
        _index(chemical_classes_col),
    )

    for iid, d in inci_map.items():
        G.add_node(_node_id("inci", iid), kind="inci", name=d.get("inciName",""))

    for bid, d in branded_map.items():
        G.add_node(_node_id("branded", bid), kind="branded", name=d.get("ingredient_name",""),
                   original_inci_name=d.get("original_inci_name",""))

    for sid, d in sup_map.items():
        G.add_node(_node_id("supplier", sid), kind="supplier", name=d.get("supplierName",""))

    for fid, d in func_map.items():
        G.add_node(_node_id("func", fid), kind="func",
                   name=d.get("functionalName") or d.get("funactionalName",""),
                   level=d.get("level"), parent=str(d.get("parent_id")) if d.get("parent_id") else None)

    for cid, d in chem_map.items():
        G.add_node(_node_id("chem", cid), kind="chem",
                   name=d.get("chemicalClassName",""),
                   level=d.get("level"), parent=str(d.get("parent_id")) if d.get("parent_id") else None)

    # edges
    for bid, d in branded_map.items():
        b = _node_id("branded", bid)
        for iid in (d.get("inci_ids") or []):
            inode = _node_id("inci", iid)
            if inode in G: G.add_edge(inode, b, type="contains")

        sid = d.get("supplier_id") or d.get("SupplierId")
        if sid and _node_id("supplier", sid) in G:
            G.add_edge(b, _node_id("supplier", sid), type="supplied_by")

        for fid in (d.get("functional_category_ids") or []):
            if _node_id("func", fid) in G: G.add_edge(b, _node_id("func", fid), type="has_function")

        for cid in (d.get("chemical_class_ids") or d.get("chemical_class_id") or []):
            if _node_id("chem", cid) in G: G.add_edge(b, _node_id("chem", cid), type="has_class")

    for fid, d in func_map.items():
        if d.get("parent_id"):
            G.add_edge(_node_id("func", d["parent_id"]), _node_id("func", fid), type="parent_of")

    for cid, d in chem_map.items():
        if d.get("parent_id"):
            G.add_edge(_node_id("chem", d["parent_id"]), _node_id("chem", cid), type="parent_of")

    _GRAPH = G
    return G
