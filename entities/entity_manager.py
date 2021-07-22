"""Entity Manager"""

from enum import Enum
from typing import List, Union

from db.dbclient import DatabaseClient

import datetime
from .record import RecordEntity
from .vehicle import VehicleEntity
from .record_type import RecordType
from .fuel_type import FuelType


class EntityType(Enum):
    """EntityType enumerator"""

    VEHICLE = 1
    RECORD = 2


class EntityManager:
    """The EntityManager collates all entities and provides methods to get and
    add new ones"""

    def __init__(self, dbclient: DatabaseClient):
        self.records: List[RecordEntity] = []
        self.vehicles: List[VehicleEntity] = []
        self.record_types: List[RecordType] = []
        self.fuel_types: List[FuelType] = []
        self.dbclient = dbclient

    def get(
        self, entity_type: EntityType, entity_id: int
    ) -> Union[VehicleEntity, RecordEntity]:
        """Get a specific entity from the collection

        :param: entity_type
        :param: entity_id
        """

        if entity_id is None:
            raise TypeError(f"get missing entity_id for entity_type {type}")

        collection = None
        if entity_type == EntityType.VEHICLE:
            collection = self.vehicles
        else:
            collection = self.records

        return next((x for x in collection if x.entity_id == entity_id), None)

    def get_records_for_vehicle(self, vehicle_id: int):
        if vehicle_id is None:
            raise TypeError("get_records_for_vehicle missing entity_id")
        print(self.records)
        return [x for x in self.records if x.vehicle_id == vehicle_id]

    def add(self, entity: Union[VehicleEntity, RecordEntity, RecordType, FuelType]):
        """Add an entity to the relevant collection

        :param: entity
        """
        if isinstance(entity, VehicleEntity):
            self.vehicles.append(entity)
        elif isinstance(entity, RecordEntity):
            self.records.append(entity)
        elif isinstance(entity, RecordType):
            self.record_types.append(entity)
        elif isinstance(entity, FuelType):
            self.fuel_types.append(entity)
        else:
            raise TypeError(f"add: unknown entity {entity}")

    def load(self):
        print("load all data")

        for x in self.dbclient.get_record_types():
            self.add(RecordType(x["ID"], x["NAME"]))

        for x in self.dbclient.get_fuel_types():
            self.add(FuelType(x["ID"], x["NAME"]))

        for x in self.dbclient.vehicles.get():
            self.add(
                VehicleEntity(
                    x["ID"],
                    x["REG_NO"],
                    x["MAKE"],
                    x["MODEL"],
                    x["YEAR"],
                    x["PURCHASE_PRICE"],
                    x["PURCHASE_DATE"],
                    x["PURCHASE_ODOMETER"],
                    x["FUEL_TYPE_ID"],
                    x["FUEL_CAPACITY"],
                    x["OIL_TYPE"],
                    x["OIL_CAPACITY"],
                    x["TYRE_SIZE_FRONT"],
                    x["TYRE_SIZE_REAR"],
                    x["TYRE_PRESSURE_FRONT"],
                    x["TYRE_PRESSURE_REAR"],
                )
            )

        for x in self.dbclient.records.get():
            self.add(
                RecordEntity(
                    x["ID"],
                    x["VEHICLE_ID"],
                    x["RECORD_TYPE_ID"],
                    datetime.datetime.strptime(x["DATE"], "%Y/%m/%d").date(),
                    int(x["ODOMETER"]),
                    float(x["TRIP"]),
                    float(x["COST"]),
                    float(x["ITEM_COUNT"]),
                    x["NOTES"],
                )
            )
