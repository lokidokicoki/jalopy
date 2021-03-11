import sqlite3

conn = sqlite3.connect("jalopy.db")
conn.row_factory = sqlite3.Row
cursor = None

def createDB():
    global cursor
    cursor = conn.cursor()
    sql = "SELECT name from sqlite_master WHERE type='table' and name=?"

    # test for vehicles vehicle
    cursor.execute(sql,["VEHICLES"])
    result = cursor.fetchone()

    if result is None:
        print("create jalopy.db tables")
        cursor.executescript("""
            CREATE TABLE VEHICLES(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                REG_NO CHAR(10) NOT NULL,
                MAKE TEXT NOT NULL,
                MODEL TEXT NOT NULL,
                YEAR INTEGER NOT NULL,
                PURCHASE_DATE TEXT,
                PURCHASE_PRICE REAL,
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
                RECORD_TYPE_ID CHAR(1) NOT NULL,
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
            """)
        conn.commit()
    else:
        print("DB exists")


def loadVehicles():
    cursor.execute("""
    SELECT 
    ID, REG_NO, MAKE, MODEL, YEAR, PURCHASE_PRICE, PURCHASE_DATE, FUEL_TYPE_ID, FUEL_CAPACITY, OIL_TYPE, OIL_CAPACITY, TYRE_SIZE_FRONT, TYRE_SIZE_REAR, TYRE_PRESSURE_FRONT, TYRE_PRESSURE_REAR
             FROM VEHICLES
            """)

    return cursor.fetchall()

def getFuelTypes():
    cursor.execute("SELECT ID,NAME from FUEL_TYPES")
    return cursor.fetchall()

def getRecordTypes():
    cursor.execute("SELECT ID,NAME from RECORD_TYPES")
    return cursor.fetchall()

def addVehicle(vehicle):
    if 'ID' in vehicle:
        sql = '''UPDATE VEHICLES set 
    REG_NO=:REG_NO,
    MAKE=:MAKE, 
    MODEL=:MODEL, 
    YEAR=:YEAR, 
    PURCHASE_PRICE=:PURCHASE_PRICE, 
    PURCHASE_DATE=:PURCHASE_DATE,
    FUEL_TYPE_ID=:FUEL_TYPE_ID, 
    FUEL_CAPACITY=:FUEL_CAPACITY, 
    OIL_TYPE=:OIL_TYPE, 
    OIL_CAPACITY=:OIL_CAPACITY, 
    TYRE_SIZE_FRONT=:TYRE_SIZE_FRONT, 
    TYRE_SIZE_REAR=:TYRE_SIZE_REAR, 
    TYRE_PRESSURE_FRONT=:TYRE_PRESSURE_FRONT, 
    TYRE_PRESSURE_REAR=:TYRE_PRESSURE_REAR
    WHERE ID=:ID
    '''

    else:
        sql = '''INSERT INTO VEHICLES (
    REG_NO, MAKE, MODEL, YEAR, PURCHASE_PRICE, PURCHASE_DATE, FUEL_TYPE_ID, FUEL_CAPACITY, OIL_TYPE, OIL_CAPACITY, TYRE_SIZE_FRONT, TYRE_SIZE_REAR, TYRE_PRESSURE_FRONT, TYRE_PRESSURE_REAR
    ) VALUES 
    (
    :REG_NO, :MAKE, :MODEL, :YEAR, :PURCHASE_PRICE, :PURCHASE_DATE, :FUEL_TYPE_ID,:FUEL_CAPACITY, :OIL_TYPE, :OIL_CAPACITY, :TYRE_SIZE_FRONT, :TYRE_SIZE_REAR, :TYRE_PRESSURE_FRONT, :TYRE_PRESSURE_REAR
    )'''

    cursor.execute(sql, vehicle)
    conn.commit()


def loadRecords(vehicleId=None):
    sql= """
    select * from RECORDS
    """

    if vehicleId:
        sql = sql + ' where VEHICLE_ID=:VEHICLE_ID'

    cursor.execute(sql, {'VEHICLE_ID':vehicleId})

    return cursor.fetchall()

def addRecord(record):
    if 'ID' in record:
        sql = '''UPDATE RECORDS set 
                VEHICLE_ID=:VEHICLE_ID,
                RECORD_TYPE_ID=:RECORD_TYPE_ID,
                DATE=:DATE,
                ODOMETER=:ODOMETER,
                TRIP=:TRIP,
                COST=:COST,
                ITEM_COUNT=:ITEM_COUNT,
                NOTES=:NOTES
    WHERE ID=:ID
    '''

    else:
        sql = '''INSERT INTO RECORDS (
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
    )'''

    cursor.execute(sql, record)
    conn.commit()


