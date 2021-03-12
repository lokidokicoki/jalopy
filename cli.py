from PyInquirer import prompt, Separator
import db
import utils


running = True

sepString = "\n===\n"


def getTypeChoices(requiredType):
    """
    Get 'type' records, either ruel or record based on 'requiredType'
    """
    types = db.getFuelTypes() if requiredType == "fuel" else db.getRecordTypes()
    choices = [{"name": i[1], "value": i[0]} for i in types]

    return choices


def recordsMenu():
    """
    CRUD ops for records
    """
    questions = [
        {
            "type": "list",
            "name": "opts",
            "message": "Records menu",
            "choices": [
                {"name": "Add", "value": "add"},
                {"name": "Edit", "value": "edit"},
                {"name": "Remove", "value": "remove"},
                Separator(),
                {"name": "Back", "value": "back"},
            ],
        }
    ]

    answers = prompt(questions)

    if answers["opts"] == "add":
        print("\nAdd record")
        recordForm()
    elif answers["opts"] == "edit":
        print("\nEdit record")
        vehicle = selectVehicle()
        record = selectRecord(vehicle)
        recordForm(record)
    elif answers["opts"] == "remove":
        print("TBD: remove vehicle")
    else:
        print("Return to main")


def vehiclesMenu():
    """
    CRUD ops for vehicles
    """
    questions = [
        {
            "type": "list",
            "name": "opts",
            "message": "Vehicle menu",
            "choices": [
                {"name": "Add", "value": "add"},
                {"name": "Edit", "value": "edit"},
                {"name": "Remove", "value": "remove"},
                {"name": "Stats", "value": "stats"},
                Separator(),
                {"name": "Back", "value": "back"},
            ],
        }
    ]

    answers = prompt(questions)

    if answers["opts"] == "add":
        print("\nAdd vehicle")
        vehicleForm()
    elif answers["opts"] == "edit":
        print("\nEdit vehicle")
        vehicle = selectVehicle()
        vehicleForm(vehicle)
    elif answers["opts"] == "stats":
        print("\nStats for vehicle")
        vehicle = selectVehicle()
        results = utils.stats(vehicle)
        print("Record counts:")
        for i in results["counts"]:
            print("{}: {}".format(i["name"], i["count"]))
        print("----")
        print("Avg. MPG: {:0.2f}".format(results["avgMpg"]))
        print("Avg. km/l: {:0.2f}".format(results["avgKpl"]))
        print("Avg. l/100Km: {:0.2f}".format(results["avgL100"]))
        print("Total cost: {:0.2f}".format(results["totalCost"]))
    elif answers["opts"] == "remove":
        print("TBD: remove vehicle")
    else:
        print("return to main")


def selectVehicle():
    """
    Prompt user to select a vehicle
    """
    allVehicles = db.getVehicles()

    questions = [
        {
            "type": "list",
            "name": "opts",
            "message": "Select vehicle",
            "choices": [{"name": i[1], "value": i[0]} for i in allVehicles],
        }
    ]

    answers = prompt(questions)

    return next(x for x in allVehicles if x[0] == answers["opts"])


def selectRecord(vehicle):
    """
    Select a record for a specific vehicle
    """
    allRecords = db.getRecords(vehicle["ID"])

    questions = [
        {
            "type": "list",
            "name": "opts",
            "message": "Select record",
            "choices": [{"name": i["DATE"], "value": i["ID"]} for i in allRecords],
        }
    ]

    answers = prompt(questions)

    return next(x for x in allRecords if x[0] == answers["opts"])


def recordForm(record=None):
    """
    Create/edit 'record'
    """
    allVehicles = db.getVehicles()
    questions = [
        {
            "type": "list",
            "name": "VEHICLE_ID",
            "message": "Reg. No.:",
            "default": record["VEHICLE_ID"] if record else "",
            "choices": [{"name": i[1], "value": i[0]} for i in allVehicles],
        },
        {
            "type": "list",
            "name": "RECORD_TYPE_ID",
            "message": "Type",
            "default": record["RECORD_TYPE_ID"] if record else "",
            "choices": getTypeChoices("record"),
        },
        {
            "type": "input",
            "name": "DATE",
            "message": "Date",
            "default": record["DATE"] if record else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "ODOMETER",
            "message": "Odometer",
            "default": str(record["ODOMETER"]) if record else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "TRIP",
            "message": "Trip (optional)",
            "default": str(record["TRIP"]) if record else "",
        },
        {
            "type": "input",
            "name": "COST",
            "message": "Cost",
            "default": str(record["COST"]) if record else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "ITEM_COUNT",
            "message": "Item Count",
            "default": str(record["ITEM_COUNT"]) if record else "1",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "NOTES",
            "message": "Notes (optional)",
            "default": record["NOTES"] if record else "",
        },
    ]

    answers = prompt(questions)

    # process, then saveo
    if record:
        answers["ID"] = record["ID"]

    answers["VEHICLE_ID"] = int(answers["VEHICLE_ID"])
    answers["RECORD_TYPE_ID"] = int(answers["RECORD_TYPE_ID"])
    answers["ODOMETER"] = int(answers["ODOMETER"])
    answers["TRIP"] = float(answers["TRIP"])
    answers["COST"] = float(answers["COST"])
    answers["ITEM_COUNT"] = float(answers["ITEM_COUNT"])

    # if it is a fuel record, calculate & display the fuel economy
    if answers["RECORD_TYPE_ID"] == 1:
        results = utils.calculateEconomy(answers)
        print("{:0.2f} mpg".format(results["mpg"]))
        print("{:0.2f} kpl".format(results["kpl"]))
        print("{:0.2f} l/100Km".format(results["l100"]))

    db.addRecord(answers)


