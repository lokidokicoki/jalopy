"""Represents a bill of some type, e.g. a service, MOT, or fuel purchase"""
from dataclasses import dataclass
from datetime import date

from .base_entity import BaseEntity


@dataclass
class RecordEntity(BaseEntity):
    """RecordEntity"""

    vehicle_id: int
    record_type_id: int
    record_date: date
    odometer: int
    trip: float
    cost: float
    item_count: float
