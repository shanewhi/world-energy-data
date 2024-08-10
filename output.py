#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:20:13 2024

@author: shanewhite
"""

########################################################################################
#
# Module: output.py
#
# Description:
# Controls chart plotting sequence.
#
########################################################################################

# Import Python modules.
import matplotlib.pyplot as plt
import pandas as pd
import os

# Import user modules.
import user_globals
import chart


########################################################################################
#
# Function: world_co2_charts()
#
# Description:
# Controls chart plotting of global carbon project data.
#
########################################################################################
def world_co2_charts(global_carbon):
    fig_dir = "charts CO2/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.
    ####################################################################################
    # Atmospheric CO2: Concentration and growth.
    ####################################################################################
    co2_ppm = global_carbon.co2_conc["Mean"]
    co2_change = global_carbon.co2_conc["Ann Inc"]
    color1 = user_globals.Color.CO2_CONC.value
    color2 = user_globals.Color.CO2_CONC.value
    country = "Global"
    title = "Atmospheric CO\u2082"
    subplot1_title = "Annual Concentration"
    subplot2_title = "Annual Change"
    start_yr1 = user_globals.Constant.CHART_START_YR.value
    start_yr2 = user_globals.Constant.CHART_START_YR.value
    x_axis1_interval = 10
    x_axis2_interval = 10
    ylabel1 = "parts per million (ppm)"
    ylabel2 = "ppm/year"
    concentration_text = (
            "Value for "
            + str(global_carbon.co2_conc.index[-1])
            + " = "
            + str(round(global_carbon.co2_conc["Mean"].iloc[-1], 1))
            + "ppm"
    )
    footer_text = "Lan, X., Tans, P. and K.W. Thoning: Trends in globally-averaged \
CO\u2082 determined from NOAA Global Monitoring Laboratory measurements. Version \
2024-05 https://doi.org/10.15138/9N0H-ZH07.\n\
Obtained from https://gml.noaa.gov/ccgg/trends/gl_data.html.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    chart.line_column1x2(
        co2_ppm,
        co2_change,
        color1,
        color2,
        country,
        title,
        subplot1_title,
        subplot2_title,
        start_yr1,
        start_yr2,
        x_axis1_interval,
        x_axis2_interval,
        ylabel1,
        ylabel2,
        concentration_text,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "1 co2 conc.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # CO2 Emissions: Shares of sources for most recent year.
    ####################################################################################

    print(
        "CO2 emission treemap, most recent year sum of category shares = "
        + str(sum(global_carbon.final_emission_category_shares["Value"]))
        + "%"
    )
    print(
        "CO2 emission treemap, most recent year sum of emission shares = "
        + str(sum(global_carbon.final_emission_shares["Value"]))
        + "%"
    )

    country = global_carbon.name
    title = "CO\u2082 Emission Sources by Share"
    title_addition = "Year " + str(global_carbon.data["Total"].index[-1])
    title1 = "By Category"
    title2 = "By Emission Source"
    footer_text = "Data: Global Carbon Project, Friedlingstein et al (2023), \
https://globalcarbonbudgetdata.org/latest-data.html.\n\
Category Fossil Fuels is the sum of emissions from coal, oil, gas, and \
flaring.\n\
For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to \
the legend.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    chart.treemap1x2(
        global_carbon.final_emission_category_shares,
        global_carbon.final_emission_shares,
        title1,
        title2,
        country,
        title,
        title_addition,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "2 co2 emission sources.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # CO2 Emissions: Annual Fossil Fuels + Cement
    ####################################################################################
    ffc_co2 = global_carbon.data["FF and Cement"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    country = "World"
    title = "Annual CO\u2082 Emissions from Fossil Fuels and Cement"
    title1 = str(min(ffc_co2.index)) + " - " + str(max(ffc_co2.index))
    title2 = (
            str(user_globals.Constant.CHART_START_YR.value)
            + " - "
            + str(ffc_co2.index.max())
    )
    start_yr1 = global_carbon.data.index.min()
    start_yr2 = user_globals.Constant.CHART_START_YR.value
    x_axis1_interval = 50
    x_axis2_interval = 10
    ylabel = "Megatonne"
    footer_text = "Data: Global Carbon Project, Friedlingstein et al (2023), \
https://globalcarbonbudgetdata.org/latest-data.html.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    print(
        "Most recent fossil fuel and cement CO2 emission = "
        + str(round(ffc_co2.iloc[-1], 1))
        + " MtCO2\n"
    )

    chart.column1x2(
        ffc_co2,
        ffc_co2,
        co2_color,
        co2_color,
        country,
        title,
        title1,
        title2,
        start_yr1,
        start_yr2,
        x_axis1_interval,
        x_axis2_interval,
        ylabel,
        footer_text,
        False,
    )
    plt.savefig(
        os.path.join(fig_dir, "3 co2 annual emissions.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # CO2 Emissions: Annual change.
    ####################################################################################
    series = global_carbon.data["FF and Cement Change"]
    title = "Annual Change of CO\u2082 Emissions from Fossil Fuels and \
Cement"
    ylabel = "Megatonne/year"
    footer_text = (
        "Data: Global Carbon Project, Friedlingstein et al (2023), \
https://globalcarbonbudgetdata.org/latest-data.html.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    )

    start_yr = user_globals.Constant.CHART_START_YR.value
    color = user_globals.Color.CO2_EMISSION.value

    chart.columngrouped(
        country,
        title,
        ylabel,
        footer_text,
        start_yr,
        color,
        series1=series,
    )
    plt.savefig(
        os.path.join(fig_dir, "4 co2 emissions change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # CO2 Emissions: Annual Coal, Oil, and Gas.
    ####################################################################################
    coalco2 = global_carbon.data["Coal"]
    oilco2 = global_carbon.data["Oil"]
    gasco2 = global_carbon.data["Gas"]
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    country = "World"
    title = "Annual CO\u2082 Emissions from Fossil Fuels"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    x_axis_interval = 25
    ylabels = "Megatonne"
    footer_text = "Data: Global Carbon Project, Friedlingstein et al (2023), \
https://globalcarbonbudgetdata.org/latest-data.html.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    equiv_yscale = True
    start_yr = global_carbon.data.index.min()

    chart.column1x3(
        coalco2,
        oilco2,
        gasco2,
        color1,
        color2,
        color3,
        country,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        start_yr,
        x_axis_interval,
        ylabels,
        footer_text,
        equiv_yscale,
    )
    plt.savefig(
        os.path.join(fig_dir, "5 co2 sep emissions.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: country_co2_charts()
#
# Description:
# Plots national CO2 emissions from fossil fuel combustion
#
########################################################################################
def country_co2_charts(energy_system, global_carbon):
    country = energy_system.name

    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    ####################################################################################
    # CO2 Emissions from fossil fuel combustion.
    ####################################################################################

    ffco2 = energy_system.ffco2["Value"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    x_interval = 10
    ylabel = "Megatonne"

    title1 = "Fossil fuel CO\u2082 emissions"
    title2 = "National shares of fossil fuel CO\u2082 emissions"
    subplot1_title = "Annual"
    subplot2_title = "Year " + str(int(max(global_carbon.final_country_shares["Year"])))

    large_emitter_share_total = 100 - float(
        global_carbon.final_country_shares[
            global_carbon.final_country_shares["Name"] == "Other"
            ].Value.values
    )
    one_percent_countries = global_carbon.final_country_shares[
        global_carbon.final_country_shares["Value"] >= 1
        ]
    one_percent_countries_share = round(
        (
                sum(one_percent_countries["Value"])
                - one_percent_countries[
                    one_percent_countries["Name"] == "Other"
                    ].Value.values[0]
        ),
        1,
    )
    half_to_one_percent_countries = global_carbon.final_country_shares.loc[
        global_carbon.final_country_shares["Value"] < 1
        ].Name.values

    s = ""
    for i in half_to_one_percent_countries:
        s += i
        s += "\n"

    additional_text1 = (
            "Shares total 100% of 2023 global\nfossil fuel CO\u2082 emissions.\n\n\n\
    Country segments shown are those\nwith a "
            + str(user_globals.Constant.CO2_SHARE_RANK_THRESHOLD.value)
            + "% or \
greater share, of which\nthere were "
            + str(len(global_carbon.final_country_shares) - 1)
            + ", totalling "
            + str(large_emitter_share_total)
            + "%.\n\n\nLabelled countries are those \
with a 1%\nor greater share, of which there were\n"
            + str(
        len(
            global_carbon.final_country_shares[
                global_carbon.final_country_shares["Value"] >= 1
                ]
        )
        - 1  # Don't include 'Other'.
    )
            + ", totalling "
            + str(one_percent_countries_share)
            + "%.\n\n\nUnlabelled countries in lower\nright corner are listed below. \
These\nhad shares greater than or equal\nto 0.5%, and less than 1% -\n\n"
            + s
    )

    footer_text = "Data: The Energy Institute Statistical Review of World Energy \
2024,\n\
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    start_yr = user_globals.Constant.CHART_START_YR.value

    chart.column_treemap1x2(
        ffco2,
        global_carbon.final_country_shares,
        co2_color,
        country,
        title1,
        title2,
        subplot1_title,
        subplot2_title,
        start_yr,
        x_interval,
        ylabel,
        additional_text1,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "1 " + country + " ff co2.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    print(
        "National CO2 emission shares treemap, most recent year sum of shares = "
        + str(sum(global_carbon.final_country_shares["Value"]))
        + "%"
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ffco2_change = energy_system.ffco2["Change"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    title = "Annual Change of CO\u2082 Emissions from Fossil Fuels"
    ylabel = "Megatonne/year"
    footer_text = "Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Primary Energy accounts for fuels input to a national, or the world energy system, \
prior to conversion to electricity or combusted for non-electric purposes. For an \
explanation of Primary Energy, see https://www.worldenergydata.org/introduction/.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    chart.columngrouped(
        country,
        title,
        ylabel,
        footer_text,
        start_yr,
        co2_color,
        series1=ffco2_change,
    )

    plt.savefig(
        os.path.join(fig_dir, "2 " + country + " ff co2 change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: world_ffprod_charts()
#
# Description:
# Controls plotting of global fossil fuel production shares by country.
#
########################################################################################
def world_ffprod_charts(coal_prods, oil_prods, gas_prods, country):
    fig_dir = "charts " + country + "/"
    print(
        "Sum of most recent year coal producer shares = "
        + str(sum(coal_prods["Value"]))
        + "%"
    )
    print(
        "Sum of most recent year oil producer shares = "
        + str(sum(oil_prods["Value"]))
        + "%"
    )
    print(
        "Sum of most recent year gas producer shares = "
        + str(sum(gas_prods["Value"]))
        + "%"
    )
    subplot1_title = "Coal Producers"  # Title above LH plot
    subplot2_title = "Oil Producers"  # Title above centre plot
    subplot3_title = "Gas Producers"  # Title above RH plot
    country = "World"
    title = "Shares of National Fossil Fuel Production"
    title_addition = "Year " + str(coal_prods.loc[0, "Year"])
    footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Ranking of producers determined using fossil fuel production data in following units: \
Coal EJ, Oil Mt, and Gas EJ.\nOil production in units of Mt is used instead of kbd \
because it's in closer agreement with IEA data. Oil production in units of Joules \
isn't available.\n\
Share labelled Other is the tally of all countries producing less than a 4% share of \
the respective fossil fuel.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    chart.treemap1x3(
        coal_prods,  # Dataframe 1
        oil_prods,  # Dataframe 2
        gas_prods,  # Dataframe 3
        subplot1_title,  # Title above LH plot
        subplot2_title,  # Title above centre plot
        subplot3_title,  # Title above RH plot
        country,
        title,
        title_addition,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "4 " + country + " prod ff shares.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: country_prod_primary_energy_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI energy data.
#
########################################################################################
def country_prod_primary_energy_charts(energy_system):
    country = energy_system.name

    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save charts in this directory.

    ####################################################################################
    # PRODUCTION: Annual Fossil Fuel Production.
    ####################################################################################
    if country == "World":
        ylabel = "Exajoule"
        ffprod_coal = (
                energy_system.ffprod_PJ["Coal"] * user_globals.Constant.PJ_TO_EJ.value
        )
        ffprod_oil = (
                energy_system.ffprod_PJ["Oil"] * user_globals.Constant.PJ_TO_EJ.value
        )
        ffprod_gas = (
                energy_system.ffprod_PJ["Gas"] * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule"
        ffprod_coal = energy_system.ffprod_PJ["Coal"]
        ffprod_oil = energy_system.ffprod_PJ["Oil"]
        ffprod_gas = energy_system.ffprod_PJ["Gas"]

    title = "Annual Production of Fossil Fuels"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"

    if country == "World":
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe. \
Initial year of data for each fuel differs: Coal 1981, Oil 1965, and Gas \
1970.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    else:
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2024 (EI(2024)), \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe. \
Initial year of data for each fuel differs: Coal 1981, Oil 1965, and Gas \
1970.\n\
For comparison, EI(2024) listed 2023 World production values as: \
Coal 179,000 PJ, Oil 197,000 PJ, and Gas 146,000 PJ.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    x_axis_interval = 5
    equiv_scale = True

    chart.column1x3(
        ffprod_coal,
        ffprod_oil,
        ffprod_gas,
        color1,
        color2,
        color3,
        country,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        user_globals.Constant.CHART_START_YR.value,
        x_axis_interval,
        ylabel,
        footer_text,
        equiv_scale,
    )
    plt.savefig(
        os.path.join(fig_dir, "3 " + country + " prod ff sep.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # PRIMARY ENERGY: Annual shares of most recent year.
    ####################################################################################
    title = "Shares of Fuels in Energy Supply (Primary Energy)"
    title_addition = (
            "Year "
            + str(energy_system.primary_PJ.index[-1])
            + ". Primary \
Energy accounts for fuels input to a national, or the world energy system, prior to \
conversion to electricity or combusted for non-electric purposes."
    )
    title1 = "By Category"
    title2 = "By Fuel"
    footer_text = "Data: The Energy Institute Statistical Review of World \
Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to \
the legend.\n\
For an explanation of Primary Energy, \
see https://www.worldenergydata.org/introduction/. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
    print(
        "Annual sum of primary energy shares = \n"
        + str(
            energy_system.primary_PJ["Coal Share"]
            + energy_system.primary_PJ["Oil Share"]
            + energy_system.primary_PJ["Gas Share"]
            + energy_system.primary_PJ["Nuclear Share"]
            + energy_system.primary_PJ["Hydro Share"]
            + energy_system.primary_PJ["Wind Share"]
            + energy_system.primary_PJ["Solar Share"]
            + energy_system.primary_PJ["Bio, Geo and Other Share"]
        )
        + "%\n"
    )

    chart.treemap1x2(
        energy_system.primary_final_category_shares,
        energy_system.primary_final_fuel_shares,
        title1,
        title2,
        country,
        title,
        title_addition,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "5 " + country + " pe shares.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # PRIMARY ENERGY: Annual shares.
    ####################################################################################
    title = "Annual Shares of Fuels in Energy Supply (Primary Energy)"

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Renewables"
    title6 = "Bio, Geo and Other"

    pes1 = pd.Series(energy_system.primary_PJ["Coal Share"])
    pes2 = pd.Series(energy_system.primary_PJ["Oil Share"])
    pes3 = pd.Series(energy_system.primary_PJ["Gas Share"])
    pes4 = pd.Series(energy_system.primary_PJ["Nuclear Share"])
    pes5 = pd.Series(energy_system.primary_PJ["Renewables Share"])
    pes6 = pd.Series(energy_system.primary_PJ["Bio, Geo and Other Share"])

    # Additional text.
    ylabel = "Annual Share (%)"
    footer_text = "Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads. \
Renewables is the sum of hydro, wind and solar.\n\
Primary Energy accounts for fuels input to a national, or the world energy system, \
prior to conversion to electricity or combusted for non-electric purposes.\nFor an \
explanation of Primary Energy, see https://www.worldenergydata.org/introduction/.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    # Plot
    chart.line2x3(
        pes1,
        pes2,
        pes3,
        pes4,
        pes5,
        pes6,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEWABLES.value,
        user_globals.Color.OTHER.value,
        country,
        title,
        title1,
        title2,
        title3,
        title4,
        title5,
        title6,
        user_globals.Constant.CHART_START_YR.value,
        ylabel,
        footer_text,
        True,
    )
    plt.savefig(
        os.path.join(fig_dir, "6 " + country + " pe share trends.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # PRIMARY ENERGY: Annual quantity of fossil fuels.
    ####################################################################################
    title = "Annual Quantity of Fossil Fuels in Energy Supply \
(Primary Energy)"

    if country == "World":
        ylabel = "Exajoule"
        peq1 = pd.Series(
            energy_system.primary_PJ["Coal"] * user_globals.Constant.PJ_TO_EJ.value
        )
        peq2 = pd.Series(
            energy_system.primary_PJ["Oil"] * user_globals.Constant.PJ_TO_EJ.value
        )
        peq3 = pd.Series(
            energy_system.primary_PJ["Gas"] * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule"
        peq1 = pd.Series(energy_system.primary_PJ["Coal"])
        peq2 = pd.Series(energy_system.primary_PJ["Oil"])
        peq3 = pd.Series(energy_system.primary_PJ["Gas"])

    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Primary Energy accounts for fuels input to a national, \
or the world energy system, prior to conversion to electricity or combusted \
for non-electric purposes. For an explanation of Primary Energy, see \
https://www.worldenergydata.org/introduction/.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    x_axis_interval = 10
    equiv_yscale = True

    chart.column1x3(
        peq1,
        peq2,
        peq3,
        color1,
        color2,
        color3,
        country,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        user_globals.Constant.CHART_START_YR.value,
        x_axis_interval,
        ylabel,
        footer_text,
        equiv_yscale,
    )
    plt.savefig(
        os.path.join(fig_dir, "7 " + country + " pe ff qty.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # PRIMARY ENERGY: Annual change of fossil fuel category.
    ####################################################################################
    title = "Annual Change of Fossil Fuels in Energy Supply \
(Primary Energy)"

    if country == "World":
        ylabel = "Exajoule/year"
        series = pd.Series(
            energy_system.primary_PJ["Fossil Fuels Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule/year"
        series = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"])

    footer_text = "Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Primary Energy accounts for fuels input to a national, or the world energy system, \
prior to conversion to electricity or combusted for non-electric purposes. For an \
explanation of Primary Energy, see https://www.worldenergydata.org/introduction/.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    start_yr = user_globals.Constant.CHART_START_YR.value
    color = user_globals.Color.FOSSIL_FUELS.value

    chart.columngrouped(
        country,
        title,
        ylabel,
        footer_text,
        start_yr,
        color,
        series1=series,
    )
    plt.savefig(
        os.path.join(fig_dir, "8 " + country + " pe ff change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # PRIMARY ENERGY: Annual change of fossil fuels.
    ####################################################################################
    title = "Annual Change of Fossil Fuels in Energy Supply \
(Primary Energy)"

    if country == "World":
        ylabel = "Exajoule/year"
        pe1 = pd.Series(
            energy_system.primary_PJ["Coal Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        pe2 = pd.Series(
            energy_system.primary_PJ["Oil Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        pe3 = pd.Series(
            energy_system.primary_PJ["Gas Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule/year"
        pe1 = pd.Series(energy_system.primary_PJ["Coal Change"])
        pe2 = pd.Series(energy_system.primary_PJ["Oil Change"])
        pe3 = pd.Series(energy_system.primary_PJ["Gas Change"])

    footer_text = "Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Primary Energy accounts for fuels input to a national, or the world energy system, \
prior to conversion to electricity or combusted for non-electric purposes. For an \
explanation of Primary Energy, see https://www.worldenergydata.org/introduction/.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value

    chart.columngrouped(
        country,
        title,
        ylabel,
        footer_text,
        start_yr,
        color1,
        color2,
        color3,
        series1=pe1,
        series2=pe2,
        series3=pe3,
    )
    plt.savefig(
        os.path.join(fig_dir, "9 " + country + " pe sep ff change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: country_consump_elec_charts()
#
# Description:
# Controls plotting sequence of all charts displaying both EI and IEA data.
#
########################################################################################
def country_consumption_elec_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.
    ####################################################################################
    # FINAL ENERGY AND ELECTRICITY COMBINED: Shares for most recent year.
    ####################################################################################
    # Plot only Final Energy if electricity data is unavailable.
    if (
            energy_system.elecprod_TWh.empty
            or energy_system.elecprod_TWh["Total Country"].iloc[-1] == 0
    ):
        print(
            "Sum of Final Energy = "
            + str(sum(energy_system.consumption_final_shares["Value"]))
        )

        title = "Energy Consumption by Share for most recent year of data"
        title_addition = "Energy Consumption is also known as Total Final \
Consumption or Final Energy.\n\
This accounts for energy in the form that it's consumed."
        title1 = "Energy Consumption by share in year " + str(
            energy_system.consumption_PJ.index[-1]
        )
        footer_text = "Latest year of data shown as of June 2024. Data: IEA 2023 \
World Energy Balances,\n\
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances.\n\
For clarity: \
(1) Shares are rounded so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to \
the legend.\n\
For an explanation of Energy Consumption, see \
https://www.worldenergydata.org/introduction/. Consumption data labelled \
'Wind, solar etc' is a non-electric form of consumption, and may be too small \
to show.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

        chart.treemap1x1(
            energy_system.consumption_final_shares,
            title1,
            country,
            title,
            title_addition,
            footer_text,
        )
    else:
        print(
            "Sum of most recent year plotted IEA Energy Consumption shares = "
            + str(sum(energy_system.consumption_final_shares["Value"]))
        )
        print(
            "Sum of most recent year plotted Electricity shares = "
            + str(sum(energy_system.elecprod_final_fuel_shares["Value"]))
        )
        title = "Energy Consumption and Electricity Generation by Share for \
most recent year of data"
        title_addition = "Energy Consumption is also known as Total Final \
Consumption or Final Energy. This accounts for energy in the form that it's \
consumed."
        title1 = (
                "Energy Consumption by Share in year "
                + str(energy_system.consumption_PJ.index[-1])
                + "\n(Electricity shares are shown in the right-hand chart)"
        )
        title2 = "Electricity Generation by Share in year " + str(
            energy_system.elecprod_TWh.index[-1]
        )
        footer_text = "Latest years of data shown as of July 2024. Energy Consumption \
data: IEA 2023 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances.\n\
Electricity Generation data: The Energy Institute Statistical Review of World \
Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Electricity generation shares may not total 100% because for some small countries \
the Energy Institute doesn't publish this data for all fuels. \
Total generation is published, so this unpublished share is calculated, & shown \
in the RH chart if applicable.\n\
For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to \
the legend.\n\
For an explanation of Energy Consumption, see \
https://www.worldenergydata.org/introduction/. Consumption data labelled \
'Wind, solar etc' is a non-electric form of consumption, and may be too small \
to show.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

        chart.treemap1x2(
            energy_system.consumption_final_shares,
            energy_system.elecprod_final_fuel_shares,
            title1,
            title2,
            country,
            title,
            title_addition,
            footer_text,
        )
    plt.savefig(
        os.path.join(fig_dir, "10 " + country + " fe elec shares.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: country_consumption_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only IEA data.
#
########################################################################################
def country_consumption_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    start_yr = user_globals.Constant.CHART_START_YR.value

    ####################################################################################
    # FINAL ENERGY: Annual shares.
    ####################################################################################
    title = "Annual Energy Consumption by Share"
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"
    ylabel = "Annual Share (%)"
    footer_text = "Latest year of data as of June 2024 is 2021. Data: IEA 2023 World \
Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances.\n\
Quantities of coal, oil, gas, biofuels, and waste shown \
were consumed for purposes other than electricity generation, such as steel \
manufacture or internal combustion etc.\nAdditional fossil fuels were combusted \
to produce electricity. For an explanation of energy consumption, see \
https://www.worldenergydata.org/introduction/.\n\
By shanewhite@worldenergydata.org using \
Python, https://github.com/shanewhi/world-energy-data."

    fes1 = energy_system.consumption_PJ["Coal Share"]
    fes2 = energy_system.consumption_PJ["Oil Share"]
    fes3 = energy_system.consumption_PJ["Gas Share"]
    fes4 = energy_system.consumption_PJ["Biofuels and Waste Share"]
    fes5 = energy_system.consumption_PJ["Electricity Share"]
    fes6 = energy_system.consumption_PJ["Heat Share"]

    print(round(fes1, 1))
    print(round(fes2, 1))
    print(round(fes3, 1))
    print(round(fes4, 1))
    print(round(fes5, 1))
    print(round(fes6, 1))

    print(
        "Annual sum of IEA energy consumption shares = \n"
        + str(fes1 + fes2 + fes3 + fes4 + fes5 + fes6)
        + "\n"
    )

    chart.line2x3(
        fes1,
        fes2,
        fes3,
        fes4,
        fes5,
        fes6,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        country,
        title,
        title1,
        title2,
        title3,
        title4,
        title5,
        title6,
        start_yr,
        ylabel,
        footer_text,
        True,
    )
    plt.savefig(
        os.path.join(fig_dir, "11 " + country + " fe share trends.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # FINAL ENERGY: Annual quantities.
    ####################################################################################
    title = "Annual Energy Consumption"
    if country == "World":
        ylabel = "Exajoules"
        feq1 = pd.Series(
            energy_system.consumption_PJ["Coal"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq2 = pd.Series(
            energy_system.consumption_PJ["Oil"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq3 = pd.Series(
            energy_system.consumption_PJ["Gas"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq4 = pd.Series(
            energy_system.consumption_PJ["Biofuels and Waste"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        feq5 = pd.Series(
            energy_system.consumption_PJ["Electricity"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        feq6 = pd.Series(
            energy_system.consumption_PJ["Heat"] * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule"
        feq1 = energy_system.consumption_PJ["Coal"]
        feq2 = energy_system.consumption_PJ["Oil"]
        feq3 = energy_system.consumption_PJ["Gas"]
        feq4 = energy_system.consumption_PJ["Biofuels and Waste"]
        feq5 = energy_system.consumption_PJ["Electricity"]
        feq6 = energy_system.consumption_PJ["Heat"]

    footer_text = "Latest year of data as of June 2024 is 2021. Data: IEA 2023 World \
Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances.\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel manufacture or \
internal combustion etc.\nAdditional fossil fuels were combusted to produce \
electricity. For an explanation of energy consumption, see \
https://www.worldenergydata.org/introduction/.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    chart.column2x3(
        feq1,
        feq2,
        feq3,
        feq4,
        feq5,
        feq6,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        country,
        title,
        title1,
        title2,
        title3,
        title4,
        title5,
        title6,
        start_yr,
        ylabel,
        footer_text,
        True,
    )
    plt.savefig(
        os.path.join(fig_dir, "12 " + country + " fe qty.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################
    # FINAL ENERGY: Annual change.
    ####################################################################################
    title = "Annual Changes of Energy Consumption"
    if country == "World":
        ylabel = "Exajoule/year"
        fec1 = pd.Series(
            energy_system.consumption_PJ["Coal Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        fec2 = pd.Series(
            energy_system.consumption_PJ["Oil Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        fec3 = pd.Series(
            energy_system.consumption_PJ["Gas Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        fec4 = pd.Series(
            energy_system.consumption_PJ["Biofuels and Waste Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        fec5 = pd.Series(
            energy_system.consumption_PJ["Electricity Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        fec6 = pd.Series(
            energy_system.consumption_PJ["Heat Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel = "Petajoule/year"
        fec1 = pd.Series(energy_system.consumption_PJ["Coal Change"])
        fec2 = pd.Series(energy_system.consumption_PJ["Oil Change"])
        fec3 = pd.Series(energy_system.consumption_PJ["Gas Change"])
        fec4 = pd.Series(energy_system.consumption_PJ["Biofuels and Waste Change"])
        fec5 = pd.Series(energy_system.consumption_PJ["Electricity Change"])
        fec6 = pd.Series(energy_system.consumption_PJ["Heat Change"])

    if energy_system.name == "World":
        footer_text = (
                "Latest year of data as of June 2024 is 2021. Data: IEA 2023 World Energy \
    Balances, https://www.iea.org/data-and-statistics/data-product/world-energy-\
    statistics-and-balances. "
                + energy_system.name
                + " most recent year Total Energy Consumption (IEA, Total TFC) = "
                + str(
            int(
                energy_system.consumption_PJ["Total"].iloc[-1]
                * user_globals.Constant.PJ_TO_EJ.value
            )
        )
                + " EJ.\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel manufacture or \
internal combustion etc.\nAdditional fossil fuels were combusted to produce \
electricity. For an explanation of energy consumption, see \
https://www.worldenergydata.org/introduction/.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )
    else:
        footer_text = (
                "Latest year of data as of June 2024 is 2021. Data: IEA 2023 World Energy \
    Balances, https://www.iea.org/data-and-statistics/data-product/world-energy-\
    statistics-and-balances. "
                + energy_system.name
                + " most recent year Total Energy Consumption (IEA, Total TFC) = "
                + str(int(energy_system.consumption_PJ["Total"].iloc[-1]))
                + " PJ.\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel manufacture or \
internal combustion etc. Additional fossil fuels were combusted to produce \
electricity. For an explanation of energy consumption, see \
https://www.worldenergydata.org/introduction/.\n\
Values are rounded to nearest whole number. \
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )

    chart.columngrouped(
        country,
        title,
        ylabel,
        footer_text,
        start_yr,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        series1=fec1,
        series2=fec2,
        series3=fec3,
        series4=fec4,
        series5=fec5,
        series6=fec6,
    )
    plt.savefig(
        os.path.join(fig_dir, "13 " + country + " fe change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################
#
# Function: country_elec_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI electricity data.
#
########################################################################################
def country_elec_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    start_yr = user_globals.Constant.CHART_START_YR.value

    ####################################################################################
    # ELECTRICITY: Annual share of generation by category.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Shares of Categories in Electricity Generation"
        ylabel = "Annual Share (%)"
        title1 = "Fossil Fuels"
        title2 = "Nuclear"
        title3 = "Renewables"
        title4 = "Bio, Geo and Other"
        footer_text = (
                "Data: The Energy Institute Statistical Review of World Energy 2024, \
    https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
    Renewables is the sum of hydro, wind and solar. Shares are calculated using gross \
    generation quantities that don't account for imports or exports.\n\
    Shares may not total 100% because for some small countries the Energy Institute \
    doesn't publish electricity generation data for all fuels. \
    Total generation is published, so this unpublished share is calculated. \
    For "
                + country
                + ", the unpublished share in year "
                + str(energy_system.elecprod_TWh.index[-1])
                + " was "
                + str(round(energy_system.elecprod_TWh["Unpublished Share"].iloc[-1], 1))
                + "%.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )

        esc1 = energy_system.elecprod_TWh["Fossil Fuels Share"]
        esc2 = energy_system.elecprod_TWh["Nuclear Share"]
        esc3 = energy_system.elecprod_TWh["Renewables Share"]
        esc4 = energy_system.elecprod_TWh["Bio, Geo and Other Share"]

        print(round(esc1, 1))
        print(round(esc2, 1))
        print(round(esc3, 1))
        print(round(esc4, 1))
        print(
            "Annual sum of electricity generation category shares = \n"
            + str(esc1 + esc2 + esc3 + esc4)
            + "\n"
        )

        chart.line1x4(
            esc1,
            esc2,
            esc3,
            esc4,
            user_globals.Color.FOSSIL_FUELS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.RENEWABLES.value,
            user_globals.Color.OTHER.value,
            country,
            title,
            title1,
            title2,
            title3,
            title4,
            start_yr,
            ylabel,
            footer_text,
            True,
        )
        plt.savefig(
            os.path.join(fig_dir, "14 " + country + " elec cat share trends.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    ####################################################################################
    # ELECTRICITY: Annual share of generation by fuel.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Shares of Fuels in Electricity Generation"
        title1 = "Coal"
        title2 = "Oil"
        title3 = "Gas"
        title4 = "Nuclear"
        title5 = "Hydro"
        title6 = "Wind"
        title7 = "Solar"
        title8 = "Bio, Geo and Other"
        ylabel = "Annual Share (%)"
        footer_text = (
                "Data: The Energy Institute Statistical Review of World Energy \
    2024, \
    https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
    Shares are calculated using gross generation quantities that don't account for imports \
    or exports.\n\
    Shares may not total 100% because for some small countries the Energy Institute \
    doesn't publish electricity generation data for all fuels. \
    Total generation is published, so this unpublished share is calculated. \
    For "
                + country
                + ", the unpublished share in year "
                + str(energy_system.elecprod_TWh.index[-1])
                + " was "
                + str(round(energy_system.elecprod_TWh["Unpublished Share"].iloc[-1], 1))
                + "%.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )

        esf1 = energy_system.elecprod_TWh["Coal Share"]
        esf2 = energy_system.elecprod_TWh["Oil Share"]
        esf3 = energy_system.elecprod_TWh["Gas Share"]
        esf4 = energy_system.elecprod_TWh["Nuclear Share"]
        esf5 = energy_system.elecprod_TWh["Hydro Share"]
        esf6 = energy_system.elecprod_TWh["Wind Share"]
        esf7 = energy_system.elecprod_TWh["Solar Share"]
        esf8 = energy_system.elecprod_TWh["Bio, Geo and Other Share"]

        print(
            "Annual sum of electricity generation fuel shares = \n"
            + str(esf1 + esf2 + esf3 + esf4 + esf5 + esf6 + esf7 + esf8)
            + "\n"
        )

        chart.line2x4(
            esf1,
            esf2,
            esf3,
            esf4,
            esf5,
            esf6,
            esf7,
            esf8,
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND.value,
            user_globals.Color.SOLAR.value,
            user_globals.Color.OTHER.value,
            country,
            title,
            title1,
            title2,
            title3,
            title4,
            title5,
            title6,
            title7,
            title8,
            start_yr,
            ylabel,
            footer_text,
            True,
        )
        plt.savefig(
            os.path.join(fig_dir, "15 " + country + " elec fuel share trends.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    ####################################################################################
    # ELECTRICITY: Annual generation quantity by category.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Electricity Generation by Category"
        title1 = "Fossil Fuels"
        title2 = "Nuclear"
        title3 = "Renewables"
        title4 = "Bio, Geo and Other"
        ylabel = "TWh"
        footer_text = (
                "Data: The Energy Institute Statistical Review of World Energy \
    2024, \
    https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
    Renewables is the sum of hydro, wind and solar. Quantities are gross generation that \
    don't account for imports or exports.\n\
    For some small countries, the Energy Institute doesn't publish electricity generation \
    data for all fuels. For "
                + country
                + ", the unpublished generation in year "
                + str(energy_system.elecprod_TWh.index[-1])
                + " was "
                + str(round(energy_system.elecprod_TWh["Unpublished"].iloc[-1], 1))
                + "TWh.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )

        chart.column1x4(
            energy_system.elecprod_TWh["Fossil Fuels"],
            energy_system.elecprod_TWh["Nuclear"],
            energy_system.elecprod_TWh["Renewables"],
            energy_system.elecprod_TWh["Bio, Geo and Other"],
            user_globals.Color.FOSSIL_FUELS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.RENEWABLES.value,
            user_globals.Color.OTHER.value,
            country,
            title,
            title1,
            title2,
            title3,
            title4,
            start_yr,
            ylabel,
            footer_text,
            True,
        )
        plt.savefig(
            os.path.join(fig_dir, "16 " + country + " elec cat qty.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()
    ####################################################################################
    # ELECTRICITY: Annual generation quantity by fuel.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Electricity Generation by Fuel"
        title1 = "Coal"
        title2 = "Oil"
        title3 = "Gas"
        title4 = "Nuclear"
        title5 = "Hydro"
        title6 = "Wind"
        title7 = "Solar"
        title8 = "Bio, Geo and Other"
        ylabel = "TWh"
        footer_text = (
                "Data: The Energy Institute Statistical Review of World Energy \
    2024, \
    https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
    Quantities are gross generation that don't account for imports or exports.\n\
    For some small countries, the Energy Institute doesn't publish electricity generation \
    data for all fuels. For "
                + country
                + ", the unpublished generation in year "
                + str(energy_system.elecprod_TWh.index[-1])
                + " was "
                + str(round(energy_system.elecprod_TWh["Unpublished"].iloc[-1], 1))
                + "TWh.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."
        )

        chart.column2x4(
            energy_system.elecprod_TWh["Coal"],
            energy_system.elecprod_TWh["Oil"],
            energy_system.elecprod_TWh["Gas"],
            energy_system.elecprod_TWh["Nuclear"],
            energy_system.elecprod_TWh["Hydro"],
            energy_system.elecprod_TWh["Wind"],
            energy_system.elecprod_TWh["Solar"],
            energy_system.elecprod_TWh["Bio, Geo and Other"],
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND.value,
            user_globals.Color.SOLAR.value,
            user_globals.Color.OTHER.value,
            country,
            title,
            title1,
            title2,
            title3,
            title4,
            title5,
            title6,
            title7,
            title8,
            start_yr,
            ylabel,
            footer_text,
            True,
        )
        plt.savefig(
            os.path.join(fig_dir, "17 " + country + " elec fuel qty.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    ####################################################################################
    # ELECTRICITY: Annual change of generation by category.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Change of Categories in Electricity Generation"
        ylabel = "TWh/year"
        footer_text = "Data: The Energy Institute Statistical Review of World Energy \
2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Renewables is the sum of hydro, wind and solar. \
Values are rounded to nearest whole number. A zero value column refers to no change \
for that category.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

        chart.columngrouped(
            country,
            title,
            ylabel,
            footer_text,
            start_yr,
            user_globals.Color.FOSSIL_FUELS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.RENEWABLES.value,
            user_globals.Color.OTHER.value,
            series1=energy_system.elecprod_TWh["Fossil Fuels Change"],
            series2=energy_system.elecprod_TWh["Nuclear Change"],
            series3=energy_system.elecprod_TWh["Renewables Change"],
            series4=energy_system.elecprod_TWh["Bio, Geo and Other Change"],
        )
        plt.savefig(
            os.path.join(fig_dir, "18 " + country + " elec cat change.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    ####################################################################################
    # ELECTRICITY: Annual change of generation by fuel.
    ####################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Change of Fuels in Electricity Generation"
        ylabel = "TWh/year"
        footer_text = "Data: The Energy Institute Statistical Review of World Energy \
2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.\n\
Values are rounded to nearest whole number. Zeroes below x-axis refer to  values \
between -0.5 and 0 that have been rounded. A zero value column refers to no change \
for that fuel.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

        chart.columngrouped(
            country,
            title,
            ylabel,
            footer_text,
            start_yr,
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND_AND_SOLAR.value,
            user_globals.Color.OTHER.value,
            series1=energy_system.elecprod_TWh["Coal Change"],
            series2=energy_system.elecprod_TWh["Oil Change"],
            series3=energy_system.elecprod_TWh["Gas Change"],
            series4=energy_system.elecprod_TWh["Nuclear Change"],
            series5=energy_system.elecprod_TWh["Hydro Change"],
            series6=energy_system.elecprod_TWh["Wind and Solar Change"],
            series8=energy_system.elecprod_TWh["Bio, Geo and Other Change"],
        )
        plt.savefig(
            os.path.join(fig_dir, "19 " + country + " elec fuel change.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

        ####################################################################################
        # ELECTRICITY: As per above, but more recent start year.
        ####################################################################################
        title = "Recent Annual Change of Fuels in Electricity Generation"
        start_yr = 2010
        chart.columngrouped(
            country,
            title,
            ylabel,
            footer_text,
            start_yr,
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND_AND_SOLAR.value,
            user_globals.Color.OTHER.value,
            series1=energy_system.elecprod_TWh["Coal Change"],
            series2=energy_system.elecprod_TWh["Oil Change"],
            series3=energy_system.elecprod_TWh["Gas Change"],
            series4=energy_system.elecprod_TWh["Nuclear Change"],
            series5=energy_system.elecprod_TWh["Hydro Change"],
            series6=energy_system.elecprod_TWh["Wind and Solar Change"],
            series8=energy_system.elecprod_TWh["Bio, Geo and Other Change"],
        )
        plt.savefig(
            os.path.join(fig_dir, "20 " + country + " elec fuel change recent.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()
