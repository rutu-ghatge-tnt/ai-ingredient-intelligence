# app/logic/matcher.py

"""Batch INCI → branded lookup using normalized fields"""

from typing import List, Tuple
import re, unicodedata
from app.db.collections import branded_ingredients_col, inci_col

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().lower()

async def match_inci_names(inci_names: List[str]) -> Tuple[List[dict], List[str]]:
    if not inci_names:
        return [], []

    normalized = [_norm(x) for x in inci_names if (x or "").strip()]
    inci_docs = await inci_col.find(
        {"inciName_normalized": {"$in": normalized}},
        {"_id": 1, "inciName": 1}
    ).to_list(None)

    inci_ids = [str(d["_id"]) for d in inci_docs]
    branded_docs = await branded_ingredients_col.find(
        {"inci_ids": {"$in": inci_ids}},
        {
            "_id": 1, "ingredient_name": 1, "original_inci_name": 1, "supplier_id": 1,
            "description": 1, "functional_category_ids": 1, "chemical_class_ids": 1,
            "documents_id": 1
        }
    ).to_list(None)

    matched = [{
        "ingredient_name": d.get("ingredient_name", "") or "",
        "original_inci_name": d.get("original_inci_name", "") or "",
        "supplier_id": str(d.get("supplier_id")) if d.get("supplier_id") else None,
        "description": d.get("description", "") or "",
        "functional_category_ids": [str(x) for x in d.get("functional_category_ids", [])],
        "chemical_class_ids": [str(x) for x in d.get("chemical_class_ids", [])],
        "documents_id": [str(x) for x in d.get("documents_id", [])],
    } for d in branded_docs]

    matched_norms = { _norm(doc["inciName"]) for doc in inci_docs }
    unmatched = [raw for raw in inci_names if _norm(raw) not in matched_norms]

    return matched, unmatched
