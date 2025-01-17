# connection_manager/__init__.py
from .tableau_connection import TableauConnectionManager
from .oracle_connection import OracleConnectionManager
from .aws_connection import AWSConnectionManager
from .redshift_connection import RedshiftConnectionManager
from .config_manager import ConfigManager

__all__ = [
    "TableauConnectionManager",
    "OracleConnectionManager",
    "AWSConnectionManager",
    "RedshiftConnectionManager",
    "ConfigManager",
]

# connection_manager/tableau_connection.py
import tableauserverclient as TSC
from tableauhyperapi import HyperProcess, Telemetry, Connection, TableDefinition, SqlType, Inserter
from tableauhyperapi import NOT_NULLABLE
import pandas as pd
from typing import Optional, List, Dict
import os

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

    def load_hyper_to_dataframe(self, datasource_id: str) -> pd.DataFrame:
        """
        Load data from a published Tableau hyper file into a Pandas DataFrame.

        :param datasource_id: The ID of the datasource on Tableau Server.
        :return: DataFrame containing the data from the hyper file.
        """
        try:
            # Download the .hyper file from Tableau Server
            temp_file = f"{datasource_id}.hyper"
            self.datasources.download(datasource_id, filepath=temp_file)

            with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                with Connection(endpoint=hyper.endpoint, database=temp_file) as connection:
                    table_names = connection.catalog.get_table_names("Extract")
                    if not table_names:
                        raise ValueError("No tables found in the Hyper file.")

                    table_name = table_names[0]
                    result = connection.execute_query(f"SELECT * FROM {table_name}")
                    dataframe = pd.DataFrame(result)
                    dataframe.columns = [column.name for column in connection.catalog.get_table_definition(table_name).columns]

            os.remove(temp_file)
            return dataframe

        except Exception as e:
            raise RuntimeError(f"Failed to load hyper file into DataFrame: {e}")

    def retrieve_data_from_local_hyper(self, hyper_file: str) -> pd.DataFrame:
        """
        Retrieve data from a local hyper file into a Pandas DataFrame.

        :param hyper_file: Path to the local hyper file.
        :return: DataFrame containing the data from the hyper file.
        """
        try:
            with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                with Connection(endpoint=hyper.endpoint, database=hyper_file) as connection:
                    table_names = connection.catalog.get_table_names("Extract")
                    if not table_names:
                        raise ValueError("No tables found in the Hyper file.")

                    table_name = table_names[0]
                    result = connection.execute_query(f"SELECT * FROM {table_name}")
                    dataframe = pd.DataFrame(result)
                    dataframe.columns = [column.name for column in connection.catalog.get_table_definition(table_name).columns]

            return dataframe

        except Exception as e:
            raise RuntimeError(f"Failed to retrieve data from local Hyper file: {e}")

    def dataframe_to_local_hyper(self, dataframe: pd.DataFrame, hyper_file: str, table_name: str = "Extract") -> None:
        """
        Save a Pandas DataFrame into a local hyper file.

        :param dataframe: DataFrame containing the data to save.
        :param hyper_file: Path to the output hyper file.
        :param table_name: Name of the table inside the Hyper file.
        """
        try:
            with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                with Connection(endpoint=hyper.endpoint, database=hyper_file, create_mode=Connection.CreateMode.CREATE_AND_REPLACE) as connection:
                    table_definition = TableDefinition(
                        table_name=table_name,
                        columns=[(col, SqlType.text(), NOT_NULLABLE) for col in dataframe.columns]
                    )
                    connection.catalog.create_table(table_definition)

                    with Inserter(connection, table_definition) as inserter:
                        inserter.add_rows(dataframe.values.tolist())
                        inserter.execute()

            print(f"DataFrame saved to {hyper_file} successfully.")

        except Exception as e:
            raise RuntimeError(f"Failed to save DataFrame to Hyper file: {e}")

    def dataframe_to_published_datasource(self, dataframe: pd.DataFrame, datasource_name: str, project_id: str) -> None:
        """
        Publish a Pandas DataFrame to Tableau Server as a datasource.

        :param dataframe: DataFrame containing the data to publish.
        :param datasource_name: Name of the published datasource.
        :param project_id: Tableau project ID where the datasource will be published.
        """
        temp_file = f"{datasource_name}.hyper"
        try:
            self.dataframe_to_local_hyper(dataframe, temp_file)

            datasource = TSC.DatasourceItem(project_id)
            self.server.datasources.publish(datasource, temp_file, TSC.Server.PublishMode.Overwrite)

            print(f"Datasource {datasource_name} published successfully.")

        except Exception as e:
            raise RuntimeError(f"Failed to publish DataFrame as datasource: {e}")

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
