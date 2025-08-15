import json
import re
from pathlib import Path
from os import PathLike
from app.logging.logging import return_logging_instance

class ExternalFileProcessing:
    """ A class to handle external file processing tasks such as reading configuration files and requirements.
    """
    @staticmethod
    def read_packages_requirements(requirements_file:str="requirements.txt") -> list[str]:
        """ Read the requirements file and return a list of installed packages.

        Returns:
            list[str]: A list of installed packages as strings.
        """
        logger=return_logging_instance("External File Processing")
        # Read the requirements.txt file and return its content as a list of strings
        if not ExternalFileProcessing.file_exists(requirements_file):
            return [] # Return an empty list if the file does not exist
        try:
            with open(requirements_file, "r") as file:
                # Exclude empty and commented lines
                packages_lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]
                logger.info(f"number of packages {len(packages_lines)} and packages are {packages_lines}")
                #Grap pakcage names and strip whitespace
                package_name_pattern=r"^([a-zA-Z0-9_.-]+)(\[[a-zA-Z0-9_,.-]+\])?"
                #Get Packages
                packages=[re.match(package_name_pattern, package).group(1) if re.match(package_name_pattern, package) else package for package in packages_lines]
                logger.info(f"Packages without version {packages}")
                return packages
        except Exception as e:
            logger.error(f"Reading packages failed due to: {e}")
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