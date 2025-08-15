import socket
from app.logging.logging import return_logging_instance

logger=return_logging_instance("HealthCheck TCP")    
class TcpBasedConnection:
    """A class to handle TCP based connections."""

    
    @staticmethod
    def determine_address_family_version(hostname:str,port:int)->dict:
        """A function to determince whether IP address version is IPV4 or IPV6.

        Args:
            hostname (str): hosttname or IP address to check

        Returns:
            any: IP address family, either socket.AF_INET or socket.AF_INET6
        """
        try:
            # Check the type of IP address whether it is IPV4 or IPV6
            ip_version=socket.getaddrinfo(hostname,port)[0][0]
            # Return IP version and announce that IP version detection was successful
            return ip_version
        except Exception as e:
            # Announce that IP version detection was failed
            logger.error(f"Failed to detect IP address version: {e}")
            return None
    
    @staticmethod
    def establish_tcp_connection(hostname:str,port:int,time_out:int=5)->bool:
        """ Establish a TCP connection to the specified hostname and port to check if the connection can be established or not.

        Args:
            hostname (str): hosttname or IP address for the destination server.
            port (int): port number on the destination server.
            time_out (int, optional): The timeout value specifies how long the service should attempt to establish a connection before stopping. The default value is 5.

        Returns:
            bool: True if the TCP connection can be established, False otherwise.
        """
        # Check if the ip address IPV4 or IPV6
        address_family=TcpBasedConnection.determine_address_family_version(hostname,port)
        # If ip address family could not be detected then TCP connection cannot be established
        if not address_family or address_family not in [socket.AF_INET,socket.AF_INET6]:
            return False
        # Create a socket based in IP version
        created_socket=socket.socket(address_family,socket.SOCK_STREAM)
        # Set timeout
        created_socket.settimeout(time_out)
        try:
            # Try to establish a connection to mentioned hostname/ip port
            created_socket.connect((hostname,port))
            # Announce that the process is successful and TCP connection can be established
            return True
        except Exception as e:
            # Report that the TCP connection cannot be established
            logger.error(f"Failed to establish TCP connection to {hostname}:{port} caused by {e}")
            return False