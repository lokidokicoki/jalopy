"""
Command line interface
"""

from PyInquirer import Separator, prompt

import utils
from entities.entity_manager import EntityManager

from .base_ui import BaseUI


class Cli(BaseUI):
    """
    CLI Class
    """

    is_running = True

    def __init__(self, entity_manager: EntityManager = None):
        super().__init__(entity_manager)

    def get_type_choices(self, required_type):
        """
        Get 'type' records, either ruel or record based on 'required_type'
        """
        types = (
            self.db_client.get_fuel_types()
            if required_type == "fuel"
            else self.db_client.get_record_types()
        )
        choices = [{"name": i[1], "value": i[0]} for i in types]

        return choices

    def records_menu(self):
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
            self.record_form()
        elif answers["opts"] == "edit":
            print("\nEdit record")
            vehicle = self.select_vehicle()
            record = self.select_record(vehicle)
            self.record_form(record)
        elif answers["opts"] == "remove":
            print("TBD: remove vehicle")
        else:
            print("Return to main")

    def vehicles_menu(self):
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
            self.vehicle_form()
        elif answers["opts"] == "edit":
            print("\nEdit vehicle")
            vehicle = self.select_vehicle()
            self.vehicle_form(vehicle)
        elif answers["opts"] == "stats":
            print("\nStats for vehicle")
            vehicle = self.select_vehicle()
            results = self.utils.stats(vehicle)
            print("Record counts:")
            for i in results["counts"]:
                print("{}: {}".format(i["name"], i["count"]))
            print("----")
            print("Avg. MPG: {:0.2f}".format(results["avg_mpg"]))
            print("Avg. km/l: {:0.2f}".format(results["avg_km_per_litre"]))
            print("Avg. l/100Km: {:0.2f}".format(results["avg_l100"]))
            print("Total cost: {:0.2f}".format(results["total_cost"]))
        elif answers["opts"] == "remove":
            print("TBD: remove vehicle")
        else:
            print("return to main")

    def select_vehicle(self):
        """
        Prompt user to select a vehicle
        """
        all_vehicles = self.entity_manager.vehicles  # self.db_client.vehicles.get()

        questions = [
            {
                "type": "list",
                "name": "opts",
                "message": "Select vehicle",
                "choices": [
                    {"name": i.reg_no, "value": i.entity_id} for i in all_vehicles
                ],
            }
        ]

        answers = prompt(questions)

        return next(x for x in all_vehicles if x.entity_id == answers["opts"])

    def record_summary(self, record):
        """
        Print summary of record
        """
        print(f"{record['DATE']}|{record['RECORD_TYPE_ID']}")
        return record["DATE"]

    def select_record(self, vehicle):
        """
        Select a record for a specific vehicle
        """
        all_records = self.db_client.records.get(vehicle["ID"])

        questions = [
            {
                "type": "list",
                "name": "opts",
                "message": "Select record",
                "choices": [
                    {"name": self.record_summary(i), "value": i["ID"]}
                    for i in all_records
                ],
            }
        ]

        answers = prompt(questions)

        return next(x for x in all_records if x[0] == answers["opts"])

    def record_form(self, record=None):
        """
        Create/edit 'record'
        """
        all_vehicles = self.db_client.vehicles.get()
        if record:
            print(record["VEHICLE_ID"])
            print(record["RECORD_TYPE_ID"])
            print(record["DATE"])
        questions = [
            {
                "type": "list",
                "name": "VEHICLE_ID",
                "message": "Reg. No.:",
                "default": record["VEHICLE_ID"] if record else "",
                "choices": [{"name": i[1], "value": i[0]} for i in all_vehicles],
            },
            {
                "type": "list",
                "name": "RECORD_TYPE_ID",
                "message": "Type",
                "default": record["RECORD_TYPE_ID"] if record else "",
                "choices": self.get_type_choices("record"),
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
                "default": str(record["TRIP"]) if record else "0",
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
            results = utils.calculate_economy(answers)
            print("{:0.2f} mpg".format(results["mpg"]))
            print("{:0.2f} kpl".format(results["kpl"]))
            print("{:0.2f} l/100Km".format(results["l100"]))

        self.db_client.records.add(answers)

    def vehicle_form(self, vehicle=None):
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
                "type": "input",
                "name": "PURCHASE_ODOMETER",
                "message": "Purchase Odometer",
                "default": str(vehicle["PURCHASE_ODOMETER"]) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "list",
                "name": "FUEL_TYPE_ID",
                "message": "Fuel type",
                "choices": self.get_type_choices("fuel"),
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
        answers["PURCHASE_ODOMETER"] = int(answers["PURCHASE_ODOMETER"])
        answers["FUEL_CAPACITY"] = float(answers["FUEL_CAPACITY"])
        answers["OIL_CAPACITY"] = float(answers["OIL_CAPACITY"])
        answers["FUEL_TYPE_ID`"] = int(answers["FUEL_TYPE_ID"])
        answers["TYRE_PRESSURE_FRONT`"] = float(answers["TYRE_PRESSURE_FRONT"])
        answers["TYRE_PRESSURE_REAR`"] = float(answers["TYRE_PRESSURE_REAR"])

        if vehicle:
            answers["ID"] = vehicle["ID"]

        return self.db_client.vehicles.add(answers)

    def show_main_menu(self):
        """
        Main menu
        """
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
            self.is_running = False
        elif answers["opts"] == "vehicles":
            self.vehicles_menu()
        elif answers["opts"] == "records":
            self.records_menu()

    def main(self):
        """Mainloop for cli"""
        while self.is_running:
            self.show_main_menu()
