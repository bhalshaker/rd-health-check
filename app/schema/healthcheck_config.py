from dataclasses import dataclass, field
import re
import ipaddress

@dataclass
class HealthcheckConfigBase:
    """
    Base class for health check configurations.
    """
    synonym: str
    
    def _is_valid_synonym(synonym:str)->bool:
        """ Check if the provided synonym is valid.

        Args:
            synonym (bool): The synonym to check.

        Returns:
            bool: True if the synonym is a not empty and string value, False otherwise.
        """
        # Check if the synonym is not null
        if not synonym:
            return False
        # Check if synonym is not a string
        if not isinstance(synonym, str):
            return False
        # Check if the synonym is not empty
        if len(synonym) == 0:
            return False
        # Return True if the synonym is a string and not empty
        return True

    def _is_valid_hostname(self,hostname:str)->bool:
        """ Check if the provided hostname is a valid hostname Based on RFC 1123.

        Args:
            hostname (str): The hostname to check.

        Returns:
            bool: True if the hostname is valid, False otherwise.
        """
        # check if hostname is not empty and does not exceed the maximum length (255 characters)
        if not hostname or len(hostname) > 255 or len(hostname)==0:
            return False
        # check if hostname starts or ends with a hyphen
        if hostname.startswith('-') or hostname.endswith('-'):
            return False
        # split the hostname into labels
        labels = hostname.split('.')
        # check if each label is valid
        for label in labels:
            # check if label is not empty and does not exceed the maximum length (63 characters)
            if not label or len(label) > 63:
                return False
            label_pattern = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$'
            # check if label contains only valid characters (letters, digits, and hyphens)
            if not re.match(label_pattern, label):
                return False
        # if all checks pass, the hostname is valid
        return True
    def _is_valid_ip_address(self,ip_address:str)->bool:
        """ Check if the provided IP address is a valid IPv4 or IPv6 address using ipaddress library.

        Args:
            ip_address (str): The IP address to check.

        Returns:
            bool: True if the IP address is valid, False otherwise.
        """
        try:
            # Try to create an IPv4 or IPv6 address object
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            # If a ValueError is raised, the IP address is not valid
            return False
    def _is_valid_port(self,port:int)->bool:
        """ Check if the provided port number is valid.

        Args:
            port (int): The port number to check.

        Returns:
            bool: True if the port number is valid (between 0 and 65535), False otherwise.
        """
        
        try:
            port_number = int(port)
            # Check if the port number is an integer between 0 and 65535
            return 0 <= port_number <= 65535
        except:
            # If the port number cannot be converted to an integer, it is not valid
            return False
    def __post_init__(self):
        # Validate synonym
        if not self._is_valid_synonym(self.synonym):
            raise ValueError(f"Invalid synonym: {self.synonym}. It must be a non-empty string.")

@dataclass
class WebserviceHealthcheckConfig(HealthcheckConfigBase):
    """
    Configuration for web service health checks.
    """
    hostname: str
    port: int
    protocol: str

    def __post_init__(self):
        # Validate protocol
        allowed_protocols = ['http', 'https']
        if self.protocol.lower() not in allowed_protocols:
            raise ValueError(f"protocol must be one of {allowed_protocols}, got '{self.protocol}'")
        # Validate hostname
        if not self._is_valid_hostname(self.hostname) and not self._is_valid_ip_address(self.hostname):
            raise ValueError(f"Invalid hostname or IP address: {self.hostname}")
        # Validate port
        if not self._is_valid_port(self.port):
            raise ValueError(f"Invalid port number: {self.port}")

@dataclass
class DatabaseHealthcheckConfig(HealthcheckConfigBase):
    """
    Configuration for database health checks.
    """
    hostname: str
    port: int
    database_type:str
    _DB_DRIVER_MAP={
        "postgresql":["psycopg","psycopg2","psycopg2-binary","asyncpg"],
        "mysql":["mysqlclient","pymysql","aiomysql","mysql-connector-python"],
        "sqlite":["sqlite3","aiosqlite"],
        "oracle":["cx_oracle","oracledb"],
        "mssql":["pymssql","pyodbc","mssql-python"], # From Microsoft Documentation
        "mariadb":["mariadb","pymysql","asyncmy"],
        "db2":["ibm_db"]
    }


    def _is_valid_db_driver(self, database_type:str)->bool:
        """ Check if the provided database driver is valid.

        Args:
            db_driver (str): The database driver to check.

        Returns:
            bool: True if the database driver is valid, False otherwise.
        """

        # Check if the database driver is in the DB_DRIVER_MAP values
        return any(database_type.lower() in drivers for drivers in self._DB_DRIVER_MAP.values())

    def _get_database_drivers_by_type(self,database_type:str)->list:
        """ Get the database drivers by type.

        Args:
            database_type (str): The database type to get the drivers for.

        Returns:
            list: The database drivers for the provided database type.
        """
        # Return the first driver from the DB_DRIVER_MAP for the provided database type
        return self._DB_DRIVER_MAP.get(database_type.lower(), [None]) if database_type else None
    
    @property
    def database_drivers(self) -> list:
        """
        Returns the database driver based on the database_type.
        """
        return self._get_database_drivers_by_type(self.database_type)

    def __post_init__(self):
        # Validate hostname
        if not self._is_valid_hostname(self.hostname) and not self._is_valid_ip_address(self.hostname):
            raise ValueError(f"Invalid hostname or IP address: {self.hostname}")
        # Validate port
        if not self._is_valid_port(self.port):
            raise ValueError(f"Invalid port number: {self.port}")
        # Validate database type
        if not self._is_valid_db_driver(self.database_type):
            raise ValueError(f"Invalid database type: {self.database_type}. Supported types are: {list(self._DB_DRIVER_MAP.keys())}")
