"""
Base db item
"""
from typing import Optional


class BaseItem:
    def __init__(self, conn, cursor, table_name: Optional[str] = None):
        self.conn = conn
        self.cursor = cursor
        self.table_name = table_name

    def create(self, data):
        print(f"create {self.table_name} record")
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
        )"""
        print(sql)
        self.cursor.execute(sql, data)
        self.conn.commit()

    def read(self, where: Optional[str] = None):
        print(f"read {self.table_name}")
        sql = f"SELECT * FROM {self.table_name} WHERE archived = 0"
        if where:
            sql += f" AND {where}"

        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, data):
        """
        Add/amend record
        """
        print(f"update {self.table_name} record")
        fields = []
        for key in data.keys():
            if key != "uid":
                fields.append(f"{key}=:{key}")

        sql = f"UPDATE {self.table_name} SET {','.join(fields)} WHERE uid=:uid"
        print(sql)
        print(data)
        self.cursor.execute(sql, data)
        self.conn.commit()

    def delete(self, uid: int):
        sql = f"UPDATE {self.table_name} SET archived=1 WHERE uid={uid}"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
