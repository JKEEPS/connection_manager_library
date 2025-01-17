import tableauserverclient as TSC
from typing import Optional, List, Dict

class TableauConnectionManager:
    """
    Manages connections to Tableau Server and provides simplified access to Tableau Server Client (TSC) resources.
    """
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialise the TableauConnectionManager with optional configuration.

        :param config: A dictionary containing Tableau connection details.
        """
        self.config: Optional[Dict] = config
        self.server: Optional[TSC.Server] = None

    def connect_to_server(
        self, 
        server_url: Optional[str] = None, 
        token_name: Optional[str] = None,
        personal_access_token: Optional[str] = None,
        site_id: Optional[str] = None,
        server_version: Optional[str] = None
    ) -> TSC.Server:
        """
        Connect to Tableau Server using Personal Access Token.

        :param server_url: The URL of the Tableau Server.
        :param token_name: The name of the personal access token.
        :param personal_access_token: The value of the personal access token.
        :param site_id: The Tableau site ID.
        :param server_version: The version of Tableau Server to use.
        :return: An authenticated Tableau Server object.
        """
        try:
            server_url = server_url or self.config["tableau"]["server_url"]
            token_name = token_name or self.config["tableau"]["token_name"]
            personal_access_token = personal_access_token or self.config["tableau"]["personal_access_token"]
            site_id = site_id or self.config["tableau"].get("site_id", "")
            server_version = server_version or self.config["tableau"].get("server_version", None)

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

    @property
    def datasources(self) -> TSC.Datasources:
        """Access the Tableau Server datasources endpoint."""
        return self.server.datasources

    @property
    def workbooks(self) -> TSC.Workbooks:
        """Access the Tableau Server workbooks endpoint."""
        return self.server.workbooks

    @property
    def flows(self) -> TSC.Flows:
        """Access the Tableau Server flows endpoint."""
        return self.server.flows

    @property
    def projects(self) -> TSC.Projects:
        """Access the Tableau Server projects endpoint."""
        return self.server.projects

    @property
    def users(self) -> TSC.Users:
        """Access the Tableau Server users endpoint."""
        return self.server.users
