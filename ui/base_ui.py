from db.dbclient import DatabaseClient


class BaseUI:
    def __init__(self, db_client: DatabaseClient = None):
        self.db_client = db_client

    def main(self):
        pass
