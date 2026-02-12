import matplotlib.pyplot as plt
import datetime
import matplotlib
import numpy as np
from floodsystem.datafetcher import fetch_measure_levels
from floodsystem.stationdata import build_station_list
from floodsystem import station, analysis



    

def plot_water_levels(station, dates, levels, ax = None): #takes in station object as a parameter and ax as a parameter with default value None
    if ax is None: 
        fig, ax = plt.subplots() 
        #create figure and axis objects if no axis is provided
    # Add axis labels, rotate date labels and add plot title

    ax.plot(dates, levels) #plot the dates and levels on the axis
    ax.set_xlabel('date')
    ax.set_ylabel('water level (m)')
    ax.set_title(f"Station {station.name}")

    # Rotate x-axis tick labels
    plt.setp(ax.get_xticklabels(), rotation=45)
    
    ax.axhline(y = station.typical_range[0], linestyle = '--')

    ax.axhline(y = station.typical_range[1], linestyle = '--')
    # Display plot

    ax.set_yticks(sorted(list(ax.get_yticks()) + [station.typical_range[0], station.typical_range[1]])) 

    plt.tight_layout()  # This makes sure plot does not cut off date labels


    return ax

def plot_water_level_with_fit(station, dates, levels, p):

    fig, ax = plt.subplots() 
    plot_water_levels(station, dates, levels, ax=ax) #plot the river data on the axis

    poly, d0 = analysis.polyfit(dates, levels, p)  #get the polynomial and offset date from the polyfit function

    x1 = np.linspace(matplotlib.dates.date2num(dates)[0], matplotlib.dates.date2num(dates)[-1], 200) #create 200 evenly spaced points between the first and last date in float format
    y1 = poly(x1 - d0) #evaluate polynomial at each of these points, adjusting for offset date

    ax.plot(matplotlib.dates.num2date(x1), y1) #plot the polynomial fit on the same axis
    plt.show()

    plt.tight_layout()  # This makes sure plot does not cut off date labels



def plot_town_risks(town_dict):
    plt.hist(town_dict.values())
    plt.xlabel("Risk")
    plt.ylabel("Frequency")

    plt.show()