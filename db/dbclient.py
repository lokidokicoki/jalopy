import sqlite3
from . import vehicles
from . import records


conn = None
cursor = None


def init():
    global conn, cursor
    conn = sqlite3.connect(
        "jalopy.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    vehicles.init(conn, cursor)
    records.init(conn, cursor)


def createDatabase():
    """
    Create DB if none exists
    """
    sql = "SELECT name from sqlite_master WHERE type='table' and name=?"

    # test for vehicles vehicle
    cursor.execute(sql, ["VEHICLES"])
    result = cursor.fetchone()

    if result is None:
        print("create jalopy.db tables")
        cursor.executescript(
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
        conn.commit()
    else:
        print("DB exists")


def getRecordTypes():
    """
    Get all record types
    """
    cursor.execute("SELECT ID,NAME from RECORD_TYPES")
    return cursor.fetchall()


def getFuelTypes():
    """
    Get fuel types
    """
    cursor.execute("SELECT ID,NAME from FUEL_TYPES")
    return cursor.fetchall()
