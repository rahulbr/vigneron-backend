from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Vigneron AI Backend",
    description="Backend API for Vigneron AI frontend application",
    version="1.0.0",
)


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Vigneron AI Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}