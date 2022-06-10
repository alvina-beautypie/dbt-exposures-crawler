import tableauserverclient as TSC
from functools import lru_cache


class TableauRestClient:
    """
    Thin wrapper around the official Tableau Server client.
    """

    def __init__(self, server_name: str, username: str, password: str, site_name: str = None):
        tableau_auth = TSC.TableauAuth(username, password, site_name)

        self.server = TSC.Server(server_name, use_server_version=True)
        self.server.auth.sign_in(tableau_auth)

    @lru_cache(maxsize=None)
    def retrieve_workbook(self, workbook_id: str):
        return self.server.workbooks.get_by_id(workbook_id)

    @lru_cache(maxsize=None)
    def retrieve_user(self, user_id: str):
        return self.server.users.get_by_id(user_id)

    def run_metadata_api(self, query: str):
        response = self.server.metadata.query(query)

        return response['data']

    def sign_out(self):
        self.server.auth.sign_out()
