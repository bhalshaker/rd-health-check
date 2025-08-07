import re
import ipaddress


DB_DRIVER_MAP={
    "postgresql":["psycopg","psycopg2","psycopg2-binary","asyncpg"],
    "mysql":["mysqlclient","pymysql","aiomysql","mysql-connector-python"],
    "sqlite":["sqlite3","aiosqlite"],
    "oracle":["cx_Oracle","oracledb"],
    "mssql":["pymssql","pyodbc","mssql-python"], # From Microsoft Documentation
    "mariadb":["mariadb","pymysql","asyncmy"],
    "db2":["ibm_db"]
}

def mount_point_template_vertification(mount_point:dict)->bool:
    """ Verify if the mount point dictionary has the required keys.

    Args:
        mount_point (dict): The mount point dictionary to verify.

    Returns:
        bool: True if the mount point dictionary has the required keys, False otherwise.
    """
    # Check if the mount point dictionary has the required keys
    return all(key in mount_point for key in ['mount_point', 'is_mounted', 'usage_percentage'])

def webservice_template_verification(webservice:dict)->bool:
    """ Verify if the webservice dictionary has the required keys.

    Args:
        webservice (dict): The webservice dictionary to verify.

    Returns:
        bool: True if the webservice dictionary has the required keys, False otherwise.
    """
    # Set the default verification result to False
    verification_results=False
    # Check if the webservice dictionary has details key
    if hasattr(webservice,'details'):
        # Copy details disctionary from webservice
        details=webservice['details']
        # Check if the details dictionary has the required keys
        if all(key in details for key in ['synonym','hostname','port']):
            pass

    return verification_results

def database_template_verification(database:dict)->bool:
    """ Verify if the database dictionary has the required keys.

    Args:
        database (dict): The database dictionary to verify.

    Returns:
        bool: True if the database dictionary has the required keys, False otherwise.
    """
    # Check if the database dictionary has the required keys
    return all(key in database for key in ['database_name', 'is_available', 'response_time'])

def requirements_template_verification(requirements:list[str])->bool:
    """ Verify if the requirements list has the required format.

    Args:
        requirements (list[str]): The list of requirements to verify.

    Returns:
        bool: True if the requirements list has the required format, False otherwise.
    """
    # Check if the requirements list is a list of strings
    return isinstance(requirements, list) and all(isinstance(item, str) for item in requirements)

def config_schmema_is_not_empty(config_schema)->bool:
    """ Verify if the config schema is not empty.

    Args:
        config_schema: The config schema to verify.

    Returns:
        bool: True if the config schema is not empty, False otherwise.
    """
    # Check if the config schema is not empty
    return bool(config_schema) and isinstance(config_schema, list) and len(config_schema) > 0

def health_check_element_is_a_dictionary(health_check_element:dict)->bool:
    """ Verify if the health check element is a dictionary.

    Args:
        health_check_element (dict): The health check element to verify.

    Returns:
        bool: True if the health check element is a dictionary, False otherwise.
    """
    # Check if the health check element is a dictionary
    return isinstance(health_check_element, dict)

def is_valid_hostname(hostname:str)->bool:
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

def is_valid_ip_address(ip_address:str)->bool:
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

def is_hostname_ipv4_ipv6(hostname:str)->bool:
    """ Check if the provided hostname is a valid IPv4 or IPv6 address.

    Args:
        hostname (str): The hostname/IPV4/IPV6 to check.

    Returns:
        bool: True if the hostname is a valid IPv4 or IPv6 address, False otherwise.
    """
    #Check if the hostname matches the IPv4 or IPv6 pattern
    return is_valid_hostname(hostname) or is_valid_ip_address(hostname)

def is_valid_port(port:int)->bool:
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

def is_valid_capacity_threshold(capacity_threshold:int)->bool:
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

def is_valid_web_protocol(protocol:str)->bool:
    """ Check if the provided web protocol is valid.

    Args:
        protocol (str): The web protocol to check.

    Returns:
        bool: True if the protocol is either 'http' or 'https', False otherwise.
    """
    # Check if the protocol is either 'http' or 'udp'
    return protocol.lower() in ['http', 'https']

def is_valid_db_driver(db_driver:str)->bool:
    """ Check if the provided database driver is valid.

    Args:
        db_driver (str): The database driver to check.

    Returns:
        bool: True if the database driver is valid, False otherwise.
    """
    # Check if the database driver is in the DB_DRIVER_MAP values
    return any(db_driver.lower() in drivers for drivers in DB_DRIVER_MAP.values())

def driver_package_list(db_driver:str)->list[str]:
    """ Get the list of packages for the provided database driver.

    Args:
        db_driver (str): The database driver to get the package list for.

    Returns:
        list[str]: A list of packages associated with the provided database driver.
    """
    # Return the list of packages for the provided database driver
    return DB_DRIVER_MAP.get(db_driver.lower(), [])

def is_valid_mount_point(mount_point:str)->bool:
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

def is_valid_file_name(file_name:str)->bool:
    """ Check if the provided file name is valid.

    Args:
        file_name (str): The file name to check.

    Returns:
        bool: True if the file name is valid, False otherwise.
    """
    # Check if the file name is not empty and does not contain any invalid characters
    return bool(file_name) and re.match(r'^[\w\-. ]+$', file_name) and len(file_name) > 0

def is_valid_file_path(file_path:str)->bool:
    """ Check if the provided file path is valid.

    Args:
        file_path (str): The file path to check.

    Returns:
        bool: True if the file path is valid, False otherwise.
    """
    # Check if the file path is not empty and does not contain any invalid characters
    return bool(file_path) and re.match(r'^[\w\-. /]+$', file_path) and len(file_path) > 0