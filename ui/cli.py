"""
Command line interface
"""

from PyInquirer import Separator, prompt

from entities import EntityManager, RecordEntity
import datetime

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
            self.entity_manager.fuel_types
            if required_type == "fuel"
            else self.entity_manager.record_types
        )
        choices = [{"name": i.name, "value": i.entity_id} for i in types]

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

    @staticmethod
    def record_summary(record):
        """
        Print summary of record
        """
        return f"{record.record_date}|{record.record_type_id}"

    def select_record(self, vehicle):
        """
        Select a record for a specific vehicle
        """
        all_records = self.entity_manager.get_records_for_vehicle(vehicle.entity_id)
        # records.get(vehicle["id"])

        questions = [
            {
                "type": "list",
                "name": "opts",
                "message": "Select record",
                "choices": [
                    {"name": self.record_summary(i), "value": i.entity_id}
                    for i in all_records
                ],
            }
        ]

        answers = prompt(questions)

        return next(x for x in all_records if x.entity_id == answers["opts"])

    def record_form(self, record=None):
        """
        Create/edit 'record'
        """
        print("record_form")
        all_vehicles = self.entity_manager.vehicles
        if record:
            print(record)

        questions = [
            {
                "type": "list",
                "name": "vehicle_id",
                "message": "Reg. No.:",
                "default": record.vehicle_id if record else "",
                "choices": [
                    {"name": i.reg_no, "value": i.entity_id} for i in all_vehicles
                ],
            },
            {
                "type": "list",
                "name": "record_type_id",
                "message": "Type",
                "default": record.record_type_id if record else "",
                "choices": self.get_type_choices("record"),
            },
            {
                "type": "input",
                "name": "record_date",
                "message": "Date",
                "default": record.record_date.strftime("%Y/%m/%d") if record else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "odometer",
                "message": "Odometer",
                "default": str(record.odometer) if record else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "trip",
                "message": "Trip (optional)",
                "default": str(record.trip) if record else "0",
            },
            {
                "type": "input",
                "name": "cost",
                "message": "Cost",
                "default": str(record.cost) if record else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "item_count",
                "message": "Item Count",
                "default": str(record.item_count) if record else "1",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "notes",
                "message": "Notes (optional)",
                "default": record.notes if record else "",
            },
        ]

        answers = prompt(questions)

        # process, then saveo
        if record:
            record.record_type_id = int(answers["record_type_id"])
            record.record_date = (
                datetime.datetime.strptime(answers["record_date"], "%Y/%m/%d").date(),
            )
            record.odometer = int(answers["odometer"])
            record.trip = float(answers["trip"])
            record.cost = float(answers["cost"])
            record.item_count = float(answers["item_count"])
            print("todo: save updated record")
        else:
            record = RecordEntity(
                -1,
                int(answers["vehicle_id"]),
                int(answers["record_type_id"]),
                datetime.datetime.strptime(answers["record_date"], "%Y/%m/%d").date(),
                int(answers["odometer"]),
                float(answers["trip"]),
                float(answers["cost"]),
                float(answers["item_count"]),
                answers["notes"],
            )
            print("todo: add new record and save to db")

        # answers["vehicle_id"] = int(answers["vehicle_id"])
        # answers["record_type_id"] = int(answers["record_type_id"])
        # answers["odometer"] = int(answers["odometer"])
        # answers["trip"] = float(answers["trip"])
        # answers["cost"] = float(answers["cost"])
        # answers["item_count"] = float(answers["item_count"])

        # if it is a fuel record, calculate & display the fuel economy
        if answers["record_type_id"] == 1:
            results = self.utils.calculate_economy(record)
            print("{:0.2f} mpg".format(results["mpg"]))
            print("{:0.2f} kpl".format(results["kpl"]))
            print("{:0.2f} l/100Km".format(results["l100"]))

        # self.entity_manager.records.add(answers)

    def vehicle_form(self, vehicle=None):
        """
        Create/edit vehicle
        """
        questions = [
            {
                "type": "input",
                "name": "reg_no",
                "message": "Reg. No.:",
                "default": vehicle.reg_no if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "make",
                "message": "Make",
                "default": vehicle.make if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "model",
                "message": "Model",
                "default": vehicle.model if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "year",
                "message": "Year",
                "default": str(vehicle.year) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "purchase_date",
                "message": "Purchase Date",
                "default": vehicle.purchase_date if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "purchase_price",
                "message": "Purchase Price",
                "default": str(vehicle.purchase_price) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "purchase_odometer",
                "message": "Purchase Odometer",
                "default": str(vehicle.purchase_odometer) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "list",
                "name": "fuel_type_id",
                "message": "Fuel type",
                "choices": self.get_type_choices("fuel"),
                "default": vehicle.fuel_type_id if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "fuel_capacity",
                "message": "Fuel Capacity (ltr)",
                "default": str(vehicle.fuel_capacity) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "oil_type",
                "message": "Oil Type",
                "default": vehicle.oil_type if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "oil_capacity",
                "message": "Oil Capacity (ltr)",
                "default": str(vehicle.oil_capacity) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "tyre_size_front",
                "message": "Tyre size front",
                "default": vehicle.tyre_size_front if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "tyre_pressure_front",
                "message": "Tyre pressure front",
                "default": str(vehicle.tyre_pressure_front) if vehicle else "",
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "tyre_size_rear",
                "message": "Tyre size rear",
                "default": lambda x: vehicle.tyre_size_rear
                if vehicle
                else x.tyre_size_front,
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
            {
                "type": "input",
                "name": "tyre_pressure_rear",
                "message": "Tyre pressure rear",
                "default": lambda x: str(vehicle.tyre_pressure_rear)
                if vehicle
                else x.tyre_pressure_front,
                "validate": lambda val: len(val) != 0 or "Please supply a value",
            },
        ]

        answers = prompt(questions)

        # process, then save
        answers["reg_no"] = answers["reg_no"].upper()
        answers["make"] = answers["make"].lower().capitalize()
        answers["model"] = answers["model"].lower().capitalize()
        answers["year"] = int(answers["year"])
        answers["purchase_price"] = float(answers["purchase_price"])
        answers["purchase_odometer"] = int(answers["purchase_odometer"])
        answers["fuel_capacity"] = float(answers["fuel_capacity"])
        answers["oil_capacity"] = float(answers["oil_capacity"])
        answers["fuel_type_id`"] = int(answers["fuel_type_id"])
        answers["tyre_pressure_front`"] = float(answers["tyre_pressure_front"])
        answers["tyre_pressure_rear`"] = float(answers["tyre_pressure_rear"])

        if vehicle:
            answers["id"] = vehicle.id

        return self.entity_manager.vehicles.add(answers)

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
