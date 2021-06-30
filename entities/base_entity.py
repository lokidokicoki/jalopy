"""BaseEntity"""
from dataclasses import dataclass


@dataclass
class BaseEntity:
    """Base entity"""

    entity_id: int
    notes: str
