cursor = None
conn = None


def init(_conn, _cursor):
    global cursor, conn
    cursor = _cursor
    conn = _conn


def get(vehicleId=None):
    sql = """
    SELECT * FROM RECORDS
    """

    if vehicleId:
        sql = sql + " where VEHICLE_ID=:VEHICLE_ID"

    cursor.execute(sql, {"VEHICLE_ID": vehicleId})

    return cursor.fetchall()


def add(record):
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

    cursor.execute(sql, record)
    conn.commit()
