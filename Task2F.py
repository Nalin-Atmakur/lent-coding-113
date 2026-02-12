# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

import datetime
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem.plot import plot_water_level_with_fit
from floodsystem.flood import stations_highest_rel_level


def run_f():
    p = 4 #degree of polynomial to fit
    dt = datetime.timedelta(days=2) #define how long ago we measure data from
    stations = build_station_list() #build list of objects of stations
    update_water_levels(stations) #upload latest data of stations using this function before ordering and outputting highest five
    highest_five = stations_highest_rel_level(stations, 5)

    for station_obj, water_level in highest_five: #iterating to get first entry of tuple in list of tuples

        dates, levels = fetch_measure_levels(station_obj.measure_id, dt) #call the two lists the function returns, taking in that objects measure id and dt
        plot_water_level_with_fit(station_obj, dates, levels, p)
run_f()
