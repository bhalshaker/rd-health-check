import json
def read_packages_requirements(requirements_file:str="requirements.txt") -> list[str]:
    """ Read the requirements.txt file and return a list of installed packages.

    Returns:
        list[str]: A list of installed packages as strings.
    """
    # Read the requirements.txt file and return its content as a list of strings
    with open(requirements_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]  # Exclude empty lines

def load_health_check_json_schema(health_check_file:str="health_check_schema.json") -> dict:
    """ Load the health check JSON schema from the 'health_check_schema.json' file.

    Returns:
        dict: The health check JSON schema as a dictionary.
    """
    # Read the health_check_schema.json file and return its content as a dictionary
    with open(health_check_file, 'r') as file:
        return json.load(file)  # Load the JSON content into a dictionary
    
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