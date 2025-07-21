# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.router.analyze import router as analyze_router
from app.router.debug import router as debug_router

# Initialize FastAPI app
app = FastAPI(
    title="AI Ingredient Intelligence API",
    description="API to analyze INCI lists and detect branded ingredients",
    version="1.0.0"
)

# Allow CORS for frontend (Bolt AI React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API route
# app.include_router(analyze.analyze_inci, prefix="/api", tags=["Analysis"])
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])
# app.include_router(debug_router, prefix="/api/debug", tags=["Debug"]) 

# Root endpoint (optional)
@app.get("/")
def root():
    return {"message": "AI Ingredient Intelligence API is running"}
