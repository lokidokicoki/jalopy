"""DB Record getter/setter"""

from db.base_item import BaseItem


class Record(BaseItem):
    """
    DB access for the 'record' table
    """

    def __init__(self, conn, cursor):
        super().__init__(conn, cursor, "record")
