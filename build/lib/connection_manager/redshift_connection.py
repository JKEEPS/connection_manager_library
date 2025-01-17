import psycopg2

class RedshiftConnectionManager:
    def __init__(self, config=None):
        self.config = config

    def connect(self, host=None, port=None, dbname=None, user=None, password=None):
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