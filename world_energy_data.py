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
# Creates charts of national energy systems.
# Written by Shane White using Python v3.11.5 and Spyder IDE.
# https://github.com/shanewhi/world-energy-data
# https://www.worldenergydata.org
#
# Files:
# world_energy_data.py (this file)
# user_globals.py (defs)
# countries.py (translates country name to IEA equivs, called in collate.py)
# collate.py (called in world_energy_data.py)
# process.py (called in collate.py)
# output.py (controls sequence of chart functions, called in collate.py)
# chart.py (generic chart functons, called in process.py)
#
# Choose a country at bottom of script.
# Country name must match that used by The Energry Institute's (EI) dataset.
# If required, update countries.py to translate country name to IEA equiv.
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
# 8. Reload page
# 9. Double click on the following result (using 2021 as an example)
# https://api.iea.org/stats?year=2021&countries=[object+Object]&series=BALANCES
# 10. Save as JSON format with name 'iea<yr>.json', where <yr> is relevant
# year.
# 11. Add to start of file: {"balances":
# 12. Add to the end of the file: }
#
# Output(s): Charts and debug text to std out.
#
########################################################################################

# Import data.
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported
# as single files below.
# The Internaitonal Energy Agency (IEA) dataset is stored in multiple JSON
# files, and therefore country specific data is searched for within these,
# rather than imported as a single file. This is done within the function
# populate_energy_system().
ei_data, gcp_data, esrl_data = collate.import_data()

# Generate charts of GCP data.
global_carbon = collate.organise_gcp_data(gcp_data, esrl_data)
output.global_carbon_charts(global_carbon)


# Generate charts of energy system data in the following sequence:
def profile(country):
    energy_system = collate.organise_energy(country, ei_data)
    if energy_system.incl_ei_flag is True:
        output.country_prod_primary_energy_charts(energy_system)

    if energy_system.incl_ei_flag is True and energy_system.incl_iea_flag is True:
        output.country_consumption_elec_charts(energy_system)

    if energy_system.incl_iea_flag is True:
        output.country_consumption_charts(energy_system)

    if energy_system.incl_ei_flag is True:
        output.country_elec_charts(energy_system)


# Profile following co`untries or "Total World".
profile("Total World")
# profile("US")
# profile("Kenya")
# profile("France")
# profile("Mexico")
# profile("Germany")
# profile("United Arab Emirates")
# profile("United Kingdom")
# profile("Sweden")
# profile("Australia")
# profile("Algeria")
# profile("Vietnam")
# profile("Azerbaijan")
