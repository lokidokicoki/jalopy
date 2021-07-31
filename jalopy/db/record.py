"""DB Record"""

from jalopy.db.base_item import BaseItem


class Record(BaseItem):
    """
    DB access for the 'record' table
    """

    def __init__(self, conn, cursor):
        """Create instance of Record"""
        super().__init__(conn, cursor, "record")