def vehicleForm(vehicle=None):
    """
    Create/edit vehicle
    """
    questions = [
        {
            "type": "input",
            "name": "REG_NO",
            "message": "Reg. No.:",
            "default": vehicle["REG_NO"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "MAKE",
            "message": "Make",
            "default": vehicle["MAKE"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "MODEL",
            "message": "Model",
            "default": vehicle["MODEL"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "YEAR",
            "message": "Year",
            "default": str(vehicle["YEAR"]) if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "PURCHASE_DATE",
            "message": "Purchase Date",
            "default": vehicle["PURCHASE_DATE"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "PURCHASE_PRICE",
            "message": "Purchase Price",
            "default": str(vehicle["PURCHASE_PRICE"]) if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "list",
            "name": "FUEL_TYPE_ID",
            "message": "Fuel type",
            "choices": getTypeChoices("fuel"),
            "default": vehicle["FUEL_TYPE_ID"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "FUEL_CAPACITY",
            "message": "Fuel Capacity (ltr)",
            "default": str(vehicle["FUEL_CAPACITY"]) if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "OIL_TYPE",
            "message": "Oil Type",
            "default": vehicle["OIL_TYPE"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "OIL_CAPACITY",
            "message": "Oil Capacity (ltr)",
            "default": str(vehicle["OIL_CAPACITY"]) if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "TYRE_SIZE_FRONT",
            "message": "Tyre size front",
            "default": vehicle["TYRE_SIZE_FRONT"] if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "TYRE_PRESSURE_FRONT",
            "message": "Tyre pressure front",
            "default": str(vehicle["TYRE_PRESSURE_FRONT"]) if vehicle else "",
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "TYRE_SIZE_REAR",
            "message": "Tyre size rear",
            "default": lambda x: vehicle["TYRE_SIZE_REAR"]
            if vehicle
            else x["TYRE_SIZE_FRONT"],
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
        {
            "type": "input",
            "name": "TYRE_PRESSURE_REAR",
            "message": "Tyre pressure rear",
            "default": lambda x: str(vehicle["TYRE_PRESSURE_REAR"])
            if vehicle
            else x["TYRE_PRESSURE_FRONT"],
            "validate": lambda val: len(val) != 0 or "Please supply a value",
        },
    ]

    answers = prompt(questions)

    # process, then save
    answers["REG_NO"] = answers["REG_NO"].upper()
    answers["MAKE"] = answers["MAKE"].lower().capitalize()
    answers["MODEL"] = answers["MODEL"].lower().capitalize()
    answers["YEAR"] = int(answers["YEAR"])
    answers["PURCHASE_PRICE"] = float(answers["PURCHASE_PRICE"])
    answers["FUEL_CAPACITY"] = float(answers["FUEL_CAPACITY"])
    answers["OIL_CAPACITY"] = float(answers["OIL_CAPACITY"])
    answers["FUEL_TYPE_ID`"] = int(answers["FUEL_TYPE_ID"])
    answers["TYRE_PRESSURE_FRONT`"] = float(answers["TYRE_PRESSURE_FRONT"])
    answers["TYRE_PRESSURE_REAR`"] = float(answers["TYRE_PRESSURE_REAR"])

    if vehicle:
        answers["ID"] = vehicle["ID"]

    return db.addVehicle(answers)


def mainMenu():
    """
    Main menu
    """
    global running

    questions = [
        {
            "type": "list",
            "name": "opts",
            "message": "Things to do",
            "choices": [
                {"name": "Vehicles", "key": "v", "value": "vehicles"},
                {"name": "Records", "key": "r", "value": "records"},
                Separator(),
                {"name": "Exit", "key": "x", "value": "exit"},
            ],
        }
    ]

    answers = prompt(questions)

    if answers["opts"] == "exit":
        running = False
    elif answers["opts"] == "vehicles":
        vehiclesMenu()
    elif answers["opts"] == "records":
        recordsMenu()


def main():
    """Mainloop for cli"""
    while running:
        mainMenu()
