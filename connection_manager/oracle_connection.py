import cx_Oracle
from typing import Optional, Dict

class OracleConnectionManager:
    """
    Manages connections to Oracle databases.
    """
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialise Oracle connection manager.

        :param config: A dictionary containing Oracle connection details.
        """
        self.config: Optional[Dict] = config

    def connect(self, dsn: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None) -> cx_Oracle.Connection:
        """
        Connect to Oracle using provided credentials.

        :param dsn: Data source name (host:port/service_name).
        :param user: Oracle username.
        :param password: Oracle password.
        :return: Oracle connection object.
        """
        try:
            dsn = dsn or self.config["oracle"]["dsn"]
            user = user or self.config["oracle"]["user"]
            password = password or self.config["oracle"]["password"]

            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            print("Successfully connected to Oracle.")
            return connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Oracle: {e}")
