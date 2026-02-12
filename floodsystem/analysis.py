import matplotlib

import datetime
import numpy as np
import matplotlib.pyplot as plt
from floodsystem import flood

from .datafetcher import fetch_measure_levels


def polyfit(dates, levels, p):
    d = matplotlib.dates.date2num(dates) #Convert dates to floats
    normalised_d = d - d[0]  # Normalize x data to improve numerical stability
    

    # Find coefficients of best-fit polynomial f(x) of degree p
    p_coeff = np.polyfit(normalised_d, levels, p)

    # Convert coefficient into a polynomial that can be evaluated,
    # e.g. poly(0.3)
    poly = np.poly1d(p_coeff)
    return poly, d[0]  # Return polynomial and offset date

def calculate_risk(station):
    '''Calculate the flood risk level for a given station based on its relative water level and trend.'''
    dates, levels = fetch_measure_levels(station.measure_id, datetime.timedelta(days=4)) #Fetch last 4 days of water level data
    poly, d0 = polyfit(dates, levels, 4) #Fit a 4th degree polynomial to the last 4 days of data
    dpoly = poly.deriv() 
    rate = dpoly(matplotlib.dates.date2num(dates[0]) - d0) #Calculate rate of change at most recent date
    risk = station.relative_water_level() + 3 * rate  
    print (risk)
    return risk

def get_town_risk(town_dict): #Calculate average flood risk for each town based on its stations and takes in dictionary of towns and their stations
    town_risks = {} 
    for town, stations in town_dict.items(): #iterating through each town and its list of stations
        risks = []
        for station in stations:
            risk = calculate_risk(station) 
            risks.append(risk) #append each station's risk to list of risks for that town

        if risks:
            avg_risk = np.mean(risks) 
            town_risks[town] = avg_risk #calculate average risk for town and store in dictionary
        else:
            town_risks[town] = None  #no stations in town
    return town_risks

def get_standardised_risk(town_dict):
    """Standardize risks using numpy operations."""
    risks = np.array(list(town_dict.values())) #convert risks to numpy array
    mean = np.mean(risks)  
    std = np.std(risks)
    for town, risk in town_dict.items(): #iterating through each town and its risk
        z_score = float(risk - mean) / std 
        town_dict[town] = z_score #update town's risk to its z-score
    return town_dict


'''def towns_at_risk(town_dict, threshold):
    return dict(filter(lambda x: x[1]>threshold, town_dict.items())) #filter towns with risk above threshold'''

'''def calculate_z_scores(levels, reference=1.0):
    """Calculate z-scores (standard deviations above reference value).
    
    Args:
        levels: Array-like of level values (may contain None)
        reference: Reference level for z-score calculation (default 1.0)
        
    Returns:
        Tuple of (z_scores array, mean_level, std_level)
    """
    numeric_levels = np.array([v for v in levels if v is not None]) #filter out None values
    if len(numeric_levels) > 0: #ensure there are numeric levels to process
        mean_level = float(np.mean(numeric_levels)) 
        std_level = float(np.std(numeric_levels, ddof=1)) #sample standard deviation (ddof is delta degrees of freedom)
        if std_level == 0: #avoid division by zero
            std_level = 1.0
        z_scores = (numeric_levels - reference) / std_level #calculate z-scores
    else:
        mean_level = reference
        std_level = 1.0
        z_scores = np.array([]) #empty array if no numeric levels
    
    return z_scores, mean_level, std_level '''
