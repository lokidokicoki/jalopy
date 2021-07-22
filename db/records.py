"""DB Record getter/setter"""

from db.base_item import BaseItem


class Records(BaseItem):
    def get(self, vehicle_id=None):
        sql = """
        SELECT * FROM RECORDS
        """

        if vehicle_id:
            sql = sql + " where VEHICLE_ID=:VEHICLE_ID"

        self.cursor.execute(sql, {"VEHICLE_ID": vehicle_id})

        return self.cursor.fetchall()

    def add(self, record):
        """
        Add/amend record
        """
        if "ID" in record:
            sql = """
                UPDATE RECORDS SET
                VEHICLE_ID=:VEHICLE_ID,
                RECORD_TYPE_ID=:RECORD_TYPE_ID,
                DATE=:DATE,
                ODOMETER=:ODOMETER,
                TRIP=:TRIP,
                COST=:COST,
                ITEM_COUNT=:ITEM_COUNT,
                NOTES=:NOTES
            WHERE ID=:ID
            """
        else:
            sql = """INSERT INTO RECORDS (
                    VEHICLE_ID,
                    RECORD_TYPE_ID,
                    DATE,
                    ODOMETER,
                    TRIP,
                    COST,
                    ITEM_COUNT,
                    NOTES
                ) VALUES (
                    :VEHICLE_ID,
                    :RECORD_TYPE_ID,
                    :DATE,
                    :ODOMETER,
                    :TRIP,
                    :COST,
                    :ITEM_COUNT,
                    :NOTES
            )"""

        self.cursor.execute(sql, record)
        self.conn.commit()
