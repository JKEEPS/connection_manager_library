import cx_Oracle

class OracleConnectionManager:
    def __init__(self, config=None):
        self.config = config

    def connect(self, dsn=None, user=None, password=None):
        try:
            dsn = dsn or self.config["oracle"]["dsn"]
            user = user or self.config["oracle"]["user"]
            password = password or self.config["oracle"]["password"]
            connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            print("Successfully connected to Oracle.")
            return connection
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Oracle: {e}")