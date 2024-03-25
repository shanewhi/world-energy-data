#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:36 2024
#@author: shanewhite

#import Python modules
import pandas as pd

#import user modules
import user_globals

#extract country specific data from Energy Institute's dataset and
#return instance of custom class Energy_System
def populate_energy_system(ei_data, country):
    country_data = ei_data.loc[country]
    primary_EJ = country_data.loc[country_data['Var'] == \
                                  'primary_ej']
    coalprod_Mt = country_data.loc[country_data['Var'] == 'coalprod_mt']
    coalprod_Mt.replace('coalprod_mt', 'coalprod_Mt')
    oilprod_kbpd = country_data.loc[country_data['Var'] == 'oilprod_kbd']
    oilprod_Mbpd = pd.DataFrame(index = oilprod_kbpd.index, \
                                columns = ['Year', 'Var', 'Value'])
    oilprod_Mbpd.Year = oilprod_kbpd.Year
    oilprod_Mbpd.Var = 'oilprod_Mbpd'
    oilprod_Mbpd.Value = oilprod_kbpd.Value *\
                         user_globals.Constant.THOUSAND_TO_MILLION.value
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
    #drop 'country' index from dataframes and replace with 'year'
    primary_EJ = primary_EJ.set_index('Year')
    coalprod_Mt = coalprod_Mt.set_index('Year')
    oilprod_Mbpd = oilprod_Mbpd.set_index('Year')
    gasprod_bcm = gasprod_bcm.set_index('Year')
    coal_primary_EJ = coal_primary_EJ.set_index('Year')
    oil_primary_EJ = oil_primary_EJ.set_index('Year')
    gas_primary_EJ = gas_primary_EJ.set_index('Year')
    nuclear_primary_EJ = nuclear_primary_EJ.set_index('Year')
    hydro_primary_EJ = hydro_primary_EJ.set_index('Year')
    wind_primary_EJ = wind_primary_EJ.set_index('Year')
    solar_primary_EJ = solar_primary_EJ.set_index('Year')
    geo_bio_other_primary_EJ = geo_bio_other_primary_EJ.set_index('Year')
    #ensure all dataframes comsist of the same range of years
    coalprod_Mt = \
        coalprod_Mt.reindex(primary_EJ.index, fill_value = 0)
    oilprod_Mbpd = \
        oilprod_Mbpd.reindex(primary_EJ.index, fill_value = 0)
    gasprod_bcm = \
        gasprod_bcm.reindex(primary_EJ.index, fill_value = 0)
    coal_primary_EJ = \
        coal_primary_EJ.reindex(primary_EJ.index)
    oil_primary_EJ = \
        oil_primary_EJ.reindex(primary_EJ.index)
    gas_primary_EJ = \
        gas_primary_EJ.reindex(primary_EJ.index)
    nuclear_primary_EJ = \
        nuclear_primary_EJ.reindex(primary_EJ.index)
    hydro_primary_EJ = \
        hydro_primary_EJ.reindex(primary_EJ.index)
    wind_primary_EJ = \
        wind_primary_EJ.reindex(primary_EJ.index)
    solar_primary_EJ = \
        solar_primary_EJ.reindex(primary_EJ.index)
    geo_bio_other_primary_EJ = \
        geo_bio_other_primary_EJ.reindex(primary_EJ.index)
    #replace world label for charts
    if country == 'Total World':
        country = 'World'
    return (user_globals.Energy_System(
            country,
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm,
            primary_EJ,
            coal_primary_EJ,
            oil_primary_EJ,
            gas_primary_EJ,
            nuclear_primary_EJ,
            hydro_primary_EJ,
            wind_primary_EJ,
            solar_primary_EJ,
            geo_bio_other_primary_EJ))
