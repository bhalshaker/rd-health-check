import socket
from app.schema import HealthStatus

def determine_address_family_version(hostname:str)->dict:
    """A function to determince whether IP address version is IPV4 or IPV6.

    Args:
        hostname (str): hosttname or IP address to check

    Returns:
        dict: return values in a dictionary with keys:
            - ip_family (any): IP address family, either socket.AF_INET or socket.AF_INET6
            - is_successful (bool): True if IP address family could be determined, False
    """
    try:
        # Check the type of IP address whether it is IPV4 or IPV6
        ip_version=socket.getaddrinfo(hostname)[0][0]
        # Return IP version and announce that IP version detection was successful
        return HealthStatus.ip_family_detection_dictionary(ip_version,True)
    except:
        # Announce that IP version detection was failed
        return HealthStatus.ip_family_detection_dictionary()

def establish_tcp_connection(hostname:str,port:int,time_out:int=5)->dict:
    """ Establish a TCP connection to the specified hostname and port to check if the connection can be established or not.

    Args:
        hostname (str): hosttname or IP address for the destination server.
        port (int): port number on the destination server.
        time_out (int, optional): The timeout value specifies how long the service should attempt to establish a connection before stopping. The default value is 5.

    Returns:
        dict: Results of the TCP connection attempt in a dictionary with keys:
            - hostname (str): The hostname or IP address that was attempted to connect.
            - port (int): The port number that was attempted to connect.
            - is_successful (bool): True if the TCP connection was established successfully, False otherwise
    """
    # Check if the ip address IPV4 or IPV6
    address_family=determine_address_family_version(hostname)
    # If ip address family could not be detected then TCP connection cannot be established
    if not address_family['is_successful'] or address_family['ip_family'] not in [socket.AF_INET,socket.AF_INET6]:
        return HealthStatus.establish_connection_status_dictionary(hostname,port)
    # Create a socket based in IP version
    created_socket=socket.socket(address_family['ip_family'],socket.SOCK_STREAM)
    # Set timeout
    created_socket.settimeout(time_out)
    try:
        # Try to establish a connection to mentioned hostname/ip port
        created_socket.connect((hostname,port))
        # Announce that the process is successful and TCP connection can be established
        return HealthStatus.establish_connection_status_dictionary(hostname,port,True)
    except:
        # Report that the TCP connection cannot be established
        return HealthStatus.establish_connection_status_dictionary(hostname,port)