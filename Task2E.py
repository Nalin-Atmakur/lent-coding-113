# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

import datetime
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_levels
from floodsystem.flood import stations_highest_rel_level
import matplotlib.pyplot as plt


def run_e():
    dt = datetime.timedelta(days=10) #define how long ago we measure data from
    stations = build_station_list() #build list of objects of stations
    update_water_levels(stations) #upload latest data of stations using this function before ordering and outputting highest five
    highest_five = stations_highest_rel_level(stations, 5)

    for station_obj in highest_five: #iterating through the highest five stations

        dates, levels = fetch_measure_levels(station_obj.measure_id, dt) #call the two lists the function returns, taking in that objects measure id and dt
        plot_water_levels(station_obj, dates, levels)
        plt.show()
run_e()
