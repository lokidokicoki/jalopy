"""Represents a type of record"""
from dataclasses import dataclass


@dataclass
class RecordType:
    entity_id: int
    name: str
