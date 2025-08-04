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
    