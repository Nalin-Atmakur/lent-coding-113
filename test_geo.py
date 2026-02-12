import pytest
import math
from floodsystem.geo import (haversine, stations_by_distance, 
                             stations_within_radius, rivers_with_station,
                             stations_by_river)
from floodsystem.station import MonitoringStation


def create_test_station(name, coord, river, town, s_id=None, m_id=None):
    if s_id is None:
        s_id = f"test-s-id-{name}"
    if m_id is None:
        m_id = f"test-m-id-{name}"
    return MonitoringStation(s_id, m_id, name, coord, (-2.0, 2.0), river, town)


def test_calculate_distance():
    dist = haversine((0.0, 0.0), (0.0, 0.0))
    assert abs(dist) < 0.001
    
    coord1 = (51.5074, -0.1278)
    coord2 = (53.4808, -2.2426)
    d1 = haversine(coord1, coord2)
    d2 = haversine(coord2, coord1)
    assert abs(d1 - d2) < 0.001
    
    assert d1 > 0
    
    assert 190 < d1 < 270


def test_stations_by_distance():
    s1 = create_test_station("Station1", (0.0, 0.0), "River A", "Town A")
    s2 = create_test_station("Station2", (0.1, 0.0), "River B", "Town B")
    s3 = create_test_station("Station3", (0.2, 0.0), "River C", "Town C")
    stations = [s3, s1, s2]
    
    centre = (0.0, 0.0)
    sorted_stations = stations_by_distance(stations, centre)
    
    assert sorted_stations[0][0] == s1
    assert sorted_stations[1][0] == s2
    assert sorted_stations[2][0] == s3
    
    distances = [dist for _, dist in sorted_stations]
    assert distances[0] <= distances[1] <= distances[2]


def test_stations_within_radius():
    s1 = create_test_station("Station1", (0.0, 0.0), "River A", "Town A")
    s2 = create_test_station("Station2", (0.040, 0.0), "River B", "Town B")
    s3 = create_test_station("Station3", (0.2, 0.0), "River C", "Town C")
    stations = [s1, s2, s3]
    
    centre = (0.0, 0.0)
    
    nearby = stations_within_radius(stations, centre, 5.5)
    assert s1 in nearby
    assert s2 in nearby
    assert s3 not in nearby
    
    all_stations = stations_within_radius(stations, centre, 100)
    assert len(all_stations) == 3


def test_rivers_with_station():
    s1 = create_test_station("Station1", (0.0, 0.0), "River Thames", "Town A")
    s2 = create_test_station("Station2", (0.1, 0.0), "River Severn", "Town B")
    s3 = create_test_station("Station3", (0.2, 0.0), "River Thames", "Town C")
    stations = [s1, s2, s3]
    
    rivers = rivers_with_station(stations)
    
    assert len(rivers) == 2
    assert "River Thames" in rivers
    assert "River Severn" in rivers


def test_stations_by_river():
    s1 = create_test_station("Station1", (0.0, 0.0), "River Thames", "Town A")
    s2 = create_test_station("Station2", (0.1, 0.0), "River Severn", "Town B")
    s3 = create_test_station("Station3", (0.2, 0.0), "River Thames", "Town C")
    s4 = create_test_station("Station4", (0.3, 0.0), "River Severn", "Town D")
    stations = [s1, s2, s3, s4]
    
    grouped = stations_by_river(stations)
    
    assert isinstance(grouped, dict)
    assert "River Thames" in grouped
    assert "River Severn" in grouped
    
    assert len(grouped["River Thames"]) == 2
    assert len(grouped["River Severn"]) == 2
    assert s1 in grouped["River Thames"]
    assert s3 in grouped["River Thames"]

'''
def test_stations_by_town():
    s1 = create_test_station("Station1", (0.0, 0.0), "River A", "Oxford")
    s2 = create_test_station("Station2", (0.1, 0.0), "River B", "Cambridge")
    s3 = create_test_station("Station3", (0.2, 0.0), "River C", "Oxford")
    stations = [s1, s2, s3]
    
    grouped = stations_by_town(stations)
    
    assert isinstance(grouped, dict)
    assert "Oxford" in grouped
    assert "Cambridge" in grouped
    
    assert len(grouped["Oxford"]) == 2
    assert len(grouped["Cambridge"]) == 1
    assert s1 in grouped["Oxford"]
    assert s3 in grouped["Oxford"]
    assert s2 in grouped["Cambridge"]


def test_empty_station_list():
    stations = []
    
    rivers = rivers_with_station(stations)
    assert len(rivers) == 0
    
    grouped = stations_by_river(stations)
    assert len(grouped) == 0
    
    grouped = stations_by_town(stations)
    assert len(grouped) == 0
    
    nearby = stations_within_radius(stations, (0.0, 0.0), 10)
    assert len(nearby) == 0
    
    sorted_stations = stations_by_distance(stations, (0.0, 0.0))
    assert len(sorted_stations) == 0
'''