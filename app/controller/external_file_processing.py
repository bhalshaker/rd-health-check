import json
import re
from pathlib import Path
from os import PathLike

class ExternalFileProcessing:
    """ A class to handle external file processing tasks such as reading configuration files and requirements.
    """
    @staticmethod
    def read_packages_requirements(requirements_file:str="requirements.txt") -> list[str]:
        """ Read the requirements file and return a list of installed packages.

        Returns:
            list[str]: A list of installed packages as strings.
        """
        # Read the requirements.txt file and return its content as a list of strings
        if not ExternalFileProcessing.file_exists(requirements_file):
            return [] # Return an empty list if the file does not exist
        try:
            with open(requirements_file, "r") as file:
                # Exclude empty and commented lines
                packages_lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]
                #Grap pakcage names and strip whitespace
                return [re.split(r"[.*\]|==|>=|<=|~=|!=|>|<|,", package)[0].strip() for package in packages_lines]
        except (FileNotFoundError, OSError):
            return [] 

    @staticmethod
    def load_health_check_json_schema(health_check_file:str="health_check_schema.json") -> list[dict]:
        """ Load the health check JSON schema from the 'health_check_schema.json' file.

        Returns:
            list[dict]: The health check JSON schema as a dictionary.
        """
        # Read the health_check_schema.json file and return its content as a dictionary
        if not ExternalFileProcessing.file_exists(health_check_file):
            # Return an empty list if the file does not exist
            return []
        try:
            with open(health_check_file, 'r') as file:
                # Load the JSON content into a dictionary
                data=json.load(file)
                # Return lodaded data if it was a list other wise return an empty list
                return data if isinstance(data,list) else []
        except (FileNotFoundError, OSError):
            # When an error occurs while reading the file return an empty list
            return []
    
    @staticmethod
    def file_exists(file_path: str | PathLike[str] | Path) -> bool:
        """ Check if the specified file exists.

        Args:
            file_path: The path-like input to the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Check if the specified file exists
        return Path(file_path).is_file()