#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################################################
#
# Module: process.py
#
# Description:
# Performs processing of collated data, such as calculating shares and changes.
#
########################################################################################################################

# Import Python modules.
import math
import pandas as pd

# Import user modules.
import user_globals
import countries


########################################################################################################################
#
# Function: calc_country_shares_fy()
#
# Description:
# For all countries, calculate shares of CO2 emissions from fossil fuel combustion for
# the final year of data.
#
########################################################################################################################
def calc_country_shares_fy(data):
    # Extract CO2 emissions from fossil fuel combustion for all years.
    ffco2_Mt = data.loc[data['Var'] == 'co2_combust_mtco2']

    # Identify most recent year.
    final_yr = max(data.index)

    # Filter for data of most recent year.
    ffco2_Mt_fy = ffco2_Mt.loc[ffco2_Mt.index == final_yr]

    # Reindex dataframe to country so that those starting with 'Total' can be
    # dropped. Record World total prior.
    ffco2_Mt_fy.set_index(['Country'], inplace=True)
    total_ffco2_Mt = ffco2_Mt_fy.loc[ffco2_Mt_fy.index == 'Total World', 'Value'].values
    ffco2_Mt_fy = ffco2_Mt_fy.drop(
        index=ffco2_Mt_fy[ffco2_Mt_fy.index.str.startswith('Total')].index
    )
    # Calculate shares.
    ffco2_Mt_fy['Share'] = round(ffco2_Mt_fy['Value'] / total_ffco2_Mt * 100, 2)
    # TDrop 'Other' regions, which are collections of low emitting countries.
    # Dropping them only prevents any being tallied as a relatively large emitter. The
    # share is still included in the chart as 1-large_emitters.
    ffco2_Mt_fy = ffco2_Mt_fy.drop(
        index=ffco2_Mt_fy[ffco2_Mt_fy.index.str.startswith('Other')].index
    )
    # Record final year for later usage.
    ffco2_Mt_fy['Year'] = final_yr
    # Clean up.
    ffco2_Mt_fy = ffco2_Mt_fy.reset_index()
    ffco2_Mt_fy = ffco2_Mt_fy.drop(['Var', 'Value'], axis=1)
    return ffco2_Mt_fy


