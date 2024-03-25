#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:43 2024
#@author: shanewhite

# mport Python modules
import pandas as pd
import matplotlib.pyplot as plt

#import user modules
import user_globals
import chart

#identify production data in energy system user class and draw charts
def production(energy_system):
    chart.column_subplot(energy_system.primary_EJ, energy_system.coalprod_Mt, \
        energy_system.oilprod_Mbpd, energy_system.gasprod_bcm, \
        user_globals.Color.COAL.value, user_globals.Color.OIL.value, \
        user_globals.Color.GAS.value, energy_system.name.upper(), 'Coal', \
        'Oil', 'Gas', 'Annual Production (Mt)', 'Annual Production (Mbpd)', \
        'Annual Production (bcm)')
    #show charts now because they have a common size
    plt.show()

#identify primary energy data in energy system user class and draw charts
def primary_energy(energy_system):
    #coal
    if energy_system.coal_primary_EJ.empty == False:
        coal_primary_share = pd.DataFrame(index = \
                             energy_system.coal_primary_EJ.index, \
                             columns = ['Var', 'Value'])
        coal_primary_share.Var = 'coal_primary_share'
        coal_primary_share.Value = \
            (energy_system.coal_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #oil
    if energy_system.oil_primary_EJ.empty == False:
        oil_primary_share = pd.DataFrame(index = \
                            energy_system.oil_primary_EJ.index, \
                            columns = ['Var', 'Value'])
        oil_primary_share.Var = 'oil_primary_share'
        oil_primary_share.Value = \
            (energy_system.oil_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #gas
    if energy_system.gas_primary_EJ.empty == False:
       gas_primary_share = pd.DataFrame(index = \
                           energy_system.gas_primary_EJ.index, \
                           columns = ['Var', 'Value'])
       gas_primary_share.Var = 'gas_primary_share'
       gas_primary_share.Value = \
           (energy_system.gas_primary_EJ.Value / \
            energy_system.primary_EJ.Value) * 100
    #nuclear
    if energy_system.nuclear_primary_EJ.empty == False:
        nuclear_primary_share = pd.DataFrame(index = \
                                energy_system.nuclear_primary_EJ.index, \
                                columns = ['Var', 'Value'])
        nuclear_primary_share.Var = 'nuclear_primary_share'
        nuclear_primary_share.Value = \
           (energy_system.nuclear_primary_EJ.Value / \
            energy_system.primary_EJ.Value) * 100
    #hydro
    if energy_system.hydro_primary_EJ.empty == False:
        hydro_primary_share = pd.DataFrame(index = \
                              energy_system.hydro_primary_EJ.index, \
                              columns = ['Var', 'Value'])
        hydro_primary_share.Var = 'hydro_primary_share'
        hydro_primary_share.Value = \
           (energy_system.hydro_primary_EJ.Value / \
            energy_system.primary_EJ.Value) * 100
    #wind
    if energy_system.wind_primary_EJ.empty == False:
        wind_primary_share = pd.DataFrame(index = \
                             energy_system.primary_EJ.index, \
                             columns = ['Var', 'Value'])
        wind_primary_share.Var = 'wind_primary_share'
        wind_primary_share.Value = \
            (energy_system.wind_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #solar
    if energy_system.solar_primary_EJ.empty == False:
        solar_primary_share = pd.DataFrame(index = \
                              energy_system.solar_primary_EJ.index , \
                              columns = ['Var', 'Value'])
        solar_primary_share.Var = 'solar_primary_share'
        solar_primary_share.Value = \
            (energy_system.solar_primary_EJ.Value / \
             energy_system.primary_EJ.Value) * 100
    #wind + solar
    if energy_system.wind_primary_EJ.empty == False or \
            energy_system.solar_primary_EJ.empty == False:
         wind_solar_primary_share = pd.DataFrame(index = \
                                    energy_system.primary_EJ.index, \
                                    columns = ['Var', 'Value'])
         wind_solar_primary_share.Var = 'wind_solar_primary_share'
         wind_solar_primary_share.Value = \
            ((energy_system.wind_primary_EJ.Value +
              energy_system.solar_primary_EJ.Value) / \
              energy_system.primary_EJ.Value) * 100
    #draw mutlichart (subplot) version of primary energy
    #title = (energy_system.name.upper() + '\nShare of Fuels in Energy Supply')
    title = (energy_system.name.upper())
    title1 = 'Coal'
    title2 = 'Oil'
    title3 = 'Gas'
    title4 = 'Nuclear'
    title5 = 'Hydro'
    title6 = 'Wind + Solar'
    ylabel = ('Annual Share of Primary Energy (%)')
    chart.line_subplot(energy_system.primary_EJ, \
                       coal_primary_share, oil_primary_share, \
                       gas_primary_share, nuclear_primary_share, \
                       hydro_primary_share, wind_solar_primary_share, \
                       user_globals.Color.COAL.value, \
                       user_globals.Color.OIL.value, \
                       user_globals.Color.GAS.value, \
                       user_globals.Color.NUCLEAR.value, \
                       user_globals.Color.HYDRO.value, \
                       user_globals.Color.WIND_SOLAR.value, \
                       title, title1, title2, title3, title4, title5, title6, \
                       ylabel)
    plt.show()
