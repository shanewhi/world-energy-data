#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################################################
#
# Module: collate.py
#
# Description:
# Imports and collates all data.
#
########################################################################################################################


# Import Python modules.
import pandas as pd
import numpy as np

import countries
# Import user modules.
import user_globals
import process


########################################################################################################################
#
# Function: import_gcp_esrl_ei_pop_data()
#
# Description:
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported as single files into Pandas dataframes.
#
########################################################################################################################
def import_gcp_esrl_ei_pop_data():
    # Import Global Carbon Project (GCP) emissions and carbon budget datasets as Pandas dataframes.
    gcp_ff_emissions_MtC = pd.read_excel(
        io='Global_Carbon_Budget_2024_v1.0.xlsx',
        sheet_name='Fossil Emissions by Category',
        header=8,
        names=[
            'FF and Cement',
            'Coal',
            'Oil',
            'Gas',
            'Cement',
            'Flaring',
            'Other',
            'Per Capita',
        ],
        index_col=0,
    )
    gcp_budget_GtC = pd.read_excel(
        io='Global_Carbon_Budget_2024_v1.0.xlsx',
        sheet_name='Global Carbon Budget',
        header=21,
        names=[
            'FF and Cement Exc Cement Carb',
            'Land Use Change',
            'Atmospheric Growth',
            'Ocean Sink',
            'Land Sink',
            'Cement Carbonation Sink',
            'Budget Imbalance',
            'Net FF and Cement',
        ],
        index_col=0,
    )

    imported_gcp_co2_rcp_pathways = pd.read_csv(
        's64_2024_LinearPathways.csv', header=0, index_col=['Year'],
        usecols=['Year', 'Historical', '1.5C / 235 GtCO2', '1.7C / 585 GtCO2', '2.0C / 1110 GtCO2']
    )

    # Convert emission units from MtC to MtCO2.
    gcp_ff_emissions_MtCO2 = gcp_ff_emissions_MtC.mul(user_globals.Constant.C_TO_CO2.value)

    # Drop emissions per-capita column.
    gcp_ff_emissions_MtCO2 = gcp_ff_emissions_MtCO2.drop(columns=['Per Capita'])

    # Convert carbon budget units from GtC to MtC.
    gcp_budget_MtC = gcp_budget_GtC.mul(user_globals.Constant.G_TO_M.value)

    # Convert carbon budget units from MtC to MtCO2.
    gcp_budget_MtCO2 = gcp_budget_MtC.mul(user_globals.Constant.C_TO_CO2.value)

    # Drop superfluous column.
    gcp_budget_MtCO2 = gcp_budget_MtCO2.drop(columns=['FF and Cement Exc Cement Carb'])

    # Combine GCP emissions and budget data.
    imported_gcp_data = gcp_ff_emissions_MtCO2.join(gcp_budget_MtCO2)

    # Import atmospheric CO2 concentration and annual change data from NOAA ESRL dataset as Pandas dataframes.
    esrl_co2_conc = pd.read_csv(
        'co2_annmean_gl.csv', header=37, index_col=['year'], usecols=['year', 'mean']
    )

    esrl_co2_change = pd.read_csv(
        'co2_gr_gl.csv', header=43, index_col=['year'], usecols=['year', 'ann inc']
    )

    # Join two datasets
    imported_esrl_data = esrl_co2_conc.join(esrl_co2_change)

    # Rename dataframe columns and make the 'Year' column the dataframe index.
    imported_esrl_data = imported_esrl_data.rename(columns={'mean': 'Mean', 'ann inc': 'Ann Inc'})
    imported_esrl_data.index.names = ['Year']

    # Import Energy Institute dataset.
    imported_ei_data = pd.read_csv(
        'Statistical Review of World Energy Narrow File.csv', index_col=['Year'],
        usecols=['Country', 'Year', 'ISO3166_alpha3', 'Var', 'Value'],
    )

    # Import World Bank human population data from all countries for most recent year of ei_data.
    imported_wb_data = pd.read_csv(
        'API_SP.POP.TOTL_DS2_en_csv_v2_38144.csv', index_col=['Country Code'], header=2,
        usecols=['Country Code', str(imported_ei_data.index[-1])], )
    imported_wb_data.rename(columns={'2024': 'Population'}, inplace=True)

    return imported_gcp_data, imported_gcp_co2_rcp_pathways, imported_esrl_data, imported_ei_data, imported_wb_data,