########################################################################################################################
#
# Function: carbon_emissions()
#
# Description:
# Calculate carbon emission shares, annual change, and generate dataframes for treemap plotting of final year data.
#
########################################################################################################################
def carbon_emissions(cdata, share_data):
    # Calculate changes and shares.
    min_year = min(cdata.index)
    max_year = max(cdata.index)
    change_yrs = range(min_year + 1, max_year + 1)
    for yr in change_yrs:
        cdata.loc[yr, 'Net FF and Cement Change'] = (
                cdata.loc[yr, 'Net FF and Cement'] - cdata.loc[yr - 1, 'Net FF and Cement']
        )
    cdata['Total'] = cdata['Net FF and Cement'] + cdata['Land Use Change']

    cdata['Fossil Fuel Share'] = (
            (cdata['Coal'] + cdata['Oil'] + cdata['Gas'] + cdata['Flaring'])
            / cdata['Total']
            * 100
    )
    cdata['Cement Share'] = (cdata['Cement'] - cdata['Cement Carbonation Sink']) / cdata['Total'] * 100
    cdata['Other Share'] = cdata['Other'] / cdata['Total'] * 100
    cdata['Land Use Change Share'] = cdata['Land Use Change'] / cdata['Total'] * 100
    cdata['Coal Share'] = cdata['Coal'] / cdata['Total'] * 100
    cdata['Oil Share'] = cdata['Oil'] / cdata['Total'] * 100
    cdata['Gas Share'] = cdata['Gas'] / cdata['Total'] * 100
    cdata['Flaring Share'] = cdata['Flaring'] / cdata['Total'] * 100

    # Display sum of carbon budget sum for every year; not just a summary.
    print('Annual Total of Carbon Budget Shares =')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(cdata['Fossil Fuel Share'] + cdata['Cement Share'] +
              cdata['Other Share'] + cdata['Land Use Change Share'])

    # Select second to last element below so as not to display projected values in treemap, because 2024 projections
    # are unavailable for 'flaring' and 'other', and shouldn't display values from a combination of years.

    ff_co2_share_fy = round(cdata['Fossil Fuel Share'].iloc[-2], 1)
    cement_co2_share_fy = round(cdata['Cement Share'].iloc[-2], 1)
    luc_co2_share_fy = round(cdata['Land Use Change Share'].iloc[-2], 1)
    other_co2_share_fy = round(cdata['Other Share'].iloc[-2], 1)

    # Generate dataframe required for treemap plot.
    emission_category = pd.DataFrame(columns=['Name', 'Value', 'Color', 'Label'])

    emission_category['Name'] = ['Fossil Fuels', 'Cement', 'Land Use Change', 'Other']

    emission_category['Value'] = [ff_co2_share_fy,
                                  cement_co2_share_fy,
                                  luc_co2_share_fy,
                                  other_co2_share_fy]

    emission_category['Color'] = [user_globals.Color.FOSSIL_FUELS.value,
                                  user_globals.Color.CEMENT.value,
                                  user_globals.Color.LUC.value,
                                  user_globals.Color.OTHER.value]

    emission_category['Label'] = fit_treemap_labels(emission_category['Name'],
                                                    emission_category['Value'], 20)

    final_coal_co2_share = round(cdata['Coal Share'].iloc[-2], 1)
    final_oil_co2_share = round(cdata['Oil Share'].iloc[-2], 1)
    final_gas_co2_share = round(cdata['Gas Share'].iloc[-2], 1)
    final_flaring_co2_share = round(cdata['Flaring Share'].iloc[-2], 1)

    # Generate dataframe required for treemap plot.
    emission = pd.DataFrame(columns=['Name', 'Value', 'Color', 'Label'])

    emission['Name'] = ['Coal',
                        'Oil',
                        'Gas',
                        'Flaring',
                        'Cement',
                        'Land Use Change',
                        'Other']

    emission['Value'] = [final_coal_co2_share,
                         final_oil_co2_share,
                         final_gas_co2_share,
                         final_flaring_co2_share,
                         cement_co2_share_fy,
                         luc_co2_share_fy,
                         other_co2_share_fy]

    emission['Color'] = [user_globals.Color.COAL.value,
                         user_globals.Color.OIL.value,
                         user_globals.Color.GAS.value,
                         user_globals.Color.FLARING.value,
                         user_globals.Color.CEMENT.value,
                         user_globals.Color.LUC.value,
                         user_globals.Color.OTHER.value]

    emission['Label'] = fit_treemap_labels(emission['Name'], emission['Value'], 5)

    # Generate dataframe required for treemap plot of country fossil fuel CO2 emissions by share.
    share_data = share_data.rename(columns={'Country': 'Name', 'Share': 'Value'})
    share_data = share_data.sort_values(by=['Value'], ascending=False)
    large_country_shares = share_data[share_data['Value'] >= user_globals.Constant.LARGE_EMITTER_SHARE_THRESHOLD.value]
    large_country_shares = large_country_shares.reset_index()
    large_country_shares = large_country_shares.drop(['index'], axis=1)
    other_country_shares = pd.DataFrame(columns=['Name', 'Value', 'Year'])
    other_country_shares['Name'] = ['Other']
    other_country_shares['Value'] = round(100 - sum(large_country_shares['Value']), 1)
    all_country_shares = pd.concat([large_country_shares, other_country_shares])
    all_country_shares = all_country_shares.sort_values(by=['Value'], ascending=False)
    all_country_shares = all_country_shares.reset_index()
    all_country_shares = all_country_shares.drop(['index'], axis=1)
    # Assign the column 'Name' to be the dataframe index.
    all_country_shares = all_country_shares.set_index('Name')

    # Assign colors.
    all_country_shares['Color'] = user_globals.Color.ALL.value
    all_country_shares.loc['China', 'Color'] = user_globals.Color.CHINA.value
    all_country_shares.loc['Other', 'Color'] = user_globals.Color.OTHER_COUNTRIES.value
    all_country_shares.loc['US', 'Color'] = user_globals.Color.US.value
    all_country_shares.loc['India', 'Color'] = user_globals.Color.INDIA.value
    all_country_shares.loc['Russian Federation', 'Color'] = user_globals.Color.RUSSIA.value
    all_country_shares.loc['Japan', 'Color'] = user_globals.Color.JAPAN.value
    all_country_shares.loc['Indonesia', 'Color'] = user_globals.Color.INDONESIA.value
    all_country_shares.loc['Iran', 'Color'] = user_globals.Color.IRAN.value
    all_country_shares.loc['Saudi Arabia', 'Color'] = user_globals.Color.SAUDI_ARABIA.value
    all_country_shares.loc['South Korea', 'Color'] = user_globals.Color.SOUTH_KOREA.value
    all_country_shares.loc['Germany', 'Color'] = user_globals.Color.GERMANY.value
    all_country_shares.loc['Canada', 'Color'] = user_globals.Color.CANADA.value
    all_country_shares.loc['Mexico', 'Color'] = user_globals.Color.MEXICO.value
    all_country_shares.loc['Brazil', 'Color'] = user_globals.Color.BRAZIL.value
    all_country_shares.loc['Turkiye', 'Color'] = user_globals.Color.TURKIYE.value
    all_country_shares.loc['South Africa', 'Color'] = user_globals.Color.SOUTH_AFRICA.value
    all_country_shares.loc['Australia', 'Color'] = user_globals.Color.AUS.value

    all_country_shares = all_country_shares.reset_index()
    # Configure treemap leaf labels. Only include country names for major emitters.
    all_country_shares['Label'] = assign_treemap_labels(all_country_shares['Name'],
                                                        round(all_country_shares['Value'], 1),
                                                        user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value)

    return emission_category, emission, all_country_shares


########################################################################################################################
#
# Function: id_major_ffco2_emitters()
#
# Description:
# Identify countries that in the most recent year of data emitted fossil fuel CO2 equal to or larger than the threshold.
#
########################################################################################################################
def id_major_ffco2_emitters(global_carbon):
    major_emitters = global_carbon.country_shares_fy[
        global_carbon.country_shares_fy['Value'] >= user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value]
    major_emitters.set_index('Name', inplace=True)
    major_emitters = major_emitters.drop('Other')

    return major_emitters.index.to_list()


