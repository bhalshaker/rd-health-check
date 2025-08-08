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

def is_config_template_checktype_valid(checkconfig:list[dict])->bool:
    """ Verify if the check configuration template has the required keys.

    Args:
        checkconfig (list[dict]): The check configuration template to verify.

    Returns:
        bool: True if the check configuration template has the required keys, False otherwise.
    """
    # Check if the check configuration template is a list of dictionaries
    if not isinstance(checkconfig, list):
        return False
    # Check if each item in the list is a dictionary
    if not all(health_check_element_is_a_dictionary(item) for item in checkconfig):
        return False
    if not all(isinstance(item, dict) for item in checkconfig):
        return False

    return isinstance(checkconfig, list) and all(isinstance(item, dict) for item in checkconfig)

def mount_point_template_vertification(mount_point:dict)->bool:
    """ Verify if the mount point dictionary has the required keys.

    Args:
        mount_point (dict): The mount point dictionary to verify.

    Returns:
        bool: True if the mount point dictionary has the required keys, False otherwise.
    """
    if not isinstance(mount_point, dict):
        return False
    # Check if the mount point dictionary has the required keys
    if not all(key in mount_point for key in ['synonym','mount_point', 'threshold_percentage']):
        return False
    # Check if the threshold percentage is a valid integer between 0 and 100
    # Check if the mount point is a valid Linux mount point syntax
    # Check if the synonym is not emp
    if not is_valid_capacity_threshold(mount_point['threshold_percentage']) \
        or not is_valid_mount_point(mount_point['mount_point']) \
            or not is_valid_synonym(mount_point["synonym"]):
        return False
    # If all checks pass, the mount point dictionary is valid
    return True

def webservice_template_verification(webservice:dict)->bool:
    """ Verify if the webservice dictionary has the required keys.

    Args:
        webservice (dict): The webservice dictionary to verify.

    Returns:
        bool: True if the webservice dictionary has the required keys, False otherwise.
    """
    # Check if the webservice dictionary has the required keys
    if not all(key in webservice for key in ['synonym','hostname','port','protocol']):
        return False
    # Check if the hostname is a valid hostname or IP address
    # Check if the port is a valid port number
    # Check if the protocol is a valid web protocol (http or https)
    if not is_hostname_ipv4_ipv6(webservice['hostname']) \
        or not is_valid_port(webservice['port']) \
            or not is_valid_web_protocol(webservice['protocol']) \
                or not is_valid_synonym(webservice["synonym"]):
        return False
    # If all checks pass, the webservice dictionary is valid
    return True

def database_template_verification(database:dict)->bool:
    """ Verify if the database dictionary has the required keys.

    Args:
        database (dict): The database dictionary to verify.

    Returns:
        bool: True if the database dictionary has the required keys, False otherwise.
    """
    # Check if the database dictionary has the required keys
    if not all(key in database for key in ['synonym','hostname','port','database_type']):
        return False
    # Check if the hostname is a valid hostname or IP address
    # Check if the port is a valid port number
    # Check if the database type is in the DB_DRIVER_MAP keys
    # Check if the synonym is valid
    if not is_hostname_ipv4_ipv6(database['hostname']) \
        or not is_valid_port(database['port']) \
            or not is_valid_db_driver(database['database_type']) \
                or not is_valid_synonym(database["synonym"]):
        return False
    return True

def requirements_template_verification(requirements:list[str])->bool:
    """ Verify if the requirements list has the required format.

    Args:
        requirements (list[str]): The list of requirements to verify.

    Returns:
        bool: True if the requirements list has the required format, False otherwise.
    """
    # Check if the requirements dictionary has the required keys
    if not all(key in requirements for key in ['synonym','requirements_file_path']):
        return False
    # Check if the requirements file path is a valid file path
    # Check if the synonym is valid
    if not is_valid_file_path(requirements['requirements_file_path']) \
        or not is_valid_synonym(requirements["synonym"]):
        return False
    # If all checks pass, the requirements list is valid    
    return True

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

def is_valid_synonym(synonym:str)->bool:
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

def is_valid_health_check_type(health_check_type:str)->bool:
    """ Check if the provided health check type is valid.

    Args:
        health_check_type (str): The health check type to check.

    Returns:
        bool: True if the health check type is valid, False otherwise.
    """
    # Check if the health check type is not empty and is a string
    if not health_check_type or not isinstance(health_check_type, str):
        return False
    # Check if the health check type is one of the valid types
    valid_health_check_types = ['mount_point', 'webservice', 'database', 'requirements']
    if health_check_type.lower() not in valid_health_check_types:
        return False
    # If all checks pass, the health
    return True

def is_valid_health_check_type_element(health_check:dict)->bool:
    """ Check if the provided health check element is valid.

    Args:
        health_check_element (dict): The health check element to check.

    Returns:
        bool: True if the health check type is element, False otherwise.
    """
    # Check if the health check is dictionry has the required keys
    if not all(key in health_check for key in ['check_type', 'details']):
        return False
    # Check if the check_type is a valid health check type
    if not is_valid_health_check_type(health_check['check_type']):
        return False
    # Check if health check type and details are valid
    if health_check['check_type'] == 'mount_point' and not mount_point_template_vertification(health_check['details']):
        return False
    if health_check['check_type'] == 'webservice' and not webservice_template_verification(health_check['details']):
        return False
    if health_check['check_type'] == 'database' and not database_template_verification(health_check['details']):
        return False
    if health_check['check_type'] == 'requirements' and not requirements_template_verification(health_check['details']):
        return False
    # If all checks pass return True
    return True
    