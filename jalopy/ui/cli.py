"""
Command line interface
"""

import datetime
from typing import Optional

import inquirer  # type: ignore

from jalopy import plots
from jalopy.entities import EntityType, RecordEntity, RecordType, VehicleEntity
from jalopy.entities.entity_manager import EntityManager
from jalopy.ui.base_ui import BaseUI


class Cli(BaseUI):
    """
    CLI Class
    """

    def __init__(self, entity_manager: EntityManager):
        super().__init__(entity_manager)
        self.is_running = True

    @staticmethod
    def get_default_tyre_size(answers):
        """
        Get default tyre size, in this case, front

        :param answers: answers so far
        """
        return answers["tyre_size_front"]

    @staticmethod
    def get_default_tyre_pressure(answers):
        """
        Get default tyre pressure, in this case, front

        :param answers: answers so far
        """
        return answers["tyre_pressure_front"]

    @staticmethod
    def check_length(_, current):
        """
        Check length of answer

        :param current: current answer
        """
        if len(current) == 0:
            print("No value given")
            raise inquirer.errors.ValidationError("", reason="Please supply a value")

        return True

    @staticmethod
    def check_date(_, current: Optional[str]):
        """
        Check current answer matches required date format

        :param current: current asnwer
        """
        if current is None or len(current) == 0:
            print("No value given")
        else:
            try:
                datetime.date.fromisoformat(current)
            except ValueError as err:
                print(err)
                return False

        return True

    def get_type_choices(self, required_type):
        """
        Get 'type' records, either fuel or record based on 'required_type'

        :param required_type: type we want
        """
        types = (
            self.entity_manager.fuel_types
            if required_type == "fuel"
            else self.entity_manager.record_types
        )
        choices = [(i.name, str(i.uid)) for i in types]

        return choices

    def plot_menu(self):
        """
        Various plots
        """
        questions = [
            inquirer.List(
                "opts",
                message="Records menu",
                choices=[
                    ("Historic prices", "1"),
                    ("Average MPG", "2"),
                    ("Back", "b"),
                ],
            )
        ]

        answers = inquirer.prompt(questions)
        assert answers, "Plot menu failed answers"

        if answers["opts"] == "1":
            print("\nHistoric prices")
            # 1 = fuel
            plots.historic_prices(self.entity_manager.filter_records_by_type(1))
        elif answers["opts"] == "2":
            vehicle = self.select_vehicle()
            if vehicle:
                print("Avg. mpg")
                all_records = self.entity_manager.get_records_for_vehicle(vehicle.uid)
                plots.fuel_economy(
                    vehicle, self.entity_manager.filter_records_by_type(1, all_records)
                )

        else:
            print("Return to main")

    def records_menu(self):
        """
        CRUD ops for records
        """
        questions = [
            inquirer.List(
                "opts",
                message="Records menu",
                choices=[
                    ("List", "l"),
                    ("Add", "a"),
                    ("Edit", "e"),
                    ("Remove", "r"),
                    ("Back", "b"),
                ],
            )
        ]

        answers = inquirer.prompt(questions)
        assert answers, "Record answers failed"

        if answers["opts"] == "a":
            print("\nAdd record")
            self.record_form()
            print("\nRecord added")
        elif answers["opts"] == "l":
            print("\nList records")
            vehicle = self.select_vehicle()
            if vehicle:
                self.select_record(vehicle)
        elif answers["opts"] == "e":
            print("\nEdit record")
            vehicle = self.select_vehicle()
            if vehicle:
                record = self.select_record(vehicle)
                if record:
                    self.record_form(record)
                    print("Record edited")
        elif answers["opts"] == "r":
            print("\nRemove record")
            vehicle = self.select_vehicle()
            if vehicle:
                record = self.select_record(vehicle)
                if record:
                    self.entity_manager.remove(record)
                    print("\nRecord removed")
        else:
            print("Return to main")

    def vehicles_menu(self):
        """
        CRUD ops for vehicles
        """
        questions = [
            inquirer.List(
                "opts",
                message="Vehicle menu",
                choices=[
                    ("Stats", "s"),
                    ("Add", "a"),
                    ("Edit", "e"),
                    ("Remove", "r"),
                    ("Back", "b"),
                ],
            )
        ]

        answers = inquirer.prompt(questions)
        assert answers, "Vehicles answers failed"

        if answers["opts"] == "a":
            print("\nAdd vehicle")
            self.vehicle_form()
            print("\nVehicle added")
        elif answers["opts"] == "e":
            print("\nEdit vehicle")
            vehicle = self.select_vehicle()
            if vehicle:
                self.vehicle_form(vehicle)
                print("\nVehicle edited")
        elif answers["opts"] == "s":
            print("\nStats for vehicle")
            vehicle = self.select_vehicle()
            if vehicle:
                results = self.utils.stats(vehicle)
                print("Record counts:")
                for i in results["counts"]:
                    print(f"{i['name']}: {i['count']}")
                print("----")
                print(f"Avg. MPG: {results['avg_mpg']:0.2f}")
                print(f"Avg. km/l: {results['avg_km_per_litre']:0.2f}")
                print(f"Avg. l/100Km: {results['avg_l100']:0.2f}")
                print(f"Total cost: {results['total_cost']:0.2f}")
                print(f"Total miles: {results['total_miles']:0.2f}")
                print(f"CPM: {results['cpm']:0.2f}")
        elif answers["opts"] == "r":
            print("\nRemove vehicle")
            vehicle = self.select_vehicle()
            if vehicle:
                self.entity_manager.remove(vehicle)
                print("\nVehicle removed")
        else:
            print("return to main")

    def select_vehicle(self) -> Optional[VehicleEntity]:
        """
        Prompt user to select a vehicle

        :returns: a Vehicle
        """
        all_vehicles = self.entity_manager.vehicles  # self.db_client.vehicles.get()

        choices = [(i.reg_no, str(i.uid)) for i in all_vehicles]
        choices.append(("Back", "b"))
        questions = [
            inquirer.List(
                "opts",
                message="Select vehicle",
                choices=choices,  # [(i.reg_no, str(i.uid)) for i in all_vehicles],
            )
        ]

        answers = inquirer.prompt(questions)

        assert answers, "Select vehicle answers failed"
        if answers["opts"] == "b":
            return None

        return next(x for x in all_vehicles if x.uid == int(answers["opts"]))

    def record_summary(self, record: RecordEntity) -> str:
        """
        Print summary of record

        :param record: record to summarise
        """
        record_type = self.entity_manager.get(
            EntityType.RECORD_TYPE, record.record_type_id
        )
        return (
            f"{record.record_date} | "
            f"{record.odometer} | "
            f"{record_type.name if isinstance(record_type, RecordType) else 'n/a'} | "
            f"£{record.cost} | "
            f"{record.notes}"
        )

    def select_record(self, vehicle: VehicleEntity):
        """
        Select a record for a specific vehicle

        :param vehicle: target to get records for
        """
        all_records = self.entity_manager.get_records_for_vehicle(vehicle.uid)

        choices = [(self.record_summary(i), str(i.uid)) for i in all_records]
        choices.append(("Back", "b"))
        questions = [
            inquirer.List(
                "opts",
                message="Select record",
                choices=choices,
            )
        ]

        answers = inquirer.prompt(questions)

        assert answers, "Select record answers failed"
        if answers["opts"] == "b":
            return None

        return next(x for x in all_records if x.uid == int(answers["opts"]))

    def record_form(self, record: Optional[RecordEntity] = None):
        """
        Create/edit 'record'

        :param record: if None, create a new record, else use this to edit.
        """
        print("record_form")
        all_vehicles = self.entity_manager.vehicles
        if record:
            print(record)
            print(type(record.record_type_id))
            print(self.get_type_choices("record"))

        questions = [
            inquirer.List(
                "vehicle_id",
                message="Reg. No.:",
                default=str(record.vehicle_id) if record else "",
                choices=[(i.reg_no, str(i.uid)) for i in all_vehicles],
            ),
            inquirer.List(
                "record_type_id",
                message="Type",
                default=str(record.record_type_id) if record else "1",
                choices=self.get_type_choices("record"),
            ),
            inquirer.Text(
                "record_date",
                message="Date (YYYY-MM-DD)",
                default=(
                    record.record_date.isoformat()
                    if record
                    else datetime.date.today().isoformat()
                ),
                validate=self.check_date,
            ),
            inquirer.Text(
                "odometer",
                message="Odometer",
                default=str(record.odometer) if record else "",
                # validate=self.check_length,
            ),
            inquirer.Text(
                "trip",
                message="Trip (optional)",
                default=str(record.trip) if record else "0",
            ),
            inquirer.Text(
                "cost",
                message="Cost",
                default=str(record.cost) if record else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "item_count",
                message="Item Count",
                default=str(record.item_count) if record else "1",
                # validate=self.check_length,
            ),
            inquirer.Text(
                "notes",
                message="Notes (optional)",
                default=record.notes if record else "",
            ),
        ]

        answers = inquirer.prompt(questions)
        assert answers, "Create/edit record answers failed"

        # process, then save
        if record:
            record.record_type_id = int(answers["record_type_id"])
            record.record_date = datetime.date.fromisoformat(answers["record_date"])
            record.odometer = int(answers["odometer"])
            record.trip = float(answers["trip"])
            record.cost = float(answers["cost"])
            record.item_count = float(answers["item_count"])
        else:
            record = RecordEntity(
                -1,
                int(answers["vehicle_id"]),
                int(answers["record_type_id"]),
                datetime.date.fromisoformat(answers["record_date"]),
                int(answers["odometer"]),
                float(answers["trip"]),
                float(answers["cost"]),
                float(answers["item_count"]),
                answers["notes"],
            )
            self.entity_manager.add(record)

        self.entity_manager.save()

        # if it is a fuel record, calculate & display the fuel economy
        if int(answers["record_type_id"]) == 1:
            results = self.utils.calculate_economy(record)
            print(f"{results['mpg']:0.2f} mpg")
            print(f"{results['kpl']:0.2f} kpl")
            print(f"{results['l100']:0.2f} l/100Km")

    def vehicle_form(self, vehicle: Optional[VehicleEntity] = None):
        """
        Create/edit vehicle

        :param vehicle: if None, create a new record, else use this to edit.
        """
        questions = [
            inquirer.Text(
                "reg_no",
                message="Reg. No.",
                default=vehicle.reg_no if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "make",
                message="Make",
                default=vehicle.make if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "model",
                message="Model",
                default=vehicle.model if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "year",
                message="Year",
                default=str(vehicle.year) if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "purchase_date",
                message="Purchase Date (YYYY-MM-DD)",
                default=vehicle.purchase_date.isoformat() if vehicle else "",
                validate=self.check_date,
            ),
            inquirer.Text(
                "purchase_price",
                message="Purchase Price",
                default=str(vehicle.purchase_price) if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "purchase_odometer",
                message="Purchase Odometer",
                default=str(vehicle.purchase_odometer) if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.List(
                "fuel_type_id",
                message="Fuel type",
                choices=self.get_type_choices("fuel"),
                default=str(vehicle.fuel_type_id) if vehicle else "",
            ),
            inquirer.Text(
                "fuel_capacity",
                message="Fuel Capacity (ltr)",
                default=str(vehicle.fuel_capacity) if vehicle else "0",
                validate=self.check_length,
            ),
            inquirer.Text(
                "oil_type",
                message="Oil Type",
                default=vehicle.oil_type if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "oil_capacity",
                message="Oil Capacity (ltr)",
                default=str(vehicle.oil_capacity) if vehicle else "0",
                validate=self.check_length,
            ),
            inquirer.Text(
                "tyre_size_front",
                message="Tyre size front",
                default=vehicle.tyre_size_front if vehicle else "",
                validate=self.check_length,
            ),
            inquirer.Text(
                "tyre_pressure_front",
                message="Tyre pressure front",
                default=str(vehicle.tyre_pressure_front) if vehicle else "0",
                validate=self.check_length,
            ),
            inquirer.Text(
                "tyre_size_rear",
                message="Tyre size rear",
                default=(
                    vehicle.tyre_size_rear if vehicle else self.get_default_tyre_size
                ),
                validate=self.check_length,
            ),
            inquirer.Text(
                "tyre_pressure_rear",
                message="Tyre pressure rear",
                default=(
                    vehicle.tyre_pressure_rear
                    if vehicle
                    else self.get_default_tyre_pressure
                ),
                validate=self.check_length,
            ),
        ]

        answers = inquirer.prompt(questions)
        assert answers, "Create/edit vehicle answers failed"

        # process, then save
        answers["reg_no"] = answers["reg_no"].upper()
        answers["make"] = answers["make"].lower().capitalize()
        answers["model"] = answers["model"].lower().capitalize()
        answers["year"] = int(answers["year"])
        answers["purchase_date"] = datetime.date.fromisoformat(answers["purchase_date"])
        answers["purchase_price"] = float(answers["purchase_price"])
        answers["purchase_odometer"] = int(answers["purchase_odometer"])
        answers["fuel_capacity"] = float(answers["fuel_capacity"])
        answers["oil_capacity"] = float(answers["oil_capacity"])
        answers["fuel_type_id"] = int(answers["fuel_type_id"])
        answers["tyre_pressure_front"] = float(answers["tyre_pressure_front"])
        answers["tyre_pressure_rear"] = float(answers["tyre_pressure_rear"])

        if vehicle:
            vehicle.reg_no = answers["reg_no"]
            vehicle.make = answers["make"]
            vehicle.model = answers["model"]
            vehicle.year = answers["year"]
            vehicle.purchase_price = answers["purchase_price"]
            vehicle.purchase_date = answers["purchase_date"]
            vehicle.purchase_odometer = answers["purchase_odometer"]
            vehicle.fuel_type_id = answers["fuel_type_id"]
            vehicle.fuel_capacity = answers["fuel_capacity"]
            vehicle.oil_type = answers["oil_type"]
            vehicle.oil_capacity = answers["oil_capacity"]
            vehicle.tyre_size_front = answers["tyre_size_front"]
            vehicle.tyre_size_rear = answers["tyre_size_rear"]
            vehicle.tyre_pressure_front = answers["tyre_pressure_front"]
            vehicle.tyre_pressure_rear = answers["tyre_pressure_rear"]
        else:
            # create new instance, add to collection
            self.entity_manager.add(
                VehicleEntity(
                    -1,
                    answers["reg_no"],
                    answers["make"],
                    answers["model"],
                    answers["year"],
                    answers["purchase_price"],
                    answers["purchase_date"],
                    answers["purchase_odometer"],
                    answers["fuel_type_id"],
                    answers["fuel_capacity"],
                    answers["oil_type"],
                    answers["oil_capacity"],
                    answers["tyre_size_front"],
                    answers["tyre_size_rear"],
                    answers["tyre_pressure_front"],
                    answers["tyre_pressure_rear"],
                )
            )

        self.entity_manager.save()

    def show_main_menu(self):
        """
        Main menu
        """
        questions = [
            inquirer.List(
                "opts",
                message="Things to do",
                choices=[
                    ("Vehicles", "v"),
                    ("Records", "r"),
                    ("Plots", "p"),
                    ("Exit", "x"),
                ],
            )
        ]

        answers = inquirer.prompt(questions)

        assert answers, "Main answers failed"
        if answers["opts"] == "x":
            self.is_running = False
        elif answers["opts"] == "v":
            self.vehicles_menu()
        elif answers["opts"] == "r":
            self.records_menu()
        elif answers["opts"] == "p":
            self.plot_menu()

    def main(self):
        """Mainloop for cli"""
        while self.is_running:
            self.show_main_menu()
