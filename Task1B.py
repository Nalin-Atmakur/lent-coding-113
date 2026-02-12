from floodsystem.stationdata import build_station_list
from floodsystem.station import MonitoringStation
from floodsystem import geo

def run():
    stations = [(x[0].name, x[0].town, x[1]) for x in geo.stations_by_distance(build_station_list(), (52.2053, 0.1218))]
    print(stations[:10])
    print(stations[-10:])
    

if __name__ == "__main__":
    run()