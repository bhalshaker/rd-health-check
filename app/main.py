from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.healthcheck import healthcheck_router
from app.routes.staticfiles import static_files_router

app= FastAPI(summary="Health Check API", description="API for interacting with health check configurations.", version="1.0.0")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(healthcheck_router, tags=["Health Check"])
app.include_router(static_files_router)