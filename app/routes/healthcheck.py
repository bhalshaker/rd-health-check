from fastapi import APIRouter

healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck")
def healthcheck():
    pass

@healthcheck_router.get("/healthcheck/databases")
def healthcheck_databases():
    pass

@healthcheck_router.get("/healthcheck/mountpoints")
def healthcheck_mountpoints():
    pass

@healthcheck_router.get("/healthcheck/webservices")
def healthcheck_webservices():
    pass