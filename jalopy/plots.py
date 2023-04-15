from typing import List

import matplotlib

matplotlib.use("TkAgg")
import matplotlib.dates as mdates  # type: ignore
import matplotlib.pyplot as plot

from jalopy.entities import RecordEntity, VehicleEntity
from jalopy.utils import Utils


def historic_prices(records: List[RecordEntity]):
    """
    Plot historic fuel prices over time

    :param records: all current records
    """
    fig, axes = plot.subplots()

    x = [x.record_date for x in records]
    y = [x.cost / x.item_count for x in records]

    axes.plot(x, y, "o", ls="-")
    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes.xaxis.set_minor_locator(mdates.MonthLocator())
    axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    axes.format_xdata = mdates.DateFormatter("%Y-%m-%d")
    axes.format_ydata = lambda x: f"£{x:.3f}"
    axes.grid(True)

    axes.set_title("Historic Fuel Price")
    axes.set_ylabel("Price per litre")
    fig.autofmt_xdate()
    plot.show()


def fuel_economy(vehicle: VehicleEntity, records: List[RecordEntity]):
    """
    Plot vehicle economy over time

    :param vehicle: selected vehicle
    :param records: vehicles records
    """
    fig, axes = plot.subplots()

    x = [x.record_date for x in records]
    y = [Utils.calculate_economy(x)["mpg"] for x in records]

    axes.plot(x, y, "o", ls="-")
    axes.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axes.xaxis.set_minor_locator(mdates.MonthLocator())
    axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    axes.format_xdata = mdates.DateFormatter("%Y-%m-%d")
    axes.format_ydata = lambda x: f"{x:.2f}"
    axes.grid(True)

    axes.set_title(f"Fuel Economy {vehicle.reg_no}")
    axes.set_ylabel("MPG")
    fig.autofmt_xdate()
    plot.show()
