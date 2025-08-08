# app/main.py

"""FastAPI app with Swagger docs + lifespan handlers (no @on_event)"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analyze_inci, predictions
from app.db.mongodb import client
# Optional: prebuild the graph at startup (uncomment if you want)
# from app.logic.graph_builder import build_graph

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # --- startup ---
    await client.admin.command("ping")          # verify Mongo is reachable
    # await build_graph(force=True)             # optional: warm the graph cache
    yield
    # --- shutdown ---
    client.close()                               # cleanly close Mongo client

app = FastAPI(
    title="Ingredient Intelligence API",
    version="1.0.0",
    description="Analyze INCI, match branded ingredients, and predict likely combinations using a graph + ML.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_inci.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")

@app.get("/", tags=["Health"])
async def root():
    return {"status": "Backend running"}
