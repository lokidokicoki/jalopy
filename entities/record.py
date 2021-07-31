"""Represents a bill of some type, e.g. a service, MOT, or fuel purchase"""
from dataclasses import dataclass
from datetime import date


@dataclass
class RecordEntity:
    """RecordEntity"""

    uid: int
    vehicle_id: int
    record_type_id: int
    record_date: date
    odometer: int
    trip: float
    cost: float
    item_count: float
    notes: str
    archived: int = 0
