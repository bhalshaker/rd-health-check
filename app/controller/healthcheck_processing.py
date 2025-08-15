import os
from app.schema.healthcheck_status import MountPointHealthcheckStatus,WebServiceHealthcheckStatus,RequirementsFileHealthcheckStatus
from app.schema.healthcheck_status import DatabaseHealthcheckStatus,AllHealthcheckStatus
from app.controller.tcp_based_connection import TcpBasedConnection
from app.controller.external_file_processing import ExternalFileProcessing
from app.controller.terminal_processing import TerminalProcessing
from app.controller.healthcheck_foundation import HealthCheckFoundation
from app.schema.healthcheck_config import DatabaseHealthcheckConfig,WebserviceHealthcheckConfig,MountPointHealthcheckConfig
from app.schema.healthcheck_config import AllHealthcheckConfig,RequirementsFileHealthcheckConfig

class HealthCheckProcessing:
    """ A class to handle health check processing tasks such as reading configuration files and performing health checks.
    """

    @staticmethod
    def _read_healthcheck_config()->list[dict]:
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
        if not HealthCheckFoundation.config_schmema_is_not_empty(config_file_content):
            return []
        # Vertify all elements in the config schema are valid
        if not all(HealthCheckFoundation.is_valid_health_check_type_element(element) for element in config_file_content):
            return []
        return config_file_content  # Return the health check configuration as a list of dictionaries
    
    @staticmethod
    def _get_healthcheck_config():
        healthcheck_config_dict = HealthCheckProcessing._read_healthcheck_config()
        healthcheck_config = AllHealthcheckConfig(healthcheck_config_dict)
        return healthcheck_config
    
    # Webservices health check
    @staticmethod
    def _webservice_health_check(webservice:WebserviceHealthcheckConfig) -> WebServiceHealthcheckStatus:
        """
        Perform a health check on a single web service.
        
        Args:
            webservice (WebserviceHealthcheckConfig): The web service configuration.
            
        Returns:
            WebServiceHealthcheckStatus: The result of the web service health check.
        """
        can_establish_tcp = TcpBasedConnection.establish_tcp_connection(
            webservice.hostname,
            webservice.port
        )
        return WebServiceHealthcheckStatus(
            synonym=webservice.synonym,
            hostname=webservice.hostname,
            port=webservice.port,
            protocol=webservice.protocol,
            can_tcp=can_establish_tcp
        )

    # Webservices health check
    @staticmethod
    def webservices_health_check(healthcheck_config:AllHealthcheckConfig=None) -> list[WebServiceHealthcheckStatus]:
        """
        Perform health checks on web services.

        Args:
            healthcheck_config (AllHealthcheckConfig): The health check configuration containing requirements.

        Returns:
            list[WebServiceHealthcheckStatus]: The results of the web services health checks.
        """
        if not healthcheck_config:
            # Read Healthcheck config from file
            healthcheck_config=HealthCheckProcessing._get_healthcheck_config()
        # If no web services are found, return an empty list
        if not healthcheck_config.webservices or len(healthcheck_config.webservices) == 0:
            return []
        # Perform health checks on each web service and return the results
        return [HealthCheckProcessing._webservice_health_check(webservice) for webservice in healthcheck_config.webservices]

    # Database health check
    @staticmethod
    def _database_health_check(database:DatabaseHealthcheckConfig) -> DatabaseHealthcheckStatus:
        """
        Perform a health check on a single database.
        
        Args:
            database DatabaseHealthcheckConfig: The database configuration.
            
        Returns:
            DatabaseHealthcheckStatus: The result of the database health check.
        """
        can_establish_tcp = TcpBasedConnection.establish_tcp_connection(
            database.hostname,
            database.port
        )
        if not can_establish_tcp:
            return DatabaseHealthcheckStatus(
                synonym=database.synonym,
                hostname=database.hostname,
                port=database.port,
                can_tcp=can_establish_tcp
            )
        installed_packages= TerminalProcessing.get_installed_packages()
        # Check if the database driver is installed
        is_db_driver_installed = any(driver in installed_packages for driver in database.database_drivers) and len(installed_packages) > 0
        # Return the health check result as a DatabaseHealthcheckStatus object
        return DatabaseHealthcheckStatus(
            synonym=database.synonym,
            hostname=database.hostname,
            port=database.port,
            type=database.database_type,
            can_tcp=can_establish_tcp,
            is_db_driver_installed=is_db_driver_installed
        )

    # Databases health check
    @staticmethod
    def databases_health_check(healthcheck_config:AllHealthcheckConfig=None) -> list[DatabaseHealthcheckStatus]:
        """
        Perform health checks on databases.

        Args:
            healthcheck_config (AllHealthcheckConfig): The health check configuration containing requirements.
        
        Returns:
            list[DatabaseHealthcheckStatus]: The results of the databases health checks.
        """
        if not healthcheck_config:
            # Read Healthcheck config from file
            healthcheck_config=HealthCheckProcessing._get_healthcheck_config()
        # If no databases are found, return an empty list
        if not healthcheck_config.databases or len(healthcheck_config.databases) == 0:
            return []
        # Perform health checks on each database and return the results
        return [HealthCheckProcessing._database_health_check(database) for database in healthcheck_config.databases]


    # Mount point health check
    @staticmethod
    def _mount_point_health_check(mount_point:MountPointHealthcheckConfig) -> MountPointHealthcheckStatus:
        """
        Perform a health check on a single mount point.
        
        Args:
            mount_point (MountPointHealthcheckConfig): The mount point configuration.
            
        Returns:
            dict: The result of the mount point health check.
        """
        # check if the mount point is mounted by the system
        is_mount_point_mounted=HealthCheckFoundation.is_file_system_mounted(mount_point.mount_point)
        # Get the usage percentage of the mount point
        usage_percentage = TerminalProcessing.get_mount_point_usages(mount_point.mount_point) if is_mount_point_mounted else None
        # Return the health check result as a dictionary
        return  MountPointHealthcheckStatus(
            synonym=mount_point.synonym,
            mount_point=mount_point.mount_point,
            is_mounted=is_mount_point_mounted,
            current_usage=usage_percentage,
            threshold_percentage=mount_point.threshold_percentage
        )
    

    # Mount points health check
    @staticmethod
    def mount_points_health_check(healthcheck_config:AllHealthcheckConfig=None) -> list[MountPointHealthcheckStatus]:
        """
        Perform health checks on mount points.

        Args:
            healthcheck_config (AllHealthcheckConfig): The health check configuration containing requirements.
        
        Returns:
            list[MountPointHealthcheckStatus]: The results of the mount points health checks.
        """
        if not healthcheck_config:
            # Read Healthcheck config from file
            healthcheck_config=HealthCheckProcessing._get_healthcheck_config()
        # If no mount points are found, return an empty list
        if not healthcheck_config.mount_points or len(healthcheck_config.mount_points) == 0:
            return []
        # Perform health checks on each mount point and return the results
        return [HealthCheckProcessing._mount_point_health_check(mount_point) for mount_point in healthcheck_config.mount_points ]

    # Required packages health check
    @staticmethod
    def _required_packages_health_check(requirements:RequirementsFileHealthcheckConfig) -> RequirementsFileHealthcheckStatus:
        """
        Perform a health check on the required packages.

        Args:
            requirements (RequirementsFileHealthcheckConfig): The requirements file configuration.
        
        Returns:
            RequirementsFileHealthcheckStatus: The results of required packages health check.
        """
        # Read the requirements from the requirements file
        required_packages = ExternalFileProcessing.read_packages_requirements(requirements.requirements_file_path)
        # Check if requirements file is empty list
        if not required_packages or len(required_packages) == 0:
            return RequirementsFileHealthcheckStatus(
                synonym=requirements.synonym,
                requirements_file_path=requirements.requirements_file_path,
                is_file_exists=False,
                are_all_packages_installed=False
            )
        # Get the list of installed packages
        installed_packages = TerminalProcessing.get_installed_packages()
        # Check if all required packages are installed
        are_all_packages_installed = all(pkg in installed_packages for pkg in required_packages)
        # Return the health check result as a RequirementsFileHealthcheckStatus object
        return RequirementsFileHealthcheckStatus(
            synonym=requirements.synonym,
            requirements_file_path=requirements.requirements_file_path,
            is_file_exists=True,
            are_all_packages_installed=are_all_packages_installed
        )

    # All required packages health check
    @staticmethod
    def all_required_packages_health_check(healthcheck_config:AllHealthcheckConfig=None) -> list[RequirementsFileHealthcheckStatus]:
        """
        Perform health checks on all required packages.

        Args:
            healthcheck_config (AllHealthcheckConfig): The health check configuration containing requirements.
        
        Returns:
            list[RequirementsFileHealthcheckStatus]: The results of all required packages health checks.
        """
        if not healthcheck_config:
            # Read Healthcheck config from file
            healthcheck_config=HealthCheckProcessing._get_healthcheck_config()
        # If no requirements are found, return an empty list
        if not healthcheck_config.requirements_files or len(healthcheck_config.requirements_files) == 0:
            return []
        # Perform health checks on each requirements and return the results
        return [HealthCheckProcessing._required_packages_health_check(requirements) for requirements in healthcheck_config.requirements_files]

    @staticmethod
    def full_health_check() -> AllHealthcheckStatus:
        """
        Perform a full health check.
        
        Returns:
            AllHealthcheckStatus: The results of the full health check.
        """
        healthcheck_config=HealthCheckProcessing._get_healthcheck_config()
        databases_healthcheck=HealthCheckProcessing.databases_health_check(healthcheck_config)
        webservices_healthcheck=HealthCheckProcessing.webservices_health_check(healthcheck_config)
        mount_points_healthcheck=HealthCheckProcessing.mount_points_health_check(healthcheck_config)
        requirements_files_healthcheck=HealthCheckProcessing.all_required_packages_health_check(healthcheck_config)
        return AllHealthcheckStatus(mount_points_healthcheck,
                                    webservices_healthcheck,
                                    databases_healthcheck,
                                    requirements_files_healthcheck)