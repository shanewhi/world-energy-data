#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

# Import user modules.
import collate
import output

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
# Balance -
# a) Load https://www.iea.org/data-and-statistics/data-tools/ \
#      energy-statistics-data-browser?country=WORLD&fuel= \
#      Energy%20supply&indicator=TESbySource
# b) Right click on chart -> Inspect
# c) Select Network tab
# d) Click XHR button
# e) Select Browse as Tables
# f) Select year from dropdown (ensure this is done manually)
# g) Reload page
# h) Double-click on the following result (using 2021 as an example)
# https://api.iea.org/stats?year=2021&countries=[object+Object]&series=BALANCES
# i) Save as JSON format with name 'iea<yr>.json', where <yr> is relevant
# year.
# k) Add to start of file: {"balances":
# l) Add to the end of the file: }
#
# Output(s): Charts and debug text to std out.
#
########################################################################################

# Import data.
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported
# as single files below.
# The International Energy Agency (IEA) dataset is stored in multiple JSON
# files, and therefore country specific data is searched for within these,
# rather than imported as a single file. This is done within the function
# populate_energy_system().
ei_data, gcp_data, esrl_data = collate.import_data()

# Generate charts of GCP data.
global_carbon = collate.co2_data(ei_data, gcp_data, esrl_data)
output.world_co2_charts(global_carbon)


# Generate energy system charts in the following order:
def profile(country):
    energy_system = collate.energy(country, ei_data)

    # Generate global fossil fuel production charts using EI data.
    if energy_system.incl_ei_flag is True:
        output.country_co2_charts(energy_system, global_carbon)

    coal_producers, oil_producers, gas_producers = collate.ffproducer_shares(ei_data)
    output.world_ffprod_charts(coal_producers, oil_producers, gas_producers, energy_system.name)

    if energy_system.incl_ei_flag is True:
        output.country_prod_primary_energy_charts(energy_system)

    if energy_system.incl_ei_flag is True and energy_system.incl_iea_flag is True:
        output.country_consumption_elec_charts(energy_system)

    if energy_system.incl_iea_flag is True:
        output.country_consumption_charts(energy_system)

    if energy_system.incl_ei_flag is True:
        output.country_elec_charts(energy_system)


# Profile following countries or "Total World". Name must match in EI data.
profile("Total World")
# profile("China")
# profile("US")
# profile("Russian Federation"),
# profile("India")
# profile("Saudi Arabia")
# profile("Germany")
# profile("Indonesia")
# profile("United Arab Emirates")
# profile("Australia")
# profile("Norway")
# profile("Azerbaijan")
# profile("Japan")
# profile("Spain")
# profile("Kenya")
# profile("France")
# profile("Mexico")
# profile("Singapore")
# profile("Algeria")
# profile("Vietnam")
# profile("United Kingdom")
# profile("Sweden")
