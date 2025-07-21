from fastapi import APIRouter, HTTPException
from time import time

from app.models.schemas import INCIListRequest, INCIAnalysisResponse, BrandedIngredient, UnmatchedINCI, Conflict
from app.db.mongo import branded_collection, inci_collection
from app.utils.preprocess import normalize_inci_list
from app.utils.scoring import score_matches
from app.utils.graph import build_ingredient_graph
from app.utils.ml_predict import predict_brands_from_ml

router = APIRouter()

@router.post("/analyze-inci", response_model=INCIAnalysisResponse)
async def analyze_inci(request: INCIListRequest):
    try:
        start = time()
        original_inci = request.inci_list
        cleaned_inci = normalize_inci_list(original_inci)

        # 1. Load branded ingredients database
        branded_data = await branded_collection.find().to_list(length=None)

        # 2. Rule-Based Scoring
        matched, conflicts, unmatched = score_matches(cleaned_inci, branded_data)

        # 3. Graph Intelligence (confidence multiplier)
        matched_dicts = [m.dict() if hasattr(m, "dict") else dict(m) for m in matched]
        graph_confidence = build_ingredient_graph(cleaned_inci, matched_dicts)

        # 4. ML Prediction Layer (if trained)
        ml_predictions = predict_brands_from_ml(cleaned_inci)

        # 5. Add ML predictions to matched list (avoid duplicates)
        for pred in ml_predictions:
            if all(m.product_name != pred.get("product_name") for m in matched):
                matched.append(BrandedIngredient(**pred))

        # 6. Calculate final confidence score
        total_confidence = min(
            1.0,
            (sum(m.confidence_score for m in matched) / max(len(matched), 1)) * graph_confidence
        )

        # 7. Enrich unmatched INCI info from MongoDB
        unmatched_details = []
        for inci in unmatched:
            record = await inci_collection.find_one({"name": inci})
            unmatched_details.append(UnmatchedINCI(
                name=inci,
                common_use=record.get("common_use") if record else None,
                category=record.get("category") if record else None
            ))

        # 8. Return full response
        return INCIAnalysisResponse(
            branded_ingredients=matched,
            unmatched_inci=unmatched_details,
            conflicts=conflicts,
            overall_confidence=round(total_confidence, 3),
            processing_time=round(time() - start, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing INCI list: {str(e)}")
