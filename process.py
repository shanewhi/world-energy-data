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


###############################################################################
#
# Function: co2_emissions()
#
# Description:
# Plot natonal co2 emissions.
#
# Input(s): Instance of user class energy_system.
# Output(s): Single figure x-y chart of national annual CO2 emissions from
# fossil fuel combustion.
#
###############################################################################
def co2_emissions(energy_system):
    chart.line_plot(
        energy_system.co2_combust_Mt.index,
        energy_system.co2_combust_Mt,
        energy_system.name.upper(),
        user_globals.Color.CO2.value,
        "Fossil Fuel Carbon Dioxide Emissions",
        "Annual Emissions (MtCO\u2082)",
        "")
    plt.show()


###############################################################################
#
# Function: production()
#
# Description:
# Plot national fossil fuel production.
#
# Input(s): Instance of user class energy_system.
# Output(s): Single figure of 1x3 subplots, showing annual quantity of national
# coal, oil and gas production.
#
###############################################################################
def production(energy_system):
    chart.column_subplot(
        energy_system.coalprod_Mt,
        energy_system.oilprod_Mbpd,
        energy_system.gasprod_bcm,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        energy_system.name.upper(),
        "Fossil Fuel Production",
        "Coal",
        "Oil",
        "Gas",
        "Annual Production (Mt)",
        "Annual Production (Mbpd)",
        "Annual Production (bcm)",
        "")
    plt.show()


