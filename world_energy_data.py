#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

# Import user modules.
import collate
import output
import process

########################################################################################
#
# Application world_energy_data.py
#
# Description:
# Creates charts of -
# 1. Global CO2 emissions;
# 2. Global fossil fuel production;
# 3. National CO2 emissions;
# 4. National fossil fuel production; and
# 5. National energy systems (fossil fuel production, primary energy, final energy and
# electricity.
# Written by Shane White using Python v3.12.2 and Spyder IDE.
# https://github.com/shanewhi/world-energy-data
# https://www.worldenergydata.org
#
# Files:
# world_energy_data.py (this file)
# user_globals.py (defs)
# collate.py (called in world_energy_data.py)
# process.py (called in collate.py)
# output.py (controls sequence of chart functions, called in collate.py)
# chart.py (generic chart functions, called in process.py)
# countries.py (translates country name to IEA equivs, called in collate.py)
#
# Choose a country at bottom of script.
# Country name must match that used by The Energy Institute's (EI) dataset.
# If required, update countries.py to translate country name to IEA equiv.
#
# Input(s):
# 1. Global Carbon Budget in .xlsx format from
# https://globalcarbonbudgetdata.org/latest-data.html
# 2. NOAA ESRL CO2 data in CSV format from
# https://gml.noaa.gov/ccgg/trends/gl_data.html
# 3. Country name, string.
# 4. EI's dataset. Download from -
# https://www.energyinst.org/statistical-review/resources-and-data-downloads
# 5. IEA's annual energy balances. To download an annual IEA World Energy
# Balance, use either of the following methods:
#
# a)
# i. Load https://api.iea.org/stats?year=2022&countries=[object+Object]&series=BALANCES
# ii. Substitute 2022 for the year required.
#
# b)
# i. Load https://www.iea.org/data-and-statistics/data-tools/ \
#      energy-statistics-data-browser?country=WORLD&fuel= \
#      Energy%20supply&indicator=TESbySource
# ii. Right click on chart -> Inspect
# iii. Select Network tab
# iv. Click XHR button
# v. Select Browse as Tables
# vi. Select year from dropdown (ensure this is done manually)
# vii. Reload page
# viii. Double-click on the following result (using 2021 as an example)
# https://api.iea.org/stats?year=2021&countries=[object+Object]&series=BALANCES
#
# c) Save as JSON format with name 'iea<yr>.json', where <yr> is relevant
# year.
# d) Add to start of file: {"balances":<cr>
# e) Add to the end of the file: }
#
# Output(s): Charts and debug text to std out.
#
########################################################################################

# 1. Import data.
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported
# as single files below.
# The International Energy Agency (IEA) dataset is stored in multiple JSON
# files, and therefore country specific data is searched for within these,
# rather than imported as a single file. This is done within the function
# populate_energy_system().
ei_data, gcp_data, esrl_data = collate.import_data()


# 2. Plot GCP data.
global_carbon = collate.co2_data(ei_data, gcp_data, esrl_data)
output.world_co2_charts(global_carbon)


# 3. Profile the following countries or "Total World". Country name must match that shown in EI data.
def profile(country):
	collate.profile(country, global_carbon, ei_data)


profile("Total World")
# profile("China")
# profile("US")
# profile("Russian Federation")
# profile("India")
# profile("Saudi Arabia")
# profile("Germany")
# profile("Indonesia")
# profile("United Arab Emirates")
# profile("Australia")
# profile("Norway")
# profile("Japan")
# profile("Spain")
# profile("France")
# profile("Singapore")
# profile("Vietnam")
# profile("United Kingdom")
# profile("Japan")
# profile("Iran")
# profile("Canada")
# profile("Mexico")
# profile("Brazil")
# profile("South Korea") # IEA = KOREA
# profile("South Africa") # IEA = SOUTHAFRIC
# profile("Turkiye")
# profile("Uruguay")

# 4. Plot FF CO2 emissions and fossil fuel primary energy trends of major (≥1%) emitters.
major_emitters = process.id_major_ffco2_emitters(global_carbon)
major_emitter_dataframe = collate.populate_major_emitter_co2_energy_dataframe(major_emitters, ei_data)
energy_system_world = collate.energy("Total World", ei_data)
output.major_emitter_charts(energy_system_world, global_carbon, major_emitter_dataframe)
