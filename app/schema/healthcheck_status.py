from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class HealthcheckStatusEnum(Enum):
    """
    Enum to represent the health check status.
    """
    FAILURE = "Failure"
    SUCCESS = "Success"
    WARNING = "Warning"

    def __str__(self):
        return self.value
    
@dataclass
class HealthcheckStatus:
    """
    Class to represent the health check status of a system.
    """
    synonym: str
    

@dataclass
class MountPointHealthcheckStatus(HealthcheckStatus):
    """
    Class to represent the health check status of a mount point.
    """
    status: Optional[str]=field(init=False, default=None)
    mount_point: str
    is_mounted: bool
    current_usage: int
    threshold_percentage: int

    def __post_init__(self):
        if not(self.is_mounted):
            self.status=HealthcheckStatusEnum.FAILURE.value
        elif self.current_usage >= self.threshold_percentage:
            self.status=HealthcheckStatusEnum.FAILURE.value
        elif self.current_usage >= (self.threshold_percentage - 5):
            self.status=HealthcheckStatusEnum.WARNING.value
        else:
            self.status=HealthcheckStatusEnum.SUCCESS.value

@dataclass
class WebServiceHealthcheckStatus(HealthcheckStatus):
    """
    Class to represent the health check status of a web service.
    """
    status: Optional[str]=field(init=False, default=None)
    hostname: str
    port: int
    protocol: str
    can_tcp: bool

    def __post_init__(self):
        if self.can_tcp:
            self.status=HealthcheckStatusEnum.SUCCESS.value
        else:
            self.status=HealthcheckStatusEnum.FAILURE.value

@dataclass
class DatabaseHealthcheckStatus(HealthcheckStatus):
    """
    Class to represent the health check status of a database.
    """
    status: Optional[str]=field(init=False, default=None)
    hostname: str
    port: int
    database_type:str
    can_tcp: bool
    db_driver_installed: bool = field(default=None)
    
    def __post_init__(self):
        if self.can_tcp and (self.db_driver_installed is None or self.db_driver_installed):
            self.status = HealthcheckStatusEnum.SUCCESS.value
        else:
            self.status = HealthcheckStatusEnum.FAILURE.value

@dataclass
class RequirementsFileHealthcheckStatus(HealthcheckStatus):
    """
    Class to represent the health check status of a requirements file.
    """
    status: Optional[str]=field(init=False, default=None)
    requirements_file_path: str
    is_file_exists: bool
    are_all_packages_installed: bool=field(default=False)

    def __post_init__(self):
        if self.is_file_exists and self.are_all_packages_installed:
            self.status = HealthcheckStatusEnum.SUCCESS.value
        else:
            self.status = HealthcheckStatusEnum.FAILURE.value

@dataclass
class AllHealthcheckStatus:
    """
    Class to represent the overall health check status of the system.
    """
    mount_points: list[MountPointHealthcheckStatus] = field(default_factory=list)
    webservices: list[WebServiceHealthcheckStatus] = field(default_factory=list)
    databases: list[DatabaseHealthcheckStatus] = field(default_factory=list)
    requirements_files: list[RequirementsFileHealthcheckStatus] = field(default_factory=list)