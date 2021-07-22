"""Represents a type of record"""
from dataclasses import dataclass


@dataclass
class FuelType:
    entity_id: int
    name: str
