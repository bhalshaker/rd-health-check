import os
from external_file_processing import (file_exists,load_health_check_json_schema)
from healthcheck_config import (config_schmema_is_not_empty)

def read_healthcheck_config()->list[dict]:
    """
    Reads the health check configuration from a file.
    
    Returns:
        list[dict]: The health check configuration.
    """
    # Get the path to the health check configuration file from environment variable or use default
    config_file_location = os.getenv('HEALTH_CHECK_CONFIG_FILE', 'health_check_config.json')
    # Check if the file exists
    if not file_exists(config_file_location):
        return []  # Return an empty list if the file does not exist
    # Read the health check configuration file and return its content as a list of dictionaries
    config_file_content = load_health_check_json_schema(config_file_location)
    # Verify if the config schema is not empty
    if not config_schmema_is_not_empty(config_file_content):
        pass