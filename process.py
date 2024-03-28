#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:43 2024
#@author: shanewhite

# mport Python modules
import pandas as pd
import matplotlib.pyplot as plt
import math

#import user modules
import user_globals
import chart

#identify production data in energy system user class and draw charts
def production(energy_system):
    chart.column_subplot(energy_system.primary_EJ, energy_system.coalprod_Mt,
        energy_system.oilprod_Mbpd, energy_system.gasprod_bcm,
        user_globals.Color.COAL.value, user_globals.Color.OIL.value,
        user_globals.Color.GAS.value, energy_system.name.upper(),
        'Fossil Fuel Production','Coal', 'Oil', 'Gas', 'Annual Production (Mt)',
        'Annual Production (Mbpd)', 'Annual Production (bcm)', 'Any gap at \
beginning of a chart is due to data not present in dataset.\n')
    plt.show()

#identify primary energy data in energy system user class and draw charts
def primary_energy(energy_system):
    #coal
    if not energy_system.coal_primary_EJ.empty:
        coal_primary_share = pd.DataFrame(index =
                             energy_system.coal_primary_EJ.index,
                             columns = ['Var', 'Value'])
        coal_primary_share.Var = 'coal_primary_share'
        coal_primary_share.Value = \
            (energy_system.coal_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100
    #oil
    if not energy_system.oil_primary_EJ.empty:
        oil_primary_share = pd.DataFrame(index = \
                            energy_system.oil_primary_EJ.index,
                            columns = ['Var', 'Value'])
        oil_primary_share.Var = 'oil_primary_share'
        oil_primary_share.Value = \
            (energy_system.oil_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #gas
    if not energy_system.gas_primary_EJ.empty:
       gas_primary_share = pd.DataFrame(index = \
                           energy_system.gas_primary_EJ.index,
                           columns = ['Var', 'Value'])
       gas_primary_share.Var = 'gas_primary_share'
       gas_primary_share.Value = \
           (energy_system.gas_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100
    #nuclear
    if not energy_system.nuclear_primary_EJ.empty:
        nuclear_primary_share = pd.DataFrame(index = \
                                energy_system.nuclear_primary_EJ.index,
                                columns = ['Var', 'Value'])
        nuclear_primary_share.Var = 'nuclear_primary_share'
        nuclear_primary_share.Value = \
           (energy_system.nuclear_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100
    #hydro
    if not energy_system.hydro_primary_EJ.empty:
        hydro_primary_share = pd.DataFrame(index = \
                              energy_system.hydro_primary_EJ.index,
                              columns = ['Var', 'Value'])
        hydro_primary_share.Var = 'hydro_primary_share'
        hydro_primary_share.Value = \
           (energy_system.hydro_primary_EJ.Value /
            energy_system.primary_EJ.Value) * 100
    #wind
    if not energy_system.wind_primary_EJ.empty:
        wind_primary_share = pd.DataFrame(index = \
                             energy_system.primary_EJ.index,
                             columns = ['Var', 'Value'])
        wind_primary_share.Var = 'wind_primary_share'
        wind_primary_share.Value = \
            (energy_system.wind_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100
    #solar
    if not energy_system.solar_primary_EJ.empty:
        solar_primary_share = pd.DataFrame(index = \
                              energy_system.solar_primary_EJ.index,
                              columns = ['Var', 'Value'])
        solar_primary_share.Var = 'solar_primary_share'
        solar_primary_share.Value = \
            (energy_system.solar_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #geo, bio and other
    if not energy_system.geo_bio_other_primary_EJ.empty:
        geo_bio_other_primary_share = pd.DataFrame(index = \
                              energy_system.geo_bio_other_primary_EJ.index,
                              columns = ['Var', 'Value'])
        geo_bio_other_primary_share.Var = 'geo_bio_other_primary_share'
        geo_bio_other_primary_share.Value = \
            (energy_system.geo_bio_other_primary_EJ.Value /
             energy_system.primary_EJ.Value) * 100
    #wind + solar
    if not (energy_system.wind_primary_EJ.empty or \
            energy_system.solar_primary_EJ.empty):
         wind_solar_primary_share = pd.DataFrame(index = \
                                    energy_system.primary_EJ.index,
                                    columns = ['Var', 'Value'])
         wind_solar_primary_share.Var = 'wind_solar_primary_share'
         wind_solar_primary_share.Value = \
            ((energy_system.wind_primary_EJ.Value +
              energy_system.solar_primary_EJ.Value) / \
              energy_system.primary_EJ.Value) * 100
    ff_primary_share = pd.DataFrame(index = \
                                   energy_system.primary_EJ.index,
                                   columns = ['Var', 'Value'])
    ff_primary_share.Var = 'ff_primary_share'
    ff_primary_share.Value = coal_primary_share.Value.fillna(0) + \
            				oil_primary_share.Value.fillna(0) + \
                			gas_primary_share.Value.fillna(0)

    renew_primary_share = pd.DataFrame(index = \
                                   energy_system.primary_EJ.index,
                                   columns = ['Var', 'Value'])
    renew_primary_share.Var = 'renew_primary_share'
    renew_primary_share.Value = wind_solar_primary_share.Value.fillna(0) + \
                                hydro_primary_share.Value.fillna(0)
    #draw line mutlichart(subplot) of primary energy
    title_addition = ''
    if not energy_system.name == 'World':
        title_addition = 'Share of Fuels in National Energy Supply'
    else:
        title_addition = 'Share of Fuels in Energy Supply'
    title = (energy_system.name.upper())
    title1 = 'Coal'
    title2 = 'Oil'
    title3 = 'Gas'
    title4 = 'Nuclear'
    title5 = 'Hydro'
    title6 = 'Wind + Solar'
    ylabel = ('Annual Share of Primary Energy (%)')
    subplot_title1 = 'Shares of geothermal, biofuels and \'other\' are small \
and omitted for clarity'
    subplot_title2 = 'Gaps may be present in line segments due to data not \
present in dataset.'
    subplot_title3 = 'Share for a given year is calculated using only data for \
fuels reported in that year.'
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
                       title4, title5, title6, ylabel, subplot_title1,
                       subplot_title2, subplot_title3)
    plt.show()
    #plot primary energy shares for most recent year
    final_coal_share = coal_primary_share.Value.iloc[-1]
    final_oil_share = oil_primary_share.Value.iloc[-1]
    final_gas_share = gas_primary_share.Value.iloc[-1]
    final_nuclear_share = nuclear_primary_share.Value.iloc[-1]
    final_hyrdo_share = hydro_primary_share.Value.iloc[-1]
    final_wind_share = wind_primary_share.Value.iloc[-1]
    final_solar_share = solar_primary_share.Value.iloc[-1]
    final_geo_bio_other_share = geo_bio_other_primary_share.Value.iloc[-1]
    final_ff_primary_share = ff_primary_share.Value.iloc[-1]
    final_renew_primary_share = renew_primary_share.Value.iloc[-1]
    final_fuel_shares = [final_coal_share,
                         final_oil_share,
                         final_gas_share,
                         final_nuclear_share,
                         final_hyrdo_share,
                         final_wind_share,
                         final_solar_share,
                         final_geo_bio_other_share]
    final_fuel_category_shares = [final_ff_primary_share,
                                  final_nuclear_share,
                                  final_renew_primary_share,
                                  final_geo_bio_other_share]
    fuel_colors = [user_globals.Color.COAL.value,
                    user_globals.Color.OIL.value,
                    user_globals.Color.GAS.value,
                    user_globals.Color.NUCLEAR.value,
                    user_globals.Color.HYDRO.value,
                    user_globals.Color.WIND.value,
                    user_globals.Color.SOLAR.value,
                    user_globals.Color.GEO_BIO_OTHER.value]
    fuel_category_colors = [user_globals.Color.FOSSIL_FUELS.value,
                            user_globals.Color.NUCLEAR.value,
                            user_globals.Color.RENEW.value,
                            user_globals.Color.GEO_BIO_OTHER.value]
    fuel_labels = ['Coal', 'Oil', 'Gas', 'Nuclear', 'Hydro', 'Wind', 'Solar',
                   'Geo+Bio+Other']
    fuel_category_labels = ['Fossil Fuels', 'Nuclear', 'Wind+Solar+Hydro',
                            'Geo+Bio+Other']
    filtered_final_fuel_shares = []
    filtered_fuel_labels = []
    filtered_fuel_colors = []
    filtered_final_fuel_category_shares = []
    filtered_fuel_category_labels = []
    filtered_fuel_category_colors = []
    #plot shares of primary energy for most recent year using treemap
    #pass to treemap shares that are not NaNs or less than 1%
    for i in range(len(final_fuel_shares)):
        if not (math.isnan(final_fuel_shares[i]) or final_fuel_shares[i] < 1):
            filtered_final_fuel_shares.append(round(final_fuel_shares[i], 1))
            filtered_fuel_colors.append(fuel_colors[i])
            filtered_fuel_labels.append(fuel_labels[i])
    for i in range(len(final_fuel_category_shares)):
        if not (math.isnan(final_fuel_category_shares[i]) or
            final_fuel_category_shares[i] < 1):
            filtered_final_fuel_category_shares.append(int(round(final_fuel_category_shares[i], 0)))
            filtered_fuel_category_colors.append(fuel_category_colors[i])
            filtered_fuel_category_labels.append(fuel_category_labels[i])
    subplot_title0 = 'Fuel Category'
    subplot_title1 = 'Fuel Share'
    suptitle = (energy_system.name.upper())
    suptitle_addition = 'Share of Fuels in Energy Supply, year ' + \
                            str(energy_system.primary_EJ.index[-1])
    footer_text = 'Values rounded so shares may not total 100%.\n' + \
        'Shares less than 1% not shown for clarity.'
    chart.treemap(filtered_final_fuel_category_shares,
                  filtered_fuel_category_colors,
                  filtered_fuel_category_labels,
                  subplot_title0,
                  filtered_final_fuel_shares,
                  filtered_fuel_colors,
                  filtered_fuel_labels,
                  subplot_title1,
                  suptitle,
                  suptitle_addition,
                  footer_text)
    plt.show()


