import numpy as np

def stations_level_over_threshold(stations, tol):
    # returns sorted list of station objects with relative water level over the threshold
    return sorted(list(filter(lambda x: x is not None, [(s, s.relative_water_level()) if s.relative_water_level() is not None and s.relative_water_level() > tol else None for s in stations])), key=lambda x: x[1], reverse=True)

def stations_highest_rel_level(stations, N):
    # returns list of the N stations with the highest relative water level, only those that have level not none
    return sorted(list(filter(lambda x: x is not None, [s if s.relative_water_level() is not None else None for s in stations])), key=lambda x: x.relative_water_level(), reverse=True)[:N]
