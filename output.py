#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:20:13 2024

@author: shanewhite
"""

########################################################################################################################
#
# Module: output.py
#
# Description:
# Controls chart plotting sequence.
#
########################################################################################################################

# Import Python modules.
import matplotlib.pyplot as plt
import pandas as pd
import decimal
import os

# Import user modules.
import user_globals
import chart


########################################################################################################################
#
# Function: world_co2_charts()
#
# Description:
# Controls chart plotting of global carbon project data.
#
########################################################################################################################
def world_co2_charts(global_carbon):
    fig_dir = "charts CO2/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.
    ####################################################################################################################
    # Atmospheric CO2: Concentration and growth.
    ####################################################################################################################
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
    ylabel1 = "Parts per million (ppm)"
    ylabel2 = "Parts per million per year (ppm/yr)"
    concentration_text = (
            "Value for "
            + str(global_carbon.co2_conc.index[-1])
            + " = "
            + str(round(global_carbon.co2_conc["Mean"].iloc[-1], 1))
            + "ppm"
    )
    footer_text = "By Shane White, whitesha@protonmail.com using Python, \
https://github.com/shanewhi/world-energy-data.\n\
Lan, X., Tans, P. and K.W. Thoning: Trends in globally-averaged CO\u2082 determined from NOAA \
Global Monitoring Laboratory measurements. Version 2024-05 https://doi.org/10.15138/9N0H-ZH07.\n\
Data obtained from https://gml.noaa.gov/ccgg/trends/gl_data.html."
    chart.line_column(
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

    ####################################################################################################################
    # CO2 Emissions: Shares of sources for most recent year.
    ####################################################################################################################

    print(
        "CO2 emission treemap, most recent year sum of category shares = "
        + str(sum(global_carbon.final_emission_category_shares["Value"]))
        + "%. Note this is sum of values displayed in chart which are rounded."
    )
    print(
        "CO2 emission treemap, most recent year sum of emission shares = "
        + str(sum(global_carbon.final_emission_shares["Value"]))
        + "%. Note this is sum of values displayed in chart which are rounded."
    )

    country = global_carbon.name
    title = "CO\u2082 Emission Sources by Share"
    # Display for second to last year so as not to display a combination of projected and historic values.
    title_addition = "Year " + str(global_carbon.data["Total"].index[-2])
    title1 = "By Category"
    title2 = "By Emission Source"
    footer_text = ("Fossil Fuels is the sum of Coal, Oil, Gas, and Flaring. \
Labels may not be shown due to a lack of space, so refer to the legend. \
Projected values of Flaring and Other for "
                   + str(global_carbon.data["Total"].index[-1]) +
                   " are unavailable. "
                   + str(global_carbon.data["Total"].index[-2]) +
                   " data is shown. 'Cement' includes cement carbonation.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html.")
    chart.treemap_2_subplots(
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

    ####################################################################################################################
    # CO2 Emissions: Annual Fossil Fuels + Cement
    ####################################################################################################################
    ffc_co2 = global_carbon.data["Net FF and Cement"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    country = "World"
    start_yr1 = min(ffc_co2.index)
    start_yr2 = user_globals.Constant.CHART_START_YR.value
    title = "Annual CO\u2082 Emissions from Fossil Fuels and Cement"
    title1 = str(start_yr1) + " - " + str(max(ffc_co2.index))
    title2 = (
            str(user_globals.Constant.CHART_START_YR.value)
            + " - "
            + str(ffc_co2.index.max())
    )

    x_axis1_interval = 50
    x_axis2_interval = 10
    ylabel = "Megatonne (Mt)"
    latest_value_text = (
            "Projected value for "
            + str(ffc_co2.index[-1])
            + " = "
            + f"{(round(ffc_co2.iloc[-1], 0)):,}".rstrip("0").rstrip(".")
            + "MtCO\u2082"
    )
    footer_text = "Values include cement carbonation and 2024 value is projected. \
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html."

    print(
        "Most recent fossil fuel and cement CO2 emission = "
        + str(round(ffc_co2.iloc[-1], 1))
        + " MtCO2\n"
    )

    chart.column_2_subplots(
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
        latest_value_text,
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

    ####################################################################################################################
    # CO2 Emissions: Annual change.
    ####################################################################################################################
    series = global_carbon.data["Net FF and Cement Change"]
    title = "Annual Change of CO\u2082 Emissions from Fossil Fuels and Cement"
    ylabel = "Megatonne per year (Mt/yr)"
    footer_text = ("Values are rounded to nearest whole number and include cement carbonation. \
2024 values is projected. \
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html.")
    color = user_globals.Color.CO2_EMISSION.value

    chart.column_grouped(
        country,
        title,
        ylabel,
        footer_text,
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

    ####################################################################################################################
    # CO2 Emissions: Annual Coal, Oil, and Gas.
    ####################################################################################################################
    coalco2 = global_carbon.data["Coal"]
    oilco2 = global_carbon.data["Oil"]
    gasco2 = global_carbon.data["Gas"]
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    country = "World"
    title = "Annual Fossil Fuel CO\u2082 Emissions"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    x_axis_interval = 25
    ylabel = "Megatonne (Mt)"
    footer_text = ("By Shane White, whitesha@protonmail.com using Python, \
https://github.com/shanewhi/world-energy-data.\n\
2024 values are projected by the Global Carbon Project: Emissions from coal, oil and gas in 2024 are expected to be \
above their 2023 levels by 0.2%, 0.9% and 2.4% respectively. \
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html.")
    equiv_yscale = True
    start_yr = global_carbon.data.index.min()

    chart.column_3_subplots(
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
        ylabel,
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


########################################################################################################################
#
# Function: country_co2_charts()
#
# Description:
# Plots national CO2 emissions from fossil fuel combustion
#
########################################################################################################################
def country_co2_charts(energy_system, global_carbon):
    country = energy_system.name

    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    ####################################################################################################################
    # CO2 Emissions from fossil fuel combustion.
    ####################################################################################################################

    ffco2 = energy_system.ffco2["Value"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    x_interval = 10
    ylabel = "Megatonne (Mt)"

    title1 = "Fossil Fuel CO\u2082 Emissions"
    title2 = "Fossil Fuel CO\u2082 Emissions by National Share"
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
Segments excluding 'Other' represent\ncountries with a "
            + str(user_globals.Constant.CO2_SHARE_RANK_THRESHOLD.value)
            + "% or greater share,\nof which there were "
            + str(len(global_carbon.final_country_shares) - 1)
            + ", totalling "
            + str(large_emitter_share_total)
            + "%.\n\n\nLabelled segments are those with a 1%\nor greater share, of which there were\n"
            + str(len(global_carbon.final_country_shares[global_carbon.final_country_shares["Value"] >= 1]) - 1)
            # Subtract 1 above so as not to include 'Other'.
            + ", totalling "
            + str(one_percent_countries_share)
            + "%.\n\n\nUnlabelled segments in lower\nright corner are listed below. \
These\nhad shares greater than or equal\nto 0.5%, and less than 1% -\n\n"
            + s
    )

    footer_text = (str(ffco2.index[-1]) + " fossil fuel CO\u2082 emissions = " +
                   f"{(round(ffco2.values[-1], 1)):,}" + "Mt\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024,\n\
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

    chart.column_treemap(
        ffco2,
        global_carbon.final_country_shares,
        co2_color,
        country,
        title1,
        title2,
        subplot1_title,
        subplot2_title,
        user_globals.Constant.CHART_START_YR.value,
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

    ffco2_change = energy_system.ffco2["Emissions Change"]
    co2_color = user_globals.Color.CO2_EMISSION.value
    title = "Annual Change of Fossil Fuel CO\u2082 Emissions"
    ylabel = "Megatonne per year (Mt/yr)"
    footer_text = "Values are rounded to nearest whole number. \
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    chart.column_grouped(
        country,
        title,
        ylabel,
        footer_text,
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


########################################################################################################################
#
# Function: world_ffprod_charts()
#
# Description:
# Controls plotting of global fossil fuel production shares by country.
#
########################################################################################################################
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
    coal_prod_total_shares = 100 - round(decimal.Decimal(coal_prods.loc[coal_prods["Name"] == "Other"].Value.item()), 1)
    oil_prod_total_shares = 100 - round(decimal.Decimal(oil_prods.loc[oil_prods["Name"] == "Other"].Value.item()), 1)
    gas_prod_total_shares = 100 - round(decimal.Decimal(gas_prods.loc[gas_prods["Name"] == "Other"].Value.item()), 1)

    # Generate list of countries with production shares greater than list above. Use Python data class Set that doesn't
    # allow duplicates; no need to use for loops.
    country_list = set(coal_prods.Name)
    country_list.update(oil_prods.Name)
    country_list.update(gas_prods.Name)
    # Remove 'Other', sort list into alphabetical order and add commas between set elements.
    country_list.remove("Other")
    country_list = sorted(country_list)
    list_divider = ", "
    printable_country_list = list_divider.join(country_list)
    num_prod_countries = len(country_list)
    print(num_prod_countries)
    print(printable_country_list)
    country = "World"
    title = "Fossil Fuel Production by National Share"
    title_addition = "Year " + str(coal_prods.loc[0, "Year"])
    # Title above LH plot
    subplot1_title = "Coal Producers with ≥" + str(user_globals.Constant.COAL_SHARE_RANK_THRESHOLD.value) + "% share"
    # Title above centre plot
    subplot2_title = "Oil Producers with ≥" + str(user_globals.Constant.OIL_SHARE_RANK_THRESHOLD.value) + "% share"
    # Title above RH plot
    subplot3_title = "Gas Producers with ≥" + str(user_globals.Constant.GAS_SHARE_RANK_THRESHOLD.value) + "% share"

    footer_upper_text = ("The " + str(
        num_prod_countries) + " countries listed below were the fossil fuel producers in " +
                         str(coal_prods.loc[0, "Year"]) +
                         " that produced a " + str(user_globals.Constant.COAL_SHARE_RANK_THRESHOLD.value) +
                         "% or greater share of global coal, \
and/or a " + str(user_globals.Constant.OIL_SHARE_RANK_THRESHOLD.value) + "% or greater share of global oil, and/or a " +
                         str(user_globals.Constant.GAS_SHARE_RANK_THRESHOLD.value) +
                         "% or greater share of global gas.\n\
Collectively their production accounted for " +
                         str(round(coal_prod_total_shares, 0)) + "% of global coal, " +
                         str(round(oil_prod_total_shares, 0)) + "% of global oil, and " +
                         str(round(gas_prod_total_shares, 0)) + "% global gas: \n" +
                         printable_country_list) + "."

    footer_lower_text = "All numerical and textual results of this chart have been computed. Ranking of producers \
determined using fossil fuel production data in following units: Coal EJ, Oil Mt, and Gas EJ. \
Oil production in units of Mt is used instead of kbd because it's in closer agreement with IEA data.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    chart.treemap_3_subplots(
        coal_prods,  # Dataframe 1
        oil_prods,  # Dataframe 2
        gas_prods,  # Dataframe 3
        subplot1_title,  # Title above LH plot
        subplot2_title,  # Title above centre plot
        subplot3_title,  # Title above RH plot
        country,
        title,
        title_addition,
        footer_upper_text,
        footer_lower_text,
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


########################################################################################################################
#
# Function: country_prod_primary_energy_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI energy data.
#
########################################################################################################################
def country_prod_primary_energy_charts(energy_system):
    country = energy_system.name

    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save charts in this directory.

    ####################################################################################################################
    # PRODUCTION: Annual Fossil Fuel Production.
    ####################################################################################################################
    if country == "World":
        ylabel = "Exajoule (EJ)"
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
        ylabel = "Petajoule (PJ)"
        ffprod_coal = energy_system.ffprod_PJ["Coal"]
        ffprod_oil = energy_system.ffprod_PJ["Oil"]
        ffprod_gas = energy_system.ffprod_PJ["Gas"]

    title = "Annual Fossil Fuel Production"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"

    if country == "World":
        footer_text = "Oil production calculated by converting units of Mt to joules using EI's approximate \
conversion factor of 41.868 GJ/toe. Production data for coal and gas provided in units of joules. \
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."
    else:
        footer_text = "For comparison, EI(2024) listed 2023 World production values as: Coal 179,000 PJ, \
Oil 197,000 PJ, and Gas 146,000 PJ.\n\
Oil production calculated by converting units of Mt to joules using EI's approximate conversion factor of \
41.868 GJ/toe. Production data for coal and gas provided in units of joules. \
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: The Energy Institute Statistical Review of World Energy 2024 (EI(2024)), \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    x_axis_interval = 5
    equiv_scale = True

    chart.column_3_subplots(
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

    ####################################################################################################################
    # PRIMARY ENERGY: Annual quantity of fossil fuels.
    ####################################################################################################################
    title = "Annual Fossil Fuel Consumption prior to partial conversions to Electricity (Primary Energy)"
    if country == "World":
        ylabel = "Exajoule (EJ)"
        peq1 = pd.Series(
            energy_system.primary_PJ["Coal"] * user_globals.Constant.PJ_TO_EJ.value
        )
        peq2 = pd.Series(
            energy_system.primary_PJ["Oil"] * user_globals.Constant.PJ_TO_EJ.value
        )
        peq3 = pd.Series(
            energy_system.primary_PJ["Gas"] * user_globals.Constant.PJ_TO_EJ.value
        )
        footer_text = (str(energy_system.primary_PJ.index[-1])
                       + " values: "
                       + "Coal = "
                       + f"{(round(energy_system.primary_PJ["Coal"].iloc[-1] *
                                   user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ, Oil = "
                       + f"{(round(energy_system.primary_PJ["Oil"].iloc[-1] * user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ, Gas = "
                       + f"{(round(energy_system.primary_PJ["Gas"].iloc[-1] * user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ. A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid \
line at zero.\n\
For an explanation of Primary Energy, see https://www.worldenergydata.org/introduction/. \
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."
                       )
    else:
        ylabel = "Petajoule (PJ)"
        peq1 = pd.Series(energy_system.primary_PJ["Coal"])
        peq2 = pd.Series(energy_system.primary_PJ["Oil"])
        peq3 = pd.Series(energy_system.primary_PJ["Gas"])
        subplot1_title = "Coal"
        subplot2_title = "Oil"
        subplot3_title = "Gas"
        footer_text = (str(energy_system.primary_PJ.index[-1])
                       + " values: "
                       + "Coal = "
                       + f"{(round(energy_system.primary_PJ["Coal"].iloc[-1])):,}"
                       + "PJ, Oil = "
                       + f"{(round(energy_system.primary_PJ["Oil"].iloc[-1])):,}"
                       + "PJ, Gas = "
                       + f"{(round(energy_system.primary_PJ["Gas"].iloc[-1])):,}"
                       + "PJ. A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid \
line at zero.\n\
For an explanation of Primary Energy, see https://www.worldenergydata.org/introduction/. \
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."
                       )

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    x_axis_interval = 10
    equiv_yscale = True

    chart.column_3_subplots(
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
        os.path.join(fig_dir, "5 " + country + " pe ff qty.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################################################
    # PRIMARY ENERGY: Annual change of fossil fuels.
    ####################################################################################################################
    title = "Annual Change of Fossil Fuel Consumption prior to partial conversions to Electricity (Primary Energy)"
    if country == "World":
        ylabel_top = "Exajoule per year (EJ/yr)"
        ylabel_bottom = "EJ/yr"
        pec = pd.Series(
            energy_system.primary_PJ["Fossil Fuels Change"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
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
        ylabel_top = "Petajoule per year (PJ/yr)"
        ylabel_bottom = "PJ/yr"
        pec = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"])
        pe1 = pd.Series(energy_system.primary_PJ["Coal Change"])
        pe2 = pd.Series(energy_system.primary_PJ["Oil Change"])
        pe3 = pd.Series(energy_system.primary_PJ["Gas Change"])

    footer_text = "Values are rounded to nearest whole number, and those 0.5 or less are displayed as zero, \
so column values in upper chart may not equal total of those in lower chart for a given year.\n\
For an explanation of Primary Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    color_category = user_globals.Color.FOSSIL_FUELS.value
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value

    chart.column_grouped_2_subplots(
        country,
        title,
        ylabel_top,
        ylabel_bottom,
        footer_text,
        color_category,
        pec,
        color1,
        color2,
        color3,
        series1=pe1,
        series2=pe2,
        series3=pe3,
    )
    plt.savefig(
        os.path.join(fig_dir, "6 " + country + " pe sep ff change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################################################
#
# Function: country_consump_elec_charts()
#
# Description:
# Controls plotting sequence of all charts displaying both EI and IEA data.
#
########################################################################################################################
def country_consumption_elec_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.
    ####################################################################################################################
    # FINAL ENERGY AND ELECTRICITY COMBINED: Shares for most recent year.
    ####################################################################################################################
    # Plot only Final Energy if electricity data is unavailable.
    if (
            energy_system.elecprod_TWh.empty
            or energy_system.elecprod_TWh["Total Country"].iloc[-1] == 0
    ):
        print(
            "Sum of Final Energy = "
            + str(sum(energy_system.consumption_final_shares["Value"]))
        )

        title = "Energy Consumption after partial conversions to Electricity (Final Energy)"
        title_addition = "Shares shown in the form that energy is consumed, for most recent year of data for \
respective dataset."
        title1 = "ENERGY Consumption by Share in year " + str(
            energy_system.consumption_PJ.index[-1]
        )
        footer_text = "For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to the legend.\n\
'Wind, solar etc' in the IEA dataset refers to a non-electric form, and usually too small to show.\n\
Shares of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
For an explanation of Final Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Energy Consumption data: IEA 2024 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-and-balances. Latest year shown."

        chart.treemap_1_subplot(
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
        title = "Energy Consumption after partial conversions to Electricity (Final Energy), & Electricity \
Generation"
        title_addition = "Shares shown in the form that energy is consumed, for most recent year of data for \
respective dataset."
        title1 = (
                "Energy Consumption by Share in year "
                + str(energy_system.consumption_PJ.index[-1])
                + "\n(Shares of fuels used for Electricity Generation are shown in adjacent chart)"
        )
        title2 = "Electricity Generation by Share in year " + str(
            energy_system.elecprod_TWh.index[-1]
        )
        footer_text = "For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to the legend.\n\
'Wind, solar etc' in the IEA dataset used for the LH chart refers to a non-electric form, and usually too small to \
show.\n\
For some countries, shares of electricity generation may not total 100% due to unavailability of data for some fuels. \
Total generation is published, so any such unpublished share is calculated, & shown in the RH chart if applicable.\n\
Shares of coal, oil, gas, biofuels, and waste shown in the LH chart were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
For an explanation of Final Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Energy Consumption data: IEA 2024 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-and-balances. Latest year shown.\n\
Electricity Generation data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

        chart.treemap_2_subplots(
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
        os.path.join(fig_dir, "9 " + country + " fe elec shares.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################################################
#
# Function: country_consumption_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only IEA data.
#
########################################################################################################################
def country_consumption_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    ####################################################################################################################
    # FINAL ENERGY: Annual quantities.
    ####################################################################################################################
    title = "Annual Energy Consumption after partial conversions to Electricity (Final Energy)"
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"
    if country == "World":
        ylabel_top = "Exajoule (EJ)"
        ylabel_bottom = "EJ"
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
        ylabel_top = "Petajoule (PJ)"
        ylabel_bottom = "PJ"
        feq1 = energy_system.consumption_PJ["Coal"]
        feq2 = energy_system.consumption_PJ["Oil"]
        feq3 = energy_system.consumption_PJ["Gas"]
        feq4 = energy_system.consumption_PJ["Biofuels and Waste"]
        feq5 = energy_system.consumption_PJ["Electricity"]
        feq6 = energy_system.consumption_PJ["Heat"]

    footer_text = "Quantities of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero. \
For an explanation of Final Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: IEA 2024 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-and-balances."

    chart.column_6_subplots(
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
        user_globals.Constant.CHART_START_YR.value,
        ylabel_top,
        ylabel_bottom,
        footer_text,
        True,
    )
    plt.savefig(
        os.path.join(fig_dir, "7 " + country + " fe qty.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################################################
    # FINAL ENERGY: Annual change.
    ####################################################################################################################
    title = "Annual Change of Energy Consumption after partial conversions to Electricity (Final Energy)"
    if country == "World":
        ylabel = "Exajoule per year (EJ/yr)"
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
        ylabel = "Petajoule per year (PJ/yr)"
        fec1 = pd.Series(energy_system.consumption_PJ["Coal Change"])
        fec2 = pd.Series(energy_system.consumption_PJ["Oil Change"])
        fec3 = pd.Series(energy_system.consumption_PJ["Gas Change"])
        fec4 = pd.Series(energy_system.consumption_PJ["Biofuels and Waste Change"])
        fec5 = pd.Series(energy_system.consumption_PJ["Electricity Change"])
        fec6 = pd.Series(energy_system.consumption_PJ["Heat Change"])

    if energy_system.name == "World":
        footer_text = (str(energy_system.consumption_PJ.index[-1])
                       + " "
                       + energy_system.name
                       + " total Final Energy = "
                       + f"{(round(energy_system.consumption_PJ["Total"].iloc[-1] *
                                   user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + " EJ. \
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc. \
For an explanation of Final Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: IEA 2024 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-and-balances."
                       )
    else:
        footer_text = (str(energy_system.consumption_PJ.index[-1])
                       + " "
                       + energy_system.name
                       + " total Final Energy = "
                       + f"{(round(energy_system.consumption_PJ["Total"].iloc[-1])):,}"
                       + " PJ. \
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc. \
For an explanation of Final Energy, see https://www.worldenergydata.org/introduction/.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: IEA 2024 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-statistics-and-balances."
                       )

    chart.column_grouped(
        country,
        title,
        ylabel,
        footer_text,
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
        os.path.join(fig_dir, "8 " + country + " fe change.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################################################
#
# Function: country_elec_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI electricity data.
#
########################################################################################################################
def country_elec_charts(energy_system):
    country = energy_system.name
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    ################################################################################################################
    # ELECTRICITY: Annual generation quantity.
    ################################################################################################################
    if country == "World" or country == "China" or country == "India" or country == "US":
        if (
                not energy_system.elecprod_TWh.empty
                and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
        ):
            title = "Annual Electricity Generation"
            title1 = "Total"
            title2 = "Nuclear"
            title3 = "Fossil Fuels"
            title4 = "Coal"
            title5 = "Oil"
            title6 = "Gas"
            title7 = "Bio, Geo and Other"
            title8 = "Renewables"
            title9 = "Hydro"
            title10 = "Wind"
            title11 = "Solar"
            ylabel_top = "Petawatt hours (PWh)"
            ylabel = "PWh"

            footer_text = ("Total electricity generation in "
                           + str(energy_system.elecprod_PWh.index[-1]) +
                           " = " +
                           f"{(round(energy_system.elecprod_PWh["Total Country"].iloc[-1], 1)):,}" +
                           "PWh. Value rounded. 1PWh = 1,000TWh.\n\
In some instances, summation of fuel quantities may not equal 'Total', due to unavailability of data for some fuels. \
Any such difference is calculated here:\nFor "
                           + country
                           + ", the unpublished quantity in year "
                           + str(energy_system.elecprod_PWh.index[-1])
                           + " was "
                           + f"{(round(energy_system.elecprod_PWh["Unpublished"].iloc[-1], 2)):,}"
                           + "PWh, or "
                           + str(round(energy_system.elecprod_TWh["Unpublished Share"].iloc[-1], 2))
                           + "%.\n\
Total = Fossil Fuels + Renewables + Nuclear + Bio, Geo and Other + any unpublished quantity above. \
Fossil Fuels = Coal + Oil + Gas.\nRenewables = Hydro + Wind + Solar. \
Quantities are gross generation that don't account for imports or exports.\n\
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

            chart.column_11_subplots(
                energy_system.elecprod_PWh["Total Country"],
                energy_system.elecprod_PWh["Nuclear"],
                energy_system.elecprod_PWh["Fossil Fuels"],
                energy_system.elecprod_PWh["Coal"],
                energy_system.elecprod_PWh["Oil"],
                energy_system.elecprod_PWh["Gas"],
                energy_system.elecprod_PWh["Bio, Geo and Other"],
                energy_system.elecprod_PWh["Renewables"],
                energy_system.elecprod_PWh["Hydro"],
                energy_system.elecprod_PWh["Wind"],
                energy_system.elecprod_PWh["Solar"],
                user_globals.Color.ELECTRICITY.value,
                user_globals.Color.NUCLEAR.value,
                user_globals.Color.FOSSIL_FUELS.value,
                user_globals.Color.COAL.value,
                user_globals.Color.OIL.value,
                user_globals.Color.GAS.value,
                user_globals.Color.OTHER.value,
                user_globals.Color.RENEWABLES.value,
                user_globals.Color.HYDRO.value,
                user_globals.Color.WIND.value,
                user_globals.Color.SOLAR.value,
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
                title9,
                title10,
                title11,
                user_globals.Constant.CHART_START_YR.value,
                ylabel_top,
                ylabel,
                footer_text,
                True,
            )
    else:
        if (
                not energy_system.elecprod_TWh.empty
                and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
        ):
            title = "Annual Electricity Generation"
            title1 = "Total"
            title2 = "Nuclear"
            title3 = "Fossil Fuels"
            title4 = "Coal"
            title5 = "Oil"
            title6 = "Gas"
            title7 = "Bio, Geo and Other"
            title8 = "Renewables"
            title9 = "Hydro"
            title10 = "Wind"
            title11 = "Solar"
            ylabel_top = "Terawatt hours (TWh)"
            ylabel = "TWh"
            footer_text = ("Total electricity generation in "
                           + str(energy_system.elecprod_TWh.index[-1]) +
                           " = " +  # Round and remove trailing zero.
                           f"{(round(energy_system.elecprod_TWh
                                     ["Total Country"].iloc[-1], 0)):,}".rstrip("0").rstrip(".") +
                           "TWh. Value rounded.\n\
In some instances, summation of fuel quantities may not equal 'Total', due to unavailability of data for some fuels. \
Any such difference is calculated here:\nFor "
                           + country
                           + ", the unpublished quantity in year "
                           + str(energy_system.elecprod_TWh.index[-1])
                           + " was "
                           + f"{(round(energy_system.elecprod_TWh["Unpublished"].iloc[-1], 2)):,}"
                           + "TWh, or "
                           + str(round(energy_system.elecprod_TWh["Unpublished Share"].iloc[-1], 2))
                           + "%.\n\
Total = Fossil Fuels + Renewables + Nuclear + Bio, Geo and Other + any unpublished quantity above. \
Fossil Fuels = Coal + Oil + Gas.\nRenewables = Hydro + Wind + Solar. \
Quantities are gross generation that don't account for imports or exports.\n\
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

            chart.column_11_subplots(
                energy_system.elecprod_TWh["Total Country"],
                energy_system.elecprod_TWh["Nuclear"],
                energy_system.elecprod_TWh["Fossil Fuels"],
                energy_system.elecprod_TWh["Coal"],
                energy_system.elecprod_TWh["Oil"],
                energy_system.elecprod_TWh["Gas"],
                energy_system.elecprod_TWh["Bio, Geo and Other"],
                energy_system.elecprod_TWh["Renewables"],
                energy_system.elecprod_TWh["Hydro"],
                energy_system.elecprod_TWh["Wind"],
                energy_system.elecprod_TWh["Solar"],
                user_globals.Color.ELECTRICITY.value,
                user_globals.Color.NUCLEAR.value,
                user_globals.Color.FOSSIL_FUELS.value,
                user_globals.Color.COAL.value,
                user_globals.Color.OIL.value,
                user_globals.Color.GAS.value,
                user_globals.Color.OTHER.value,
                user_globals.Color.RENEWABLES.value,
                user_globals.Color.HYDRO.value,
                user_globals.Color.WIND.value,
                user_globals.Color.SOLAR.value,
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
                title9,
                title10,
                title11,
                user_globals.Constant.CHART_START_YR.value,
                ylabel_top,
                ylabel,
                footer_text,
                True,
            )
    plt.savefig(
        os.path.join(fig_dir, "10 " + country + " elec fuel qty.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    ####################################################################################################################
    # ELECTRICITY: Annual change of generation by fuel.
    ####################################################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = "Annual Change of Electricity Generation"
        ylabel_top = "Terawatt hours per year (TWh/yr)"
        ylabel_bottom = "TWh/yr"
        footer_text = ("Values are rounded to nearest whole number, and those 0.5 or less are displayed as zero, \
so column values in upper chart may not equal total of those in lower chart for a given year. 1TWh = 0.1PWh.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        chart.column_grouped_2_subplots(
            country,
            title,
            ylabel_top,
            ylabel_bottom,
            footer_text,
            user_globals.Color.FOSSIL_FUELS.value,
            energy_system.elecprod_TWh["Fossil Fuels Change"],
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
            os.path.join(fig_dir, "11 " + country + " elec fuel change.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

  ####################################################################################################################
    # ELECTRICITY: Annual share of generation by fuel.
    ####################################################################################################################
    if (
            not energy_system.elecprod_TWh.empty
            and energy_system.elecprod_TWh["Total Country"].iloc[-1] != 0
    ):
        title = ("Annual Electricity Generation by Share (" + str(energy_system.elecprod_TWh.index[-1]) +
                 " values shown after title of each plot, rounded)")
        title1 = ("Nuclear, " +
                  f"{(round(energy_system.elecprod_TWh["Nuclear Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".") + "%")
        title2 = ("Fossil Fuels, " +
                  f"{(round(energy_system.elecprod_TWh["Fossil Fuels Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title3 = ("Coal, " +
                  f"{(round(energy_system.elecprod_TWh["Coal Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title4 = ("Oil, " +
                  f"{(round(energy_system.elecprod_TWh["Oil Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title5 = ("Gas, " +
                  f"{(round(energy_system.elecprod_TWh["Gas Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title6 = ("Bio, Geo and Other, " +
                  f"{(round(energy_system.elecprod_TWh["Bio, Geo and Other Share"].iloc[-1], 0)):,}"
                  .rstrip("0").rstrip(".")
                  + "%")
        title7 = ("Renewables, " +
                  f"{(round(energy_system.elecprod_TWh["Renewables Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title8 = ("Hydro, " +
                  f"{(round(energy_system.elecprod_TWh["Hydro Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title9 = ("Wind, " +
                  f"{(round(energy_system.elecprod_TWh["Wind Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                  + "%")
        title10 = ("Solar, " +
                   f"{(round(energy_system.elecprod_TWh["Solar Share"].iloc[-1], 0)):,}".rstrip("0").rstrip(".")
                   + "%")
        ylabel = "Annual Share (%)"
        footer_text = ("For some countries, shares may not total 100% due to unavailability of data for some fuels. \
Total generation is published, so any unpublished share is calculated here: For "
                       + country
                       + ", the unpublished share in year "
                       + str(energy_system.elecprod_TWh.index[-1])
                       + " was "
                       + str(round(energy_system.elecprod_TWh["Unpublished Share"].iloc[-1], 1))
                       + "%.\n\
Total (100%) = Fossil Fuels + Renewables + Nuclear + Bio, Geo and Other + any unpublished share above. \
Fossil Fuels = Coal + Oil + Gas. Renewables = Hydro + Wind + Solar.\n\
Shares are calculated using gross generation quantities that don't account for imports or exports. While geothermal is \
renewable, the data groups geothermal with biofuels that may not be renewable.\n\
By Shane White, whitesha@protonmail.com using Python, https://github.com/shanewhi/world-energy-data. \
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        elec_share1 = energy_system.elecprod_TWh["Nuclear Share"]
        elec_share2 = energy_system.elecprod_TWh["Fossil Fuels Share"]
        elec_share3 = energy_system.elecprod_TWh["Coal Share"]
        elec_share4 = energy_system.elecprod_TWh["Oil Share"]
        elec_share5 = energy_system.elecprod_TWh["Gas Share"]
        elec_share6 = energy_system.elecprod_TWh["Bio, Geo and Other Share"]
        elec_share7 = energy_system.elecprod_TWh["Renewables Share"]
        elec_share8 = energy_system.elecprod_TWh["Hydro Share"]
        elec_share9 = energy_system.elecprod_TWh["Wind Share"]
        elec_share10 = energy_system.elecprod_TWh["Solar Share"]

        print(
            "Annual sum of electricity generation fuel shares = \n"
            + str(
                elec_share1 + elec_share2 + elec_share3 + elec_share4 + elec_share5 + elec_share6 + elec_share7 +
                elec_share8 + elec_share9 + elec_share10)
            + "\n"
        )

        chart.line_10_subplots(
            elec_share1,
            elec_share2,
            elec_share3,
            elec_share4,
            elec_share5,
            elec_share6,
            elec_share7,
            elec_share8,
            elec_share9,
            elec_share10,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.FOSSIL_FUELS.value,
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.OTHER.value,
            user_globals.Color.RENEWABLES.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND.value,
            user_globals.Color.SOLAR.value,
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
            title9,
            title10,
            user_globals.Constant.CHART_START_YR.value,
            ylabel,
            footer_text,
            True,
        )

        plt.savefig(
            os.path.join(fig_dir, "12 " + country + " elec fuel share trends.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