########################################################################################################################
#
# Function: world_fossil_fuel_production()
#
# Description:
# Calculate shares of fossil fuel production by country, and construct dataframes for each fossil fuel suitable for
# chart.treemap1x3().
#
########################################################################################################################
def world_fossil_fuel_production(coal, oil, gas, total_coal, total_oil, total_gas):
    # Drop all rows with Country value 'Total', leaving only countries. Identify latest
    # production values, rank them, and calculate shares.
    # 1. Coal
    coal_producers = coal[~coal.Country.str.contains('Total')]
    coal_producers_fy = coal_producers.loc[
        coal_producers.index == max(coal_producers.index)
        ]
    coal_producer_shares = coal_producers_fy.copy()
    coal_producer_shares['Value'] = round(
        coal_producer_shares['Value'] / total_coal * 100, 1
    )

    coal_producer_shares = coal_producer_shares.sort_values(
        by=['Value'], ascending=False
    )
    large_coal_producers = coal_producer_shares[
        coal_producer_shares['Value']
        >= user_globals.Constant.COAL_SHARE_RANK_THRESHOLD.value
        ]
    other_coal_producers = pd.DataFrame(
        index=[max(coal_producers.index)], columns=['Country', 'Var', 'Value', 'Year']
    )
    other_coal_producers.index.name = 'Year'
    other_coal_producers['Country'] = 'Other'
    other_coal_producers['Var'] = 'coalprod_ej'
    other_coal_producers['Value'] = round(100 - sum(large_coal_producers['Value']), 1)
    all_coal_producers = pd.concat([large_coal_producers, other_coal_producers])

    # 2. Oil
    oil_producers = oil[~oil.Country.str.contains('Total')]
    oil_producers_fy = oil_producers.loc[
        oil_producers.index == max(oil_producers.index)
        ]
    oil_producer_shares = oil_producers_fy.copy()
    oil_producer_shares['Value'] = round(oil_producers_fy['Value'] / total_oil * 100, 1)
    oil_producer_shares = oil_producer_shares.sort_values(by=['Value'], ascending=False)
    large_oil_producers = oil_producer_shares[
        oil_producer_shares['Value']
        >= user_globals.Constant.OIL_SHARE_RANK_THRESHOLD.value
        ]
    other_oil_producers = pd.DataFrame(
        index=[max(oil_producers.index)], columns=['Country', 'Var', 'Value', 'Year']
    )
    other_oil_producers.index.name = 'Year'
    other_oil_producers['Country'] = 'Other'
    other_oil_producers['Var'] = 'oilprod_ej'
    other_oil_producers['Value'] = round(100 - sum(large_oil_producers['Value']), 1)
    all_oil_producers = pd.concat([large_oil_producers, other_oil_producers])

    # 3. Gas
    gas_producers = gas[~gas.Country.str.contains('Total')]
    gas_producers_fy = gas_producers.loc[
        gas_producers.index == max(gas_producers.index)
        ]
    gas_producer_shares = gas_producers_fy.copy()
    gas_producer_shares['Value'] = round(gas_producers_fy['Value'] / total_gas * 100, 1)
    gas_producer_shares = gas_producer_shares.sort_values(by=['Value'], ascending=False)
    large_gas_producers = gas_producer_shares[
        gas_producer_shares['Value']
        >= user_globals.Constant.GAS_SHARE_RANK_THRESHOLD.value
        ]
    other_gas_producers = pd.DataFrame(
        index=[max(gas_producers.index)], columns=['Country', 'Var', 'Value', 'Year']
    )
    other_gas_producers.index.name = 'Year'
    other_gas_producers['Country'] = 'Other'
    other_gas_producers['Var'] = 'gasprod_ej'
    other_gas_producers['Value'] = round(100 - sum(large_gas_producers['Value']), 1)
    all_gas_producers = pd.concat([large_gas_producers, other_gas_producers])
    all_coal_producers, all_oil_producers, all_gas_producers = (
        countries.ffprod_shorten_country(
            all_coal_producers, all_oil_producers, all_gas_producers
        )
    )

    # Generate dataframes required for treemap charts.
    coal_prod_shares = pd.DataFrame(columns=['Name', 'Value', 'Color', 'Label', 'Year'])
    oil_prod_shares = pd.DataFrame(columns=['Name', 'Value', 'Color', 'Label', 'Year'])
    gas_prod_shares = pd.DataFrame(columns=['Name', 'Value', 'Color', 'Label', 'Year'])

    coal_prod_shares['Name'] = all_coal_producers['Country'].values
    oil_prod_shares['Name'] = all_oil_producers['Country'].values
    gas_prod_shares['Name'] = all_gas_producers['Country'].values

    coal_prod_shares['Value'] = all_coal_producers['Value'].values
    oil_prod_shares['Value'] = all_oil_producers['Value'].values
    gas_prod_shares['Value'] = all_gas_producers['Value'].values

    coal_prod_shares['Color'] = user_globals.Color.COAL.value
    oil_prod_shares['Color'] = user_globals.Color.OIL.value
    gas_prod_shares['Color'] = user_globals.Color.GAS.value

    coal_prod_shares['Label'] = fit_treemap_labels(coal_prod_shares['Name'], coal_prod_shares['Value'], 1)
    oil_prod_shares['Label'] = fit_treemap_labels(oil_prod_shares['Name'], oil_prod_shares['Value'], 1)
    gas_prod_shares['Label'] = fit_treemap_labels(gas_prod_shares['Name'], gas_prod_shares['Value'], 1)
    coal_prod_shares['Year'] = max(coal.index)
    oil_prod_shares['Year'] = max(coal.index)
    gas_prod_shares['Year'] = max(coal.index)

    return coal_prod_shares, oil_prod_shares, gas_prod_shares


