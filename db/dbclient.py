"""
Database client
"""
import sqlite3

from . import record, vehicle


class DatabaseClient:
    """
    Database CLient class
    """

    def __init__(self, db_name):
        self.conn = sqlite3.connect(
            db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.vehicle = vehicle.Vehicle(self.conn, self.cursor)
        self.record = record.Record(self.conn, self.cursor)

    def create_database(self):
        """
        Create DB if none exists
        """
        sql = "SELECT name from sqlite_master WHERE type='table' and name=?"

        # test for vehicles vehicle
        self.cursor.execute(sql, ["vehicle"])
        result = self.cursor.fetchone()

        if result is None:
            print("create jalopy.db tables")
            self.cursor.executescript(
                """
                CREATE TABLE vehicle(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    reg_no CHAR(10) NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    purchase_date TEXT,
                    purchase_price REAL,
                    purchase_odometer INTEGER,
                    fuel_type_id INTEGER NOT NULL,
                    fuel_capacity REAL,
                    oil_type TEXT,
                    oil_capacity REAL,
                    tyre_size_front TEXT,
                    tyre_size_rear TEXT,
                    tyre_pressure_front REAL,
                    tyre_pressure_rear REAL
                );

                CREATE TABLE fuel_type(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );

                INSERT INTO fuel_type(name) VALUES('Unleaded');
                INSERT INTO fuel_type(name) VALUES('Super Unleaded');
                INSERT INTO fuel_type(name) VALUES('Diesel');
                INSERT INTO fuel_type(name) VALUES('Super Diesel');

                CREATE TABLE records(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    record_type_id INTEGER NOT NULL,
                    record_date TEXT NOT NULL,
                    odometer INTEGER NOT NULL,
                    trip REAL,
                    cost REAL NOT NULL,
                    item_count REAL,
                    notes TEXT
                );

                CREATE TABLE record_type(
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );
                INSERT INTO record_type(name) VALUES('Fuel');
                INSERT INTO record_type(name) VALUES('Service');
                INSERT INTO record_type(name) VALUES('Maintenance');
                INSERT INTO record_type(name) VALUES('Tax');
                INSERT INTO record_type(name) VALUES('Insurance');
                INSERT INTO record_type(name) VALUES('M.O.T.');
                """
            )
            self.conn.commit()
        else:
            print("DB exists")

    def get_record_types(self):
        """
        Get all record types
        """
        self.cursor.execute("SELECT uid,name FROM record_type")
        return self.cursor.fetchall()

    def get_fuel_types(self):
        """
        Get fuel types
        """
        self.cursor.execute("SELECT uid,name FROM fuel_type")
        return self.cursor.fetchall()
