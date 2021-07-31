"""Represents a type of record"""
from dataclasses import dataclass


@dataclass
class FuelType:
    uid: int
    name: str
