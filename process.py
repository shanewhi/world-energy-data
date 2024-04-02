#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:43 2024
#@author: shanewhite


# Import Python modules.
import pandas as pd
import matplotlib.pyplot as plt
import math


# Import user modules.
import user_globals
import chart


# Plot national fossil fuel production.
def production(energy_system):
    chart.column_subplot(energy_system.primary_EJ, energy_system.coalprod_Mt,
        energy_system.oilprod_Mbpd, energy_system.gasprod_bcm,
        user_globals.Color.COAL.value, user_globals.Color.OIL.value,
        user_globals.Color.GAS.value, energy_system.name.upper(),
        'Fossil Fuel Production','Coal', 'Oil', 'Gas',
        'Annual Production (Mt)', 'Annual Production (Mbpd)',
        'Annual Production (bcm)', 'Any gap at beginning of a chart is due to\
data not present in dataset.\n')
    plt.show()


# Identify national primary energy data, and plot.
def primary_energy(energy_system):
    # Calculate shares of primary energy over time for each fuel.
    # Coal.
    if not energy_system.coal_primary_EJ.empty:
        coal_primary_share = pd.DataFrame(index =
                             energy_system.coal_primary_EJ.index,
                             columns = ['Var', 'Value'])
        coal_primary_share['Var'] = 'coal_primary_share'
        coal_primary_share['Value'] = \
            (energy_system.coal_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100

    # Oil.
    if not energy_system.oil_primary_EJ.empty:
        oil_primary_share = pd.DataFrame(index = \
                            energy_system.oil_primary_EJ.index,
                            columns = ['Var', 'Value'])
        oil_primary_share['Var'] = 'oil_primary_share'
        oil_primary_share['Value'] = \
            (energy_system.oil_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100

    # Gas.
    if not energy_system.gas_primary_EJ.empty:
       gas_primary_share = pd.DataFrame(index = \
                           energy_system.gas_primary_EJ.index,
                           columns = ['Var', 'Value'])
       gas_primary_share['Var'] = 'gas_primary_share'
       gas_primary_share['Value'] = \
           (energy_system.gas_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100

    # Nuclear.
    if not energy_system.nuclear_primary_EJ.empty:
        nuclear_primary_share = pd.DataFrame(index = \
                                energy_system.nuclear_primary_EJ.index,
                                columns = ['Var', 'Value'])
        nuclear_primary_share['Var'] = 'nuclear_primary_share'
        nuclear_primary_share['Value'] = \
           (energy_system.nuclear_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100

    # Hydro.
    if not energy_system.hydro_primary_EJ.empty:
        hydro_primary_share = pd.DataFrame(index = \
                              energy_system.hydro_primary_EJ.index,
                              columns = ['Var', 'Value'])
        hydro_primary_share['Var'] = 'hydro_primary_share'
        hydro_primary_share['Value'] = \
           (energy_system.hydro_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100

    # Wind.
    if not energy_system.wind_primary_EJ.empty:
        wind_primary_share = pd.DataFrame(index = \
                             energy_system.primary_EJ.index,
                             columns = ['Var', 'Value'])
        wind_primary_share['Var'] = 'wind_primary_share'
        wind_primary_share['Value'] = \
            (energy_system.wind_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100

    # Solar.
    if not energy_system.solar_primary_EJ.empty:
        solar_primary_share = pd.DataFrame(index = \
                              energy_system.solar_primary_EJ.index,
                              columns = ['Var', 'Value'])
        solar_primary_share['Var'] = 'solar_primary_share'
        solar_primary_share['Value'] = \
            (energy_system.solar_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100

    # Geo, Bio and Other.
    if not energy_system.geo_bio_other_primary_EJ.empty:
        geo_bio_other_primary_share = pd.DataFrame(index = \
                              energy_system.geo_bio_other_primary_EJ.index,
                              columns = ['Var', 'Value'])
        geo_bio_other_primary_share['Var'] = 'geo_bio_other_primary_share'
        geo_bio_other_primary_share['Value'] = \
            (energy_system.geo_bio_other_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100

    # Wind + Solar.
    if not (energy_system.wind_primary_EJ.empty or \
            energy_system.solar_primary_EJ.empty):
         wind_solar_primary_share = pd.DataFrame(index = \
                                    energy_system.primary_EJ.index,
                                    columns = ['Var', 'Value'])
         wind_solar_primary_share['Var'] = 'wind_solar_primary_share'
         wind_solar_primary_share['Value'] = \
            ((energy_system.wind_primary_EJ.Value +
              energy_system.solar_primary_EJ.Value) / \
              energy_system.primary_EJ.Value) * 100

    # Fossil Fuels.
    ff_primary_share = pd.DataFrame(index = \
                                   energy_system.primary_EJ.index,
                                   columns = ['Var', 'Value'])
    ff_primary_share['Var'] = 'ff_primary_share'
    ff_primary_share['Value'] = coal_primary_share.Value.fillna(0) + \
            				oil_primary_share.Value.fillna(0) + \
                			gas_primary_share.Value.fillna(0)

    # Renewables (Wind + Solar + Hydro).
    renew_primary_share = pd.DataFrame(index = \
                                   energy_system.primary_EJ.index,
                                   columns = ['Var', 'Value'])
    renew_primary_share['Var'] = 'renew_primary_share'
    renew_primary_share['Value'] = wind_solar_primary_share.Value.fillna(0) + \
                                hydro_primary_share.Value.fillna(0)

    # Chart title.
    title = (energy_system.name.upper())
    title_addition = ''
    if not energy_system.name == 'World':
        title_addition = 'Share of Fuels in National Energy Supply'
    else:
        title_addition = 'Share of Fuels in Energy Supply'

    # Subplot titles.
    title1 = 'Coal'
    title2 = 'Oil'
    title3 = 'Gas'
    title4 = 'Nuclear'
    title5 = 'Hydro'
    title6 = 'Wind + Solar'

    # Additional text.
    ylabel = ('Annual Share of Primary Energy (%)')
    footer_text = "Annual share is calculated only using data for \
fuels reported in that year.\nGaps may be present in line segments due to \
data not present in dataset.\n'Shares of geothermal, biofuels and 'other' \
are small and omitted for clarity."

    chart.line_subplot(energy_system.primary_EJ,
                       coal_primary_share, oil_primary_share,
                       gas_primary_share, nuclear_primary_share,
                       hydro_primary_share, wind_solar_primary_share,
                       user_globals.Color.COAL.value,
                       user_globals.Color.OIL.value,
                       user_globals.Color.GAS.value,
                       user_globals.Color.NUCLEAR.value,
                       user_globals.Color.HYDRO.value,
                       user_globals.Color.WIND_SOLAR.value,
                       title, title_addition, title1, title2, title3,
                       title4, title5, title6, ylabel, footer_text)
    plt.show()

    # Plot primary energy shares for most recent year using treemaps.
    # Extract data for most recent year and arrange into dataframes.
    final_ff_primary_share = ff_primary_share.Value.iloc[-1]
    final_renew_primary_share = renew_primary_share.Value.iloc[-1]
    final_coal_share = coal_primary_share.Value.iloc[-1]
    final_oil_share = oil_primary_share.Value.iloc[-1]
    final_gas_share = gas_primary_share.Value.iloc[-1]
    final_nuclear_share = nuclear_primary_share.Value.iloc[-1]
    final_hyrdo_share = hydro_primary_share.Value.iloc[-1]
    final_wind_share = wind_primary_share.Value.iloc[-1]
    final_solar_share = solar_primary_share.Value.iloc[-1]
    final_geo_bio_other_share = geo_bio_other_primary_share.Value.iloc[-1]

    category_name = [
        'Fossil Fuels',
        'Nuclear',
        'Renewables',
        'Geo, Bio, Other']
    fuel_name = [
        'Coal',
        'Oil',
        'Gas',
        'Nuclear',
        'Hydro',
        'Wind',
        'Solar',
        'Geo, Bio, Other']

    final_category_share = [
        final_ff_primary_share,
        final_nuclear_share,
        final_renew_primary_share,
        final_geo_bio_other_share]
    final_fuel_share = [
        final_coal_share,
        final_oil_share,
        final_gas_share,
        final_nuclear_share,
        final_hyrdo_share,
        final_wind_share,
        final_solar_share,
        final_geo_bio_other_share]

    category_color = [
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEW.value,
        user_globals.Color.GEO_BIO_OTHER.value]
    fuel_color = [
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND.value,
        user_globals.Color.SOLAR.value,
        user_globals.Color.GEO_BIO_OTHER.value]

    # Filter out shares that are NaN or < 1%.

    filtered_final_category_share = []
    filtered_category_name = []
    filtered_category_color = []
    filtered_final_fuel_share = []
    filtered_fuel_name = []
    filtered_fuel_color = []
    for i in range(len(final_category_share)):
        if not (math.isnan(final_category_share[i]) or
        final_category_share[i] < 1):
            filtered_category_name.append(category_name[i])
            filtered_final_category_share.append \
                (int(round(final_category_share[i], 0)))
            filtered_category_color.append(category_color[i])
    for i in range(len(final_fuel_share)):
        if not (math.isnan(final_fuel_share[i]) or final_fuel_share[i] < 1):
            filtered_fuel_name.append(fuel_name[i])
            filtered_final_fuel_share.append(int(round(final_fuel_share[i], 0)))
            filtered_fuel_color.append(fuel_color[i])

    suptitle = (energy_system.name.upper())
    suptitle_addition = 'Share of Fuels in Energy Supply (Primary Energy), \
year ' + str(energy_system.primary_EJ.index[-1])
    title1 = 'Category Shares'
    title2 = 'Individual Fuel Shares'
    footer_text = "For clarity: (1) Values are rounded, so shares may not total \
100%, (2) Shares <1% aren't shown,\n(3) Labels for categories <20% \
aren't shown if there's a large difference between lowest & highest \
shares."

    df_category = pd.DataFrame(columns = [
        'Name',
        'Value',
        'Color'
        'Label'])
    df_category['Name'] = filtered_category_name
    df_category['Value'] = filtered_final_category_share
    df_category['Color'] = filtered_category_color

    df_fuel = pd.DataFrame(columns = [
        'Name',
        'Value',
        'Color'
        'Label'])
    df_fuel['Name'] = filtered_fuel_name
    df_fuel['Value'] = filtered_final_fuel_share
    df_fuel['Color'] = filtered_fuel_color

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_category['Value'].max() / df_category['Value'].min()) >= 5:
        df_category.loc[df_category['Value'] < 20, ['Label']] = \
            df_category['Value'].astype(str) + '%'
        df_category.loc[df_category['Value'] >= 20, ['Label']] = \
            df_category['Name'].astype(str) + ' ' + \
            df_category['Value'].astype(str) + '%'
    else:
        df_category['Label'] = \
            df_category['Name'].astype(str) + ' ' + \
            df_category['Value'].astype(str) + '%'

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_fuel['Value'].max() / df_fuel['Value'].min()) >= 5:
        df_fuel.loc[df_fuel['Value'] < 10, ['Label']] = \
            df_fuel['Value'].astype(str) + '%'
        df_fuel.loc[df_fuel['Value'] >= 10, ['Label']] = \
            df_fuel['Name'].astype(str) + ' ' + \
            df_fuel['Value'].astype(str) + '%'
    else:
        df_fuel['Label'] = \
            df_fuel['Name'].astype(str) + ' ' + \
            df_fuel['Value'].astype(str) + '%'

    chart.treemap(
        df_category,
        df_fuel,
        title1,
        title2,
        suptitle,
        suptitle_addition,
        footer_text)
    plt.show()


