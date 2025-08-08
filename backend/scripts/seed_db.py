# import json
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from tqdm import tqdm

# # --- MongoDB Connection ---
# client = MongoClient("mongodb://localhost:27017")
# db = client["ingredients_db"]

# # Collections
# branded_col = db["branded_ingredients"]
# inci_col = db["inci"]
# supplier_col = db["suppliers"]
# func_cat_col = db["functional_categories"]
# chem_class_col = db["chemical_classes"]
# docs_col = db["documents"]

# # --- Caches to avoid duplicates ---
# inci_cache = {}
# supplier_cache = {}
# func_cat_cache = {}
# chem_class_cache = {}

# # --- Helper functions ---
# def get_or_create_inci(name):
#     if name in inci_cache:
#         return inci_cache[name]
#     doc = inci_col.find_one({"inciName": name})
#     if doc:
#         _id = doc["_id"]
#     else:
#         _id = inci_col.insert_one({"inciName": name}).inserted_id
#     inci_cache[name] = _id
#     return _id

# def get_or_create_supplier(name):
#     if name in supplier_cache:
#         return supplier_cache[name]
#     doc = supplier_col.find_one({"supplierName": name})
#     if doc:
#         _id = doc["_id"]
#     else:
#         _id = supplier_col.insert_one({"supplierName": name}).inserted_id
#     supplier_cache[name] = _id
#     return _id

# def get_or_create_category(tree, col, cache):
#     """
#     tree: list like ["Skin Conditioning Agents", "Emollients"]
#     col: MongoDB collection
#     cache: dict for local memory
#     """
#     parent_id = None
#     for level, name in enumerate(tree, start=1):
#         key = (name, parent_id)
#         if key in cache:
#             _id = cache[key]
#         else:
#             doc = col.find_one({"name": name, "parent_id": parent_id})
#             if doc:
#                 _id = doc["_id"]
#             else:
#                 _id = col.insert_one({
#                     "name": name,
#                     "level": level,
#                     "parent_id": parent_id
#                 }).inserted_id
#             cache[key] = _id
#         parent_id = _id
#     return parent_id  # return deepest level id

# # --- Load JSON Data ---
# with open("cleaned_ingredients.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# # --- Process each ingredient ---
# for item in tqdm(data, desc="Seeding data"):
#     inci_ids = [get_or_create_inci(n) for n in item.get("inci_names", [])]
#     supplier_id = get_or_create_supplier(item.get("supplier"))

#     func_ids = []
#     for tree in item.get("functionality_category_tree", []):
#         func_ids.append(get_or_create_category(tree, func_cat_col, func_cat_cache))

#     chem_ids = []
#     for tree in item.get("chemical_class_category_tree", []):
#         chem_ids.append(get_or_create_category(tree, chem_class_col, chem_class_cache))

#     # Insert into branded_ingredients
#     branded_col.insert_one({
#         "ingredient_name": item.get("ingredient_name"),
#         "original_inci_name": item.get("original_inci_name"),
#         "inci_ids": inci_ids,
#         "functional_category_ids": func_ids,
#         "chemical_class_ids": chem_ids,
#         "supplierId": supplier_id,
#         "description": item.get("description", ""),
#         "documentsId": []  # placeholder for now
#     })

# print("✅ Seeding completed!")


# scripts/seed.py

"""
Seeds MongoDB with cleaned ingredient data AND bootstraps weak training labels.

What this does:
1) Inserts/links:
   - INCI                    -> collection: inci
   - Suppliers               -> suppliers
   - Functional categories   -> functional_categories (with hierarchy)
   - Chemical classes        -> chemical_classes (with hierarchy)
   - Branded ingredients     -> branded_ingredients (links to all above)
2) Creates helpful normalized fields for search/index:
   - inci.inciName_normalized
   - functional_categories.functionalName_normalized
   - chemical_classes.chemicalClassName_normalized
3) (NEW) Bootstraps weak **formulations** labels for ML training:
   - For each branded ingredient B:
       query INCI set = B.inci_ids
       true branded   = [B._id]
     -> inserts into formulations as one "auto_*" doc with split="train"
4) (Optional) Creates indexes for faster lookups.

Usage:
  python scripts/seed.py
  # or customize options below in __main__
"""

