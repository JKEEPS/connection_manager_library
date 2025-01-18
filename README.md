# Connection Manager

The `connection_manager` library provides a unified interface for managing connections to:
- Tableau Server
- Oracle Databases
- AWS (S3, etc.)
- Amazon Redshift

## Installation

Install the library with:

```bash
pip install connection_manager
```

## Usage

```python
import connection_manager as cm

config = cm.load_config("config.yaml")
tableau_manager = TableauConnectionManager(config)
tableau_manager.connect_to_server()
```

## Features
- Manage Tableau connections and admin tasks.
- Connect to Oracle databases, AWS services, and Redshift.
- Simplifies multi-service connection workflows.
