"""
Collection of utility functions
"""
from jalopy.entities.entity_manager import EntityManager

LITRES_PER_GALLON = 4.54609
KM_PER_MILE = 1.60934
MPG_TO_L100_KM = 235.215


class Utils:
	"""
	Utility methods
	"""
	def __init__(self, entity_manager: EntityManager):
		self.entity_manager = entity_manager

	@staticmethod
	def calculate_economy(record):
		"""
		mpg
		l/100km
		km/l
		"""
		trip_km = record.trip * KM_PER_MILE
		kpl = trip_km / record.item_count
		mpg = record.trip / (record.item_count / LITRES_PER_GALLON)
		l100 = MPG_TO_L100_KM / mpg

		return {"mpg": mpg, "kpl": kpl, "l100": l100}

	def stats(self, vehicle):
		"""
		Accumulative stats for this vehicle
		"""
		# get all records for this vehicle
		records = self.entity_manager.get_records_for_vehicle(vehicle.uid)
		types = self.entity_manager.record_types
		total_cost = 0
		avg_mpg = 0
		avg_km_per_litre = 0
		avg_l100 = 0
		counts = [{"id": x.uid, "name": x.name, "count": 0} for x in types]

		for record in records:
			count = next(x for x in counts if x["id"] == record.record_type_id)
			count["count"] = count["count"] + 1
			if record.record_type_id == 1:
				eff = self.calculate_economy(record)

				avg_mpg = avg_mpg + eff["mpg"]
				avg_km_per_litre = avg_km_per_litre + eff["kpl"]
				avg_l100 = avg_l100 + eff["l100"]

			total_cost = total_cost + record.cost
		fuel_count = next(x for x in counts if x["id"] == 1)

		if fuel_count["count"] > 0:
			avg_mpg = avg_mpg / fuel_count["count"]
			avg_km_per_litre = avg_km_per_litre / fuel_count["count"]
			avg_l100 = avg_l100 / fuel_count["count"]

		return {
			"counts": counts,
			"avg_mpg": avg_mpg,
			"avg_km_per_litre": avg_km_per_litre,
			"avg_l100": avg_l100,
			"total_cost": total_cost,
		}
