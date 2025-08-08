# app/api/predictions.py

"""Predict likely branded combinations from INCI"""

from fastapi import APIRouter, HTTPException
from app.logic.graph_builder import build_graph, _node_id
from app.db.collections import inci_col
from app.ml.predict import predict_branded_for_inci
from app.models.schemas import PredictCombinationRequest, PredictCombinationResponse, PredictionItem

router = APIRouter(tags=["Predictions"])

def _norm(s: str) -> str:
    return " ".join((s or "").strip().lower().split())

@router.post("/predict-combination", response_model=PredictCombinationResponse, summary="Predict likely branded combos from INCI")
async def predict_combination(payload: PredictCombinationRequest):
    if not payload.inci_names:
        raise HTTPException(status_code=400, detail="Provide at least one INCI name")

    G = await build_graph(force=False)

    norms = [_norm(x) for x in payload.inci_names if (x or "").strip()]
    inci_docs = await inci_col.find(
        {"$or": [{"inciName": {"$in": norms}}, {"inciName_normalized": {"$in": norms}}]},
        {"_id": 1, "inciName": 1}
    ).to_list(None)

    qnodes = [_node_id("inci", d["_id"]) for d in inci_docs]
    if not qnodes:
        return PredictCombinationResponse(predictions=[], matched_inci=[], unmatched=payload.inci_names)

    preds = predict_branded_for_inci(G, qnodes, top_k=15)
    out = []
    for p in preds:
        (kind, bid) = p["node"]
        meta = G.nodes[p["node"]]
        out.append(PredictionItem(branded_id=bid, name=meta.get("name"), score=p["score"], features=p["features"]))

    matched_inci = [d["inciName"] for d in inci_docs]
    unmatched = [raw for raw in payload.inci_names if _norm(raw) not in { _norm(n) for n in matched_inci }]

    return PredictCombinationResponse(predictions=out, matched_inci=matched_inci, unmatched=unmatched)
