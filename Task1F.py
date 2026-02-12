from floodsystem.stationdata import build_station_list
from floodsystem.station import MonitoringStation

def run():
    print([x.name for x in MonitoringStation.inconsistent_typical_range_stations(build_station_list())])
if __name__ == "__main__":
    run()