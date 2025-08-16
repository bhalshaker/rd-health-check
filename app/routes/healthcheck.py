from fastapi import APIRouter,Depends
from app.depend.authentication import Auth
from app.controller.healthcheck_processing import HealthCheckProcessing
from app.schema.healthcheck_status import MountPointHealthcheckStatus,WebServiceHealthcheckStatus, DatabaseHealthcheckStatus
from app.schema.healthcheck_status import RequirementsFileHealthcheckStatus,AllHealthcheckStatus
from dataclasses import asdict



healthcheck_router = APIRouter()


@healthcheck_router.get(path="/healthcheck",
                        summary="Healthcheck Endpoint",
                        description="This endpoint is used to check the health checkpoints of the application.",
                        response_model=AllHealthcheckStatus)
def healthcheck()-> AllHealthcheckStatus:
    return HealthCheckProcessing.full_health_check()

@healthcheck_router.get(path="/healthcheck/databases",
                        summary="Databases Healthcheck Endpoint",
                        description="This endpoint is used to check the health of databases defined in the health check configuration.",
                        response_model=list[DatabaseHealthcheckStatus])
def healthcheck_databases(is_admin: bool = Depends(Auth.is_admin))-> list[DatabaseHealthcheckStatus]:
    return HealthCheckProcessing.databases_health_check()

@healthcheck_router.get(path="/healthcheck/mountpoints",
                        summary="Mount Points Healthcheck Endpoint",
                        description="This endpoint is used to check the health of mount points defined in the health check configuration.",
                        response_model=list[MountPointHealthcheckStatus])
def healthcheck_mountpoints(is_admin: bool = Depends(Auth.is_admin))-> list[MountPointHealthcheckStatus]:
    mount_point_healthcheck_status=HealthCheckProcessing.mount_points_health_check()
    return mount_point_healthcheck_status

@healthcheck_router.get(path="/healthcheck/webservices",
                        summary="Web Services Healthcheck Endpoint",
                        description="This endpoint is used to check the health of web services defined in the health check configuration.",
                        response_model=list[WebServiceHealthcheckStatus])
def healthcheck_webservices(is_admin: bool = Depends(Auth.is_admin))-> list[WebServiceHealthcheckStatus]:
    return HealthCheckProcessing.webservices_health_check()

@healthcheck_router.get(path="/healthcheck/requirements",
                        summary="Requirement files Healthcheck Endpoint",
                        description="This endpoint is used to check the health of requirements files defined in the health check configuration.",
                        response_model=list[RequirementsFileHealthcheckStatus])
def healthcheck_requirements(is_admin: bool = Depends(Auth.is_admin))-> list[RequirementsFileHealthcheckStatus]:
    return HealthCheckProcessing.all_required_packages_health_check()