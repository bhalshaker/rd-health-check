import json
import os
import re

class ExternalFileProcessing:
    """ A class to handle external file processing tasks such as reading configuration files and requirements.
    """
    @staticmethod
    def read_packages_requirements(requirements_file:str="requirements.txt") -> list[str]:
        """ Read the requirements.txt file and return a list of installed packages.

        Returns:
            list[str]: A list of installed packages as strings.
        """
        # Read the requirements.txt file and return its content as a list of strings
        if not ExternalFileProcessing.file_exists(requirements_file):
            return [] # Return an empty list if the file does not exist
        with open(requirements_file, 'r') as file:
            packages_lines=[line.strip() for line in file if line.strip() and not line.startswith('#')]  # Exclude empty and commented lines
            return [re.split(r'[.*\]|==|>=|<=|~=|!=|>|<|,',package)[0].strip() for package in packages_lines]  #Grap pakcage names and strip whitespace

    @staticmethod
    def load_health_check_json_schema(health_check_file:str="health_check_schema.json") -> dict:
        """ Load the health check JSON schema from the 'health_check_schema.json' file.

        Returns:
            dict: The health check JSON schema as a dictionary.
        """
        # Read the health_check_schema.json file and return its content as a dictionary
        if not ExternalFileProcessing.file_exists(health_check_file):
            return []  # Return an empty list if the file does not exist
        with open(health_check_file, 'r') as file:
            return json.load(file)  # Load the JSON content into a dictionary
    
    @staticmethod
    def file_exists(file_path:str) -> bool:
        """ Check if the specified file exists.

        Args:
            file_path (str): The path to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Check if the specified file exists
        return os.path.isfile(file_path)