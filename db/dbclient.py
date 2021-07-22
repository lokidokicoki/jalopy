"""
Database client
"""
import sqlite3

from . import records, vehicles


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
        self.vehicles = vehicles.Vehicles(self.conn, self.cursor)
        self.records = records.Records(self.conn, self.cursor)

    def create_database(self):
        """
        Create DB if none exists
        """
        sql = "SELECT name from sqlite_master WHERE type='table' and name=?"

        # test for vehicles vehicle
        self.cursor.execute(sql, ["VEHICLES"])
        result = self.cursor.fetchone()

        if result is None:
            print("create jalopy.db tables")
            self.cursor.executescript(
                """
                CREATE TABLE VEHICLES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    REG_NO CHAR(10) NOT NULL,
                    MAKE TEXT NOT NULL,
                    MODEL TEXT NOT NULL,
                    YEAR INTEGER NOT NULL,
                    PURCHASE_DATE TEXT,
                    PURCHASE_PRICE REAL,
                    PURCHASE_ODOMETER INTEGER,
                    FUEL_TYPE_ID INTEGER NOT NULL,
                    FUEL_CAPACITY REAL,
                    OIL_TYPE TEXT,
                    OIL_CAPACITY REAL,
                    TYRE_SIZE_FRONT TEXT,
                    TYRE_SIZE_REAR TEXT,
                    TYRE_PRESSURE_FRONT REAL,
                    TYRE_PRESSURE_REAR REAL
                );

                CREATE TABLE FUEL_TYPES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL
                );

                INSERT INTO FUEL_TYPES(NAME) VALUES('Unleaded');
                INSERT INTO FUEL_TYPES(NAME) VALUES('Super Unleaded');
                INSERT INTO FUEL_TYPES(NAME) VALUES('Diesel');
                INSERT INTO FUEL_TYPES(NAME) VALUES('Super Diesel');

                CREATE TABLE RECORDS(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    VEHICLE_ID INTEGER NOT NULL,
                    RECORD_TYPE_ID INTEGER NOT NULL,
                    DATE TEXT NOT NULL,
                    ODOMETER INTEGER NOT NULL,
                    TRIP REAL,
                    COST REAL NOT NULL,
                    ITEM_COUNT REAL,
                    NOTES TEXT
                );

                CREATE TABLE RECORD_TYPES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL
                );
                INSERT INTO RECORD_TYPES(NAME) VALUES('Fuel');
                INSERT INTO RECORD_TYPES(NAME) VALUES('Service');
                INSERT INTO RECORD_TYPES(NAME) VALUES('Maintenance');
                INSERT INTO RECORD_TYPES(NAME) VALUES('Tax');
                INSERT INTO RECORD_TYPES(NAME) VALUES('Insurance');
                INSERT INTO RECORD_TYPES(NAME) VALUES('M.O.T.');
                """
            )
            self.conn.commit()
        else:
            print("DB exists")

    def get_record_types(self):
        """
        Get all record types
        """
        self.cursor.execute("SELECT ID,NAME from RECORD_TYPES")
        return self.cursor.fetchall()

    def get_fuel_types(self):
        """
        Get fuel types
        """
        self.cursor.execute("SELECT ID,NAME from FUEL_TYPES")
        return self.cursor.fetchall()
