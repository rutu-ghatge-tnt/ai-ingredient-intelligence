# app/main.py
from fastapi import FastAPI
from app.api.analyze_inci import router as analyze_inci_router
from app.db.mongodb import db

app = FastAPI(title="Ingredient Intelligence — Direct INCI Matcher", debug=True)

@app.get("/", tags=["Health"])
async def root():
    # Basic ping to confirm DB connection
    try:
        await db.command("ping")
        mongo = "ok"
    except Exception as e:
        mongo = f"error: {e}"
    return {"status": "ok", "mongo": mongo, "docs": "/docs"}

app.include_router(analyze_inci_router, prefix="/api")
