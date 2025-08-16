# app/db/collections.py

"""Typed collection refs (import these elsewhere)"""

from app.db.mongodb import db

branded_ingredients_col = db["ingre_branded_ingredients"]
inci_col = db["ingre_inci"]
suppliers_col = db["ingre_suppliers"]
functional_categories_col = db["ingre_functional_categories"]
chemical_classes_col = db["ingre_chemical_classes"]
documents_col = db["ingre_documents"]
formulations_col = db["ingre_formulations"]