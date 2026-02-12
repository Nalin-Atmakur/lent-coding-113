from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem import flood

def run():
    # Build list of stations
    stations = build_station_list()
    # Update latest level data for all stations
    update_water_levels(stations)

    print([(x.name, x.relative_water_level()) for x in flood.stations_highest_rel_level(stations, 10)])


if __name__ == "__main__":
    print("*** Task 2C: CUED Part IA Flood Warning System ***")
    run()
