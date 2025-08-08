import subprocess
import os
import re


def return_terminal_cmd_output(command:list[str])->str:
    """    A function to execute a terminal command and return its output as a UTF-8 decoded string.

    Args:
        command (list[str]): A list of command and its arguments to be executed in the terminal.

    Returns:
        str: The output of the command as a UTF-8 decoded string.
    """
    # Send the command to the terminal and return caputre the output as a UTF-8 decoded string
    output= subprocess.check_output(command)
    return output.decode('UTF-8')

def is_file_system_mounted(mount_point:str)->bool:
    """ Check whether the provided mount point is mounted or not.

    Args:
        mount_point (str): The mount point to check if it is mounted or not.

    Returns:
        bool: True if the mount point is mounted, False otherwise.
    """
    # Check whether provided mount_point is mounted or not
    return os.path.ismount(mount_point)

def is_os_unix_list()->bool:
    """ Check if the current operating system is a Unix-based system.

    Returns:
        bool: True if the current OS is Unix-based (like Linux or macOS), False otherwise.
    """
    # Check if the current os is a Unix based
    return os.name=='posix'


def get_mount_point_usages(mount_point:str)->int:
    """ Get the usage percentage of the specified mount point by executing the 'df' command in the terminal.

    Args:
        mount_point (str): The mount point to check the usage percentage for.

    Returns:
        int: The usage percentage of the specified mount point as an integer.
    """
    # AWK script: on the second line of input, remove the '%' character and print the numeric value
    awk_parameter='\'NR==2 { gsub(/%/, ""); print }\'}\''
    # df --output=pcent {mount_point} | awk 'NR==2 { gsub(/%/, ""); print }'}'
    terminal_command=['df',mount_point,'|','awk',awk_parameter]
    output=return_terminal_cmd_output(terminal_command)
    # Convert the output to an integer and return it
    return int(output.strip())

def get_installed_packages()->list[str]:
    """_summary_

    Returns:
        list[str]: _description_
    """
    # 'pip freeze' command in the terminal and capture its output
    command=['pip','freeze']
    try:
        output = return_terminal_cmd_output(command)
        # Split the output into a list of lines, each representing a package
        packages = output.splitlines()
        # Extract only the package names by splitting each line at '=='
        # and stripping any extra whitespace
        packages_name=[package.split('==')[0].strip() for package in packages if package]
        # Return the list of package names
        return packages_name
    except subprocess.CalledProcessError:
        # If pip freeze returns a terminal error, then return an empty list
        return []
