#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:36 2024
#@author: shanewhite


# Import Python modules.
import pandas as pd


# Import user modules.
import user_globals


# Extract national data from Energy Institute's dataset and return
# populated instance of custom class Energy_System.
def populate_energy_system(ei_data, country):
    country_data = ei_data.loc[country]
    primary_EJ = country_data.loc[country_data['Var'] ==
                                  'primary_ej']
    coalprod_Mt = country_data.loc[country_data['Var'] == 'coalprod_mt']
    coalprod_Mt.replace('coalprod_mt', 'coalprod_Mt')
    oilprod_kbpd = country_data.loc[country_data['Var'] == 'oilprod_kbd']
    oilprod_Mbpd = pd.DataFrame(index = oilprod_kbpd.index,
                                columns = ['Year', 'Var', 'Value'])
    oilprod_Mbpd['Year'] = oilprod_kbpd['Year']
    oilprod_Mbpd['Var'] = 'oilprod_Mbpd'
    oilprod_Mbpd['Value'] = oilprod_kbpd['Value'] * \
                         user_globals.Constant.THOUSAND_TO_MILLION.value
    gasprod_bcm = country_data.loc[country_data['Var'] == 'gasprod_bcm']
    coal_primary_EJ = country_data.loc[country_data['Var'] == 'coalcons_ej']
    oil_primary_EJ = country_data.loc[country_data['Var'] == 'oilcons_ej']
    gas_primary_EJ = country_data.loc[country_data['Var'] == 'gascons_ej']
    nuclear_primary_EJ = country_data.loc[country_data['Var'] == 'nuclear_ej']
    hydro_primary_EJ = country_data.loc[country_data['Var'] == 'hydro_ej']
    wind_primary_EJ = country_data.loc[country_data['Var'] == 'wind_ej']
    solar_primary_EJ = country_data.loc[country_data['Var'] == 'solar_ej']
    biogeo_primary_EJ = country_data.loc[country_data['Var'] ==
                                                'biogeo_ej']
    biofuels_primary_PJ = country_data.loc[country_data['Var'] ==
                                           'biofuels_cons_pj']

    # Drop 'country' index from dataframes and replace with 'Year'.
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
    biogeo_primary_EJ = biogeo_primary_EJ.set_index('Year')
    biofuels_primary_PJ = biofuels_primary_PJ.set_index('Year')

    # Ensure all dataframes comsist of the same range of years.

    # Fill any missing values with 0.
    coalprod_Mt = \
        coalprod_Mt.reindex(primary_EJ.index, fill_value = 0)
    oilprod_Mbpd = \
        oilprod_Mbpd.reindex(primary_EJ.index, fill_value = 0)
    gasprod_bcm = \
        gasprod_bcm.reindex(primary_EJ.index, fill_value = 0)
    coal_primary_EJ = \
        coal_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    oil_primary_EJ = \
        oil_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    gas_primary_EJ = \
        gas_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    nuclear_primary_EJ = \
        nuclear_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    hydro_primary_EJ = \
        hydro_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    wind_primary_EJ = \
        wind_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    solar_primary_EJ = \
        solar_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    biogeo_primary_EJ  = \
        biogeo_primary_EJ.reindex(primary_EJ.index, fill_value = 0)
    biofuels_primary_PJ  = \
        biofuels_primary_PJ.reindex(primary_EJ.index, fill_value = 0)

    # Construct geo_bio_other dataframe to combine biogeo_cons_ej and
    # biofuels_cons_pj (i.e. combine solid and liquid biofuels).
    geo_bio_other_primary_EJ = pd.DataFrame(index = biogeo_primary_EJ.index,
                                columns = ['Var', 'Value'])
    geo_bio_other_primary_EJ['Var'] = 'geo_bio_other_ej'
    geo_bio_other_primary_EJ['Value'] = biogeo_primary_EJ['Value'] + \
                            (biofuels_primary_PJ.Value / 1000)

    # Replace 'Totl World' label for chart titles.
    if country == 'Total World':
        country = 'World'

    # Return national energy system data
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
