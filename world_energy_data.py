#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite


# Import Python modules.
import pandas as pd


# Import user modules.
import user_globals
import collate
import process


###############################################################################
#
# Function: profile(country)
#
# Description:
# Calls all functions required to profile a national enegry system.
#
# Input(s): Country name, string.
# Output(s): None.
#
###############################################################################
def profile(country):
    country_energy_system = collate.populate_energy_system(country)
    process.production(country_energy_system)
    process.co2_emissions(country_energy_system)
    process.primary_energy(country_energy_system)
    process.consumption(country_energy_system)


###############################################################################
#
# Function: Main
#
# Description:
# Creates charts of national energy systems.
# Written by Shane White using Python v3.11.5 and Spyder IDE.
# https://github.com/shanewhi
# https://www.worldenergydata.org
#
# Files:
# world_energy_data.py (this one)
# user_globals.py (defs)
# collate.py (called by world_energy_data.py)
# process.py (called by world_energy_data.py)
# chart.py (called by process.py)
#
# Choose a country at bottom of script.
# Name must match that used by The Energry Institute's (EI) dataset and or
# IEA's.
#
# Input(s):
# 1. Country name, string.
# 2. EI's dataset. Download from -
# https://www.energyinst.org/statistical-review/resources-and-data-downloads
# 3. IEA's annual energy balances. To download an annual IEA World Energy
# Balance -
# Load https://www.iea.org/data-and-statistics/data-tools/ \
#      energy-statistics-data-browser?country=WORLD&fuel= \
#      Energy%20supply&indicator=TESbySource
# 2. Right click on chart -> Inspect
# 3. Select Network tab
# 5. Click XHR button
# 6. Select Browse as Tables
# 7. Select year from dropdown (ensure this is done manually)
# 8. Double click on the following result (using 2021 as an example)
# https://api.iea.org/stats?year=2021&countries=[object+Object]&series=BALANCES
# 9. Save as JSON format
# 10. Add to start of file {"balances": and to the end }
#
# Output(s): Charts.
#
###############################################################################

# Import Energy Institute's dataset, once only.
user_globals.ei_data_import = pd.read_csv(
    "Statistical Review of World Energy Narrow File.csv",
	index_col = ["Year"],
    usecols = ["Country", "Year", "Var", "Value"])
# IEA's dataset is imported in collate.populate_energy_system(). This is
# because it's imported as annual Energy Balances stored in separate JSON
# files, because their Highlights dataset omits some countries.

# Profile following countries or "Total World".
#profile("Mexico")
#profile("Germany")
#profile("United Arab Emirates")
#profile("United Kingdom")
#profile("Sweden")
#profile("Australia")
#profile("Total World")
#profile("Algeria")
profile("Vietnam")
