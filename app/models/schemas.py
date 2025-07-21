# app/models/schemas.py

from typing import List, Optional
from pydantic import BaseModel, Field


# -------------------------
# INPUT SCHEMA
# -------------------------

class INCIListRequest(BaseModel):
    inci_list: List[str] = Field(..., description="List of INCI names from product")


# -------------------------
# OUTPUT SCHEMAS
# -------------------------

from typing import Optional, List
from pydantic import BaseModel, Field

class BrandedIngredient(BaseModel):
    product_name: str = Field(..., description="Name of the branded ingredient")
    supplier: str = Field(..., description="Supplier or manufacturer")
    matched_inci: List[str] = Field(..., description="INCI names that match this brand")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Match confidence score between 0.0 and 1.0")
    functionality_category: Optional[str] = Field(None, description="Functional category")
    chemical_class_category: Optional[str] = Field(None, description="Chemical class category")
    documentation_url: Optional[str] = Field(None, description="Optional URL to TDS or brochure")
    description: Optional[str] = Field(None, description="Optional summary of the branded ingredient")


class UnmatchedINCI(BaseModel):
    name: str = Field(..., description="Unmatched INCI name")
    common_use: Optional[str] = Field(None, description="Likely function (e.g., solvent, emollient)")
    category: Optional[str] = Field(None, description="Ingredient type category: Base, Moisturizer, etc.")


class Conflict(BaseModel):
    inci_name: str = Field(..., description="INCI name that appears in multiple branded ingredients")
    possible_brands: List[str] = Field(..., description="All branded ingredients it could belong to")
    context: Optional[str] = Field(None, description="Explanation of why this conflict exists")


# -------------------------
# FINAL RESPONSE SCHEMA
# -------------------------

class INCIAnalysisResponse(BaseModel):
    branded_ingredients: List[BrandedIngredient]
    unmatched_inci: List[UnmatchedINCI]
    conflicts: List[Conflict]
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float = Field(..., description="Total time taken in seconds")