@dataclass
class MountPointHealthcheckConfig(HealthcheckConfigBase):
    """
    Configuration for mount point health checks.
    """
    mount_point: str
    threshold_percentage: int

    def _is_valid_mount_point(mount_point:str)->bool:
        """ Check if the provided mount point has a valid Linux mount point syntax using regular expression.

        Args:
            mount_point (str): mount point to check if it is valid or not.

        Returns:
            bool: True if the mount point is valid, False otherwise.
        """
        # Regex pattern to match valid Linux mount points (absolute paths like /, /home, /mnt/data)
        mount_point_pattern=r'^/(?:[\w.-]+/?)+'
        # Return 
        return re.match(mount_point_pattern,mount_point)
    
    def _is_valid_capacity_threshold(capacity_threshold:int)->bool:
        """ Check if the provided capacity threshold is valid.

        Args:
            capacity_threshold (int): The capacity threshold to check.

        Returns:
            bool: True if the threshold is a positive integer betweeen 0 and 100, False otherwise.
        """

        try:
            threshold = int(capacity_threshold)
            # Check if the threshold is a positive integer between 0 and 100
            return 0<threshold<100
        except ValueError:
            # If the threshold cannot be converted to an integer, it is not valid
            return False


    def __post_init__(self):
        # Validate mount point syntax
        if not self._is_valid_mount_point(self.mount_point):
            raise ValueError(f"Invalid mount point: {self.mount_point}. It must be a valid mount point.")
        # Validate capacity threshold
        if not self._is_valid_capacity_threshold(self.threshold_percentage):
            raise ValueError(f"Invalid capacity threshold: {self.threshold_percentage}. It must be a positive integer between 0 and 100.")

@dataclass
class RequirementsFileHealthcheckConfig(HealthcheckConfigBase):
    """
    Configuration for requirements file health checks.
    """
    requirements_file_path: str

    def _is_valid_file_path(file_path:str)->bool:
        """ Check if the provided file path is valid.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if the file path is valid, False otherwise.
        """
        # Check if the file path is not empty and does not contain any invalid characters
        return bool(file_path) and re.match(r'^[\w\-. /]+$', file_path) and len(file_path) > 0

    def __post_init__(self):
        # Validate requirements file path syntax
        if not self._is_valid_file_path(self.requirements_file_path):
            raise ValueError(f"Invalid requirements file path: {self.requirements_file_path}. It must be a valid file path.")
@dataclass
class AllHealthcheckConfig:
    """
    Configuration for all health checks.
    """
    mount_points: list[MountPointHealthcheckConfig] = field(default_factory=list)
    webservices: list[WebserviceHealthcheckConfig] = field(default_factory=list)
    databases: list[DatabaseHealthcheckConfig] = field(default_factory=list)
    requirements_files: list[RequirementsFileHealthcheckConfig] = field(default_factory=list)

    def __init__(self,healthcheck_config):
        """
        Initialize AllHealthcheckConfig with the provided healthcheck_config.

        Args:
            healthcheck_config (dict): The health check configuration to initialize the object with.
        """
        # Initialize empty lists for each type of health check configuration
        self.mount_points = []
        self.databases = []
        self.webservices = []
        self.requirements_files = []
        # Iterate through the healthcheck_config and create instances of the respective health check configuration classes
        for item in healthcheck_config:
            match item['check_type']:
                case 'mount_point':
                    try:
                        self.mount_points.append(MountPointHealthcheckConfig(**item))
                    except:
                        pass
                case 'webservice':
                    try:
                        self.web_services.append(WebserviceHealthcheckConfig(**item))
                    except:
                        pass
                case 'database':
                    try:
                        self.databases.append(DatabaseHealthcheckConfig(**item))
                    except:
                        pass
                case 'requirements_file':
                    try:
                        self.requirements_files.append(RequirementsFileHealthcheckConfig(**item))
                    except:
                        pass