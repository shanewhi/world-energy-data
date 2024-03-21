#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:56:36 2024

@author: shanewhite
"""

# Import Python modules.
import pandas as pd

# Import user modules.
import user_globals


# Function extracts country specific data from Energy Institute's dataset.
# Returns instance of custom class Energy_System.
def populate_energy_system(ei_data, country):
    country_data = ei_data.loc[country]
    coalprod_Mt = country_data.loc[country_data['Var'] == 'coalprod_mt']
    oilprod_kbpd = country_data.loc[country_data['Var'] == 'oilprod_kbd']
    gasprod_bcm = country_data.loc[country_data['Var'] == 'gasprod_bcm']
    coal_primary_EJ = country_data.loc[country_data['Var'] == 'coalcons_ej']
    oil_primary_EJ = country_data.loc[country_data['Var'] == 'oilcons_ej']
    gas_primary_EJ = country_data.loc[country_data['Var'] == 'gascons_ej']
    nuclear_primary_EJ = country_data.loc[country_data['Var'] == 'nuclear_ej']
    hydro_primary_EJ = country_data.loc[country_data['Var'] == 'hydro_ej']
    wind_primary_EJ = country_data.loc[country_data['Var'] == 'wind_ej']
    solar_primary_EJ = country_data.loc[country_data['Var'] == 'solar_ej']
    geo_bio_other_primary_EJ = country_data.loc[country_data['Var'] == \
                                                'biogeo_ej']
    primary_EJ = country_data.loc[country_data['Var'] == \
                                                'primary_ej']
    # Create new empty pandas dataframe for oil production unit conversion
    # kbpd -> Mpbd.
    oilprod_Mbpd = pd.DataFrame(columns = ['Year', 'Var', 'Value'])
    oilprod_Mbpd['Year'] = oilprod_kbpd['Year']
    oilprod_Mbpd['Var'] = 'oilprod_Mbpd'
    oilprod_Mbpd['Value'] = oilprod_kbpd['Value'] * \
        user_globals.Constant.THOUSAND_TO_MILLION.value
    if country == 'Total World':
        country = 'World'
    return (user_globals.Energy_System(
        country,
        coalprod_Mt,
        oilprod_Mbpd,
        gasprod_bcm,
        coal_primary_EJ,
        oil_primary_EJ,
        gas_primary_EJ,
        nuclear_primary_EJ,
        hydro_primary_EJ,
        wind_primary_EJ,
        solar_primary_EJ,
        geo_bio_other_primary_EJ,
        primary_EJ))
