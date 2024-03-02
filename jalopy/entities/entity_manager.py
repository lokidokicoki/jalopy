"""Entity Manager"""

import datetime
from dataclasses import asdict
from typing import List, Optional, Union

from jalopy.db.dbclient import DatabaseClient

from .entity_type import EntityType
from .fuel_type import FuelType
from .record import RecordEntity
from .record_type import RecordType
from .vehicle import VehicleEntity


class EntityManager:
    """
    The EntityManager collates all entities and provides methods to get and add new ones
    """

    def __init__(self, dbclient: DatabaseClient):
        self.records: List[RecordEntity] = []
        self.vehicles: List[VehicleEntity] = []
        self.record_types: List[RecordType] = []
        self.fuel_types: List[FuelType] = []
        self.dbclient = dbclient

    def get(
        self, entity_type: EntityType, uid: int
    ) -> Optional[Union[VehicleEntity, RecordEntity, RecordType, FuelType]]:
        """
        Get a specific entity from the collection

        :param entity_type: type of entity to get
        :param uid: entity UID
        """

        if uid is None:
            raise TypeError(f"get missing uid for entity_type {entity_type}")

        collection = None
        if entity_type == EntityType.VEHICLE:
            collection = self.vehicles
        elif entity_type == EntityType.RECORD:
            collection = self.records
        elif entity_type == EntityType.RECORD_TYPE:
            collection = self.record_types
        elif entity_type == EntityType.FUEL_TYPE:
            collection = self.fuel_types
        else:
            raise TypeError(f"Unknown entity type {entity_type}!")

        return next((x for x in collection if x.uid == uid), None)

    def get_records_for_vehicle(self, vehicle_id: int):
        """
        Get records for a specific vehicle

        :param vehicle_id: UID of vehicle
        """
        if vehicle_id is None:
            raise TypeError("get_records_for_vehicle missing entity_id")

        records = [
            x for x in self.records if x.vehicle_id == vehicle_id and x.archived == 0
        ]

        records.sort(key=lambda x: x.record_date)

        return records

    def add(self, entity: Union[VehicleEntity, RecordEntity, RecordType, FuelType]):
        """
        Add an entity to the relevant collection

        :param entity: to be added
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
        """
        Save all details
        """
        for entity in self.vehicles:
            if entity.uid == -1:
                retval = self.dbclient.vehicle.create(self.as_record(entity))
                entity.uid = retval["uid"]
            else:
                self.dbclient.vehicle.update(self.as_record(entity))

        for entity in self.records:
            if entity.uid == -1:
                retval = self.dbclient.record.create(self.as_record(entity))
                entity.uid = retval["uid"]
            else:
                self.dbclient.record.update(self.as_record(entity))

        self.dbclient.commit()

    @staticmethod
    def as_record(entity):
        """
        Convert entity dict members to correct type for DB update.

        :param entity: to be converted
        """
        record = asdict(entity)
        for key in record.keys():
            if isinstance(record[key], datetime.date):
                record[key] = datetime.date.isoformat(record[key])
        return record

    def remove(self, entity: Union[RecordEntity, VehicleEntity]):
        """
        Remove an Entity from the database

        :param entity: the entity isntance to remove
        :type entity: Union[RecordEntity,VehicleEntity]
        """
        if isinstance(entity, VehicleEntity):
            self.dbclient.vehicle.delete(entity.uid)
            self.vehicles.remove(entity)
        elif isinstance(entity, RecordEntity):
            self.dbclient.record.delete(entity.uid)
            self.records.remove(entity)
        else:
            raise TypeError(f"add: unknown entity {entity}")

    def filter_records_by_type(
        self, type_: int, records: Optional[List[RecordEntity]] = None
    ):
        """
        Filter all or subset of records by record type

        :param type_: record type to filter for
        :param records: optional list of records to filter
        """
        if records:
            records = [
                x for x in records if x.record_type_id == type_ and x.archived == 0
            ]
        else:
            records = [
                x for x in self.records if x.record_type_id == type_ and x.archived == 0
            ]

        records.sort(key=lambda x: x.record_date)

        return records
