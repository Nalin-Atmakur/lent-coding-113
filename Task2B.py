from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem import flood

def run():
    # Build list of stations
    stations = build_station_list()
    # Update latest level data for all stations
    update_water_levels(stations)

    print([(x[0].name, x[1]) for x in flood.stations_level_over_threshold(stations, 0.8)])


if __name__ == "__main__":
    print("*** Task 2B: CUED Part IA Flood Warning System ***")
    run()
