"""Represents a type of record"""
from dataclasses import dataclass


@dataclass
class RecordType:
    uid: int
    name: str
