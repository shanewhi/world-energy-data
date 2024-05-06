#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""


###############################################################################
#
# Module: process.py
#
# Description:
# Performs processing of collated data, such as calcuating shares and changes.
#
###############################################################################


# Import Python modules.
import math
import pandas as pd


# Import user modules.
import user_globals


###############################################################################
#
# Function: primary_energy()
#
# Description:
# Calculate primary energy annual quantities, shares, and annual additions and
# subtractions.
#
###############################################################################
def primary_energy(energy_system):

    # Calculate shares and changes.
    min_year = min(energy_system.primary_PJ.index)
    max_year = max(energy_system.primary_PJ.index)
    change_yrs = range(min_year + 1, max_year + 1)

    # Coal.
    if not energy_system.primary_PJ["Coal"].empty:
        energy_system.primary_PJ["Coal Share"] = \
            (energy_system.primary_PJ["Coal"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Coal Change"] = \
                    energy_system.primary_PJ.loc[yr, "Coal"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Coal"]
    # Oil.
    if not energy_system.primary_PJ["Oil"].empty:
        energy_system.primary_PJ["Oil Share"] = \
            (energy_system.primary_PJ["Oil"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Oil Change"] = \
                    energy_system.primary_PJ.loc[yr, "Oil"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Oil"]
    # Gas.
    if not energy_system.primary_PJ["Gas"].empty:
        energy_system.primary_PJ["Gas Share"] = \
            (energy_system.primary_PJ["Gas"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Gas Change"] = \
                    energy_system.primary_PJ.loc[yr, "Gas"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Gas"]
    # Nuclear.
    if not energy_system.primary_PJ["Nuclear"].empty:
        energy_system.primary_PJ["Nuclear Share"] = \
            (energy_system.primary_PJ["Nuclear"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Nuclear Change"] = \
                    energy_system.primary_PJ.loc[yr, "Nuclear"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Nuclear"]

    # Hydro.
    if not energy_system.primary_PJ["Hydro"].empty:
        energy_system.primary_PJ["Hydro Share"] = \
            (energy_system.primary_PJ["Hydro"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Hydro Change"] = \
                    energy_system.primary_PJ.loc[yr, "Hydro"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Hydro"]
   # Wind.
    if not energy_system.primary_PJ["Wind"].empty:
        energy_system.primary_PJ["Wind Share"] = \
            (energy_system.primary_PJ["Wind"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Wind Change"] = \
                    energy_system.primary_PJ.loc[yr, "Wind"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Wind"]
    # Solar.
    if not energy_system.primary_PJ["Solar"].empty:
        energy_system.primary_PJ["Solar Share"] = \
            (energy_system.primary_PJ["Solar"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Solar Change"] = \
                    energy_system.primary_PJ.loc[yr, "Solar"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Solar"]

    # Bio Geo and Other.
    if not energy_system.primary_PJ["Bio Geo and Other"].empty:
        energy_system.primary_PJ["Bio Geo and Other Share"] = \
            (energy_system.primary_PJ["Bio Geo and Other"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
            energy_system.primary_PJ.loc[yr, "Bio Geo and Other Change"] = \
                energy_system.primary_PJ.loc[yr, "Bio Geo and Other"] - \
                energy_system.primary_PJ.loc[yr - 1, "Bio Geo and Other"]

    # Fossil Fuels.
    if not energy_system.primary_PJ["Fossil Fuels"].empty:
        energy_system.primary_PJ["Fossil Fuels Share"] = \
            (energy_system.primary_PJ["Fossil Fuels"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Fossil Fuels Change"] = \
                    energy_system.primary_PJ.loc[yr, "Fossil Fuels"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Fossil Fuels"]

    # Renewables.
    if not energy_system.primary_PJ["Renewables"].empty:
        energy_system.primary_PJ["Renewables Share"] = \
            (energy_system.primary_PJ["Renewables"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Renewables Change"] = \
                    energy_system.primary_PJ.loc[yr, "Renewables"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Renewables"]

    print("Sum of Primary Energy shares: \n",
        energy_system.primary_PJ["Coal Share"] + \
        energy_system.primary_PJ["Oil Share"] + \
        energy_system.primary_PJ["Gas Share"] + \
        energy_system.primary_PJ["Nuclear Share"] + \
        energy_system.primary_PJ["Hydro Share"] + \
        energy_system.primary_PJ["Wind Share"] + \
        energy_system.primary_PJ["Solar Share"] + \
        energy_system.primary_PJ["Bio Geo and Other Share"])

    # To enable plotting of shares for most recent year, organise into
    # dataframes.
    final_ff_primary_share = \
        energy_system.primary_PJ["Fossil Fuels Share"].iloc[-1]
    final_renewables_primary_share = \
        energy_system.primary_PJ["Renewables Share"].iloc[-1]
    final_coal_primary_share = \
        energy_system.primary_PJ["Coal Share"].iloc[-1]
    final_oil_primary_share = \
        energy_system.primary_PJ["Oil Share"].iloc[-1]
    final_gas_primary_share = \
        energy_system.primary_PJ["Gas Share"].iloc[-1]
    final_nuclear_primary_share = \
        energy_system.primary_PJ["Nuclear Share"].iloc[-1]
    final_hydro_primary_share = \
        energy_system.primary_PJ["Hydro Share"].iloc[-1]
    final_wind_primary_share = \
        energy_system.primary_PJ["Wind Share"].iloc[-1]
    final_solar_primary_share = \
        energy_system.primary_PJ["Solar Share"].iloc[-1]
    final_bio_geo_other_primary_share = \
        energy_system.primary_PJ["Bio Geo and Other Share"].iloc[-1]

    category_name = [
        "Fossil Fuels",
        "Nuclear",
        "Renewables",
        "Bio Geo and Other"
        ]
    fuel_name = [
        "Coal",
        "Oil",
        "Gas",
        "Nuclear",
        "Hydro",
        "Wind",
        "Solar",
        "Bio Geo and Other"
        ]
    final_category_share = [
        final_ff_primary_share,
        final_nuclear_primary_share,
        final_renewables_primary_share,
        final_bio_geo_other_primary_share
        ]
    final_fuel_share = [
        final_coal_primary_share,
        final_oil_primary_share,
        final_gas_primary_share,
        final_nuclear_primary_share,
        final_hydro_primary_share,
        final_wind_primary_share,
        final_solar_primary_share,
        final_bio_geo_other_primary_share
        ]
    category_color = [
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEWABLES.value,
        user_globals.Color.OTHER.value
        ]
    fuel_color = [
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND.value,
        user_globals.Color.SOLAR.value,
        user_globals.Color.OTHER.value
        ]

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
            filtered_final_fuel_share.append(int(round(final_fuel_share[i],
                                                       0)))
            filtered_fuel_color.append(fuel_color[i])

    df_category = pd.DataFrame(columns = [
        "Name",
        "Value",
        "Color"
        "Label"])
    df_category["Name"] = filtered_category_name
    df_category["Value"] = filtered_final_category_share
    df_category["Color"] = filtered_category_color

    df_fuel = pd.DataFrame(columns = [
        "Name",
        "Value",
        "Color"
        "Label"])
    df_fuel["Name"] = filtered_fuel_name
    df_fuel["Value"] = filtered_final_fuel_share
    df_fuel["Color"] = filtered_fuel_color

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_category["Value"].max() / df_category["Value"].min()) >= 20:
        df_category.loc[df_category["Value"] < 20, ["Label"]] = \
            df_category["Value"].astype(str) + "%"
        df_category.loc[df_category["Value"] >= 20, ["Label"]] = \
            df_category["Name"].astype(str) + " " + \
            df_category["Value"].astype(str) + "%"
    else:
        df_category["Label"] = \
            df_category["Name"].astype(str) + " " + \
            df_category["Value"].astype(str) + "%"

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_fuel["Value"].max() / df_fuel["Value"].min()) >= 5:
        df_fuel.loc[df_fuel["Value"] < 5, ["Label"]] = \
            df_fuel["Value"].astype(str) + "%"
        df_fuel.loc[df_fuel["Value"] >= 5, ["Label"]] = \
            df_fuel["Name"].astype(str) + " " + \
            df_fuel["Value"].astype(str) + "%"
    else:
        df_fuel["Label"] = \
            df_fuel["Name"].astype(str) + " " + \
            df_fuel["Value"].astype(str) + "%"

    energy_system.primary_category_shares = df_category
    energy_system.primary_fuel_shares = df_fuel


###############################################################################
#
# Function: electricity()
#
# Description:
# Calculate electricity production shares, and annual change.
#
###############################################################################
def electricity(energy_system):
    if energy_system.elecprod_TWh.empty:
        print("No electricity data.\n")
        return()
    
    min_year = min(energy_system.elecprod_TWh.index)
    max_year = max(energy_system.elecprod_TWh.index)
    change_yrs = range(min_year + 1, max_year + 1)

    # Coal.
    if not energy_system.elecprod_TWh["Coal"].empty:
        energy_system.elecprod_TWh["Coal Share"] = \
            (energy_system.elecprod_TWh["Coal"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Coal Change"] = \
                    (energy_system.elecprod_TWh.loc[yr, "Coal"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Coal"])

    # Oil.
    if not energy_system.elecprod_TWh["Oil"].empty:
        energy_system.elecprod_TWh["Oil Share"] = \
            (energy_system.elecprod_TWh["Oil"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Oil Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Oil"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Oil"]

    # Gas.
    if not energy_system.elecprod_TWh["Gas"].empty:
        energy_system.elecprod_TWh["Gas Share"] = \
            (energy_system.elecprod_TWh["Gas"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Gas Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Gas"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Gas"]

    # Nuclear.
    if not energy_system.elecprod_TWh["Nuclear"].empty:
        energy_system.elecprod_TWh["Nuclear Share"] = \
            (energy_system.elecprod_TWh["Nuclear"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Nuclear Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Nuclear"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Nuclear"]


    # Hydro.
    if not energy_system.elecprod_TWh["Hydro"].empty:
        energy_system.elecprod_TWh["Hydro Share"] = \
            (energy_system.elecprod_TWh["Hydro"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Hydro Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Hydro"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Hydro"]

    # Wind.
    if not energy_system.elecprod_TWh["Wind"].empty:
        energy_system.elecprod_TWh["Wind Share"] = \
            (energy_system.elecprod_TWh["Wind"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Wind Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Wind"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Wind"]

    # Solar.
    if not energy_system.elecprod_TWh["Solar"].empty:
        energy_system.elecprod_TWh["Solar Share"] = \
            (energy_system.elecprod_TWh["Solar"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Solar Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Solar"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Solar"]

    # Bio Geo and Other.
    if not energy_system.elecprod_TWh["Bio Geo and Other"].empty:
        energy_system.elecprod_TWh["Bio Geo and Other Share"] = \
            (energy_system.elecprod_TWh["Bio Geo and Other"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
            energy_system.elecprod_TWh.loc[yr, "Bio Geo and Other Change"] = \
                energy_system.elecprod_TWh.loc[yr, "Bio Geo and Other"] - \
                energy_system.elecprod_TWh.loc[yr - 1, "Bio Geo and Other"]

    # Fossil Fuels.
    if not energy_system.elecprod_TWh["Fossil Fuels"].empty:
        energy_system.elecprod_TWh["Fossil Fuels Share"] = \
            (energy_system.elecprod_TWh["Fossil Fuels"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Fossil Fuels Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Fossil Fuels"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Fossil Fuels"]

    # Wind and Solar.
    if not energy_system.elecprod_TWh["Wind and Solar"].empty:
        energy_system.elecprod_TWh["Wind and Solar Share"] = \
            (energy_system.elecprod_TWh["Wind and Solar"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Wind and Solar Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Wind and Solar"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Wind and Solar"]

    # Renewables.
    if not energy_system.elecprod_TWh["Renewables"].empty:
        energy_system.elecprod_TWh["Renewables Share"] = \
            (energy_system.elecprod_TWh["Renewables"] /
            energy_system.elecprod_TWh["Total"]) * 100
        for yr in change_yrs:
                energy_system.elecprod_TWh.loc[yr, "Renewables Change"] = \
                    energy_system.elecprod_TWh.loc[yr, "Renewables"] - \
                    energy_system.elecprod_TWh.loc[yr - 1, "Renewables"]

    print("Sum of Electricity shares: \n",
        energy_system.elecprod_TWh["Coal Share"] + \
        energy_system.elecprod_TWh["Oil Share"] + \
        energy_system.elecprod_TWh["Gas Share"] + \
        energy_system.elecprod_TWh["Nuclear Share"] + \
        energy_system.elecprod_TWh["Hydro Share"] + \
        energy_system.elecprod_TWh["Wind Share"] + \
        energy_system.elecprod_TWh["Solar Share"] + \
        energy_system.elecprod_TWh["Bio Geo and Other Share"])

    # To enable plotting of shares for most recent year, organise into
    # dataframes.
    final_ff_elec_share = \
        energy_system.elecprod_TWh["Fossil Fuels Share"].iloc[-1]
    final_renewables_elec_share = \
        energy_system.elecprod_TWh["Renewables Share"].iloc[-1]
    final_coal_elec_share = \
        energy_system.elecprod_TWh["Coal Share"].iloc[-1]
    final_oil_elec_share = \
        energy_system.elecprod_TWh["Oil Share"].iloc[-1]
    final_gas_elec_share = \
        energy_system.elecprod_TWh["Gas Share"].iloc[-1]
    final_nuclear_elec_share = \
        energy_system.elecprod_TWh["Nuclear Share"].iloc[-1]
    final_hydro_elec_share = \
        energy_system.elecprod_TWh["Hydro Share"].iloc[-1]
    final_wind_solar_elec_share = \
        energy_system.elecprod_TWh["Wind and Solar Share"].iloc[-1]
    final_bio_geo_other_elec_share = \
        energy_system.elecprod_TWh["Bio Geo and Other Share"].iloc[-1]

    category_name = [
        "Fossil Fuels",
        "Nuclear",
        "Renewables",
        "Bio Geo and Other"
        ]
    fuel_name = [
        "Coal",
        "Oil",
        "Gas",
        "Nuclear",
        "Hydro",
        "Wind & Solar",
        "Bio Geo and Other"
        ]
    final_category_share = [
        final_ff_elec_share,
        final_nuclear_elec_share,
        final_renewables_elec_share,
        final_bio_geo_other_elec_share
        ]
    final_fuel_share = [
        final_coal_elec_share,
        final_oil_elec_share,
        final_gas_elec_share,
        final_nuclear_elec_share,
        final_hydro_elec_share,
        final_wind_solar_elec_share,
        final_bio_geo_other_elec_share
        ]
    category_color = [
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEWABLES.value,
        user_globals.Color.OTHER.value
        ]
    fuel_color = [
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_AND_SOLAR.value,
        user_globals.Color.OTHER.value
        ]

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
            filtered_final_fuel_share.append(int(round(final_fuel_share[i],
                                                       0)))
            filtered_fuel_color.append(fuel_color[i])

    df_category = pd.DataFrame(columns = [
        "Name",
        "Value",
        "Color"
        "Label"]
        )
    df_category["Name"] = filtered_category_name
    df_category["Value"] = filtered_final_category_share
    df_category["Color"] = filtered_category_color

    df_fuel = pd.DataFrame(columns = [
        "Name",
        "Value",
        "Color"
        "Label"]
        )
    df_fuel["Name"] = filtered_fuel_name
    df_fuel["Value"] = filtered_final_fuel_share
    df_fuel["Color"] = filtered_fuel_color

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_category["Value"].max() / df_category["Value"].min()) >= 20:
        df_category.loc[df_category["Value"] < 20, ["Label"]] = \
            df_category["Value"].astype(str) + "%"
        df_category.loc[df_category["Value"] >= 20, ["Label"]] = \
            df_category["Name"].astype(str) + " " + \
            df_category["Value"].astype(str) + "%"
    else:
        df_category["Label"] = \
            df_category["Name"].astype(str) + " " + \
            df_category["Value"].astype(str) + "%"

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df_fuel["Value"].max() / df_fuel["Value"].min()) >= 5:
        df_fuel.loc[df_fuel["Value"] < 5, ["Label"]] = \
            df_fuel["Value"].astype(str) + "%"
        df_fuel.loc[df_fuel["Value"] >= 5, ["Label"]] = \
            df_fuel["Name"].astype(str) + " " + \
            df_fuel["Value"].astype(str) + "%"
    else:
        df_fuel["Label"] = \
            df_fuel["Name"].astype(str) + " " + \
            df_fuel["Value"].astype(str) + "%"

    energy_system.elecprod_final_category_shares = df_category
    energy_system.elecprod_final_fuel_shares = df_fuel


###############################################################################
#
# Function: consumption()
#
# Description:
# Calculates TFC fuel shares and annual change.
#
###############################################################################
def consumption(energy_system):
    energy_system.consumption_PJ["Coal Share"] = \
        energy_system.consumption_PJ["Coal"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Oil Share"] = \
        energy_system.consumption_PJ["Oil"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Gas Share"] = \
        energy_system.consumption_PJ["Gas"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Wind Solar Etc Share"] = \
        energy_system.consumption_PJ["Wind Solar Etc"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Biofuels and Waste Share"] = \
        energy_system.consumption_PJ["Biofuels and Waste"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Electricity Share"] = \
        energy_system.consumption_PJ["Electricity"] / \
        energy_system.consumption_PJ["Total"] * 100
    energy_system.consumption_PJ["Heat Share"] = \
        energy_system.consumption_PJ["Heat"] / \
        energy_system.consumption_PJ["Total"] * 100
    print("Total Final Energy Shares:\n",
          energy_system.consumption_PJ["Coal Share"] +
          energy_system.consumption_PJ["Oil Share"] +
          energy_system.consumption_PJ["Gas Share"] +
          energy_system.consumption_PJ["Wind Solar Etc Share"] +
          energy_system.consumption_PJ["Biofuels and Waste Share"] +
          energy_system.consumption_PJ["Electricity Share"] +
          energy_system.consumption_PJ["Heat Share"])

    change_yrs = range(user_globals.Constant.TFC_START_YEAR.value + 1,
                       user_globals.Constant.TFC_END_YEAR.value + 1)

    for yr in change_yrs:
        energy_system.consumption_PJ.loc[yr, "Coal Change"] = \
            energy_system.consumption_PJ.loc[yr, "Coal"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Coal"]
        energy_system.consumption_PJ.loc[yr, "Oil Change"] = \
            energy_system.consumption_PJ.loc[yr, "Oil"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Oil"]
        energy_system.consumption_PJ.loc[yr, "Gas Change"] = \
            energy_system.consumption_PJ.loc[yr, "Gas"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Gas"]
        energy_system.consumption_PJ.loc[yr, "Wind Solar Etc Change"] = \
            energy_system.consumption_PJ.loc[yr, "Wind Solar Etc"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Wind Solar Etc"]
        energy_system.consumption_PJ.loc[yr, "Biofuels and Waste Change"] = \
            energy_system.consumption_PJ.loc[yr, "Biofuels and Waste"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Biofuels and Waste"]
        energy_system.consumption_PJ.loc[yr, "Electricity Change"] = \
            energy_system.consumption_PJ.loc[yr, "Electricity"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Electricity"]
        energy_system.consumption_PJ.loc[yr, "Heat Change"] = \
            energy_system.consumption_PJ.loc[yr, "Heat"] - \
            energy_system.consumption_PJ.loc[yr - 1, "Heat"]

   # To enable plotting of shares for most recent year, organise into
   # dataframes.

    final_coal_consumption_share = \
        energy_system.consumption_PJ["Coal Share"].iloc[-1]
    final_oil_consumption_share = \
        energy_system.consumption_PJ["Oil Share"].iloc[-1]
    final_gas_consumption_share = \
        energy_system.consumption_PJ["Gas Share"].iloc[-1]
    final_wse_consumption_share = \
        energy_system.consumption_PJ["Wind Solar Etc Share"].iloc[-1]
    final_bio_waste_consumption_share = \
        energy_system.consumption_PJ["Biofuels and Waste Share"].iloc[-1]
    final_elec_consumption_share = \
        energy_system.consumption_PJ["Electricity Share"].iloc[-1]
    final_heat_consumption_share = \
        energy_system.consumption_PJ["Heat Share"].iloc[-1]

    name = [
        "Coal",
        "Oil",
        "Gas",
        "Wind Solar Etc Share",
        "Biofuels & Waste",
        "Electricity",
        "Heat"
        ]
    final_share = [
        final_coal_consumption_share,
        final_oil_consumption_share,
        final_gas_consumption_share,
        final_wse_consumption_share,
        final_bio_waste_consumption_share,
        final_elec_consumption_share,
        final_heat_consumption_share
        ]
    color = [
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.WIND_AND_SOLAR.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value
        ]
    
    # Filter out shares that are NaN or < 1%.
    filtered_share = []
    filtered_name = []
    filtered_color = []
    for i in range(len(final_share)):
        if not (math.isnan(final_share[i]) or final_share[i] < 1):
            filtered_name.append(name[i])
            filtered_share.append(int(round(final_share[i], 0)))
            filtered_color.append(color[i])
    
    df = pd.DataFrame(columns = [
        "Name",
        "Value",
        "Color"
        "Label"]
        )
    df["Name"] = filtered_name
    df["Value"] = filtered_share
    df["Color"] = filtered_color

    # Configure labels to suit narrow treemap leafs caused by large ratios
    # of data Values.
    if (df["Value"].max() / df["Value"].min()) >= 20:
        df.loc[df["Value"] < 20, ["Label"]] = \
            df["Value"].astype(str) + "%"
        df.loc[df["Value"] >= 20, ["Label"]] = \
            df["Name"].astype(str) + " " + \
            df["Value"].astype(str) + "%"
    else:
        df["Label"] = \
            df["Name"].astype(str) + " " + \
            df["Value"].astype(str) + "%"

    energy_system.consumption_final_shares = df