import json
import unicodedata
import re
from typing import List, Optional, Tuple
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from tqdm import tqdm

# -------------------
# Config
# -------------------
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ingredients_db"
DATA_FILE = "cleaned_ingredients.json"

# Toggle behaviors
CREATE_INDEXES = True
CREATE_WEAK_FORMULATIONS = True
WEAK_LIMIT = None  # set an int to cap how many weak formulations to insert

# -------------------
# Connect
# -------------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
branded_col = db["branded_ingredients"]
inci_col = db["inci"]
supplier_col = db["suppliers"]
func_cat_col = db["functional_categories"]
chem_class_col = db["chemical_classes"]
docs_col = db["documents"]
formulations_col = db["formulations"]

# -------------------
# Caches (avoid dups)
# -------------------
inci_cache = {}          # key: normalized INCI name -> _id
supplier_cache = {}      # key: supplierName -> _id
func_cat_cache = {}      # key: (name, parent_id) -> _id
chem_class_cache = {}    # key: (name, parent_id) -> _id

# -------------------
# Helpers
# -------------------
def normalize_text(s: str) -> str:
    """Remove accents, lowercase, collapse spaces for search normalization."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).strip().lower()

def get_or_create_inci(name: Optional[str]) -> Optional[ObjectId]:
    """Create/find an INCI by name; also stores a normalized variant for fast search."""
    if not name:
        return None
    norm = normalize_text(name)
    if norm in inci_cache:
        return inci_cache[norm]
    doc = inci_col.find_one({"inciName_normalized": norm}, {"_id": 1})
    if doc:
        _id = doc["_id"]
    else:
        _id = inci_col.insert_one({"inciName": name, "inciName_normalized": norm}).inserted_id
    inci_cache[norm] = _id
    return _id

def get_or_create_supplier(name: Optional[str]) -> Optional[ObjectId]:
    """Create/find a supplier by exact name (no normalization for display accuracy)."""
    if not name:
        return None
    if name in supplier_cache:
        return supplier_cache[name]
    doc = supplier_col.find_one({"supplierName": name}, {"_id": 1})
    if doc:
        _id = doc["_id"]
    else:
        _id = supplier_col.insert_one({"supplierName": name}).inserted_id
    supplier_cache[name] = _id
    return _id

def get_or_create_category(
    tree: List[str],
    col,
    cache: dict,
    name_field: str,
    norm_field: str
) -> Optional[ObjectId]:
    """
    Create/find a nested category structure.

    Args:
      tree: e.g. ["Skin Conditioning Agents", "Emollients"]
      col:  functional_categories or chemical_classes collection
      cache: local cache dict
      name_field: "functionalName" | "chemicalClassName"
      norm_field: "functionalName_normalized" | "chemicalClassName_normalized"

    Returns:
      The deepest level category _id (ObjectId) or None.
    """
    parent_id = None
    for level, name in enumerate(tree, start=1):
        key = (name, parent_id)
        if key in cache:
            _id = cache[key]
        else:
            doc = col.find_one({name_field: name, "parent_id": parent_id}, {"_id": 1})
            if doc:
                _id = doc["_id"]
            else:
                _id = col.insert_one({
                    name_field: name,
                    norm_field: normalize_text(name),
                    "level": level,
                    "parent_id": parent_id
                }).inserted_id
            cache[key] = _id
        parent_id = _id
    return parent_id

def create_indexes():
    """Create helpful indexes once. Safe to run repeatedly."""
    # INCI normalized field for quick lookup
    inci_col.create_index([("inciName_normalized", ASCENDING)], name="idx_inci_norm")

    # Category normalized fields
    func_cat_col.create_index([("functionalName_normalized", ASCENDING)], name="idx_func_norm")
    chem_class_col.create_index([("chemicalClassName_normalized", ASCENDING)], name="idx_chem_norm")

    # Branded lookups by references
    branded_col.create_index([("inci_ids", ASCENDING)], name="idx_branded_inci_ids")
    branded_col.create_index([("supplier_id", ASCENDING)], name="idx_branded_supplier")
    branded_col.create_index([("functional_category_ids", ASCENDING)], name="idx_branded_func")
    branded_col.create_index([("chemical_class_ids", ASCENDING)], name="idx_branded_chem")

# -------------------
# Seed main entities
# -------------------
def seed_main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in tqdm(data, desc="Seeding data"):
        # INCI references
        inci_ids = [oid for n in item.get("inci_names", []) for oid in [get_or_create_inci(n)] if oid]

        # Supplier
        supplier_id = get_or_create_supplier(item.get("supplier"))

        # Functional categories (deepest node per path)
        func_ids: List[ObjectId] = []
        for tree in item.get("functionality_category_tree", []):
            fid = get_or_create_category(
                tree=tree,
                col=func_cat_col,
                cache=func_cat_cache,
                name_field="functionalName",
                norm_field="functionalName_normalized",
            )
            if fid:
                func_ids.append(fid)

        # Chemical classes (deepest node per path)
        chem_ids: List[ObjectId] = []
        for tree in item.get("chemical_class_category_tree", []):
            cid = get_or_create_category(
                tree=tree,
                col=chem_class_col,
                cache=chem_class_cache,
                name_field="chemicalClassName",
                norm_field="chemicalClassName_normalized",
            )
            if cid:
                chem_ids.append(cid)

        # Insert branded ingredient (one per input row)
        branded_col.insert_one({
            "ingredient_name": item.get("ingredient_name"),
            "original_inci_name": item.get("original_inci_name"),
            "inci_ids": inci_ids,                         # [ObjectId, ...]
            "functional_category_ids": func_ids,          # [ObjectId, ...]
            "chemical_class_ids": chem_ids,               # [ObjectId, ...]
            "supplier_id": supplier_id,                   # ObjectId or None
            "description": item.get("description", "") or "",
            "documents_id": [],                           # placeholder
        })

# -------------------
# Weak formulations bootstrap
# -------------------
def bootstrap_weak_formulations(limit: Optional[int] = None):
    """
    Create weak labels for ML:
      For each branded ingredient B:
        - Query INCI set     = B.inci_ids
        - True branded set   = [B._id]
      -> Insert into 'formulations' with name 'auto_<ingredient_name>' and split 'train'

    This gives you immediate training data for LightGBM;
    later you can replace/augment with human-verified formulations.
    """
    count = 0
    cursor = branded_col.find({}, {"_id": 1, "ingredient_name": 1, "inci_ids": 1})
    bulk: List[dict] = []

    for doc in cursor:
        if limit and count >= limit:
            break
        inci_ids = [str(i) for i in (doc.get("inci_ids") or [])]  # stringify for model/graph node keys
        if not inci_ids:
            continue
        bulk.append({
            "name": f"auto_{doc.get('ingredient_name', 'unnamed')}",
            "inci_ids": inci_ids,                          # [str(ObjectId), ...]
            "branded_true_ids": [str(doc["_id"])],         # [str(ObjectId)]
            "split": "train"
        })
        count += 1

    if bulk:
        formulations_col.insert_many(bulk)
        print(f"🧪 Bootstrapped {len(bulk)} weak formulations.")
    else:
        print("No weak formulations created (no branded items with INCI).")

# -------------------
# Main
# -------------------
if __name__ == "__main__":
    if CREATE_INDEXES:
        create_indexes()
        print("✅ Indexes ensured.")

    seed_main()
    print("✅ Seeding of core collections completed.")

    if CREATE_WEAK_FORMULATIONS:
        bootstrap_weak_formulations(limit=WEAK_LIMIT)

    print("🎉 All done.")