########################################################################################################################
#
# Function: import_iea_data()
#
# Description:
# International Energy Agency (IEA) datasets in two files are imported into Pandas dataframes and combined.
#
########################################################################################################################
def import_iea_data(country_name):
    iea_country_name = countries.translate_country_name(country_name)
    filename_co2_emissions_by_sector = 'CO2 emissions by sector - ' + str(iea_country_name) + '.csv'
    filename_tfc = 'Total final consumption (TFC) by source - ' + str(iea_country_name) + '.csv'
    try:
        co2_by_sector = pd.read_csv(filename_co2_emissions_by_sector, skiprows=3, index_col=0,
                                    dtype={'Electricity and heat producers': float, 'Other energy industries': float,
                                           'Transport Sector': float, 'Industry Sector': float,
                                           'Commercial and Public Services': float,
                                           'Residential': float, 'Agriculture/Forestry': float, 'Fishing': float,
                                           'Non-specified (Other)': float, 'Units': str})
        co2_by_sector.drop(columns='Units', inplace=True)
        co2_by_sector.fillna(value=0, inplace=True)
        co2_by_sector.rename(columns={'Electricity and heat producers': 'Electricity & Heat Producers',
                                      'Other energy industries': 'Other Energy Producers',
                                      'Transport Sector': 'Transport', 'Industry Sector': 'Manufacturing Industry',
                                      'Residential': 'Residences',
                                      'Commercial and Public Services': 'Commercial & Public Services'}, inplace=True)

    except FileNotFoundError:
        co2_by_sector = None
        print('\nFile not found: ' + filename_co2_emissions_by_sector)
    try:
        tfc = pd.read_csv(filename_tfc, index_col=0, skiprows=3,
                          dtype={'Coal': float, 'Crude oil': float,
                                 'Oil products': float, 'Natural gas': float, 'Wind, solar, etc.': float,
                                 'Biofuels and waste': float, 'Electricity': float, 'Heat': float, 'Units': str},
                          )
        # IEA TFC data for some countries does not list all forms of consumption. Assign a value of 0 to such columns.
        tfc_keys = tfc.keys()
        if 'Coal' not in tfc_keys:
            tfc['Coal'] = 0
        if 'Crude oil' not in tfc_keys:
            tfc['Crude oil'] = 0
        if 'Oil products' not in tfc_keys:
            tfc['Oil products'] = 0
        if 'Natural gas' not in tfc_keys:
            tfc['Natural gas'] = 0
        if 'Wind, solar, etc.' not in tfc_keys:
            tfc['Wind, solar, etc.'] = 0
        if 'Biofuels and waste' not in tfc_keys:
            tfc['Biofuels and waste'] = 0
        if 'Electricity' not in tfc_keys:
            tfc['Electricity'] = 0
        if 'Heat' not in tfc_keys:
            tfc['Heat'] = 0

        tfc.drop(columns='Units', inplace=True)
        tfc.fillna(value=0, inplace=True)
        tfc.rename(columns={'Natural gas': 'Gas', 'Wind, solar, etc.': 'Wind Solar Etc',
                            'Biofuels and waste': 'Biofuels and Waste', }, inplace=True)

    except FileNotFoundError:
        tfc = None
        print('\nFile not found: ' + filename_tfc + '\n')
    return co2_by_sector, tfc


