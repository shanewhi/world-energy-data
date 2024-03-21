#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:56:43 2024

@author: shanewhite
"""

# Import Python modules.
import pandas as pd


# Import user modules.
import user_globals
import chart


# Identify production data in energy system user class and draw chart
def production(energy_system):

    if energy_system.coalprod_Mt.empty == False:
        title = energy_system.name + ': Coal Production'
        ylabel = ('Annual Production (Mt)')
        chart.column(energy_system.coalprod_Mt,
            user_globals.Color.COAL.value,
            title,
            ylabel)

    if energy_system.oilprod_Mbpd.empty == False:
        title = energy_system.name + ': Oil Production'
        ylabel = ('Annual Production (Mbpd)')
        chart.column(energy_system.oilprod_Mbpd,
            user_globals.Color.OIL.value,
            title,
            ylabel)
    
    if energy_system.gasprod_bcm.empty == False:
        title = energy_system.name + ': Gas Production'
        ylabel = ('Annual Production (bcm)')
        chart.column(energy_system.gasprod_bcm,
            user_globals.Color.GAS.value,
            title,
            ylabel)


# Identify primary energy data in energy system user class and draw chart
def primary_energy(energy_system):

    # Coal
    if energy_system.coal_primary_EJ.empty == False:
        coal_primary_share = pd.DataFrame(columns = \
                                          ['Year', 'Var', 'Value'])
        coal_primary_share['Year'] = \
            energy_system.coal_primary_EJ['Year']
        coal_primary_share['Var'] = 'coal_primary_share'
        coal_primary_share['Value'] = \
            (energy_system.coal_primary_EJ['Value'] / \
             energy_system.primary_EJ['Value']) * 100
        title = energy_system.name + \
            ': Coal in Energy Supply'
        ylabel = ('Annual Share of Primary Energy (%)')
        chart.line(coal_primary_share,
                   user_globals.Color.COAL.value,
                   title,
                   ylabel)

    # Oil
    if energy_system.oil_primary_EJ.empty == False:
        oil_primary_share = pd.DataFrame(columns = \
                                          ['Year', 'Var', 'Value'])
        oil_primary_share['Year'] = \
            energy_system.oil_primary_EJ['Year']
        oil_primary_share['Var'] = 'oil_primary_share'
        oil_primary_share['Value'] = \
            (energy_system.oil_primary_EJ['Value'] / \
             energy_system.primary_EJ['Value']) * 100
        title = energy_system.name + \
            ': Oil in Energy Supply'
        ylabel = ('Annual Share of Primary Energy (%)')
        chart.line(oil_primary_share,
                   user_globals.Color.OIL.value,
                   title,
                   ylabel)

    # Gas
    if energy_system.gas_primary_EJ.empty == False:
       gas_primary_share = pd.DataFrame(columns = \
                                        ['Year', 'Var', 'Value'])
       gas_primary_share['Year'] = \
           energy_system.gas_primary_EJ['Year']
       gas_primary_share['Var'] = 'gas_primary_share'
       gas_primary_share['Value'] = \
           (energy_system.gas_primary_EJ['Value'] / \
            energy_system.primary_EJ['Value']) * 100
       title = energy_system.name + \
           ': Gas in Energy Supply'
       ylabel = ('Annual Share of Primary Energy (%)')
       chart.line(gas_primary_share,
                  user_globals.Color.GAS.value,
                  title,
                  ylabel)

    # Nuclear
    if energy_system.nuclear_primary_EJ.empty == False:
       nuclear_primary_share = pd.DataFrame(columns = \
                                        ['Year', 'Var', 'Value'])
       nuclear_primary_share['Year'] = \
           energy_system.nuclear_primary_EJ['Year']
       nuclear_primary_share['Var'] = 'nuclear_primary_share'
       nuclear_primary_share['Value'] = \
           (energy_system.nuclear_primary_EJ['Value'] / \
            energy_system.primary_EJ['Value']) * 100
       title = energy_system.name + \
           ': Nuclear in Energy Supply'
       ylabel = ('Annual Share of Primary Energy (%)')
       chart.line(nuclear_primary_share,
                  user_globals.Color.NUCLEAR.value,
                  title,
                  ylabel)

    # Hydro
    if energy_system.hydro_primary_EJ.empty == False:
       hydro_primary_share = pd.DataFrame(columns = \
                                        ['Year', 'Var', 'Value'])
       hydro_primary_share['Year'] = \
           energy_system.hydro_primary_EJ['Year']
       hydro_primary_share['Var'] = 'hydro_primary_share'
       hydro_primary_share['Value'] = \
           (energy_system.hydro_primary_EJ['Value'] / \
            energy_system.primary_EJ['Value']) * 100
       title = energy_system.name + \
           ': Hydro in Energy Supply'
       ylabel = ('Annual Share of Primary Energy (%)')
       chart.line(hydro_primary_share,
                  user_globals.Color.HYDRO.value,
                  title,
                  ylabel)

    # Wind + Solar
    if energy_system.wind_primary_EJ.empty == False or \
            energy_system.solar_primary_EJ.empty == False:
        wind_solar_primary_share = pd.DataFrame(columns = \
                                        ['Year', 'Var', 'Value'])
        if energy_system.wind_primary_EJ.empty == False:
            wind_solar_primary_share['Year'] = \
                energy_system.wind_primary_EJ['Year']
        else:
            wind_solar_primary_share['Year'] = \
                energy_system.solar_primary_EJ['Year']
        wind_solar_primary_share['Var'] = 'wind_solar_primary_share'
        wind_solar_primary_share['Value'] = \
           ((energy_system.wind_primary_EJ['Value'] +
             energy_system.solar_primary_EJ['Value']) / \
           energy_system.primary_EJ['Value']) * 100
        title = energy_system.name + \
           ': Wind and Solar in Energy Supply'
        ylabel = ('Annual Share of Primary Energy (%)')
        chart.line(wind_solar_primary_share,
                  user_globals.Color.WIND_SOLAR.value,
                  title,
                  ylabel)

