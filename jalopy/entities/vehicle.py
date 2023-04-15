"""Represents a vehicle"""
from dataclasses import dataclass
from datetime import date


@dataclass
class VehicleEntity:
    """VehicleEntity"""

    uid: int
    reg_no: str
    make: str
    model: str
    year: int
    purchase_price: float
    purchase_date: date
    purchase_odometer: int
    fuel_type_id: int
    fuel_capacity: float
    oil_type: str
    oil_capacity: float
    tyre_size_front: str
    tyre_size_rear: str
    tyre_pressure_front: float
    tyre_pressure_rear: float
    archived: int = 0
