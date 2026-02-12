# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
import numpy as np
from functools import reduce
from collections import defaultdict

# Radius of earth in km
R = 6371

def stations_by_distance(stations, p):
    # gets list of stations ordered by closest to coordinate p
    return sorted(list(map(lambda x: (x, haversine(x.coord, p)), stations)), key=lambda x: x[1])


def haversine(coord1, coord2):
    """Calculate great-circle distance between two points using haversine formula.
    Distance measured in km using numpy for efficiency.
    """
    # Convert to radians using numpy
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = np.sin(delta_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return float(d)

def stations_within_radius(stations, centre, r):
    stations_in_radius = [] #create an empty list to store stations within radius r
    for station in stations:
        distance = haversine(station.coord, centre) #calculate the distance between station and centre
        if distance < r:
            stations_in_radius.append(station) #append station to the list if distance is less than r
    return stations_in_radius #return the list of stations within radius r

def rivers_with_station(stations):
    return list(set([x.river for x in stations]))

def stations_by_river(stations):
    # append station to dict if river exists, else create new entry if river not added yet, using default dict
    return dict(sorted(reduce(lambda d, s: (d[s.river].append(s), d)[1], stations, defaultdict(list)).items(), key=lambda x: len(x[1]), reverse=True))


def rivers_by_station_number(stations, N):
    stations_dict = stations_by_river(stations)  #get the dictionary of rivers and their stations
    
    river_count_list = []  #create an empty list to store the output tuples
    
    for river in stations_dict: # iterate through each river in the dictionary
        number_stations = len(stations_dict[river])  #replace the list
        river_count_list.append((river, number_stations))  #append a tuple of river and number of stations to the list

    river_count_list = sorted_by_key(river_count_list, 1, reverse=True)  #sort the list by number of stations in descending order
    final_list = river_count_list  #initialize final_list as river_count_list
    if N < len(river_count_list): #check if N is less than the length of the list

        rest_of_list = river_count_list[N:] #create a new list with the elements from index N to the end of the list
        river_count_list = river_count_list[0:N]  #slice the first N elements of the output list



        extra_rivers = [] #create an empty list to store extra rivers with same number of stations as Nth river
        for extra in rest_of_list:
            if extra[1] == river_count_list[N-1][1]:
                extra_rivers.append(extra)
            else:
                break

        final_list = river_count_list + extra_rivers
    return final_list

def stations_by_town(stations):
    return dict(reduce(lambda d, s: (d[s.town].append(s), d)[1], stations, defaultdict(list)).items())

