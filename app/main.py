from fastapi import FastAPI
from app.routes import HealthcheckRouter

app= FastAPI(summary="Health Check API", description="API for interacting with health check configurations.", version="1.0.0")

app.include_router(HealthcheckRouter, prefix="/healthcheck", tags=["Health Check"])