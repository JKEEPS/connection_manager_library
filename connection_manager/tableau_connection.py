import tableauserverclient as TSC

class TableauConnectionManager:
    def __init__(self, config=None):
        """
        Initialise the TableauConnectionManager with optional config.
        :param config: (dict) Configuration containing Tableau connection details.
        """
        self.config = config
        self.server = None

    def connect_to_server(self, server_url=None, token_name=None, personal_access_token=None, site_id=None, server_version=None):
        """
        Connect to Tableau Server using Personal Access Token.
        """
        try:
            # Retrieve connection details from the configuration or parameters
            server_url = server_url or self.config["tableau"]["server_url"]
            token_name = token_name or self.config["tableau"]["token_name"]
            personal_access_token = personal_access_token or self.config["tableau"]["personal_access_token"]
            site_id = site_id or self.config["tableau"].get("site_id", "")
            server_version = server_version or self.config["tableau"].get("server_version", None)

            # Create Tableau authentication and server instance
            tableau_auth = TSC.PersonalAccessTokenAuth(
                token_name=token_name,
                personal_access_token=personal_access_token,
                site_id=site_id
            )
            self.server = TSC.Server(server_url, use_server_version=(server_version is None))
            if server_version:
                self.server.server_info.server_version = server_version
            self.server.auth.sign_in(tableau_auth)
            print(f"Connected to Tableau Server version {server_version or 'latest'}.")
            return self.server
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Tableau Server: {e}")

    # Expose TSC resources as properties for intuitive access
    @property
    def datasources(self):
        """
        Access the Tableau Server datasources endpoint.
        """
        return self.server.datasources

    @property
    def workbooks(self):
        """
        Access the Tableau Server workbooks endpoint.
        """
        return self.server.workbooks

    @property
    def flows(self):
        """
        Access the Tableau Server flows endpoint.
        """
        return self.server.flows

    @property
    def projects(self):
        """
        Access the Tableau Server projects endpoint.
        """
        return self.server.projects

    @property
    def users(self):
        """
        Access the Tableau Server users endpoint.
        """
        return self.server.users
