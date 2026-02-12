# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

from floodsystem.stationdata import build_station_list
from floodsystem import geo
from floodsystem.station import MonitoringStation

def run_e():
    river_count_list = geo.rivers_by_station_number(build_station_list(), 10) #call the rivers_by_station_number function with the list of stations and N=9
    print(river_count_list)
    return river_count_list
run_e()
