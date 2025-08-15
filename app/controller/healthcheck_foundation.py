import os

class HealthCheckFoundation:
    """ A class to handle basic health check tasks such as verifying configuration templates and checking system properties.
    """
    
    @staticmethod
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
        if not all(HealthCheckFoundation.health_check_element_is_a_dictionary(item) for item in checkconfig):
            return False
        # Check if each health check element has the required keys
        if not all(HealthCheckFoundation.is_valid_health_check_type_element(item) for item in checkconfig):
            return False
        # Check if the config schema is not empty
        if not HealthCheckFoundation.config_schmema_is_not_empty(checkconfig):
            return False
        # If all checks pass, the check configuration template is valid
        return True

    @staticmethod
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
        return all(key in mount_point for key in ['synonym','mount_point', 'threshold_percentage'])
            
    @staticmethod
    def webservice_template_verification(webservice:dict)->bool:
        """ Verify if the webservice dictionary has the required keys.

        Args:
            webservice (dict): The webservice dictionary to verify.

        Returns:
            bool: True if the webservice dictionary has the required keys, False otherwise.
        """
        # Check if the webservice dictionary has the required keys
        return all(key in webservice for key in ['synonym','hostname','port','protocol'])

    @staticmethod
    def database_template_verification(database:dict)->bool:
        """ Verify if the database dictionary has the required keys.

        Args:
            database (dict): The database dictionary to verify.

        Returns:
            bool: True if the database dictionary has the required keys, False otherwise.
        """
        # Check if the database dictionary has the required keys
        return all(key in database for key in ['synonym','hostname','port','database_type'])

    @staticmethod
    def requirements_template_verification(requirements:list[str])->bool:
        """ Verify if the requirements list has the required format.

        Args:
            requirements (list[str]): The list of requirements to verify.

        Returns:
            bool: True if the requirements list has the required format, False otherwise.
        """
        # Check if the requirements dictionary has the required keys
        return all(key in requirements for key in ['synonym','requirements_file_path'])

    @staticmethod
    def config_schmema_is_not_empty(config_schema)->bool:
        """ Verify if the config schema is not empty.

        Args:
            config_schema: The config schema to verify.

        Returns:
            bool: True if the config schema is not empty, False otherwise.
        """
        # Check if the config schema is not empty
        return bool(config_schema) and isinstance(config_schema, list) and len(config_schema) > 0

    @staticmethod
    def health_check_element_is_a_dictionary(health_check_element:dict)->bool:
        """ Verify if the health check element is a dictionary.

        Args:
            health_check_element (dict): The health check element to verify.

        Returns:
            bool: True if the health check element is a dictionary, False otherwise.
        """
        # Check if the health check element is a dictionary
        return isinstance(health_check_element, dict)


    @staticmethod
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

    @staticmethod
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
        if not HealthCheckFoundation.is_valid_health_check_type(health_check['check_type']):
            return False
        # Check if health check type and details are valid
        if health_check['check_type'] == 'mount_point' and not HealthCheckFoundation.mount_point_template_vertification(health_check['details']):
            return False
        if health_check['check_type'] == 'webservice' and not HealthCheckFoundation.webservice_template_verification(health_check['details']):
            return False
        if health_check['check_type'] == 'database' and not HealthCheckFoundation.database_template_verification(health_check['details']):
            return False
        if health_check['check_type'] == 'requirements' and not HealthCheckFoundation.requirements_template_verification(health_check['details']):
            return False
        # If all checks pass return True
        return True

    @staticmethod
    def is_file_system_mounted(mount_point:str)->bool:
        """ Check whether the provided mount point is mounted or not.

        Args:
            mount_point (str): The mount point to check if it is mounted or not.

        Returns:
            bool: True if the mount point is mounted, False otherwise.
        """
        # Check whether provided mount_point is mounted or not
        return os.path.ismount(mount_point)