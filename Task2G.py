# Copyright (C) 2018 Garth N. Wells
#
# SPDX-License-Identifier: MIT

import datetime

from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list, update_water_levels
from floodsystem import plot, flood, analysis, geo

def run():
    stations = build_station_list()
    update_water_levels(stations)
    stations = [x[0] for x in flood.stations_level_over_threshold(stations, 1.8)]
    town_dict = analysis.get_town_risk(geo.stations_by_town(stations))
    std_risk_dict = analysis.get_standardised_risk(town_dict)
    
    # Categorize towns by risk level
    moderate = dict(filter(lambda x: 0.5 <= x[1] < 1, std_risk_dict.items()))
    high = dict(filter(lambda x: 2 <= x[1] < 2.5, std_risk_dict.items()))
    severe = dict(filter(lambda x: x[1] >= 2.5, std_risk_dict.items()))
    
    print("\n=== FLOOD RISK ASSESSMENT ===\n")
    
    print("MODERATE RISK (0.5 - 1.0):")
    print('\n'.join(f"  {town}: {risk:.2f}" for town, risk in sorted(moderate.items())) if moderate else "  None")
    
    print("\nHIGH RISK (2.0 - 2.5):")
    print('\n'.join(f"  {town}: {risk:.2f}" for town, risk in sorted(high.items())) if high else "  None")
    
    print("\nSEVERE RISK (2.5+):")
    print('\n'.join(f"  {town}: {risk:.2f}" for town, risk in sorted(severe.items())) if severe else "  None")
    print()
    
    plot.plot_town_risks(std_risk_dict)


if __name__ == "__main__":
    print("*** Task 2G: CUED Part IA Flood Warning System ***")
    run()
