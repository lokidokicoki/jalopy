"""
Collection of utility functions
"""
from db.dbclient import DatabaseClient

LITRES_PER_GALLON = 4.54609
KM_PER_MILE = 1.60934
MPG_TO_L100_KM = 235.215

dbclient = None


def set_dbclient(client: DatabaseClient):
    dbclient = client


def calculate_economy(record):
    """
    mpg
    l/100km
    km/l
    """
    trip_km = record["TRIP"] * KM_PER_MILE
    kpl = trip_km / record["ITEM_COUNT"]
    mpg = record["TRIP"] / (record["ITEM_COUNT"] / LITRES_PER_GALLON)
    l100 = MPG_TO_L100_KM / mpg

    return {"mpg": mpg, "kpl": kpl, "l100": l100}


def stats(vehicle):
    """
    Accumulative stats for this vehicle
    """
    global dbclient

    # get all records for this vehicle
    records = dbclient.records.get(vehicle["ID"])
    types = dbclient.get_record_types()
    total_cost = 0
    avg_mpg = 0
    avg_km_per_litre = 0
    avg_l100 = 0
    counts = [{"id": x["ID"], "name": x["NAME"], "count": 0} for x in types]

    for record in records:
        count = next(x for x in counts if x["id"] == record["RECORD_TYPE_ID"])
        count["count"] = count["count"] + 1
        if record["RECORD_TYPE_ID"] == 1:
            eff = calculate_economy(record)

            avg_mpg = avg_mpg + eff["mpg"]
            avg_km_per_litre = avg_km_per_litre + eff["kpl"]
            avg_l100 = avg_l100 + eff["l100"]

        total_cost = total_cost + record["COST"]
    fuel_count = next(x for x in counts if x["id"] == 1)

    if fuel_count["count"] > 0:
        avg_mpg = avg_mpg / fuel_count["count"]
        avg_km_per_litre = avg_km_per_litre / fuel_count["count"]
        avg_l100 = avg_l100 / fuel_count["count"]

    return {
        "counts": counts,
        "avg_mpg": avg_mpg,
        "avg_km_per_litre": avg_km_per_litre,
        "avg_l100": avg_l100,
        "total_cost": total_cost,
    }
