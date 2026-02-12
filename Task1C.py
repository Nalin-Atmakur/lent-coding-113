# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

from floodsystem.stationdata import build_station_list
from floodsystem import geo
from floodsystem.station import MonitoringStation


centre = (52.2053, 0.1218)  # Coordinates of Cambridge city centre
def run_c():
    output_c = []  # create an empty list to store the output tuples
    list = geo.stations_within_radius(build_station_list(), centre, 10) #get list of stations within radius 10

    for s in list:
        output_c.append(s.name)  # append the station name to the output list
    return print(output_c)

run_c()