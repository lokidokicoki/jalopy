"""Entity Manager"""

from enum import Enum
from typing import List, Union

from db.dbclient import DatabaseClient

import datetime
from .record import RecordEntity
from .vehicle import VehicleEntity
from .record_type import RecordType
from .fuel_type import FuelType
from dataclasses import asdict


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
        """Get records for a specific vehicle"""
        if vehicle_id is None:
            raise TypeError("get_records_for_vehicle missing entity_id")
        # print(self.records)
        return [
            x for x in self.records if x.vehicle_id == vehicle_id and x.archived == 0
        ]

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
        """Load all data from dbclient into entities"""
        print("load all data")

        for row in self.dbclient.get_record_types():
            self.add(RecordType(row["uid"], row["name"]))

        for row in self.dbclient.get_fuel_types():
            self.add(FuelType(row["uid"], row["name"]))

        for row in self.dbclient.vehicle.read():
            self.add(
                VehicleEntity(
                    row["uid"],
                    row["reg_no"],
                    row["make"],
                    row["model"],
                    row["year"],
                    row["purchase_price"],
                    datetime.date.fromisoformat(row["purchase_date"]),
                    row["purchase_odometer"],
                    row["fuel_type_id"],
                    row["fuel_capacity"],
                    row["oil_type"],
                    row["oil_capacity"],
                    row["tyre_size_front"],
                    row["tyre_size_rear"],
                    row["tyre_pressure_front"],
                    row["tyre_pressure_rear"],
                    row["archived"],
                )
            )

        for row in self.dbclient.record.read():
            self.add(
                RecordEntity(
                    row["uid"],
                    row["vehicle_id"],
                    row["record_type_id"],
                    datetime.date.fromisoformat(row["record_date"]),
                    int(row["odometer"]),
                    float(row["trip"]),
                    float(row["cost"]),
                    float(row["item_count"]),
                    row["notes"],
                    row["archived"],
                )
            )

    def save(self):
        for entity in self.vehicles:
            if entity.uid == -1:
                self.dbclient.vehicle.create(self.as_record(entity))
            else:
                self.dbclient.vehicle.update(self.as_record(entity))

        for entity in self.records:
            if entity.uid == -1:
                self.dbclient.record.create(self.as_record(entity))
            else:
                self.dbclient.record.update(self.as_record(entity))

    @staticmethod
    def as_record(entity):
        record = asdict(entity)
        for key in record.keys():
            if isinstance(record[key], datetime.date):
                record[key] = datetime.date.isoformat(record[key])
        return record

    def remove(self, entity):
        if isinstance(entity, VehicleEntity):
            self.dbclient.vehicle.delete(entity.uid)
            self.vehicles.remove(entity)
        elif isinstance(entity, RecordEntity):
            self.dbclient.record.delete(entity.uid)
            self.records.remove(entity)
        else:
            raise TypeError(f"add: unknown entity {entity}")
