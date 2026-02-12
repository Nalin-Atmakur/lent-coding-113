import pytest
from floodsystem.flood import stations_level_over_threshold, stations_highest_rel_level
from floodsystem.station import MonitoringStation


def create_test_station(name, coord, river, town, typical_range, latest_level, s_id=None, m_id=None):
    if s_id is None:
        s_id = f"test-s-id-{name}"
    if m_id is None:
        m_id = f"test-m-id-{name}"
    station = MonitoringStation(s_id, m_id, name, coord, typical_range, river, town)
    station.latest_level = latest_level
    return station


def test_stations_level_over_threshold_empty():
    stations = []
    result = stations_level_over_threshold(stations, 0.5)
    assert len(result) == 0


def test_stations_level_over_threshold_some_above():
    s1 = create_test_station("S1", (0.0, 0.0), "River A", "Town A", (0.0, 1.0), 0.2)
    s2 = create_test_station("S2", (0.1, 0.0), "River B", "Town B", (0.0, 1.0), 0.7)
    s3 = create_test_station("S3", (0.2, 0.0), "River C", "Town C", (0.0, 1.0), 0.6)
    stations = [s1, s2, s3]
    
    result = stations_level_over_threshold(stations, 0.5)
    assert len(result) == 2
    assert result[0][0] == s2
    assert result[1][0] == s3


def test_stations_level_over_threshold_sorted():
    s1 = create_test_station("S1", (0.0, 0.0), "River A", "Town A", (0.0, 1.0), 0.6)
    s2 = create_test_station("S2", (0.1, 0.0), "River B", "Town B", (0.0, 1.0), 0.9)
    s3 = create_test_station("S3", (0.2, 0.0), "River C", "Town C", (0.0, 1.0), 0.7)
    stations = [s1, s2, s3]
    
    result = stations_level_over_threshold(stations, 0.5)
    assert len(result) == 3
    assert result[0][0] == s2
    assert result[1][0] == s3
    assert result[2][0] == s1
    
    levels = [level for _, level in result]
    assert levels[0] >= levels[1] >= levels[2]


def test_stations_level_over_threshold_with_none():
    s1 = create_test_station("S1", (0.0, 0.0), "River A", "Town A", (0.0, 1.0), 0.6)
    s2 = create_test_station("S2", (0.1, 0.0), "River B", "Town B", (0.0, 1.0), None)
    s3 = create_test_station("S3", (0.2, 0.0), "River C", "Town C", (0.0, 1.0), 0.7)
    stations = [s1, s2, s3]
    
    result = stations_level_over_threshold(stations, 0.5)
    assert len(result) == 2
    assert s2 not in [s for s, _ in result]


def test_stations_highest_rel_level_empty():
    s1 = create_test_station("S1", (0.0, 0.0), "River A", "Town A", (0.0, 1.0), 0.6)
    s2 = create_test_station("S2", (0.1, 0.0), "River B", "Town B", (0.0, 1.0), None)
    s3 = create_test_station("S3", (0.2, 0.0), "River C", "Town C", (0.0, 1.0), 0.8)
    stations = [s1, s2, s3]
    
    result = stations_highest_rel_level(stations, 2)
    assert len(result) == 2
    assert s2 not in result
    assert result[0] == s3
    assert result[1] == s1