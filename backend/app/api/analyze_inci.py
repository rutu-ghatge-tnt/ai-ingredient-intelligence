# app/api/analyze_inci.py

"""Swagger-friendly INCI analysis endpoint"""

from fastapi import APIRouter
import time
from app.logic.matcher import match_inci_names
from app.models.schemas import AnalyzeInciRequest, AnalyzeInciResponse, AnalyzeInciItem

router = APIRouter(tags=["INCI Analysis"])

@router.post("/analyze-inci", response_model=AnalyzeInciResponse, summary="Analyze INCI and list matching branded ingredients")
async def analyze_inci(payload: AnalyzeInciRequest):
    start = time.time()
    matched_raw, unmatched = await match_inci_names(payload.inci_names)
    items = [AnalyzeInciItem(**m) for m in matched_raw]
    conf = round(len(items) / max(len(payload.inci_names), 1), 2)
    return AnalyzeInciResponse(
        matched=items,
        unmatched=unmatched,
        overall_confidence=conf,
        processing_time=round(time.time() - start, 3)
    )
