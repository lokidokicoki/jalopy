import db

litresPerGallon = 4.54609
kmPerMile = 1.60934
mpgToL100km = 235.215


def calculateEconomy(record):
    """
    mpg
    l/100km
    km/l
    """
    tripKm = record["TRIP"] * kmPerMile

    kpl = tripKm / record["ITEM_COUNT"]
    mpg = record["TRIP"] / (record["ITEM_COUNT"] / litresPerGallon)
    l100 = mpgToL100km / mpg

    return {"mpg": mpg, "kpl": kpl, "l100": l100}


def stats(vehicle):
    """
    Accumulative stats for this vehicle
    """

    # get all records for this vehicle
    records = db.getRecords(vehicle["ID"])
    types = db.getRecordTypes()
    totalCost = 0
    avgMpg = 0
    avgKpl = 0
    avgL100 = 0
    counts = [{"id": x["ID"], "name": x["NAME"], "count": 0} for x in types]

    for record in records:
        count = next(x for x in counts if x["id"] == record["RECORD_TYPE_ID"])
        count["count"] = count["count"] + 1
        if record["RECORD_TYPE_ID"] == 1:
            eff = calculateEconomy(record)

            avgMpg = avgMpg + eff["mpg"]
            avgKpl = avgKpl + eff["kpl"]
            avgL100 = avgL100 + eff["l100"]

        totalCost = totalCost + record["COST"]
    fuelCount = next(x for x in counts if x["id"] == 1)

    avgMpg = avgMpg / fuelCount["count"]
    avgKpl = avgKpl / fuelCount["count"]
    avgL100 = avgL100 / fuelCount["count"]

    return {
        "counts": counts,
        "avgMpg": avgMpg,
        "avgKpl": avgKpl,
        "avgL100": avgL100,
        "totalCost": totalCost,
    }