########################################################################################################################
#
# Function: co2_data()
#
# Description:
# Organises into a user defined class all required CO2 related data in the following formats required for plots of -
# 1. Final year global shares of CO2 emissions by category treemap plot (using GCP carbon budget data)
# 2. Final year global shares of CO2 emissions by source treemap plot (using GCP carbon budget data)
# 3. Atmospheric CO2 concentration plots (NOAA ESRL data)
# 4. Final year country shares of global fossil fuel CO2 emissions treemap plot (using EI data)
#
########################################################################################################################
def co2_data(energy_data, c_budget_data, remaining_c_budget_data, conc_data):
    country = 'World'

    # Calculate country shares of fossil fuel CO2 emissions for final year of EI dataset. This is used in following code
    # for generation of data required for treemap plots.
    country_shares_fy = process.calc_country_shares_fy(energy_data)

    # Calculate all carbon related shares and organise into format required for treemap plots.
    treemap_c_budget_categories, treemap_c_budget_sources, treemap_country_emission_shares = (
        process.carbon_emissions(c_budget_data, country_shares_fy)
    )

    # Return user defined class containing all CO2 related data in formats ready to plot.
    return user_globals.Global_Carbon(
        country,
        c_budget_data,
        treemap_c_budget_categories,
        treemap_c_budget_sources,
        remaining_c_budget_data,
        conc_data,
        treemap_country_emission_shares,
    )


########################################################################################################################
#
# Function: fossil_fuel_producer_shares()
#
# Description:
# Identifies and organises annual production shares of fossil fuel producers into dataframes as required fo plotting of
# treemaps.
#
########################################################################################################################
def fossil_fuel_producer_shares(data):
    # Extract fossil fuel production data from dataframe into separate dataframes.
    coal_prod = data.loc[data['Var'] == 'coalprod_ej']
    oil_prod = data.loc[data['Var'] == 'oilprod_mt']
    gas_prod = data.loc[data['Var'] == 'gasprod_ej']

    # Obtain latest world production value of each fossil fuel in order to calculate shares of each country's
    # production.
    # 1. Coal
    world_coal_prod = coal_prod.loc[coal_prod['Country'] == 'Total World']
    world_coal_prod_latest = world_coal_prod.loc[
        world_coal_prod.index == max(world_coal_prod.index), 'Value'
    ]
    total_coal = float(world_coal_prod_latest.values)

    # 2. Oil
    world_oil_prod = oil_prod.loc[oil_prod['Country'] == 'Total World']
    world_oil_prod_latest = world_oil_prod.loc[
        world_oil_prod.index == max(world_oil_prod.index), 'Value'
    ]
    total_oil = float(world_oil_prod_latest.values)

    # 3. Gas
    world_gas_prod = gas_prod.loc[gas_prod['Country'] == 'Total World']
    world_gas_prod_latest = world_gas_prod.loc[
        world_gas_prod.index == max(world_gas_prod.index), 'Value'
    ]
    total_gas = float(world_gas_prod_latest.values)

    # Generate dataframes of fossil fuel producers in format required by treemap plotting functions.
    coal_producer_df, oil_producer_df, gas_producer_df = process.world_fossil_fuel_production(
        coal_prod, oil_prod, gas_prod, total_coal, total_oil, total_gas
    )

    # Output above dataframes to console.
    print('Large coal producers:\n', str(coal_producer_df))
    print('\nLarge oil producers:\n', str(oil_producer_df))
    print('\nLarge gas producers:\n', str(gas_producer_df), '\n')

    return coal_producer_df, oil_producer_df, gas_producer_df


########################################################################################################################
#
# Function: energy()
#
# Description:
# Calls all functions required to populate data of a specified country's energy system in the object
# country_energy_system.
#
########################################################################################################################
def energy(country, ei_data, co2_by_sector_Mt, tfc_TJ, wb_data):
    country_energy_system = populate_energy_system(country, ei_data, co2_by_sector_Mt, tfc_TJ, wb_data)
    if country_energy_system.incl_ei_flag is True:
        # Calculate primary energy annual quantities, shares, and change.
        process.primary_energy(country_energy_system)
        # Calculate electricity generation shares, and change.
        process.electricity(country_energy_system)
    else:
        print('Country not found in EI data')
    if country_energy_system.sector_co2_Mt is not None:
        # Calculate columns to be plotted.
        process.sector_co2(country_energy_system)
    if country_energy_system.finalenergy_PJ is not None:
        # Calculate final energy annual shares and changes.
        process.final_energy(country_energy_system)
    return country_energy_system


