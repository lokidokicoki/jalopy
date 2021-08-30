from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from jalopy.entities import RecordEntity, VehicleEntity
from jalopy.utils import Utils


def historic_prices(records: List[RecordEntity]):
	fig, ax = plt.subplots()

	x = [x.record_date for x in records]
	y = [x.cost / x.item_count for x in records]

	ax.plot(x, y, 'o', ls='-')
	ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
	ax.xaxis.set_minor_locator(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	#ax.set_xlim(records[0].record_date, records[len(records) - 1].record_date)

	ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.format_ydata = lambda x : f'£{x:.3f}'
	ax.grid(True)

	ax.set_title(f'Historic Fuel Price')
	ax.set_ylabel('Price per litre')
	fig.autofmt_xdate()
	plt.show()

def fuel_economy(vehicle:VehicleEntity, records: List[RecordEntity]):
	print('plot fuel economy')
	fig, ax = plt.subplots()

	x = [x.record_date for x in records]
	y = [Utils.calculate_economy(x)['mpg'] for x in records]

	ax.plot(x, y, 'o', ls='-')
	ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
	ax.xaxis.set_minor_locator(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	#ax.set_xlim(records[0].record_date, records[len(records) - 1].record_date)

	ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax.format_ydata = lambda x : f'{x:.2f}'
	ax.grid(True)

	ax.set_title(f'Fuel Economy {vehicle.reg_no}')
	ax.set_ylabel('MPG')
	fig.autofmt_xdate()
	plt.show()
