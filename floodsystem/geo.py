# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT
"""This module contains a collection of functions related to
geographical data.

"""

from .utils import sorted_by_key  # noqa
import numpy as np

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