########################################################################################################################
#
# Function: populate_energy_system()
#
# Description:
# Collates country specific annual fossil fuel CO2 emissions, country per capita fossil fuel CO2 emissions for final
# year of data, annual fossil fuel production, annual fossil fuel primary energy, and annual electricity data using
# the Energy Institute's dataset. Collates country specific final energy data using the IEA's dataset.
#
########################################################################################################################
def populate_energy_system(country, ei_data, co2_by_sector_Mt, tfc_TJ, pop_data):
    # Flag if country is included in EI data, and extract the country's data.
    if country in ei_data['Country'].values:
        incl_ei_flag = True
        country_data = ei_data.loc[ei_data['Country'] == country]

        # Replace EI's 'Total World' label for chart titles.
        if country == 'Total World':
            country = 'World'

        ################################################################################################################
        # Fossil Fuel CO2 Emissions.
        ################################################################################################################
        # Construct dataframe of fossil fuel CO2 emissions.
        ffco2_data_Mt = country_data.loc[country_data['Var'] == 'co2_combust_mtco2', 'Value']
        ffco2_Mt = pd.DataFrame(index=ffco2_data_Mt.index, columns=['Value', 'Change'])
        ffco2_Gt = pd.DataFrame(index=ffco2_data_Mt.index, columns=['Value', 'Change'])

        ffco2_Mt['Value'] = ffco2_data_Mt
        ffco2_Gt['Value'] = ffco2_data_Mt / 1000

        # Calculate annual change.
        process.ffco2_change(ffco2_Mt)

        ################################################################################################################
        # Per Capita Fossil Fuel CO2 Emissions.
        ################################################################################################################
        if country == 'World':
            profile_country = 'Total World'
        else:
            profile_country = country
        # Per capita emissions for specific country being profiled, dictionary.
        profile_country_pc_tco2 = {}
        # All per capita emissions, dictionary.
        all_pc_tco2 = {}
        # All per capita emissions being plotted (those below set threshold will be included in 'Other').
        high_pc_tco2 = pd.Series(name='Per capita FFCO2 emissions')

        # Associated data for chart footer text.
        pc_associated_data = {}
        # During calculations, tally emissions and population plotted and processed.
        plotted_emissions_mtco2 = 0
        plotted_pop = 0
        pop_at_or_below_world_mean_pc_emissions = 0
        emissions_at_or_below_world_mean_pc_emissions_Mtco2 = 0
        assessed_population = 0
        assessed_emissions_mtco2 = 0
        # Set flag for country being profiled to be assigned per capita emissions of 'Other' unless found to be above
        # per capita emission threshold.
        country_below_threshold = True
        # Determine final year of EI data.
        fy = max(ei_data.index)
        # Determine world population.
        world_population = pop_data.at['WLD', 'Population']
        # To reduce execution time, only use most recent year of energy data.
        fy_energy_data = ei_data.loc[max(ei_data.index)]
        # Change index to allow sorting by FF CO2.
        fy_energy_data.set_index('Var', inplace=True)
        # Determine world FF CO2 emissions in final year.
        world_emissions_mtco2 = fy_energy_data.loc[
            (fy_energy_data.index == 'co2_combust_mtco2') & (
                    fy_energy_data['Country'] == 'Total World'), 'Value'].values[0]
        # Calculate world mean per capita FF CO2 emissions
        world_pc_tco2 = world_emissions_mtco2 * 1e6 / world_population
        # Identify those countries that appear in both datasets, and calculate their per capita emissions.
        for pop_row in pop_data.itertuples():
            for energy_row in fy_energy_data.itertuples():
                if pop_row.Index == energy_row.ISO3166_alpha3:
                    # Calculate per capita emissions of each country.
                    if energy_row.Index == 'co2_combust_mtco2':
                        country_pc_tco2 = energy_row.Value * 1e6 / pop_row.Population
                        all_pc_tco2[energy_row.Country] = country_pc_tco2
                        # Save separate value for country being profiled to allow it to be highlighted in chart.
                        if energy_row.Country == profile_country and not pop_row.Index == 'WLD':
                            profile_country_pc_tco2['Country'] = profile_country
                            profile_country_pc_tco2['Value'] = country_pc_tco2
                            # Rename if need be.
                            if profile_country_pc_tco2['Country'] == 'United Arab Emirates':
                                profile_country_pc_tco2['Country'] = 'UAE'
                            if profile_country_pc_tco2['Country'] == 'Total World':
                                profile_country_pc_tco2['Country'] = 'World'
                        # Separate countries that exceed set threshold and tally the cumulative population and
                        # emissions.
                        if (country_pc_tco2 >= user_globals.Constant.PER_CAPITA_THRESHOLD.value
                                and not pop_row.Index == 'WLD'):  # World is added at end of chart.
                            high_pc_tco2[energy_row.Country] = country_pc_tco2
                            # If the current country is that being profiled, and is above the threshold, then disable
                            # the flag that assigns the column to be highlighted in the chart is that of 'Other'.
                            if energy_row.Country == profile_country:
                                country_below_threshold = False
                            # Tally country above threshold provided it's not World.
                            plotted_pop += pop_row.Population
                            plotted_emissions_mtco2 += energy_row.Value
                        # Tally population and emissions of countries with per capita FF CO2 emissions less than or
                        # equal to world mean emissions.
                        if country_pc_tco2 <= world_pc_tco2 and not pop_row.Index == 'WLD':
                            pop_at_or_below_world_mean_pc_emissions += pop_row.Population
                            emissions_at_or_below_world_mean_pc_emissions_Mtco2 += energy_row.Value
                        # Tally population and emissions for countries that appeared in both datasets.
                        if not pop_row.Index == 'WLD':
                            assessed_population += pop_row.Population
                        if not energy_row.Country == 'Total World':
                            assessed_emissions_mtco2 += energy_row.Value
        # Calculate the share of world population assessed.
        assessed_share_world_population = assessed_population / world_population
        # Calculate the share of world FF CO2 emissions assessed.
        assessed_share_world_co2_emissions = assessed_emissions_mtco2 / world_emissions_mtco2
        # Calculate the per capita emissions of the remaining population.
        other_pc_emissions_for_plot_tco2 = pd.Series(
            data=[1e6 * (world_emissions_mtco2 - plotted_emissions_mtco2) / (world_population - plotted_pop)],
            index=['Other'])
        # If country being profiled is below threshold, then 'Other' are assigned to its per capita emissions to be
        # plotted in the per capita chart.
        if country_below_threshold is True and not profile_country == 'World':
            profile_country_pc_tco2 = {'Country': 'Other', 'Value': other_pc_emissions_for_plot_tco2.values[0]}
        high_pc_tco2.sort_values(ascending=False, inplace=True)
        world_pc_emissions_for_plot_tco2 = pd.Series(data=[world_pc_tco2], index=['World'])
        # Concat for plotting.
        plot_pc_tco2 = pd.concat([high_pc_tco2, other_pc_emissions_for_plot_tco2, world_pc_emissions_for_plot_tco2])

        # If World is being profiled, then assign world per capita emissions to it's highlighted.
        if profile_country == 'Total World':
            profile_country_pc_tco2 = {'Country': 'World', 'Value': world_pc_emissions_for_plot_tco2}

        # Shorten relevant country names
        plot_pc_tco2.rename(index={'Total World': 'World'}, inplace=True)
        plot_pc_tco2.rename(index={'China Hong Kong SAR': 'Hong Kong'}, inplace=True)
        plot_pc_tco2.rename(index={'United Arab Emirates': 'UAE'}, inplace=True)

        # Collect associated per capita stats required for chart's footnotes.
        pc_associated_data['Assessed Pop Share'] = assessed_share_world_population
        pc_associated_data['Assessed FFCO2 Emissions Share'] = assessed_share_world_co2_emissions
        pc_associated_data['World Pop'] = world_population
        pc_associated_data['Pop At Or Below PC Mean'] = pop_at_or_below_world_mean_pc_emissions
        pc_associated_data['Emissions At Or Below PC Mean MtCO2'] = emissions_at_or_below_world_mean_pc_emissions_Mtco2
        pc_associated_data['World FFCO2 Emissions MtCO2'] = world_emissions_mtco2
        pc_associated_data['World PC tCO2'] = world_pc_tco2
        pc_associated_data['FY'] = fy

        ################################################################################################################
        # Fossil Fuel Production.
        ################################################################################################################

        # Identify primary energy in country data.
        total_primary_EJ = country_data.loc[country_data['Var'] == 'tes_ej', 'Value']

        # Extract fossil fuel production data, convert to PJ, and copy to dataframe ffprod_PJ.
        ffprod_PJ = pd.DataFrame(index=total_primary_EJ.index, columns=['Coal', 'Oil', 'Gas'])
        ffprod_PJ['Coal'] = (
                country_data.loc[country_data['Var'] == 'coalprod_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        oil_mt = country_data.loc[country_data['Var'] == 'oilprod_mt', 'Value']
        ffprod_PJ['Oil'] = (
                oil_mt
                * 1e6
                * user_globals.Constant.TOE_TO_GJ.value
                * user_globals.Constant.GJ_TO_PJ.value
        )
        ffprod_PJ['Gas'] = (
                country_data.loc[country_data['Var'] == 'gasprod_ej', 'Value'] * user_globals.Constant.EJ_TO_PJ.value)
        # If nil production, create 0 series in order for chart function to plot correctly.
        if ffprod_PJ['Coal'].empty or ffprod_PJ['Coal'].dropna().empty:
            ffprod_PJ['Coal'] = pd.Series(data=0, index=total_primary_EJ.index)
        if ffprod_PJ['Oil'].empty or ffprod_PJ['Oil'].dropna().empty:
            ffprod_PJ['Oil'] = pd.Series(data=0, index=total_primary_EJ.index)
        if ffprod_PJ['Gas'].empty or ffprod_PJ['Gas'].dropna().empty:
            ffprod_PJ['Gas'] = pd.Series(data=0, index=total_primary_EJ.index)

        ################################################################################################################
        # Primary Energy.
        ################################################################################################################

        # Extract primary energy data, convert to PJ, and copy to dataframe primary_PJ.
        primary_PJ = pd.DataFrame(
            index=total_primary_EJ.index,
            columns=[
                'Coal',
                'Oil',
                'Gas',
                'Nuclear',
                'Hydro',
                'Wind',
                'Solar',
                'Bio, Geo and Other',
                'Fossil Fuels',
                'Renewables',
                'Total',
            ],
        )
        primary_PJ['Coal'] = (
                country_data.loc[country_data['Var'] == 'coalcons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Oil'] = (
                country_data.loc[country_data['Var'] == 'oilcons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Gas'] = (
                country_data.loc[country_data['Var'] == 'gascons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Nuclear'] = (
                country_data.loc[country_data['Var'] == 'nuclear_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Hydro'] = (
                country_data.loc[country_data['Var'] == 'hydro_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Wind'] = (
                country_data.loc[country_data['Var'] == 'wind_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Solar'] = (
                country_data.loc[country_data['Var'] == 'solar_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ['Bio, Geo and Other'] = (
                country_data.loc[country_data['Var'] == 'biogeo_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
                + country_data.loc[country_data['Var'] == 'biofuels_cons_pj', 'Value']
        )
        # Replace any NaNs with 0 in fields imported into primary_PJ.
        with pd.option_context('future.no_silent_downcasting', True):
            primary_PJ.fillna(0, inplace=True)

        # Calculate primary energy categories.
        primary_PJ['Fossil Fuels'] = (primary_PJ['Coal'] + primary_PJ['Oil'] + primary_PJ['Gas'])
        primary_PJ['Renewables'] = (primary_PJ['Hydro'] + primary_PJ['Wind'] + primary_PJ['Solar'])
        primary_PJ['Total'] = total_primary_EJ * user_globals.Constant.EJ_TO_PJ.value

        ################################################################################################################
        # Electricity Generation.
        ################################################################################################################

        # Extract electricity generation data and copy to dataframe total_elecgen_TWh.
        # For some countries (e.g. Norway, Luxembourg), EI data contains a total for the country ('elect_twh'), but not
        # a value for every fuel. In such cases, the country's value for total electricity generation, 'elect_twh', will
        # have a value and any difference between this and the sum of electricity generation by individual fuels is
        # classified here as 'Unpublished', and appear as a share in text in the top right of the plot. Data may
        # be provided for non-combustible fuels, in which case these will are plotted and totalled.

        total_elecgen_TWh = country_data.loc[country_data['Var'] == 'elect_twh']
        elecgen_TWh = pd.DataFrame(
            index=total_elecgen_TWh.index,
            columns=[
                'Coal',
                'Oil',
                'Gas',
                'Nuclear',
                'Hydro',
                'Wind',
                'Solar',
                'Bio, Geo and Other',
                'Fossil Fuels',
                'Wind and Solar',
                'Renewables',
                'Sum Fuels',
                'Total Fuels',
                'Total Country',
                'Unpublished',
            ],
        )
        elecgen_TWh['Coal'] = country_data.loc[country_data['Var'] == 'electbyfuel_coal', 'Value']
        elecgen_TWh['Oil'] = country_data.loc[country_data['Var'] == 'electbyfuel_oil', 'Value']
        elecgen_TWh['Gas'] = country_data.loc[country_data['Var'] == 'electbyfuel_gas', 'Value']
        elecgen_TWh['Nuclear'] = country_data.loc[country_data['Var'] == 'nuclear_twh', 'Value']
        elecgen_TWh['Hydro'] = country_data.loc[country_data['Var'] == 'hydro_twh', 'Value']
        elecgen_TWh['Wind'] = country_data.loc[country_data['Var'] == 'wind_twh', 'Value']
        elecgen_TWh['Solar'] = country_data.loc[country_data['Var'] == 'solar_twh', 'Value']
        elecgen_TWh['Bio, Geo and Other'] = (
                country_data.loc[country_data['Var'] == 'biogeo_twh', 'Value']
                + country_data.loc[country_data['Var'] == 'electbyfuel_other', 'Value']
        )
        # Replace any NaNs with 0.
        with pd.option_context('future.no_silent_downcasting', True):
            elecgen_TWh.fillna(0, inplace=True)
        # Calculate categories.
        elecgen_TWh['Fossil Fuels'] = (elecgen_TWh['Coal'] + elecgen_TWh['Oil'] + elecgen_TWh['Gas'])
        elecgen_TWh['Wind and Solar'] = elecgen_TWh['Wind'] + elecgen_TWh['Solar']
        elecgen_TWh['Renewables'] = (elecgen_TWh['Wind'] + elecgen_TWh['Solar'] + elecgen_TWh['Hydro'])

        # Calculate unpublished quantity for the country.
        # Extract country total from data.
        elecgen_TWh['Total Country'] = country_data.loc[country_data['Var'] == 'elect_twh', 'Value']
        # Calculate sum of elec gen by individual fuels in data.
        elecgen_TWh['Sum Fuels'] = (
                elecgen_TWh['Coal']
                + elecgen_TWh['Oil']
                + elecgen_TWh['Gas']
                + elecgen_TWh['Nuclear']
                + elecgen_TWh['Hydro']
                + elecgen_TWh['Wind']
                + elecgen_TWh['Solar']
                + elecgen_TWh['Bio, Geo and Other']
        )
        # Calculate annual unpublished quantity.
        elecgen_TWh['Unpublished'] = (elecgen_TWh['Total Country'] - elecgen_TWh['Sum Fuels'])

        # Replace very small quantities with 0, for purpose of plotting.
        elecgen_TWh['Coal'] = np.where(elecgen_TWh['Coal'] < 0.1, 0, elecgen_TWh['Coal'])
        elecgen_TWh['Oil'] = np.where(elecgen_TWh['Oil'] < 0.1, 0, elecgen_TWh['Oil'])
        elecgen_TWh['Gas'] = np.where(elecgen_TWh['Gas'] < 0.1, 0, elecgen_TWh['Gas'])
        elecgen_TWh['Nuclear'] = np.where(elecgen_TWh['Nuclear'] < 0.1, 0, elecgen_TWh['Nuclear'])
        elecgen_TWh['Hydro'] = np.where(elecgen_TWh['Hydro'] < 0.1, 0, elecgen_TWh['Hydro'])
        elecgen_TWh['Wind'] = np.where(elecgen_TWh['Wind'] < 0.1, 0, elecgen_TWh['Wind'])
        elecgen_TWh['Solar'] = np.where(elecgen_TWh['Solar'] < 0.1, 0, elecgen_TWh['Solar'])
        elecgen_TWh['Bio, Geo and Other'] = np.where(elecgen_TWh['Bio, Geo and Other'] <
                                                     0.1, 0, elecgen_TWh['Bio, Geo and Other'])
        elecgen_TWh['Unpublished'] = np.where(elecgen_TWh['Unpublished'] < 0.1, 0, elecgen_TWh['Unpublished'])
    else:
        print('Country not in EI data.\n')
        incl_ei_flag = False
        ffco2_Mt = None
        ffco2_Gt = None
        plot_pc_tco2 = None
        profile_country_pc_tco2 = None
        pc_associated_data = None
        ffprod_PJ = None
        primary_PJ = None
        elecgen_TWh = None

    # Collate final energy values from IEA data.
    if tfc_TJ is not None:
        finalenergy_PJ = tfc_TJ.mul(user_globals.Constant.TJ_TO_PJ.value)
    else:
        finalenergy_PJ = None

    # Return country energy system data as object.
    return user_globals.Energy_System(
        country,
        incl_ei_flag,
        ffco2_Mt,
        ffco2_Gt,
        plot_pc_tco2,
        profile_country_pc_tco2,
        pc_associated_data,
        co2_by_sector_Mt,
        ffprod_PJ,
        primary_PJ,
        elecgen_TWh,
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        finalenergy_PJ,
        pd.DataFrame(),  # Populated in process.py
    )


########################################################################################################################
#
# Function: populate_major_emitter_co2_energy_dataframe()
#
# Description:
# For major emitters, construct dataframe of fossil fuel CO2 emissions and primary energy data.
#
########################################################################################################################
def populate_major_emitter_co2_energy_dataframe(major_emitters, ei_data):
    # Initialise loop counter
    n = 0
    # For each large emitting country -
    for country in major_emitters:
        # Generate multi index indices for dataframe
        parameters = ['ffco2_Mt', 'primary_PJ_coal', 'primary_PJ_oil', 'primary_PJ_gas']
        country_name = []
        for i in range(4):
            country_name = country_name + [country]
        arrays = [country_name, parameters]
        indices = pd.MultiIndex.from_arrays(arrays, names=('Country', 'Parameter'))

        # Assemble data
        country_energy_data = ei_data.loc[ei_data['Country'] == country]
        ffco2_Mt = country_energy_data.loc[country_energy_data['Var'] == 'co2_combust_mtco2', 'Value']
        primary_PJ_coal = (
                country_energy_data.loc[country_energy_data['Var'] == 'coalcons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ_oil = (
                country_energy_data.loc[country_energy_data['Var'] == 'oilcons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ_gas = (
                country_energy_data.loc[country_energy_data['Var'] == 'gascons_ej', 'Value']
                * user_globals.Constant.EJ_TO_PJ.value
        )

        # Name each data series
        ffco2_Mt.name = 'ffco2_Mt'
        primary_PJ_coal.name = 'primary_PJ_coal'
        primary_PJ_oil.name = 'primary_PJ_oil'
        primary_PJ_gas.name = 'primary_PJ_gas'

        # Concatenate series to create a dataframe
        dataframe = pd.concat([ffco2_Mt, primary_PJ_coal, primary_PJ_oil, primary_PJ_gas], axis=1)
        # Transpose
        dataframe = dataframe.T
        # Replace index with multi index generated above
        dataframe.index = indices
        # Create parent dataframe
        if n == 0:
            major_emitter_co2_energy_dataframe = dataframe
        else:
            major_emitter_co2_energy_dataframe = pd.concat([major_emitter_co2_energy_dataframe, dataframe])
        # Increment loop counter
        n += 1
    return major_emitter_co2_energy_dataframe
