"""DB Vehicle"""
from jalopy.db.base_item import BaseItem


class Vehicle(BaseItem):
	"""
	DB access for the 'vehicle' table
	"""

	def __init__(self, conn, cursor):
		"""Create instance of Vehicle"""
		super().__init__(conn, cursor, "vehicle")
