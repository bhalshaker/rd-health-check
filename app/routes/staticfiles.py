from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

static_files_router=APIRouter()

static_files_router.mount("/static",StaticFiles(directory="app/static"),name="static")

@static_files_router.get("/")
def home():
    return FileResponse("app/static/dashboard-demo.html")