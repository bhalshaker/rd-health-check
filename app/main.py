from fastapi import FastAPI
from app.routes.healthcheck import healthcheck_router

app= FastAPI(summary="Health Check API", description="API for interacting with health check configurations.", version="1.0.0")

app.include_router(healthcheck_router, tags=["Health Check"])