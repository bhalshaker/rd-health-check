from fastapi import FastAPI
from app.routes import HealthcheckRouter

app= FastAPI()

app.include_router(HealthcheckRouter, prefix="/healthcheck", tags=["Health Check"])