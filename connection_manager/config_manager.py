import json
import yaml
from typing import Dict

class ConfigManager:
    """
    Handles loading and saving of configuration files.
    """
    @staticmethod
    def load_config(file_path: str) -> Dict:
        """
        Load a configuration file (YAML or JSON).

        :param file_path: Path to the configuration file.
        :return: Dictionary with configuration data.
        """
        try:
            with open(file_path, 'r') as file:
                if file_path.endswith('.json'):
                    return json.load(file)
                elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(file)
                else:
                    raise ValueError("Unsupported config file format.")
        except Exception as e:
            raise FileNotFoundError(f"Failed to load config file: {e}")

    @staticmethod
    def create_sample_config(file_path: str, format: str = "yaml") -> None:
        """
        Create a sample configuration file.

        :param file_path: Path where the sample config file will be created.
        :param format: Format of the config file (yaml or json).
        """
        sample_config = {
            "tableau": {
                "server_url": "https://your-tableau-server.com",
                "token_name": "your-token-name",
                "personal_access_token": "your-personal-access-token",
                "site_id": "default",
                "server_version": "2023.2"
            },
            "oracle": {
                "dsn": "your-host:1521/your-service",
                "user": "your-username",
                "password": "your-password"
            },
            "aws": {
                "access_key_id": "your-access-key-id",
                "secret_access_key": "your-secret-access-key",
                "region_name": "your-region"
            },
            "redshift": {
                "host": "your-cluster-endpoint",
                "port": 5439,
                "dbname": "your-database-name",
                "user": "your-username",
                "password": "your-password"
            }
        }

        try:
            with open(file_path, 'w') as file:
                if format == "yaml":
                    yaml.dump(sample_config, file, default_flow_style=False)
                elif format == "json":
                    json.dump(sample_config, file, indent=4)
                else:
                    raise ValueError("Unsupported file format. Choose 'yaml' or 'json'.")
            print(f"Sample configuration file created at: {file_path}")
        except Exception as e:
            raise IOError(f"Failed to create sample config file: {e}")
