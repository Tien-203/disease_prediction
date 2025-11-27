"""API v1 router aggregation"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, symptoms, diseases, prediction, auth, model, dataset

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
api_router.include_router(diseases.router, prefix="/diseases", tags=["diseases"])
api_router.include_router(prediction.router, prefix="/predict", tags=["prediction"])
api_router.include_router(model.router, prefix="/model", tags=["model"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])

