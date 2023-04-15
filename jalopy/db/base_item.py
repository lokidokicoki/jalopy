"""
Base db item
"""
from typing import Optional


class BaseItem:
    """BaseItem"""

    def __init__(self, conn, cursor, table_name: Optional[str] = None):
        """Create an instance of a BaseItem

        :param conn database connection
        :param cursor database cursor
        :param table_name table the item represents
        """
        self.conn = conn
        self.cursor = cursor
        self.table_name = table_name

    def create(self, data):
        """Create a new row in the database

        :param data: row data
        :return: newly inserted row
        """
        fields = []
        values = []
        for key in data.keys():
            if key != "uid":
                fields.append(f"{key}")
                values.append(f":{key}")

        sql = f"""INSERT INTO {self.table_name} (
            {','.join(fields)}
        ) VALUES (
            {','.join(values)}
        ) RETURNING *;"""
        self.cursor.execute(sql, data)
        new_record = self.cursor.fetchone()
        self.conn.commit()
        return new_record

    def read(self, where: Optional[str] = None):
        """Read from the table

        :param where optional where clause
        """
        sql = f"SELECT * FROM {self.table_name} WHERE archived = 0"
        if where:
            sql += f" AND {where}"

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, data):
        """Update record in table

        :param data details to update
        """
        fields = []
        for key in data.keys():
            if key != "uid":
                fields.append(f"{key}=:{key}")

        sql = f"UPDATE {self.table_name} SET {','.join(fields)} WHERE uid=:uid"
        self.cursor.execute(sql, data)
        self.conn.commit()

    def delete(self, uid: int):
        """Delete/archive row in table

        :param uid identifer or row
        """
        sql = f"UPDATE {self.table_name} SET archived=1 WHERE uid={uid}"
        self.cursor.execute(sql)
        self.conn.commit()
