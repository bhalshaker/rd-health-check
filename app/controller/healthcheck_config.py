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
    # Check if the webservice dictionary has the required keys
    return all(key in webservice for key in ['webservice_name', 'is_available', 'response_time'])

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