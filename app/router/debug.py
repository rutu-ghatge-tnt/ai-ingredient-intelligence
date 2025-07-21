# app/routers/debug.py

from fastapi import APIRouter
from app.db.mongo import branded_collection

router = APIRouter()

@router.get("/debug/sample")
async def get_sample_branded():
    sample = await branded_collection.find_one()
    return sample or {"message": "No data found"}
