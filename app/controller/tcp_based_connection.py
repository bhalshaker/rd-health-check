import socket
from app.logging.logging import return_logging_instance

logger=return_logging_instance("HealthCheck TCP")    
class TcpBasedConnection:
    """A class to handle TCP based connections."""

    @staticmethod
    def establish_tcp_connection(hostname:str,port:int,time_out:int=1)->bool:
        """ Establish a TCP connection to the specified hostname and port to check if the connection can be established or not.

        Args:
            hostname (str): hosttname or IP address for the destination server.
            port (int): port number on the destination server.
            time_out (int, optional): The timeout value specifies how long the service should attempt to establish a connection before stopping. The default value is 5.

        Returns:
            bool: True if the TCP connection can be established, False otherwise.
        """
        try:
            # Try to establish a connection to mentioned hostname/ip port
            socket.create_connection((hostname,port),timeout=time_out)
            # Announce that the process is successful and TCP connection can be established
            return True
        except Exception as e:
            # Report that the TCP connection cannot be established
            logger.error(f"Failed to establish TCP connection to {hostname}:{port} caused by {e}")
            return False