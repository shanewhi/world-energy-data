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
        energy_system.total_primary_PJ.index,
        energy_system.co2_combust_mtco2["Value"],
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
        energy_system.total_primary_PJ,
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
        energy_system.total_primary_PJ,
        energy_system.coal_primary_PJ,
        energy_system.oil_primary_PJ,
        energy_system.gas_primary_PJ,
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
    min_year = min(energy_system.total_primary_PJ.index)
    max_year = max(energy_system.total_primary_PJ.index)
    change_period = range(min_year + 1, max_year + 1)
    # Coal.
    if not energy_system.coal_primary_PJ.empty:
        coal_primary = pd.DataFrame(index =
                             energy_system.coal_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        # Provide name for plot legend.
        coal_primary.at[min(coal_primary.index), "Name"] = "Coal"
        coal_primary["Value"] = energy_system.coal_primary_PJ["Value"]
        coal_primary["Share"] = (coal_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            coal_primary.loc[yr, "Change"] = \
                coal_primary.loc[yr, "Value"] - \
                coal_primary.loc[yr - 1, "Value"]

    # Oil.
    if not energy_system.oil_primary_PJ.empty:
        oil_primary = pd.DataFrame(index =
                             energy_system.oil_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        oil_primary.at[min(oil_primary.index), "Name"] = "Oil"
        oil_primary["Value"] = energy_system.oil_primary_PJ["Value"]
        oil_primary["Share"] = (oil_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            oil_primary.loc[yr, "Change"] = \
                oil_primary.loc[yr, "Value"] - \
                oil_primary.loc[yr - 1, "Value"]

    # Gas.
    if not energy_system.gas_primary_PJ.empty:
        gas_primary = pd.DataFrame(index =
                             energy_system.gas_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        gas_primary.at[min(gas_primary.index), "Name"] = "Gas"
        gas_primary["Value"] = energy_system.gas_primary_PJ["Value"]
        gas_primary["Share"] = (gas_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            gas_primary.loc[yr, "Change"] = \
                gas_primary.loc[yr, "Value"] - \
                gas_primary.loc[yr - 1, "Value"]

    # Nuclear.
    if not energy_system.nuclear_primary_PJ.empty:
        nuclear_primary = pd.DataFrame(index =
                             energy_system.nuclear_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        nuclear_primary.at[min(nuclear_primary.index), "Name"] = \
            "Nuclear"
        nuclear_primary["Value"] = energy_system.nuclear_primary_PJ["Value"]
        nuclear_primary["Share"] = (nuclear_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            nuclear_primary.loc[yr, "Change"] = \
                nuclear_primary.loc[yr, "Value"] - \
                nuclear_primary.loc[yr - 1, "Value"]

    # Hydro.
    if not energy_system.hydro_primary_PJ.empty:
        hydro_primary = pd.DataFrame(index =
                             energy_system.hydro_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        hydro_primary.at[min(hydro_primary.index), "Name"] = "Hydro"
        hydro_primary["Value"] = energy_system.hydro_primary_PJ["Value"]
        hydro_primary["Share"] = (hydro_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            hydro_primary.loc[yr, "Change"] = \
                hydro_primary.loc[yr, "Value"] - \
                hydro_primary.loc[yr - 1, "Value"]

    # Wind.
    if not energy_system.wind_primary_PJ.empty:
        wind_primary = pd.DataFrame(index =
                             energy_system.wind_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        wind_primary.at[min(wind_primary.index), "Name"] = "Wind"
        wind_primary["Value"] = energy_system.wind_primary_PJ["Value"]
        wind_primary["Share"] = (wind_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            wind_primary.loc[yr, "Change"] = \
                wind_primary.loc[yr, "Value"] - \
                wind_primary.loc[yr - 1, "Value"]

    # Solar.
    if not energy_system.solar_primary_PJ.empty:
        solar_primary = pd.DataFrame(index =
                             energy_system.solar_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        solar_primary.at[min(solar_primary.index), "Name"] = "Solar"
        solar_primary["Value"] = energy_system.solar_primary_PJ["Value"]
        solar_primary["Share"] = (solar_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            solar_primary.loc[yr, "Change"] = \
                solar_primary.loc[yr, "Value"] - \
                solar_primary.loc[yr - 1, "Value"]

    # Geo, Bio and Other.
    if not energy_system.geo_bio_other_primary_PJ.empty:
        geo_bio_other_primary = pd.DataFrame(index =
                             energy_system.geo_bio_other_primary_PJ.index,
                             columns = ["Name", "Value", "Share", "Change"])
        geo_bio_other_primary.at[min(geo_bio_other_primary.index), \
                                    "Name"] = "Geo + Bio + Other"
        geo_bio_other_primary["Value"] = \
            energy_system.geo_bio_other_primary_PJ["Value"]
        geo_bio_other_primary["Share"] = \
            (geo_bio_other_primary["Value"] /
            energy_system.total_primary_PJ["Value"]) * 100
        for yr in change_period:
            geo_bio_other_primary.loc[yr, "Change"] = \
                geo_bio_other_primary.loc[yr, "Value"] - \
                geo_bio_other_primary.loc[yr - 1, "Value"]

    # Wind + Solar.
    if not (energy_system.wind_primary_PJ.empty or \
            energy_system.solar_primary_PJ.empty):
         wind_solar_primary = pd.DataFrame(index =
                              energy_system.total_primary_PJ.index,
                              columns = ["Name", "Value", "Share", "Change"])
         wind_solar_primary.at[min(wind_solar_primary.index), "Name"] = \
             "Wind + Solar"
         wind_solar_primary["Value"] = wind_primary["Value"] + \
                                             solar_primary["Value"]
         wind_solar_primary["Share"] = \
            ((wind_primary["Value"] + solar_primary["Value"]) /
            energy_system.total_primary_PJ.Value) * 100
         for yr in change_period:
             wind_solar_primary.loc[yr, "Change"] = \
             wind_solar_primary.loc[yr, "Value"] - \
             wind_solar_primary.loc[yr - 1, "Value"]

    # Fossil Fuels.
    ff_primary = pd.DataFrame(index =
                    energy_system.total_primary_PJ.index,
                    columns = ["Name", "Value", "Share", "Change"])
    ff_primary.at[min(ff_primary.index), "Name"] = "Fossil Fuels"
    ff_primary["Value"] = coal_primary["Value"] + \
        gas_primary["Value"] + oil_primary["Value"]
    ff_primary["Share"] = (ff_primary["Value"] /
                              energy_system.total_primary_PJ["Value"]) * 100
    for yr in change_period:
        ff_primary.loc[yr, "Change"] = ff_primary.loc[yr, "Value"] - \
            ff_primary.loc[yr - 1, "Value"]

    # Renewables (Wind + Solar + Hydro).
    renew_primary = pd.DataFrame(index =
                    energy_system.total_primary_PJ.index,
                    columns = ["Name", "Value", "Share", "Change"])
    renew_primary.at[min(renew_primary.index), "Name"] = "Renewables"
    renew_primary["Value"] = wind_solar_primary["Value"] + \
        hydro_primary["Value"]
    renew_primary["Share"] = (renew_primary["Value"] /
                              energy_system.total_primary_PJ["Value"]) * 100
    for yr in change_period:
        renew_primary.loc[yr, "Change"] = \
            renew_primary.loc[yr, "Value"] - \
            renew_primary.loc[yr - 1, "Value"]

    # Chart title.
    title = (energy_system.name.upper())
    title_addition = ""
    if not energy_system.name == "World":
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
    footer_text = "Shares of geothermal, biofuels and 'other' are small and\
omitted for clarity."

    #Plot
    chart.line_subplot(energy_system.total_primary_PJ,
                       coal_primary, oil_primary,
                       gas_primary, nuclear_primary,
                       hydro_primary, wind_solar_primary,
                       user_globals.Color.COAL.value,
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
    final_ff_primary_share = ff_primary["Share"].iloc[-1]
    final_renew_primary_share = renew_primary["Share"].iloc[-1]
    final_coal_primary_share = coal_primary["Share"].iloc[-1]
    final_oil_primary_share = oil_primary["Share"].iloc[-1]
    final_gas_primary_share = gas_primary["Share"].iloc[-1]
    final_nuclear_primary_share = nuclear_primary["Share"].iloc[-1]
    final_hyrdo_primary_share = hydro_primary["Share"].iloc[-1]
    final_wind_primary_share = wind_primary["Share"].iloc[-1]
    final_solar_primary_share = solar_primary["Share"].iloc[-1]
    final_geo_bio_other_primary_share = geo_bio_other_primary["Share"].iloc[-1]

    category_name = [
        "Fossil Fuels",
        "Nuclear",
        "Renewables",
        "Geo, Bio, Other"]
    fuel_name = [
        "Coal",
        "Oil",
        "Gas",
        "Nuclear",
        "Hydro",
        "Wind",
        "Solar",
        "Geo, Bio, Other"]

    final_category_share = [
        final_ff_primary_share,
        final_nuclear_primary_share,
        final_renew_primary_share,
        final_geo_bio_other_primary_share]
    final_fuel_share = [
        final_coal_primary_share,
        final_oil_primary_share,
        final_gas_primary_share,
        final_nuclear_primary_share,
        final_hyrdo_primary_share,
        final_wind_primary_share,
        final_solar_primary_share,
        final_geo_bio_other_primary_share]

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
            filtered_final_fuel_share.append(int(round(final_fuel_share[i],
                                                       0)))
            filtered_fuel_color.append(fuel_color[i])

    suptitle = (energy_system.name.upper())
    suptitle_addition = "Share of Fuels in Energy Supply (Primary Energy), \
year " + str(energy_system.total_primary_PJ.index[-1])
    title1 = "Category Shares"
    title2 = "Individual Fuel Shares"
    footer_text = "For clarity: (1) Values are rounded, so shares may not \
total 100%, (2) Shares <1% aren't shown,\n(3) Labels for categories <20% \
aren't shown if there's a large difference between lowest & highest \
shares."

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
    if (df_category["Value"].max() / df_category["Value"].min()) >= 5:
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
        df_fuel.loc[df_fuel["Value"] < 10, ["Label"]] = \
            df_fuel["Value"].astype(str) + "%"
        df_fuel.loc[df_fuel["Value"] >= 10, ["Label"]] = \
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
    chart_start_yr = 1995
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
\n(3) When the value of a fuel is zero or rounds to zero, the column is not \
shown resulting in a gap between plotted columns.",
        chart_start_yr,
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEW.value,
        df1 = ff_primary,
        df2 = nuclear_primary,
        df3 = renew_primary)
    plt.show()

    chart.column_grouped(
        energy_system.name.upper(),
        "Annual Additions to and Subtractions from Fuels in Energy Supply \
(Primary Energy)",
        y_label,
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
\n(3) When the value of a fuel is zero or rounds to zero, the column is not \
shown resulting in a gap between plotted columns.",
        chart_start_yr,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_SOLAR.value,
        df1 = coal_primary,
        df2 = oil_primary,
        df3 = gas_primary,
        df4 = nuclear_primary,
        df5 = hydro_primary,
        df6 = wind_solar_primary)
    plt.show()

###############################################################################
#
# Function: consumptiom()
#
# Description:
# Plot total final consumption.
#
# Input(s): Instance of user class energy_system.
# Output(s): ?
#
###############################################################################
def consumption(energy_system):
    # Plot absolute quantity of primary energy of fossil fuels.
    if energy_system.name == 'World':
        unit = "(EJ)"
    else:
        unit = "(PJ)"

    fig, ax = plt.subplots(1, 1,
                figsize = (user_globals.Constant.FIG_SIZE.value,
                           user_globals.Constant.FIG_SIZE.value))
    ax.plot(energy_system.tf_consumption_PJ.index, energy_system.tf_consumption_PJ["Coal"], color = 'black', linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 7, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = .3)
    ax.plot(energy_system.tf_consumption_PJ.index, energy_system.tf_consumption_PJ["Oil"], color = 'brown', linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 7, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = .3)
    ax.plot(energy_system.tf_consumption_PJ.index, energy_system.tf_consumption_PJ["Gas"], color = 'orange', linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 7, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = .3)
    ax.plot(energy_system.tf_consumption_PJ.index, energy_system.tf_consumption_PJ["Electricity"], color = 'teal', linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 7, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = .3)


