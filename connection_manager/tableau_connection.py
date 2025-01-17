import tableauserverclient as TSC

class TableauConnectionManager:
    def __init__(self, config=None):
        self.config = config
        self.server = None

    def connect_to_server(self, server_url=None, token_name=None, personal_access_token=None, site_id=None, server_version=None):
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

    def list_users(self):
        try:
            all_users, _ = self.server.users.get()
            return [{"id": user.id, "name": user.name, "email": user.email, "site_role": user.site_role} for user in all_users]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve users: {e}")

    def list_datasources(self):
        try:
            all_datasources, _ = self.server.datasources.get()
            return [{"id": ds.id, "name": ds.name, "project_name": ds.project_name, "created_at": ds.created_at} for ds in all_datasources]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve datasources: {e}")

    def list_flows(self):
        try:
            all_flows, _ = self.server.flows.get()
            return [{"id": flow.id, "name": flow.name, "project_name": flow.project_name, "created_at": flow.created_at} for flow in all_flows]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve flows: {e}")

    def list_dashboards(self):
        try:
            all_workbooks, _ = self.server.workbooks.get()
            return [{"id": wb.id, "name": wb.name, "project_name": wb.project_name, "created_at": wb.created_at} for wb in all_workbooks]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve dashboards: {e}")

    def create_user(self, username, site_role, email=None):
        try:
            new_user = TSC.UserItem(name=username, site_role=site_role, auth_setting="ServerDefault")
            if email:
                new_user.email = email
            user = self.server.users.add(new_user)
            print(f"User '{username}' created successfully.")
            return {"id": user.id, "name": user.name, "email": user.email, "site_role": user.site_role}
        except Exception as e:
            raise RuntimeError(f"Failed to create user '{username}': {e}")

    def delete_user(self, username_or_id):
        try:
            all_users = self.list_users()
            user_to_delete = next((u for u in all_users if u["id"] == username_or_id or u["name"] == username_or_id), None)
            if not user_to_delete:
                raise ValueError(f"User '{username_or_id}' not found.")
            self.server.users.remove(user_to_delete["id"])
            print(f"User '{user_to_delete['name']}' deleted successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to delete user '{username_or_id}': {e}")

    def update_user_role(self, username_or_id, new_role):
        try:
            all_users = self.list_users()
            user_to_update = next((u for u in all_users if u["id"] == username_or_id or u["name"] == username_or_id), None)
            if not user_to_update:
                raise ValueError(f"User '{username_or_id}' not found.")
            user = self.server.users.get_by_id(user_to_update["id"])
            user.site_role = new_role
            self.server.users.update(user)
            print(f"User '{user.name}' updated to role '{new_role}' successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to update user '{username_or_id}': {e}")

    def list_projects(self):
        try:
            all_projects, _ = self.server.projects.get()
            return [{"id": project.id, "name": project.name, "description": project.description} for project in all_projects]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve projects: {e}")