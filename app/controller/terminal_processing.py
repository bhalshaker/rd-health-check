import subprocess
import os
from app.logging.logging import return_logging_instance

class TerminalProcessing:
    """
    A class to handle terminal processing tasks such as executing commands and checking system properties.
    """
    @staticmethod
    def return_terminal_cmd_output(command:list[str])->str:
        """    A function to execute a terminal command and return its output as a UTF-8 decoded string.

        Args:
            command (list[str]): A list of command and its arguments to be executed in the terminal.

        Returns:
            str: The output of the command as a UTF-8 decoded string.
        """
        # Send the command to the terminal and return caputre the output as a UTF-8 decoded string
        logger=return_logging_instance("Terminal Processing")
        logger.info(f"Executing command: {command}")
        output= subprocess.check_output(command)
        return output.decode('UTF-8')
    
    @staticmethod
    def is_os_unix_list()->bool:
        """ Check if the current operating system is a Unix-based system.

        Returns:
            bool: True if the current OS is Unix-based (like Linux or macOS), False otherwise.
        """
        # Check if the current os is a Unix based
        return os.name=='posix'

    @staticmethod
    def get_mount_point_usages(mount_point:str)->int:
        """ Get the usage percentage of the specified mount point by executing the 'df' command in the terminal.

        Args:
            mount_point (str): The mount point to check the usage percentage for.

        Returns:
            int: The usage percentage of the specified mount point as an integer.
        """
        # Execute the 'df' command in the terminal and capture its output
        terminal_command=['df',mount_point]
        output=TerminalProcessing.return_terminal_cmd_output(terminal_command)
        # Extract the usage percentage from the output
        lines=output.splitlines()
        data=lines[1].split()
        # Extract the usage percentage from the data list
        usage_percentage=int(data[4].strip('%'))
        # Convert the output to an integer and return it
        return usage_percentage

    @staticmethod
    def get_installed_packages()->list[str]:
        """_summary_

        Returns:
            list[str]: _description_
        """
        logger=return_logging_instance("Terminal Processing")
        # 'pip freeze' command in the terminal and capture its output
        command=['pip','freeze']
        try:
            output = TerminalProcessing.return_terminal_cmd_output(command)
            # Split the output into a list of lines, each representing a package
            packages = output.splitlines()
            # Extract only the package names by splitting each line at '=='
            # and stripping any extra whitespace
            packages_name=[package.split('==')[0].strip() for package in packages if package]
            logger.info(f"Cleaned installed packages: {packages_name}")
            # Return the list of package names
            return packages_name
        except subprocess.CalledProcessError:
            # If pip freeze returns a terminal error, then return an empty list
            return []
