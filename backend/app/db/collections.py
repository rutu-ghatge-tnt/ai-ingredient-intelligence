# app/db/collections.py

"""Typed collection refs (import these elsewhere)"""

from app.db.mongodb import db

branded_ingredients_col = db["branded_ingredients"]
inci_col = db["inci"]
suppliers_col = db["suppliers"]
functional_categories_col = db["functional_categories"]
chemical_classes_col = db["chemical_classes"]
documents_col = db["documents"]
formulations_col = db["formulations"]