###############################################################################
#
# Function: primary_energy()
#
# Description:
# Plot primary energy annual quantities, shares, and annual additions and
# subtractions.
#
# Input(s): Instance of user class energy_system.
# Output(s):
# 1. Figure of 1x3 subplots with equivalent scales, showing annual primary
# energy of fossil fuels.
# 2. Figure of 2x3 subplots showing annual shares of primary energy of each
# fuel.
# 3. Figure of 1x2 treemaps showing primary energy shares for categories and
# fuels in the most recent year of EI's dataset.
# 4. Single figure of grouped columns showing annual addition and subtractions
# to and from primary energy of categories.
# 5. Single figure of grouped columns showing annual addition and subtractions
# to and from primary energy of fuels.
#
###############################################################################
def primary_energy(energy_system):
    if energy_system.name == "World":
        unit = "(EJ)"
    else:
        unit = "(PJ)"

    ###########################################################################
    # Absolute quantity of fossi fuel primary energy.
    ###########################################################################
    chart.column_subplot_equiv_units(
        energy_system.primary_PJ["Coal"],
        energy_system.primary_PJ["Oil"],
        energy_system.primary_PJ["Gas"],
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        energy_system.name.upper(),
        "Fossil Fuels in Energy Supply (Primary Energy)",
        "Coal",
        "Oil",
        "Gas",
        "Annual Primary Energy " + unit,
        "")
    plt.show()

    ###########################################################################
    # Primary energy shares.
    ###########################################################################
    min_year = min(energy_system.primary_PJ.index)
    max_year = max(energy_system.primary_PJ.index)
    change_yrs = range(min_year + 1, max_year + 1)

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
    # Bio Geo.
    if not energy_system.primary_PJ["Bio Geo"].empty:
        energy_system.primary_PJ["Bio Geo Share"] = \
            (energy_system.primary_PJ["Bio Geo"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Bio Geo Change"] = \
                    energy_system.primary_PJ.loc[yr, "Bio Geo"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Bio Geo"]

    # Wind and Solar.
    if not energy_system.primary_PJ["Wind and Solar"].empty:
        energy_system.primary_PJ["Wind and Solar Share"] = \
            (energy_system.primary_PJ["Wind and Solar"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Wind and Solar Change"] = \
                    energy_system.primary_PJ.loc[yr, "Wind and Solar"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Wind and Solar"]
    # Fossil Fuels.
    if not energy_system.primary_PJ["Fossil Fuels"].empty:
        energy_system.primary_PJ["Fossil Fuels Share"] = \
            (energy_system.primary_PJ["Fossil Fuels"] /
            energy_system.primary_PJ["Total"]) * 100
        for yr in change_yrs:
                energy_system.primary_PJ.loc[yr, "Fossil Fuels Change"] = \
                    energy_system.primary_PJ.loc[yr, "Fossil Fuels"] - \
                    energy_system.primary_PJ.loc[yr - 1, "Fossil Fuels"]

    print("Sum of Primary Energy shares: \n",
        energy_system.primary_PJ["Coal Share"] + \
        energy_system.primary_PJ["Oil Share"] + \
        energy_system.primary_PJ["Gas Share"] + \
        energy_system.primary_PJ["Nuclear Share"] + \
        energy_system.primary_PJ["Hydro Share"] + \
        energy_system.primary_PJ["Wind Share"] + \
        energy_system.primary_PJ["Solar Share"] + \
        energy_system.primary_PJ["Bio Geo Share"])

    # Chart title.
    title = (energy_system.name.upper())
    title_addition = ""
    if energy_system.name == "World":
        title_addition =\
            "Share of Fuels in World Energy Supply (Primary Energy)"
    else:
        title_addition =\
            "Share of Fuels in National Energy Supply (Primary Energy)"

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Wind + Solar"

    # Additional text.
    ylabel = ("Annual Share of Primary Energy (%)")
    footer_text = "Shares of geothermal, biofuels and 'other' are small and \
omitted for clarity."

    #Plot
    chart.line_subplot(energy_system.primary_PJ["Coal Share"],
                       energy_system.primary_PJ["Oil Share"],
                       energy_system.primary_PJ["Gas Share"],
                       energy_system.primary_PJ["Nuclear Share"],
                       energy_system.primary_PJ["Hydro Share"],
                       energy_system.primary_PJ["Wind and Solar Share"],                       user_globals.Color.COAL.value,
                       user_globals.Color.OIL.value,
                       user_globals.Color.GAS.value,
                       user_globals.Color.NUCLEAR.value,
                       user_globals.Color.HYDRO.value,
                       user_globals.Color.WIND_SOLAR.value,
                       title, title_addition, title1, title2, title3,
                       title4, title5, title6, ylabel, footer_text)
    plt.show()

    ###########################################################################
    # Primary energy shares for most recent year using treemaps.
    ###########################################################################
    # Organise data for most recent year into dataframes labelled df_category
    # and df_fuel.
    final_ff_primary_share = \
        energy_system.primary_PJ["Fossil Fuels Share"].iloc[-1]
    final_ws_primary_share = \
        energy_system.primary_PJ["Wind and Solar Share"].iloc[-1]
    final_hydro_primary_share = \
        energy_system.primary_PJ["Hydro Share"].iloc[-1]
    final_coal_primary_share = \
        energy_system.primary_PJ["Coal Share"].iloc[-1]
    final_oil_primary_share = \
        energy_system.primary_PJ["Oil Share"].iloc[-1]
    final_gas_primary_share = \
        energy_system.primary_PJ["Gas Share"].iloc[-1]
    final_nuclear_primary_share = \
        energy_system.primary_PJ["Nuclear Share"].iloc[-1]
    final_wind_primary_share = \
        energy_system.primary_PJ["Wind Share"].iloc[-1]
    final_solar_primary_share = \
        energy_system.primary_PJ["Solar Share"].iloc[-1]
    final_geo_bio_primary_share = \
        energy_system.primary_PJ["Bio Geo Share"].iloc[-1]

    category_name = [
        "Fossil Fuels",
        "Nuclear",
        "Hydro",
        "Wind Solar",
        "Geo Bio"]
    fuel_name = [
        "Coal",
        "Oil",
        "Gas",
        "Nuclear",
        "Hydro",
        "Wind",
        "Solar",
        "Geo Bio"]
    final_category_share = [
        final_ff_primary_share,
        final_nuclear_primary_share,
        final_hydro_primary_share,
        final_ws_primary_share,
        final_geo_bio_primary_share]
    final_fuel_share = [
        final_coal_primary_share,
        final_oil_primary_share,
        final_gas_primary_share,
        final_nuclear_primary_share,
        final_hydro_primary_share,
        final_wind_primary_share,
        final_solar_primary_share,
        final_geo_bio_primary_share]
    category_color = [
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_SOLAR.value,
        user_globals.Color.GEO_BIO.value]
    fuel_color = [
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND.value,
        user_globals.Color.SOLAR.value,
        user_globals.Color.GEO_BIO.value]

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

    suptitle = (energy_system.name.upper())
    suptitle_addition = "Share of Fuels in Energy Supply (Primary Energy), \
year " + str(energy_system.primary_PJ.index[-1])
    title1 = "Category Shares"
    title2 = "Individual Fuel Shares"
    footer_text = "For clarity: (1) Values are rounded, so shares may not \
total 100%, (2) Shares <1% aren't shown,\n(3) Labels may not be shown due to \
a lack of space, in which case refer to the legend."

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
        df_category.loc[df_category["Value"] < 5, ["Label"]] = \
            df_category["Value"].astype(str) + "%"
        df_category.loc[df_category["Value"] >= 5, ["Label"]] = \
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

    chart.treemap(
        df_category,
        df_fuel,
        title1,
        title2,
        suptitle,
        suptitle_addition,
        footer_text)
    plt.show()

    ###########################################################################
    # Annual additions and subtractions of categories and fuels
    ###########################################################################
    if energy_system.name == "World":
        y_label = "Annual Change (EJ/year)"
    else:
        y_label = "Annual Change (PJ/year)"
    chart.column_grouped(
        energy_system.name.upper(),
        "Annual Additions to and Subtractions from Categories in Energy \
Supply (Primary Energy)",
        y_label,
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
\n(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.",
        user_globals.Constant.CHANGE_START_YEAR.value,
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_SOLAR.value,
        series1 = energy_system.primary_PJ["Fossil Fuels Change"],
        series2 = energy_system.primary_PJ["Nuclear Change"],
        series3 = energy_system.primary_PJ["Hydro Change"],
        series4 = energy_system.primary_PJ["Wind and Solar Change"])
    plt.show()

    chart.column_grouped(
        energy_system.name.upper(),
        "Annual Additions to and Subtractions from Fuels in Energy Supply \
(Primary Energy)",
        y_label,
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
\n(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.",
        user_globals.Constant.CHANGE_START_YEAR.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_SOLAR.value,
        series1 = energy_system.primary_PJ["Coal Change"],
        series2 = energy_system.primary_PJ["Oil Change"],
        series3 = energy_system.primary_PJ["Gas Change"],
        series4 = energy_system.primary_PJ["Nuclear Change"],
        series5 = energy_system.primary_PJ["Hydro Change"],
        series6 = energy_system.primary_PJ["Wind and Solar Change"])
    plt.show()

###############################################################################
#
# Function: consumption()
#
# Description:
# Calculate TFC fuel shares and plot.
#
# Input(s): Instance of user class energy_system.
# Output(s): TFC fuel shares appended to energy_system.
#
###############################################################################
def consumption(energy_system):
    ###########################################################################
    # Calculate TFC shares and changes.
    ###########################################################################

    energy_system.tf_consumption_PJ["Coal Share"] = \
        energy_system.tf_consumption_PJ["Coal"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Oil Share"] = \
        energy_system.tf_consumption_PJ["Oil"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Gas Share"] = \
        energy_system.tf_consumption_PJ["Gas"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Wind Solar Etc Share"] = \
        energy_system.tf_consumption_PJ["Wind Solar Etc"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Biofuels and Waste Share"] = \
        energy_system.tf_consumption_PJ["Biofuels and Waste"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Electricity Share"] = \
        energy_system.tf_consumption_PJ["Electricity"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    energy_system.tf_consumption_PJ["Heat Share"] = \
        energy_system.tf_consumption_PJ["Heat"] / \
        energy_system.tf_consumption_PJ["Total"] * 100
    print("TFC Shares: \n",
          energy_system.tf_consumption_PJ["Coal Share"] +
          energy_system.tf_consumption_PJ["Oil Share"] +
          energy_system.tf_consumption_PJ["Gas Share"] +
          energy_system.tf_consumption_PJ["Wind Solar Etc Share"] +
          energy_system.tf_consumption_PJ["Biofuels and Waste Share"] +
          energy_system.tf_consumption_PJ["Electricity Share"] +
          energy_system.tf_consumption_PJ["Heat Share"])

    change_yrs = range(user_globals.Constant.TFC_START_YEAR.value + 1,
                       user_globals.Constant.TFC_END_YEAR.value + 1)

    for yr in change_yrs:
        energy_system.tf_consumption_PJ.loc[yr, "Coal Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Coal"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Coal"]
        energy_system.tf_consumption_PJ.loc[yr, "Oil Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Oil"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Oil"]
        energy_system.tf_consumption_PJ.loc[yr, "Gas Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Gas"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Gas"]
        energy_system.tf_consumption_PJ.loc[yr, "Wind Solar Etc Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Wind Solar Etc"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Wind Solar Etc"]
        energy_system.tf_consumption_PJ.loc[yr, "Biofuels and Waste Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Biofuels and Waste"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Biofuels and Waste"]
        energy_system.tf_consumption_PJ.loc[yr, "Electricity Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Electricity"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Electricity"]
        energy_system.tf_consumption_PJ.loc[yr, "Heat Change"] = \
            energy_system.tf_consumption_PJ.loc[yr, "Heat"] - \
            energy_system.tf_consumption_PJ.loc[yr - 1, "Heat"]

    # Chart title.
    title = (energy_system.name.upper())

    title_addition = "Annual Energy Consumption by share (Total Final \
Consumption or Final Energy). Final forms of consumed energy."

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"

    # Additional text.
    ylabel = ("Annual Share (%)")
    footer_text = "Shares of coal, oil, gas, biofuels, and waste shown were \
consumed to produce heat for purposes other than electricity production, \
such as steel maufacture or internal combustion etc.\nShares labelled \
'Wind, solar etc' in TFC by the IEA were small and omitted for clarity, and also \
consumed for purposes other than electricty production."

    #Plot
    chart.line_subplot(energy_system.tf_consumption_PJ["Coal Share"],
                       energy_system.tf_consumption_PJ["Oil Share"],
                       energy_system.tf_consumption_PJ["Gas Share"],
                       energy_system.tf_consumption_PJ["Biofuels and Waste \
Share"],
                       energy_system.tf_consumption_PJ["Electricity Share"],
                       energy_system.tf_consumption_PJ["Heat Share"],
                       user_globals.Color.COAL.value,
                       user_globals.Color.OIL.value,
                       user_globals.Color.GAS.value,
                       user_globals.Color.GEO_BIO.value,
                       user_globals.Color.ELECTRICITY.value,
                       user_globals.Color.HEAT.value,
                       title, title_addition, title1, title2, title3,
                       title4, title5, title6, ylabel, footer_text)

    plt.show()

###############################################################################
#
# Function: electricity()
#
# Description:
# Calculate and plot electricity generation shares, and annual additions and
# subtractions.
#
# Input(s): Instance of user class energy_system.
# Output(s):
# 1. Figure of 1x3 subplots with equivalent scales, showing annual primary
# energy of fossil fuels.
# 2. Figure of 2x3 subplots showing annual shares of primary energy of each
# fuel.
# 3. Figure of 1x2 treemaps showing primary energy shares for categories and
# fuels in the most recent year of EI's dataset.
# 4. Single figure of grouped columns showing annual addition and subtractions
# to and from primary energy of categories.
# 5. Single figure of grouped columns showing annual addition and subtractions
# to and from primary energy of fuels.
#
###############################################################################
#def consumption(energy_system):
    ###########################################################################
    # Calculate TFC fuel shares.
    ###########################################################################
