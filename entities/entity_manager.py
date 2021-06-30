"""Entity Manager"""
from enum import Enum
from typing import List, Union

from .record import RecordEntity
from .vehicle import VehicleEntity


class EntityType(Enum):
    """EntityType enumerator"""

    VEHICLE = 1
    RECORD = 2


class EntityManager:
    """The EntityManager collates all entities and provides methods to get and
    add new ones"""

    def __init__(self):
        self.records: List[RecordEntity] = []
        self.vehicles: List[VehicleEntity] = []

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

    def add(self, entity: Union[VehicleEntity, RecordEntity]):
        """Add an entity to the relevant collection

        :param: entity
        """
        if isinstance(entity, VehicleEntity):
            self.vehicles.append(entity)
        elif isinstance(entity, RecordEntity):
            self.records.append(entity)
        else:
            raise TypeError(f"add: unknown entity {entity}")
