import json
import yaml

class ConfigManager:
    @staticmethod
    def load_config(file_path):
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