from floodsystem.stationdata import build_station_list
from floodsystem.station import MonitoringStation
from floodsystem import geo

def run():
    stations = build_station_list()
    print(sorted(geo.rivers_with_station(stations))[:10])
    rivers = geo.stations_by_river(stations)
    print(sorted([x.name for x in rivers["River Aire"]]))
    print(sorted([x.name for x in rivers["River Cam"]]))
    print(sorted([x.name for x in rivers["River Thames"]]))

if __name__ == "__main__":
    run()