"""Represents a type of fuel"""
from dataclasses import dataclass


@dataclass
class FuelType:
	"""FuelType"""

	uid: int
	name: str
