# app/models/schemas.py

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# ---------- Base entities ----------

class BrandedIngredient(BaseModel):
    ingredient_name: str
    original_inci_name: Optional[str] = None
    inci_ids: List[str] = Field(default_factory=list)
    functional_category_ids: List[str] = Field(default_factory=list)
    chemical_class_ids: List[str] = Field(default_factory=list)
    supplier_id: Optional[str] = None
    description: Optional[str] = ""
    documents_id: List[str] = Field(default_factory=list)

class Inci(BaseModel):
    inciName: str

class Supplier(BaseModel):
    supplierName: str

class FunctionalCategory(BaseModel):
    functionalName: str
    level: int
    parent_id: Optional[str] = None

class ChemicalClass(BaseModel):
    chemicalClassName: str
    level: int
    parent_id: Optional[str] = None

class Document(BaseModel):
    folder: str
    key: str
    format: str
    eTag: str
    alt: Optional[str] = ""
    caption: Optional[str] = ""
    description: Optional[str] = ""
    title: Optional[str] = ""

# ---------- INCI Analysis ----------

class AnalyzeInciRequest(BaseModel):
    inci_names: List[str]

    # Put Swagger examples here (works in Pydantic v2)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"inci_names": ["Glycerin", "Niacinamide", "Butylene Glycol"]}
            ]
        }
    }

class AnalyzeInciItem(BaseModel):
    ingredient_name: str
    original_inci_name: Optional[str] = ""
    supplier_id: Optional[str] = None
    description: Optional[str] = ""
    functional_category_ids: List[str] = Field(default_factory=list)
    chemical_class_ids: List[str] = Field(default_factory=list)
    documents_id: List[str] = Field(default_factory=list)

class AnalyzeInciResponse(BaseModel):
    matched: List[AnalyzeInciItem] = Field(default_factory=list)
    unmatched: List[str] = Field(default_factory=list)
    overall_confidence: float = 0.0
    processing_time: float = 0.0

# ---------- Predictions ----------

class PredictCombinationRequest(BaseModel):
    inci_names: List[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"inci_names": ["Glycerin", "Niacinamide"]}
            ]
        }
    }

class PredictionItem(BaseModel):
    branded_id: str
    name: Optional[str] = None
    score: float
    features: Dict[str, Any]

class PredictCombinationResponse(BaseModel):
    predictions: List[PredictionItem] = Field(default_factory=list)
    matched_inci: List[str] = Field(default_factory=list)
    unmatched: List[str] = Field(default_factory=list)
