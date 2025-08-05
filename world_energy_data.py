#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

# Import user modules.
import collate
import process
import output

########################################################################################################################
#
# Python script world_energy_data.py
#
# Description:
# Creates all charts for the site https://www.worldenergydata.org
# Written by Shane White using Python
# https://github.com/shanewhi/world-energy-data
#
# Files:
# world_energy_data.py (this file)
# user_globals.py (definitions)
# collate.py (imports and collates data)
# process.py (performs all calculations)
# output.py (controls sequence of calling chart functions)
# chart.py (generic chart functions)
# countries.py (translates country names for display in charts)
#
#
# Outputs: Charts shown at https://www.worldenergydata.org
#
########################################################################################################################

# Define countries to profile using tuple.
countries = ('Total World',)

# 1. Import all data except IEA data, which is done on a per-country basis as it's contained in separate files provided
# by user. This is done in profile(country) below.
print('Importing and collating data.\n')
gcp_data, gcp_co2_rcp_pathways, esrl_data, ei_data, wb_data = collate.import_gcp_esrl_ei_pop_data()

# 2. Organise all CO2 related data as required for plots, and plot GCP and NOAA ESRL data.
print('Processing CO2 data:\n')
global_carbon = collate.co2_data(ei_data, gcp_data, gcp_co2_rcp_pathways, esrl_data)
output.world_co2_charts(global_carbon)

# 3. Generate dataframes of major coal, oil and gas producers as required for plot of shares for final year of data in
# profile() below.
print('\nIdentifying major fossil fuel producers:\n')
coal_producers, oil_producers, gas_producers = collate.fossil_fuel_producer_shares(ei_data)


# 4. Profile specified country, countries and or 'Total World'. This also includes plotting country shares of coal,
# oil and gas production from above, and ensures this chart is included in each country, or world, profile's folder.


def profile(country):
    # Import country specific IEA data.
    iea_co2_by_sector_Mt, iea_tfc_TJ = collate.import_iea_data(country)
    # Generate object containing all energy related data, in format suitable for plotting, for specified country.
    country_energy_system = collate.energy(country, ei_data, iea_co2_by_sector_Mt, iea_tfc_TJ, wb_data)
    if country_energy_system.incl_ei_flag is True:
        output.country_co2_charts(country_energy_system, global_carbon)
        output.per_capita_emissions(country_energy_system)
        output.country_ffprod_primaryenergy_charts(country_energy_system)
        output.country_elecgen_charts(country_energy_system)
    if iea_co2_by_sector_Mt is not None:
        output.co2_by_sector_chart(country_energy_system)
    if iea_tfc_TJ is not None and country_energy_system.incl_ei_flag is True:
        output.country_finalenergy_elec_charts(country_energy_system)
    if iea_tfc_TJ is not None:
        output.country_finalenergy_charts(country_energy_system)
    output.world_ffprod_charts(coal_producers, oil_producers, gas_producers, country_energy_system.country)


for name in countries:
    print('\n\nGenerating charts for: ' + str(name))
    profile(name)

# 5. Plot annual fossil fuel CO2 emissions and fossil fuel primary energy trends of Major Emitters in separate folder.
# Identify major emitters.
print('\n\nGenerating fossil fuel consumption charts of major emitting countries:\n')
major_emitters = process.id_major_ffco2_emitters(global_carbon)
# Collate major emitter data.
major_emitter_dataframe = collate.populate_major_emitter_co2_energy_dataframe(major_emitters, ei_data)
# Include plot of global CO2 emissions trend and shares in above folder.
energy_system_world = collate.energy('Total World', ei_data, None, None, wb_data)
# Plot world and major emitter charts.
output.major_emitter_charts(energy_system_world, global_carbon, major_emitter_dataframe)
