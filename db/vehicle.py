"""Interface to the 'vehicle' table."""
from db.base_item import BaseItem


class Vehicle(BaseItem):
    def get(self):
        self.cursor.execute(
            """
            SELECT
            ID,
            reg_no,
            make,
            model,
            year,
            purchase_price,
            purchase_date,
            purchase_odometer,
            fuel_type_id,
            fuel_capacity,
            oil_type,
            oil_capacity,
            tyre_size_front,
            tyre_size_rear,
            tyre_pressure_front,
            tyre_pressure_rear
            FROM vehicle
            """
        )

        return self.cursor.fetchall()

    def add(self, vehicle):
        """
        Add/amend vehicle record
        """
        if "id" in vehicle:
            sql = """
            UPDATE vehicle SET
            reg_no=:reg_no,
            make=:make,
            model=:model,
            year=:year,
            purchase_price=:purchase_price,
            purchase_date=:purchase_date,
            purchase_odometer=:purchase_odometer,
            fuel_type_id=:fuel_type_id,
            fuel_capacity=:fuel_capacity,
            oil_type=:oil_type,
            oil_capacity=:oil_capacity,
            tyre_size_front=:tyre_size_front,
            tyre_size_rear=:tyre_size_rear,
            tyre_pressure_front=:tyre_pressure_front,
            tyre_pressure_rear=:tyre_pressure_rear
            WHERE id=:id
            """

        else:
            sql = """INSERT INTO vehicle (
                reg_no,
                make,
                model,
                year,
                purchase_price,
                purchase_date,
                purchase_odometer,
                fuel_type_id,
                fuel_capacity,
                oil_type,
                oil_capacity,
                tyre_size_front,
                tyre_size_rear,
                tyre_pressure_front,
                tyre_pressure_rear
                ) VALUES (
                :reg_no,
                :make,
                :model,
                :year,
                :purchase_price,
                :purchase_date,
                :purchase_odometer,
                :fuel_type_id,
                :fuel_capacity,
                :oil_type,
                :oil_capacity,
                :tyre_size_front,
                :tyre_size_rear,
                :tyre_pressure_front,
                :tyre_pressure_rear
                )"""

        self.cursor.execute(sql, vehicle)
        self.conn.commit()
