from db.base_item import BaseItem


class Vehicles(BaseItem):
    def get(self):
        self.cursor.execute(
            """
            SELECT
            ID,
            REG_NO,
            MAKE,
            MODEL,
            YEAR,
            PURCHASE_PRICE,
            PURCHASE_DATE,
            PURCHASE_ODOMETER,
            FUEL_TYPE_ID,
            FUEL_CAPACITY,
            OIL_TYPE,
            OIL_CAPACITY,
            TYRE_SIZE_FRONT,
            TYRE_SIZE_REAR,
            TYRE_PRESSURE_FRONT,
            TYRE_PRESSURE_REAR
            FROM VEHICLES
            """
        )

        return self.cursor.fetchall()

    def add(self, vehicle):
        """
        Add/amend vehicle record
        """
        if "ID" in vehicle:
            sql = """
            UPDATE VEHICLES SET
            REG_NO=:REG_NO,
            MAKE=:MAKE,
            MODEL=:MODEL,
            YEAR=:YEAR,
            PURCHASE_PRICE=:PURCHASE_PRICE,
            PURCHASE_DATE=:PURCHASE_DATE,
            PURCHASE_ODOMETER=:PURCHASE_ODOMETER,
            FUEL_TYPE_ID=:FUEL_TYPE_ID,
            FUEL_CAPACITY=:FUEL_CAPACITY,
            OIL_TYPE=:OIL_TYPE,
            OIL_CAPACITY=:OIL_CAPACITY,
            TYRE_SIZE_FRONT=:TYRE_SIZE_FRONT,
            TYRE_SIZE_REAR=:TYRE_SIZE_REAR,
            TYRE_PRESSURE_FRONT=:TYRE_PRESSURE_FRONT,
            TYRE_PRESSURE_REAR=:TYRE_PRESSURE_REAR
            WHERE ID=:ID
            """

        else:
            sql = """INSERT INTO VEHICLES (
                REG_NO,
                MAKE,
                MODEL,
                YEAR,
                PURCHASE_PRICE,
                PURCHASE_DATE,
                PURCHASE_ODOMETER,
                FUEL_TYPE_ID,
                FUEL_CAPACITY,
                OIL_TYPE,
                OIL_CAPACITY,
                TYRE_SIZE_FRONT,
                TYRE_SIZE_REAR,
                TYRE_PRESSURE_FRONT,
                TYRE_PRESSURE_REAR
                ) VALUES (
                :REG_NO,
                :MAKE,
                :MODEL,
                :YEAR,
                :PURCHASE_PRICE,
                :PURCHASE_DATE,
                :PURCHASE_ODOMETER,
                :FUEL_TYPE_ID,
                :FUEL_CAPACITY,
                :OIL_TYPE,
                :OIL_CAPACITY,
                :TYRE_SIZE_FRONT,
                :TYRE_SIZE_REAR,
                :TYRE_PRESSURE_FRONT,
                :TYRE_PRESSURE_REAR
                )"""

        self.cursor.execute(sql, vehicle)
        self.conn.commit()
