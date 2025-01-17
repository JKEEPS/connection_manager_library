import psycopg2
from typing import Optional, Dict

class RedshiftConnectionManager:
    """
    Manages connections to Amazon Redshift.
    """
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialise Redshift connection manager.

        :param config: A dictionary containing Redshift connection details.
        """
        self.config: Optional[Dict] = config

    def connect(self, host: Optional[str] = None, port: Optional[int] = None, dbname: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None) -> psycopg2.extensions.connection:
        """
        Connect to Redshift using provided credentials.

        :param host: Redshift cluster host.
        :param port: Redshift port (default is 5439).
        :param dbname: Redshift database name.
        :param user: Redshift username.
        :param password: Redshift password.
        :return: Redshift connection object.
        """
        try:
            host = host or self.config["redshift"]["host"]
            port = port or self.config["redshift"]["port"]
            dbname = dbname or self.config["redshift"]["dbname"]
            user = user or self.config["redshift"]["user"]
            password = password or self.config["redshift"]["password"]

            connection = psycopg2.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
            print("Successfully connected to Redshift.")
            return connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Redshift: {e}")