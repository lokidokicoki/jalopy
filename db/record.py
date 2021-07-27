"""DB Record getter/setter"""

from db.base_item import BaseItem


class Records(BaseItem):
    """
    DB access for the 'record' table
    """

    def get(self, vehicle_id=None):
        """
        Get all or single vehicle from table.

        """
        sql = "SELECT * FROM record"

        if vehicle_id:
            sql = sql + " WHERE vehicle_id=:vehicle_id"

        self.cursor.execute(sql, {"vehicle_id": vehicle_id})

        return self.cursor.fetchall()

    def add(self, record):
        """
        Add/amend record
        """
        if "id" in record:
            sql = """
                UPDATE record SET
                vehicle_id=:vehicle_id,
                record_type_id=:record_type_id,
                date=:date,
                odometer=:odometer,
                trip=:trip,
                cost=:cost,
                item_count=:item_count,
                notes=:notes
            WHERE id=:id
            """
        else:
            sql = """INSERT INTO record (
                    vehicle_id,
                    record_type_id,
                    date,
                    odometer,
                    trip,
                    cost,
                    item_count,
                    notes
                ) VALUES (
                    :vehicle_id,
                    :record_type_id,
                    :date,
                    :odometer,
                    :trip,
                    :cost,
                    :item_count,
                    :notes
            )"""

        self.cursor.execute(sql, record)
        self.conn.commit()