########################################################################################################################
#
# Function: ffco2_change()
#
# Description:
# Calculate annual change of fossil fuel CO2 emissions.
#
########################################################################################################################
def ffco2_change(df):
    min_year = min(df.index)
    max_year = max(df.index)
    change_yrs = range(min_year + 1, max_year + 1)

    for yr in change_yrs:
        df.loc[yr, 'Change'] = df.loc[yr, 'Value'] - df.loc[yr - 1, 'Value']


########################################################################################################################
#
# Function: sector_co2()
#
# Description:
# Calculates columns for plotting.
#
########################################################################################################################
def sector_co2(energy_system):
    energy_system.sector_co2_Mt['Ag, Forestry & Fishing'] = energy_system.sector_co2_Mt['Agriculture/Forestry'] + \
                                                            energy_system.sector_co2_Mt['Fishing']
    energy_system.sector_co2_Mt['Total'] = energy_system.sector_co2_Mt['Electricity & Heat Producers'] + \
                                           energy_system.sector_co2_Mt['Other Energy Producers'] + \
                                           energy_system.sector_co2_Mt['Transport'] + \
                                           energy_system.sector_co2_Mt['Manufacturing Industry'] + \
                                           energy_system.sector_co2_Mt['Commercial & Public Services'] + \
                                           energy_system.sector_co2_Mt['Residences'] + \
                                           energy_system.sector_co2_Mt['Ag, Forestry & Fishing'] + \
                                           energy_system.sector_co2_Mt['Non-specified (Other)']

    energy_system.sector_co2_Mt['Electricity & Heat Producers Share'] = round(
        energy_system.sector_co2_Mt['Electricity & Heat Producers'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Other Energy Producers Share'] = round(
        energy_system.sector_co2_Mt['Other Energy Producers'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Transport Share'] = round(
        energy_system.sector_co2_Mt['Transport'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Manufacturing Industry Share'] = round(
        energy_system.sector_co2_Mt['Manufacturing Industry'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Commercial & Public Services Share'] = round(
        energy_system.sector_co2_Mt['Commercial & Public Services'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Residential Share'] = round(
        energy_system.sector_co2_Mt['Residences'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Ag, Forestry & Fishing Share'] = round(
        energy_system.sector_co2_Mt['Ag, Forestry & Fishing'] / energy_system.sector_co2_Mt['Total'] * 100, 1)

    energy_system.sector_co2_Mt['Non-specified (Other) Share'] = round(
        energy_system.sector_co2_Mt['Non-specified (Other)'] / energy_system.sector_co2_Mt['Total'] * 100, 1)


########################################################################################################################
#
# Function: primary_energy()
#
# Description:
# Calculates primary energy annual quantities, shares, and change.
#
########################################################################################################################
def primary_energy(energy_system):
    # Calculate annual shares and changes.
    min_year = min(energy_system.primary_PJ.index)
    max_year = max(energy_system.primary_PJ.index)
    change_yrs = range(min_year + 1, max_year + 1)

    # Coal.
    if not energy_system.primary_PJ['Coal'].empty:
        energy_system.primary_PJ['Coal Share'] = (
                (energy_system.primary_PJ['Coal'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Coal Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Coal']
                    - energy_system.primary_PJ.loc[yr - 1, 'Coal']
            )
    # Oil.
    if not energy_system.primary_PJ['Oil'].empty:
        energy_system.primary_PJ['Oil Share'] = (
                (energy_system.primary_PJ['Oil'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Oil Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Oil']
                    - energy_system.primary_PJ.loc[yr - 1, 'Oil']
            )
    # Gas.
    if not energy_system.primary_PJ['Gas'].empty:
        energy_system.primary_PJ['Gas Share'] = (
                (energy_system.primary_PJ['Gas'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Gas Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Gas']
                    - energy_system.primary_PJ.loc[yr - 1, 'Gas']
            )
    # Nuclear.
    if not energy_system.primary_PJ['Nuclear'].empty:
        energy_system.primary_PJ['Nuclear Share'] = (
                (energy_system.primary_PJ['Nuclear'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Nuclear Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Nuclear']
                    - energy_system.primary_PJ.loc[yr - 1, 'Nuclear']
            )

    # Hydro.
    if not energy_system.primary_PJ['Hydro'].empty:
        energy_system.primary_PJ['Hydro Share'] = (
                (energy_system.primary_PJ['Hydro'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Hydro Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Hydro']
                    - energy_system.primary_PJ.loc[yr - 1, 'Hydro']
            )
    # Wind.
    if not energy_system.primary_PJ['Wind'].empty:
        energy_system.primary_PJ['Wind Share'] = (
                (energy_system.primary_PJ['Wind'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Wind Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Wind']
                    - energy_system.primary_PJ.loc[yr - 1, 'Wind']
            )
    # Solar.
    if not energy_system.primary_PJ['Solar'].empty:
        energy_system.primary_PJ['Solar Share'] = (
                (energy_system.primary_PJ['Solar'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Solar Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Solar']
                    - energy_system.primary_PJ.loc[yr - 1, 'Solar']
            )

    # Bio Geo and Other.
    if not energy_system.primary_PJ['Bio, Geo and Other'].empty:
        energy_system.primary_PJ['Bio, Geo and Other Share'] = (
                (energy_system.primary_PJ['Bio, Geo and Other'] / energy_system.primary_PJ['Total']) * 100)
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Bio, Geo and Other Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Bio, Geo and Other']
                    - energy_system.primary_PJ.loc[yr - 1, 'Bio, Geo and Other']
            )

    # Fossil Fuels.
    if not energy_system.primary_PJ['Fossil Fuels'].empty:
        energy_system.primary_PJ['Fossil Fuels Share'] = (energy_system.primary_PJ['Fossil Fuels'] /
                                                          energy_system.primary_PJ['Total']) * 100
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Fossil Fuels Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Fossil Fuels']
                    - energy_system.primary_PJ.loc[yr - 1, 'Fossil Fuels']
            )

    # Renewables.
    if not energy_system.primary_PJ['Renewables'].empty:
        energy_system.primary_PJ['Renewables Share'] = (energy_system.primary_PJ['Renewables'] /
                                                        energy_system.primary_PJ['Total']) * 100
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, 'Renewables Change'] = (
                    energy_system.primary_PJ.loc[yr, 'Renewables']
                    - energy_system.primary_PJ.loc[yr - 1, 'Renewables']
            )


########################################################################################################################
#
# Function: electricity()
#
# Description:
# Calculate electricity generation shares, annual change, and generate dataframes for treemap plotting of final year of
# data.
#
########################################################################################################################
def electricity(energy_system):
    if (
            energy_system.elecgen_TWh.empty
            or energy_system.elecgen_TWh['Total Country'].iloc[-1] == 0
    ):
        print('No electricity data for country in EI dataset.\n')
        return ()

    min_year = min(energy_system.elecgen_TWh.index)
    max_year = max(energy_system.elecgen_TWh.index)
    change_yrs = range(min_year + 1, max_year + 1)

    # Coal.
    if not energy_system.elecgen_TWh['Coal'].empty:
        energy_system.elecgen_TWh['Coal Share'] = (energy_system.elecgen_TWh['Coal'] /
                                                   energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Coal Change'] = (energy_system.elecgen_TWh.loc[yr, 'Coal'] -
                                                                energy_system.elecgen_TWh.loc[yr - 1, 'Coal'])
        energy_system.elecgen_PWh['Coal'] = energy_system.elecgen_TWh['Coal'] * user_globals.Constant.TWH_TO_PWH.value

    # Oil.
    if not energy_system.elecgen_TWh['Oil'].empty:
        energy_system.elecgen_TWh['Oil Share'] = (energy_system.elecgen_TWh['Oil'] /
                                                  energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Oil Change'] = (energy_system.elecgen_TWh.loc[yr, 'Oil'] -
                                                               energy_system.elecgen_TWh.loc[yr - 1, 'Oil'])
        energy_system.elecgen_PWh['Oil'] = energy_system.elecgen_TWh['Oil'] * user_globals.Constant.TWH_TO_PWH.value

    # Gas.
    if not energy_system.elecgen_TWh['Gas'].empty:
        energy_system.elecgen_TWh['Gas Share'] = (energy_system.elecgen_TWh['Gas'] /
                                                  energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Gas Change'] = (energy_system.elecgen_TWh.loc[yr, 'Gas'] -
                                                               energy_system.elecgen_TWh.loc[yr - 1, 'Gas'])
        energy_system.elecgen_PWh['Gas'] = energy_system.elecgen_TWh['Gas'] * user_globals.Constant.TWH_TO_PWH.value

    # Nuclear.
    if not energy_system.elecgen_TWh['Nuclear'].empty:
        energy_system.elecgen_TWh['Nuclear Share'] = (energy_system.elecgen_TWh['Nuclear'] /
                                                      energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Nuclear Change'] = (energy_system.elecgen_TWh.loc[yr, 'Nuclear'] -
                                                                   energy_system.elecgen_TWh.loc[yr - 1, 'Nuclear'])
        energy_system.elecgen_PWh['Nuclear'] = (energy_system.elecgen_TWh['Nuclear'] *
                                                user_globals.Constant.TWH_TO_PWH.value)

    # Hydro.
    if not energy_system.elecgen_TWh['Hydro'].empty:
        energy_system.elecgen_TWh['Hydro Share'] = ((energy_system.elecgen_TWh['Hydro'] /
                                                     energy_system.elecgen_TWh['Total Country']) * 100)
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Hydro Change'] = (energy_system.elecgen_TWh.loc[yr, 'Hydro']
                                                                 - energy_system.elecgen_TWh.loc[yr - 1, 'Hydro'])
        energy_system.elecgen_PWh['Hydro'] = energy_system.elecgen_TWh['Hydro'] * user_globals.Constant.TWH_TO_PWH.value

    # Wind.
    if not energy_system.elecgen_TWh['Wind'].empty:
        energy_system.elecgen_TWh['Wind Share'] = (energy_system.elecgen_TWh['Wind']
                                                   / energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Wind Change'] = (energy_system.elecgen_TWh.loc[yr, 'Wind']
                                                                - energy_system.elecgen_TWh.loc[yr - 1, 'Wind'])
        energy_system.elecgen_PWh['Wind'] = energy_system.elecgen_TWh['Wind'] * user_globals.Constant.TWH_TO_PWH.value

    # Solar.
    if not energy_system.elecgen_TWh['Solar'].empty:
        energy_system.elecgen_TWh['Solar Share'] = (energy_system.elecgen_TWh['Solar'] /
                                                    energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Solar Change'] = (energy_system.elecgen_TWh.loc[yr, 'Solar']
                                                                 - energy_system.elecgen_TWh.loc[yr - 1, 'Solar'])
        energy_system.elecgen_PWh['Solar'] = (energy_system.elecgen_TWh['Solar'] *
                                              user_globals.Constant.TWH_TO_PWH.value)

    # Bio Geo and Other.
    if not energy_system.elecgen_TWh['Bio, Geo and Other'].empty:
        energy_system.elecgen_TWh['Bio, Geo and Other Share'] = (energy_system.elecgen_TWh['Bio, Geo and Other'] /
                                                                 energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Bio, Geo and Other Change'] = (
                    energy_system.elecgen_TWh.loc[yr, 'Bio, Geo and Other']
                    - energy_system.elecgen_TWh.loc[yr - 1, 'Bio, Geo and Other']
            )
        energy_system.elecgen_PWh['Bio, Geo and Other'] = (energy_system.elecgen_TWh['Bio, Geo and Other'] *
                                                           user_globals.Constant.TWH_TO_PWH.value
                                                           )

    # Fossil Fuels.
    if not energy_system.elecgen_TWh['Fossil Fuels'].empty:
        energy_system.elecgen_TWh['Fossil Fuels Share'] = (energy_system.elecgen_TWh['Fossil Fuels']
                                                           / energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Fossil Fuels Change'] = (
                    energy_system.elecgen_TWh.loc[yr, 'Fossil Fuels']
                    - energy_system.elecgen_TWh.loc[yr - 1, 'Fossil Fuels'])
        energy_system.elecgen_PWh['Fossil Fuels'] = (energy_system.elecgen_TWh['Fossil Fuels'] *
                                                     user_globals.Constant.TWH_TO_PWH.value)

    # Wind and Solar.
    if not energy_system.elecgen_TWh['Wind and Solar'].empty:
        energy_system.elecgen_TWh['Wind and Solar Share'] = (energy_system.elecgen_TWh['Wind and Solar'] /
                                                             energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Wind and Solar Change'] = (
                    energy_system.elecgen_TWh.loc[yr, 'Wind and Solar']
                    - energy_system.elecgen_TWh.loc[yr - 1, 'Wind and Solar'])
        energy_system.elecgen_PWh['Wind and Solar'] = (
                energy_system.elecgen_TWh['Wind and Solar'] * user_globals.Constant.TWH_TO_PWH.value)

    # Renewables.
    if not energy_system.elecgen_TWh['Renewables'].empty:
        energy_system.elecgen_TWh['Renewables Share'] = (energy_system.elecgen_TWh['Renewables'] /
                                                         energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Renewables Change'] = (
                    energy_system.elecgen_TWh.loc[yr, 'Renewables'] -
                    energy_system.elecgen_TWh.loc[yr - 1, 'Renewables'])
        energy_system.elecgen_PWh['Renewables'] = (energy_system.elecgen_TWh['Renewables'] *
                                                   user_globals.Constant.TWH_TO_PWH.value)

    # Unpublished.
    if not energy_system.elecgen_TWh['Unpublished'].empty:
        energy_system.elecgen_TWh['Unpublished Share'] = (energy_system.elecgen_TWh['Unpublished'] /
                                                          energy_system.elecgen_TWh['Total Country']) * 100
        for yr in change_yrs:
            energy_system.elecgen_TWh.loc[yr, 'Unpublished Change'] = (
                    energy_system.elecgen_TWh.loc[yr, 'Unpublished']
                    - energy_system.elecgen_TWh.loc[yr - 1, 'Unpublished'])
        energy_system.elecgen_PWh['Unpublished'] = (energy_system.elecgen_TWh['Unpublished'] *
                                                    user_globals.Constant.TWH_TO_PWH.value)

    # Total.
    energy_system.elecgen_PWh['Total Country'] = (energy_system.elecgen_TWh['Total Country'] *
                                                  user_globals.Constant.TWH_TO_PWH.value)

    # To plot shares for final year, organise into dataframes of the prerequisite format.
    ff_elec_share_fy = energy_system.elecgen_TWh['Fossil Fuels Share'].iloc[-1]
    renewables_elec_share_fy = energy_system.elecgen_TWh['Renewables Share'].iloc[-1]
    coal_elec_share_fy = energy_system.elecgen_TWh['Coal Share'].iloc[-1]
    oil_elec_share_fy = energy_system.elecgen_TWh['Oil Share'].iloc[-1]
    gas_elec_share_fy = energy_system.elecgen_TWh['Gas Share'].iloc[-1]
    nuclear_elec_share_fy = energy_system.elecgen_TWh['Nuclear Share'].iloc[-1]
    hydro_elec_share_fy = energy_system.elecgen_TWh['Hydro Share'].iloc[-1]
    wind_solar_elec_share_fy = energy_system.elecgen_TWh['Wind and Solar Share'].iloc[-1]
    bio_geo_other_elec_share_fy = energy_system.elecgen_TWh['Bio, Geo and Other Share'].iloc[-1]
    unpublished_elec_share_fy = energy_system.elecgen_TWh['Unpublished Share'].iloc[-1]

    # Process categories.
    category_name = ['Fossil Fuels',
                     'Nuclear',
                     'Renewables',
                     'Bio, Geo and Other',
                     'Unpublished']

    category_share_fy = [ff_elec_share_fy,
                         nuclear_elec_share_fy,
                         renewables_elec_share_fy,
                         bio_geo_other_elec_share_fy,
                         unpublished_elec_share_fy]

    category_color = [user_globals.Color.FOSSIL_FUELS.value,
                      user_globals.Color.NUCLEAR.value,
                      user_globals.Color.RENEWABLES.value,
                      user_globals.Color.OTHER.value,
                      user_globals.Color.UNPUBLISHED.value]

    # Filter out shares that are NaN or < 1%. Round values for plotting.
    filtered_final_category_share = []
    filtered_category_name = []
    filtered_category_color = []
    for i in range(len(category_share_fy)):
        if not (math.isnan(category_share_fy[i]) or category_share_fy[i] < 1):
            filtered_category_name.append(category_name[i])
            filtered_final_category_share.append(round(category_share_fy[i]))
            filtered_category_color.append(category_color[i])
    # Generate dataframe required for treemap plot.
    df_category = pd.DataFrame(columns=['Name', 'Value', 'Color' 'Label'])
    df_category['Name'] = filtered_category_name
    df_category['Value'] = filtered_final_category_share
    df_category['Color'] = filtered_category_color
    df_category['Label'] = fit_treemap_labels(df_category['Name'], df_category['Value'], 20)
    # Process fuels.
    fuel_name = ['Coal',
                 'Oil',
                 'Gas',
                 'Nuclear',
                 'Hydro',
                 'Wind & Solar',
                 'Bio, Geo and Other',
                 'Unpublished']

    fuel_share_fy = [coal_elec_share_fy,
                     oil_elec_share_fy,
                     gas_elec_share_fy,
                     nuclear_elec_share_fy,
                     hydro_elec_share_fy,
                     wind_solar_elec_share_fy,
                     bio_geo_other_elec_share_fy,
                     unpublished_elec_share_fy]

    fuel_color = [user_globals.Color.COAL.value,
                  user_globals.Color.OIL.value,
                  user_globals.Color.GAS.value,
                  user_globals.Color.NUCLEAR.value,
                  user_globals.Color.HYDRO.value,
                  user_globals.Color.WIND_AND_SOLAR.value,
                  user_globals.Color.OTHER.value,
                  user_globals.Color.UNPUBLISHED.value]

    # Filter out shares that are NaN or < 1%. Round values for plotting.
    filtered_final_fuel_share = []
    filtered_fuel_name = []
    filtered_fuel_color = []
    for i in range(len(fuel_share_fy)):
        if not (math.isnan(fuel_share_fy[i]) or fuel_share_fy[i] < 1):
            filtered_fuel_name.append(fuel_name[i])
            filtered_final_fuel_share.append(round(fuel_share_fy[i]))
            filtered_fuel_color.append(fuel_color[i])
    # Generate dataframe required for treemap plot.
    df_fuel = pd.DataFrame(columns=['Name', 'Value', 'Color' 'Label'])
    df_fuel['Name'] = filtered_fuel_name
    df_fuel['Value'] = filtered_final_fuel_share
    df_fuel['Color'] = filtered_fuel_color
    df_fuel['Label'] = fit_treemap_labels(df_fuel['Name'], df_fuel['Value'], 5)

    # Store resulting dataframes in energy_system_object.
    energy_system.elecgen_category_fy_shares = df_category
    energy_system.elecgen_fuel_fy_shares = df_fuel


########################################################################################################################
#
# Function: final_energy()
#
# Description:
# Calculates final energy annual shares and change, and generates dataframe for treemap plotting of final year data.
#
########################################################################################################################
def final_energy(energy_system):
    energy_system.finalenergy_PJ['Oil'] = (energy_system.finalenergy_PJ['Crude oil'] +
                                           energy_system.finalenergy_PJ['Oil products'])
    energy_system.finalenergy_PJ.drop(columns=['Crude oil', 'Oil products'], inplace=True)

    energy_system.finalenergy_PJ['Total'] = energy_system.finalenergy_PJ.sum(axis=1)

    energy_system.finalenergy_PJ['Coal Share'] = (energy_system.finalenergy_PJ['Coal']
                                                  / energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Oil Share'] = (energy_system.finalenergy_PJ['Oil'] /
                                                 energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Gas Share'] = (energy_system.finalenergy_PJ['Gas'] /
                                                 energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Wind Solar Etc Share'] = (energy_system.finalenergy_PJ['Wind Solar Etc'] /
                                                            energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Biofuels and Waste Share'] = (energy_system.finalenergy_PJ['Biofuels and Waste'] /
                                                                energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Electricity Share'] = (energy_system.finalenergy_PJ['Electricity'] /
                                                         energy_system.finalenergy_PJ['Total'] * 100)

    energy_system.finalenergy_PJ['Heat Share'] = (energy_system.finalenergy_PJ['Heat'] /
                                                  energy_system.finalenergy_PJ['Total'] * 100)

    print('\nMost recent year Total Energy Consumption (IEA) = ' +
          str(int(energy_system.finalenergy_PJ['Total'].iloc[-1])) + 'PJ\n')

    change_yrs = range(user_globals.Constant.TFC_START_YEAR.value + 1, user_globals.Constant.TFC_END_YEAR.value + 1)

    for yr in change_yrs:
        energy_system.finalenergy_PJ.loc[yr, 'Coal Change'] = (energy_system.finalenergy_PJ.loc[yr, 'Coal'] -
                                                               energy_system.finalenergy_PJ.loc[yr - 1, 'Coal'])

        energy_system.finalenergy_PJ.loc[yr, 'Oil Change'] = (energy_system.finalenergy_PJ.loc[yr, 'Oil'] -
                                                              energy_system.finalenergy_PJ.loc[yr - 1, 'Oil'])

        energy_system.finalenergy_PJ.loc[yr, 'Gas Change'] = (energy_system.finalenergy_PJ.loc[yr, 'Gas'] -
                                                              energy_system.finalenergy_PJ.loc[yr - 1, 'Gas'])

        energy_system.finalenergy_PJ.loc[yr, 'Wind Solar Etc Change'] = (
                energy_system.finalenergy_PJ.loc[yr, 'Wind Solar Etc']
                - energy_system.finalenergy_PJ.loc[yr - 1, 'Wind Solar Etc'])

        energy_system.finalenergy_PJ.loc[yr, 'Biofuels and Waste Change'] = (
                energy_system.finalenergy_PJ.loc[yr, 'Biofuels and Waste']
                - energy_system.finalenergy_PJ.loc[yr - 1, 'Biofuels and Waste'])

        energy_system.finalenergy_PJ.loc[yr, 'Electricity Change'] = (
                energy_system.finalenergy_PJ.loc[yr, 'Electricity']
                - energy_system.finalenergy_PJ.loc[yr - 1, 'Electricity'])

        energy_system.finalenergy_PJ.loc[yr, 'Heat Change'] = (energy_system.finalenergy_PJ.loc[yr, 'Heat'] -
                                                               energy_system.finalenergy_PJ.loc[yr - 1, 'Heat'])

    # To plot shares for final year, organise into dataframes of the prerequisite format.
    coal_finalenergy_share_fy = energy_system.finalenergy_PJ['Coal Share'].iloc[-1]
    oil_finalenergy_share_fy = energy_system.finalenergy_PJ['Oil Share'].iloc[-1]
    gas_finalenergy_share_fy = energy_system.finalenergy_PJ['Gas Share'].iloc[-1]
    wse_finalenergy_share_fy = energy_system.finalenergy_PJ['Wind Solar Etc Share'].iloc[-1]
    bio_waste_finalenergy_share_fy = energy_system.finalenergy_PJ['Biofuels and Waste Share'].iloc[-1]
    elec_finalenergy_share_fy = energy_system.finalenergy_PJ['Electricity Share'].iloc[-1]
    heat_finalenergy_share_fy = energy_system.finalenergy_PJ['Heat Share'].iloc[-1]

    name = ['Coal',
            'Oil',
            'Gas',
            'Wind Solar Etc',
            'Biofuels & Waste',
            'Electricity',
            'Heat']

    share_fy = [coal_finalenergy_share_fy,
                oil_finalenergy_share_fy,
                gas_finalenergy_share_fy,
                wse_finalenergy_share_fy,
                bio_waste_finalenergy_share_fy,
                elec_finalenergy_share_fy,
                heat_finalenergy_share_fy
                ]

    color = [user_globals.Color.COAL.value,
             user_globals.Color.OIL.value,
             user_globals.Color.GAS.value,
             user_globals.Color.WIND_AND_SOLAR.value,
             user_globals.Color.BIOFUELS_AND_WASTE.value,
             user_globals.Color.ELECTRICITY.value,
             user_globals.Color.HEAT.value]

    # Filter out shares that are NaN or < 1%.
    filtered_share = []
    filtered_name = []
    filtered_color = []
    for i in range(len(share_fy)):
        if not (math.isnan(share_fy[i]) or share_fy[i] < 1):
            filtered_name.append(name[i])
            filtered_share.append(round(share_fy[i]))
            filtered_color.append(color[i])
    # Generate dataframe required for treemap plot.
    df = pd.DataFrame(columns=['Name', 'Value', 'Color' 'Label'])
    df['Name'] = filtered_name
    df['Value'] = filtered_share
    df['Color'] = filtered_color
    df['Label'] = fit_treemap_labels(df['Name'], df['Value'], 20)
    energy_system.finalenergy_fy_shares = df


########################################################################################################################
#
# Function: assign_treemap_labels()
#
# Description:
# Assigns full treemap labels to shares above the input argument 'threshold'.
#
########################################################################################################################
def assign_treemap_labels(names, values, threshold):
    labels = []
    for i in range(len(values)):
        if values[i] < threshold:
            labels.append(str(values[i]) + '%')
        else:
            labels.append(names[i] + '\n' + str(values[i]) + '%')
    return labels


########################################################################################################################
#
# Function: fit_treemap_labels()
#
# Description:
# Configure and fit treemap labels as appropriate. Large ratios of values can cause narrow treemap leafs, in which case
# this function will remove the name from the label, and only include the value, if the ratio of values exceeds the
# input argument 'ratio_threshold'.
#
########################################################################################################################
def fit_treemap_labels(names, values, ratio_threshold):
    labels = []
    if (max(values) / min(values)) >= ratio_threshold:
        for i in range(len(values)):
            if values[i] < ratio_threshold:
                labels.append(str(values[i]) + '%')
            else:
                labels.append(names[i] + '\n' + str(values[i]) + '%')
    else:
        for i in range(len(values)):
            labels.append(names[i] + '\n' + str(values[i]) + '%')
    return labels
