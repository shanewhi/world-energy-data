#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:56:55 2024

@author: shanewhite
"""
    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Creates charts of national energy systems.
# Written by Shane White using Python v3.11.5 and Spyder IDE.
# https://github.com/shanewhi
# https://www.worldenergydata.org

# Choose a country at bottom of script. If that country has never produced a
# specific fuel, then a corresponding chart isn't created. Entered country
# name must match that used by The Energry Institute's dataset.


# Import Python modules.
import pandas as pd
import matplotlib.pyplot as plt

# Import user modules.
import collate
import process


# Function creates profile of a country's energy system by creating an
# instance of custom class Energy_System, populating that object with data,
# and creating charts.
def profile(country):
    country_energy_system = collate.populate_energy_system(ei_data, country)
    process.production(country_energy_system)
    process.primary_energy(country_energy_system)

# Main function.
plt.close('all')
ei_data = pd.read_csv(
    "Statistical Review of World Energy Narrow File.csv",
    index_col=['Country'],
    usecols=['Country', 'Year', 'Var', 'Value'])
# Create energy system charts for the following countries:
profile('Total World')
#profile('Germany')
#profile('United Arab Emirates')
#profile('United Kingdom')
plt.show()
