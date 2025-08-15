import os

from .healthcheck_foundation import (config_schmema_is_not_empty,is_valid_health_check_type_element)
from .healthcheck_foundation import (is_file_system_mounted)
from schema import MountPointHealthcheckStatus,WebServiceHealthcheckStatus,RequirementsFileHealthcheckStatus,DatabaseHealthcheckStatus
from .tcp_based_connection import TcpBasedConnection
from .external_file_processing import ExternalFileProcessing
from .terminal_processing import TerminalProcessing

class HealthCheckProcessing:
    """ A class to handle health check processing tasks such as reading configuration files and performing health checks.
    """
    @staticmethod
    def read_healthcheck_config()->list[dict]:
        """
        Reads the health check configuration from a file.
        
        Returns:
            list[dict]: The health check configuration.
        """
        # Get the path to the health check configuration file from environment variable or use default
        config_file_location = os.getenv('HEALTH_CHECK_CONFIG_FILE', 'health_check_config.json')
        # Check if the file exists
        if not ExternalFileProcessing.file_exists(config_file_location):
            return []  # Return an empty list if the file does not exist
        # Read the health check configuration file and return its content as a list of dictionaries
        config_file_content = ExternalFileProcessing.load_health_check_json_schema(config_file_location)
        # Verify if the config schema is not empty
        if not config_schmema_is_not_empty(config_file_content):
            return []
        # Vertify all elements in the config schema are valid
        if not all(is_valid_health_check_type_element(element) for element in config_file_content):
            return []
        return config_file_content  # Return the health check configuration as a list of dictionaries

    def read_and_filter_healthcheck_config(check_type:str,healthcheck_config:list[dict]=None) -> list[dict]:
        """
        Reads the health check configuration and filters it by check type.
        
        Args:
            check_type (str): The type of health check to filter by.
            healthcheck_config list[dict]: Optional; if provided, it will be used instead of reading from the file.
            
        Returns:
            list[dict]: The filtered health check configuration.
        """
        # Read the health check configuration
        if healthcheck_config is None:
            healthcheck_config = HealthCheckProcessing.read_healthcheck_config()
        # Filter the configuration by the specified check type
        return [element for element in healthcheck_config if element.get('check_type') == check_type]

    # Webservices health check
    def webservice_health_check(webservice:dict) -> WebServiceHealthcheckStatus:
        """
        Perform a health check on a single web service.
        
        Args:
            webservice (dict): The web service configuration.
            
        Returns:
            WebServiceHealthcheckStatus: The result of the web service health check.
        """
        can_establish_tcp = TcpBasedConnection.establish_tcp_connection(
            webservice['hostname'],
            webservice['port']
        )
        return WebServiceHealthcheckStatus(
            synonym=webservice['synonym'],
            hostname=webservice['hostname'],
            port=webservice['port'],
            protocol=webservice['protocol'],
            can_tcp=can_establish_tcp
        )


    # Webservices health check
    def webservices_health_check(webservices:list[dict]) -> list[WebServiceHealthcheckStatus]:
        """
        Perform health checks on web services.
        Args:
            webservices (list[dict]): The list of web service configurations.
        Returns:
            list[WebServiceHealthcheckStatus]: The results of the web services health checks.
        """
        # Filter the web services from the health check configuration
        webservices= HealthCheckProcessing.read_and_filter_healthcheck_config('webservice')
        # If no web services are found, return an empty list
        if not webservices or len(webservices) == 0:
            return []
        # Perform health checks on each web service and return the results
        return [HealthCheckProcessing.webservice_health_check(webservice) for webservice in webservices]

    # Database health check
    def database_health_check(database:dict) -> DatabaseHealthcheckStatus:
        """
        Perform a health check on a single database.
        
        Args:
            database (dict): The database configuration.
            
        Returns:
            DatabaseHealthcheckStatus: The result of the database health check.
        """
        can_establish_tcp = TcpBasedConnection.establish_tcp_connection(
            database['hostname'],
            database['port']
        )
        if not can_establish_tcp:
            return DatabaseHealthcheckStatus(
                synonym=database['synonym'],
                hostname=database['hostname'],
                port=database['port'],
                can_tcp=can_establish_tcp
            )
        installed_packages= TerminalProcessing.get_installed_packages()
        possible_db_drivers = HealthCheckProcessing.get_database_driver_by_type(database['type'])
        # Check if the database driver is installed
        is_db_driver_installed = any(driver in installed_packages for driver in possible_db_drivers) and len(installed_packages) > 0
        # Return the health check result as a DatabaseHealthcheckStatus object
        return DatabaseHealthcheckStatus(
            synonym=database['synonym'],
            hostname=database['hostname'],
            port=database['port'],
            type=database['type'],
            can_tcp=can_establish_tcp,
            is_db_driver_installed=is_db_driver_installed
        )

    # Databases health check
    def databases_health_check() -> list[DatabaseHealthcheckStatus]:
        """
        Perform health checks on databases.
        
        Returns:
            list[dict]: The results of the databases health checks.
        """
        # Filter the databases from the health check configuration
        databases= HealthCheckProcessing.read_and_filter_healthcheck_config('database')
        # If no databases are found, return an empty list
        if not databases or len(databases) == 0:
            return []
        # Perform health checks on each database and return the results
        return [HealthCheckProcessing.database_health_check(database) for database in databases]


    # Mount point health check
    def mount_point_health_check(mount_point:dict) -> MountPointHealthcheckStatus:
        """
        Perform a health check on a single mount point.
        
        Args:
            mount_point (dict): The mount point configuration.
            
        Returns:
            dict: The result of the mount point health check.
        """
        # check if the mount point is mounted by the system
        is_mount_point_mounted=is_file_system_mounted(mount_point['mount_point'])
        # Get the usage percentage of the mount point
        usage_percentage = TerminalProcessing.get_mount_point_usages(mount_point['mount_point']) if is_mount_point_mounted else None
        # Return the health check result as a dictionary
        return  MountPointHealthcheckStatus(
            synonym=mount_point['synonym'],
            mount_point=mount_point['mount_point'],
            is_mounted=is_mount_point_mounted,
            current_usage=usage_percentage,
            threshold_percentage=mount_point['threashold_percentage']
        )
    

    # Mount points health check
    def mount_points_health_check() -> list[MountPointHealthcheckStatus]:
        """
        Perform health checks on mount points.
        
        Returns:
            list[MountPointHealthcheckStatus]: The results of the mount points health checks.
        """
        # Filter the mount points from the health check configuration
        mount_points= HealthCheckProcessing.read_and_filter_healthcheck_config('mount_point')
        # If no mount points are found, return an empty list
        if not mount_points or len(mount_points) == 0:
            return []
        # Perform health checks on each mount point and return the results
        return [HealthCheckProcessing.mount_point_health_check(mount_point) for mount_point in mount_points]

    # Required packages health check
    def required_packages_health_check(requirements:dict) -> RequirementsFileHealthcheckStatus:
        """
        Perform a health check on the required packages.
        
        Returns:
            RequirementsFileHealthcheckStatus: The results of required packages health check.
        """
        # Read the requirements from the requirements file
        required_packages = ExternalFileProcessing.read_packages_requirements(requirements['requirements_file'])
        # Check if requirements file is empty list
        if not required_packages or len(required_packages) == 0:
            return RequirementsFileHealthcheckStatus(
                synonym=requirements['synonym'],
                requirements_file_path=requirements['requirements_file'],
                is_file_exists=False,
                are_all_packages_installed=False
            )
        # Get the list of installed packages
        installed_packages = TerminalProcessing.get_installed_packages()
        # Check if all required packages are installed
        are_all_packages_installed = all(pkg in installed_packages for pkg in required_packages)
        # Return the health check result as a RequirementsFileHealthcheckStatus object
        return RequirementsFileHealthcheckStatus(
            synonym=requirements['synonym'],
            requirements_file_path=requirements['requirements_file'],
            is_file_exists=True,
            are_all_packages_installed=are_all_packages_installed
        )

    # All required packages health check
    def all_required_packages_health_check() -> list[RequirementsFileHealthcheckStatus]:
        """
        Perform health checks on all required packages.
        
        Returns:
            list[RequirementsFileHealthcheckStatus]: The results of all required packages health checks.
        """
        # Filter the requirements from the health check configuration
        all_requirements= HealthCheckProcessing.read_and_filter_healthcheck_config('requirements')
        # If no requirements are found, return an empty list
        if not all_requirements or len(all_requirements) == 0:
            return []
        # Perform health checks on each requirements and return the results
        return [HealthCheckProcessing.required_packages_health_check(requirements) for requirements in all_requirements]

    def full_health_check() -> list[dict]:
        """
        Perform a full health check.
        
        Returns:
            dict: The results of the full health check.
        """
        pass