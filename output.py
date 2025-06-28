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
# Controls plotting of atmospheric CO2 data and global carbon budget.
#
########################################################################################################################
def world_co2_charts(global_carbon):
    fig_dir = "charts CO2/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    # CHART 1: Annual atmospheric CO2 concentration and growth.
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
    footer_text = "Lan, X., Tans, P. and K.W. Thoning: Trends in globally-averaged CO\u2082 determined from NOAA \
Global Monitoring Laboratory measurements. Version 2024-05 https://doi.org/10.15138/9N0H-ZH07.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: https://gml.noaa.gov/ccgg/trends/gl_data.html."
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

    # CHART 2: Annual CO2 emissions shares of sources for most recent year (not only fossil fuel CO2 emissions).
    print(
        "CO2 emission treemap, most recent year sum of category shares = "
        + str(sum(global_carbon.emission_category_shares_fy["Value"]))
        + "%. Note this is sum of values displayed in chart which are rounded."
    )
    print(
        "CO2 emission treemap, most recent year sum of emission shares = "
        + str(sum(global_carbon.emission_source_shares_fy["Value"]))
        + "%. Note this is sum of values displayed in chart which are rounded."
    )

    country = global_carbon.name
    title = "CO\u2082 Emission Sources by Share"
    # Display for second to last year so as not to display a combination of projected and historic values.
    title_addition = "Year " + str(global_carbon.c_budget["Total"].index[-2])
    title1 = "By Category"
    title2 = "By Emission Source"
    footer_text = ("Fossil Fuels is the sum of Coal, Oil, Gas, and Flaring. \
Projected values of Flaring and Other for "
                   + str(global_carbon.c_budget["Total"].index[-1]) +
                   " are unavailable. "
                   + str(global_carbon.c_budget["Total"].index[-2]) +
                   " data is shown. 'Cement' includes cement carbonation.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html.")
    chart.treemap_2_subplots(
        global_carbon.emission_category_shares_fy,
        global_carbon.emission_source_shares_fy,
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

    # CHART 3: Annual fossil fuels and cement CO2 emissions.
    ffc_co2 = global_carbon.c_budget["Net FF and Cement"]
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
    footer_text = "Values include cement carbonation and 2024 value is projected.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
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

    # CHART 4: Annual change of fossil fuels and cement CO2 emissions.
    series = global_carbon.c_budget["Net FF and Cement Change"]
    title = "Annual Change of CO\u2082 Emissions from Fossil Fuels and Cement"
    ylabel = "Megatonne per year (Mt/yr)"
    footer_text = ("Values are rounded to nearest whole number and include cement carbonation. \
2024 values is projected.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
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

    # CHART 5: Annual coal, oil and gas CO2 emissions.
    coalco2 = global_carbon.c_budget["Coal"]
    oilco2 = global_carbon.c_budget["Oil"]
    gasco2 = global_carbon.c_budget["Gas"]
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
    footer_text = ("2024 values are projected by the Global Carbon Project: Emissions from coal, oil and gas in 2024 \
are expected to be above their 2023 levels by 0.2%, 0.9% and 2.4% respectively.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: Global Carbon Project, Friedlingstein et al (2024), https://globalcarbonbudgetdata.org/latest-data.html.")
    equiv_yscale = True
    start_yr = global_carbon.c_budget.index.min()

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
        8
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

    # CHART 6 Global CO2 emission pathways using remaining carbon budgets.

    title = "Global CO\u2082 Pathways using Remaining Carbon Budget"
    xlabel = "Year"
    ylabel = "CO\u2082 Emissions from Fossil Fuels, Cement, & Land Use Change (Gt)"
    footer_text = "By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: Global Carbon Project, Global Carbon Budget, slide 64, \
https://robbieandrew.github.io/GCB2024/, data in csv format.\nFor more info see the Global Carbon Budget 2024: \
https://essd.copernicus.org/articles/17/965/2025/essd-17-965-2025.pdf, p. 1011.\n\
Final value of Historical emissions shown by black line is 41.6GtCO\u2082 for year 2024."
    series_names = ("Historical", "1.5\N{DEGREE SIGN}C, 235 GtCO\u2082", "1.7\N{DEGREE SIGN}C, 585 GtCO\u2082",
                    "2.0\N{DEGREE SIGN}C, 1,110 GtCO\u2082")
    additional_text = "Likelihood of warming values is 50%.\n\
Values shown alongside are the respective remaining carbon budgets and apply for year\n\
2025 onwards.\n\
An uncertainty of \u00B1220GtCO\u2082 applies to each due to alternative non-CO\u2082 emission\n\
scenarios, and other sources of uncertainties.\n\
Net-zero CO\u2082 by 2040 now exceeds the budget for 1.5\N{DEGREE SIGN}C, but net-zero CO\u2082 by 2050 is still\n\
within the budget to limit warming to 1.7\N{DEGREE SIGN}C."

    chart.line_plot(
        title,
        xlabel,
        ylabel,
        footer_text,
        additional_text,
        series_names,
        "dimgrey", "green", "blue", "red",
        series1=global_carbon.remaining_c_budget_data["Historical"],
        series2=global_carbon.remaining_c_budget_data["1.5C / 235 GtCO2"],
        series3=global_carbon.remaining_c_budget_data["1.7C / 585 GtCO2"],
        series4=global_carbon.remaining_c_budget_data["2.0C / 1110 GtCO2"]
    )

    plt.savefig(
        os.path.join(fig_dir, "6 co2 pathways using budget.svg"),
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
# Plots country CO2 emissions from fossil fuel combustion
#
########################################################################################################################
def country_co2_charts(energy_system, global_carbon):
    fig_dir = "charts " + energy_system.country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    # CHART 1: Annual fossil fuel CO2 emissions alongside treemap of country shares.
    title1 = "Fossil Fuel CO\u2082 Emissions"
    title2 = "Fossil Fuel CO\u2082 Emissions by National Share"
    subplot1_title = "Annual"
    subplot2_title = "Year " + str(int(max(global_carbon.country_shares_fy["Year"])))
    x_interval = 10
    ylabel = "Megatonne (Mt)"

    large_emitter_share = 100 - float(
        global_carbon.country_shares_fy[
            global_carbon.country_shares_fy["Name"] == "Other"
            ].Value.values
    )
    major_emitter_countries = global_carbon.country_shares_fy[
        global_carbon.country_shares_fy["Value"] >= user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value
        ]
    major_emitter_share = round(
        (sum(major_emitter_countries["Value"]) -
         major_emitter_countries[major_emitter_countries["Name"] == "Other"].Value.values[0]), 1)

    large_not_major_emitter_countries = global_carbon.country_shares_fy.loc[
        global_carbon.country_shares_fy["Value"] < user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value
        ].Name.values

    s = ""
    for i in large_not_major_emitter_countries:
        s += i
        s += "\n"

    additional_text1 = ("Shares total 100% of " + str(int(max(global_carbon.country_shares_fy["Year"]))) +
                        " global\nfossil fuel CO\u2082 emissions.\n\n\n\
Segments excluding 'Other' represent\ncountries with a "
                        + str(user_globals.Constant.LARGE_EMITTER_SHARE_THRESHOLD.value)
                        + "% or greater share,\nof which there were "
                        + str(len(global_carbon.country_shares_fy) - 1)
                        + ", totalling "
                        + str(large_emitter_share)
                        + "%.\n\n\nLabelled segments are those with a 1%\nor greater share, of which there were\n"
                        # Subtract 1 so as not to include 'Other'.
                        + str(len(global_carbon.country_shares_fy[global_carbon.country_shares_fy["Value"] >= 1]) - 1)
                        + ", totalling "
                        + str(major_emitter_share)
                        + "%.\n\n\nUnlabelled segments in lower\nright corner are listed below. \
These\nhad shares greater than or equal\nto " + str(user_globals.Constant.LARGE_EMITTER_SHARE_THRESHOLD.value)
                        + "%, and less than " + str(user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value)
                        + "% -\n"
                        + s)

    footer_text = (str(energy_system.ffco2_Mt["Value"].index[-1]) + " fossil fuel CO\u2082 emissions = " +
                   f"{(round(energy_system.ffco2_Mt["Value"].values[-1], 1)):,}" + "Mt\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

    chart.column_treemap(
        energy_system.ffco2_Mt["Value"],
        global_carbon.country_shares_fy,
        user_globals.Color.CO2_EMISSION.value,
        energy_system.country,
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
        os.path.join(fig_dir, "1 " + energy_system.country + " ff co2.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    print(
        "National CO2 emission shares treemap, most recent year sum of shares = "
        + str(sum(global_carbon.country_shares_fy["Value"]))
        + "%"
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()

    # CHART 2: Annual change of fossil fuel CO2 emissions.
    title = "Annual Change of Fossil Fuel CO\u2082 Emissions"
    ylabel = "Megatonne per year (Mt/yr)"
    footer_text = "Values are rounded to nearest whole number. \n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    chart.column_grouped(
        energy_system.country,
        title,
        ylabel,
        footer_text,
        user_globals.Color.CO2_EMISSION.value,
        series1=energy_system.ffco2_Mt["Change"],
    )

    plt.savefig(
        os.path.join(fig_dir, "2 " + energy_system.country + " ff co2 change.svg"),
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
# Controls plotting of global fossil fuel production shares by country. Country is included as an input argument so
# that chart is saved in the folder of the country being profiled.
#
########################################################################################################################
def world_ffprod_charts(coal_prods, oil_prods, gas_prods, country):
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save chart in this directory.
    # Print info to console.
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
    print("Number of high fossil fuel producers = " + str(num_prod_countries))
    print("High fossil fuel producers = \n" + printable_country_list)
    title = "Fossil Fuel Production by National Share"
    title_addition = "Year " + str(coal_prods.loc[0, "Year"])
    # Title above LH plot
    subplot1_title = "Coal Producers with ≥" + str(user_globals.Constant.COAL_SHARE_RANK_THRESHOLD.value) + "% share"
    # Title above centre plot
    subplot2_title = "Oil Producers with ≥" + str(user_globals.Constant.OIL_SHARE_RANK_THRESHOLD.value) + "% share"
    # Title above RH plot
    subplot3_title = "Gas Producers with ≥" + str(user_globals.Constant.GAS_SHARE_RANK_THRESHOLD.value) + "% share"

    footer_upper_text = ("The charts above show that the " + str(
        num_prod_countries) + " countries listed below produced a " + str(
        user_globals.Constant.COAL_SHARE_RANK_THRESHOLD.value) +
                         "% or greater share of coal, \
and or a " + str(user_globals.Constant.OIL_SHARE_RANK_THRESHOLD.value) + "% or greater share of oil, and or a " +
                         str(user_globals.Constant.GAS_SHARE_RANK_THRESHOLD.value) +
                         "% or greater share of gas in " + str(coal_prods.loc[0, "Year"]) +
                         ", collectively\naccounting for " +
                         str(round(coal_prod_total_shares, 0)) + "% of global coal, " +
                         str(round(oil_prod_total_shares, 0)) + "% of global oil, and " +
                         str(round(gas_prod_total_shares, 0)) + "% of global gas production: \n" +
                         printable_country_list) + "."

    footer_lower_text = "Ranking of producers was determined using fossil fuel production data in following units: \
Coal EJ, Oil Mt, and Gas EJ. Oil production in units of Mt is used instead of kbd because it's in closer agreement \
with IEA data.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data. \
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads."

    chart.treemap_3_subplots(
        coal_prods,  # Dataframe 1
        oil_prods,  # Dataframe 2
        gas_prods,  # Dataframe 3
        subplot1_title,  # Title above LH plot
        subplot2_title,  # Title above centre plot
        subplot3_title,  # Title above RH plot
        "World",
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
# Function: country_ffprod_primaryenergy_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI energy data.
#
########################################################################################################################
def country_ffprod_primaryenergy_charts(energy_system):
    if energy_system.incl_ei_flag is False:
        return None
    country = energy_system.country

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
        footer_text = (str(energy_system.ffprod_PJ.index[-1])
                       + " values: "
                       + "Coal = "
                       + f"{(round(energy_system.ffprod_PJ["Coal"].iloc[-1] *
                                   user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ, Oil = "
                       + f"{(round(energy_system.ffprod_PJ["Oil"].iloc[-1] * user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ, Gas = "
                       + f"{(round(energy_system.ffprod_PJ["Gas"].iloc[-1] * user_globals.Constant.PJ_TO_EJ.value)):,}"
                       + "EJ. Oil production calculated by converting units of Mt to joules using EI's approximate \
conversion factor of 41.868 GJ/toe. Production data for coal and gas provided in units of joules.\n\
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")
    else:
        footer_text = (str(energy_system.primary_PJ.index[-1])
                       + " values: "
                       + "Coal = "
                       + f"{(round(energy_system.ffprod_PJ["Coal"].iloc[-1])):,}"
                       + "PJ, Oil = "
                       + f"{(round(energy_system.ffprod_PJ["Oil"].iloc[-1])):,}"
                       + "PJ, Gas = "
                       + f"{(round(energy_system.ffprod_PJ["Gas"].iloc[-1])):,}"
                       + "PJ. Oil production calculated by converting units of Mt to joules using EI's approximate \
conversion factor of 41.868 GJ/toe. Production data for coal and gas provided in units of joules.\n\
A plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid line at zero.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    x_axis_interval = 10
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
        10
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
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
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
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
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
        10
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
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
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
# Function: country_finalenergy_elec_charts()
#
# Description:
# Controls plotting sequence of all charts displaying both EI and IEA data.
#
########################################################################################################################
def country_finalenergy_elec_charts(energy_system):
    country = energy_system.country
    if energy_system.incl_iea_flag is False:
        return None
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.
    ####################################################################################################################
    # FINAL ENERGY AND ELECTRICITY COMBINED: Shares for most recent year.
    ####################################################################################################################
    # Plot only Final Energy if electricity data is unavailable.
    if energy_system.elecgen_TWh is None:
        print(
            "Sum of Final Energy = "
            + str(sum(energy_system.consumption_final_shares["Value"]))
        )

        title = "Energy Consumption after partial conversions to Electricity (Final Energy)"
        title_addition = "Shares are shown account for energy in the final form that it's consumed, for most recent \
        year of data in each dataset."
        title1 = "ENERGY Consumption by Share in year " + str(
            energy_system.finalenergy_PJ.index[-1]
        )
        footer_text = "For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to the legend.\n\
'Wind, solar etc' in the IEA dataset refers to a non-electric form, and usually too small to show.\n\
Shares of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Energy Consumption data: IEA World Energy Balances, \
https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser?country\
WORLD&fuel=Energy%20consumption&indicator=TFCbySource."

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
            + str(sum(energy_system.finalenergy_fy_shares["Value"]))
        )
        print(
            "Sum of most recent year plotted Electricity shares = "
            + str(sum(energy_system.elecgen_fuel_fy_shares["Value"]))
        )
        title = "Energy Consumption after partial conversions to Electricity (Final Energy), & Electricity \
Generation"
        title_addition = "Shares are shown in the form that energy is consumed, for most recent year of data for \
respective dataset."
        title1 = (
                "Energy Consumption by Share in year "
                + str(energy_system.finalenergy_PJ.index[-1])
                + "\n(Fuels used for generation of Electricity are shown in the adjacent chart)"
        )
        title2 = "Electricity Generation by Share in year " + str(
            energy_system.elecgen_TWh.index[-1]
        )
        footer_text = ("For clarity: \
(1) Shares are rounded and values <1% aren't shown, so may not total 100%; \
(2) Labels may not be shown due to a lack of space, in which case refer to the legend.\n\
'Wind, solar etc' in the IEA dataset used for the LH chart refers to a non-electric form, and usually too small to \
show.\n\
For some countries, shares of electricity generation may not total 100% due to unavailability of data for some fuels. \
Total generation is published, so any such unpublished share is calculated, & shown in the RH\n\
chart if applicable. Shares of coal, oil, gas, biofuels, and waste shown in the LH chart were consumed for purposes \
other than electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Energy Consumption data: IEA World Energy Balances,\
https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser?country=WORLD\
&fuel=Energy%20consumption&indicator=TFCbySource\n\
Electricity Generation data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        chart.treemap_2_subplots(
            energy_system.finalenergy_fy_shares,
            energy_system.elecgen_fuel_fy_shares,
            title1,
            title2,
            country,
            title,
            title_addition,
            footer_text,
        )
    plt.savefig(
        os.path.join(fig_dir, "8 " + country + " fe elec shares.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()


########################################################################################################################
#
# Function: country_finalenergy_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only IEA data.
#
########################################################################################################################
def country_finalenergy_charts(energy_system):
    country = energy_system.country
    if energy_system.incl_iea_flag is False:
        return None
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
            energy_system.finalenergy_PJ["Coal"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq2 = pd.Series(
            energy_system.finalenergy_PJ["Oil"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq3 = pd.Series(
            energy_system.finalenergy_PJ["Gas"] * user_globals.Constant.PJ_TO_EJ.value
        )
        feq4 = pd.Series(
            energy_system.finalenergy_PJ["Biofuels and Waste"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        feq5 = pd.Series(
            energy_system.finalenergy_PJ["Electricity"]
            * user_globals.Constant.PJ_TO_EJ.value
        )
        feq6 = pd.Series(
            energy_system.finalenergy_PJ["Heat"] * user_globals.Constant.PJ_TO_EJ.value
        )
    else:
        ylabel_top = "Petajoule (PJ)"
        ylabel_bottom = "PJ"
        feq1 = energy_system.finalenergy_PJ["Coal"]
        feq2 = energy_system.finalenergy_PJ["Oil"]
        feq3 = energy_system.finalenergy_PJ["Gas"]
        feq4 = energy_system.finalenergy_PJ["Biofuels and Waste"]
        feq5 = energy_system.finalenergy_PJ["Electricity"]
        feq6 = energy_system.finalenergy_PJ["Heat"]

    footer_text = "Quantities of coal, oil, gas, biofuels, and waste shown were consumed for purposes other than \
electricity generation, such as steel manufacture, internal combustion, cooking, etc.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data. \n\
Data: IEA World Energy Balances, https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser?\
country=WORLD&fuel=Energy%20consumption&indicator=TFCbySource."

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


########################################################################################################################
#
# Function: country_elecgen_charts()
#
# Description:
# Controls plotting sequence of all charts displaying only EI electricity data.
#
########################################################################################################################
def country_elecgen_charts(energy_system):
    country = energy_system.country
    fig_dir = "charts " + country + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save co2 charts in this directory.

    ################################################################################################################
    # ELECTRICITY: Annual generation quantity.
    ################################################################################################################

    if energy_system.elecgen_TWh is not None:
        title = "Annual Electricity Generation"
        title1 = "Total"
        title2 = "Nuclear"
        title3 = "Fossil Fuels\n(Coal+Oil+Gas)"
        title4 = "Coal"
        title5 = "Oil"
        title6 = "Gas"
        title7 = "Bio, Geo and Other"
        title8 = "Renewables\n(Hydro+Wind+Solar)"
        title9 = "Hydro"
        title10 = "Wind"
        title11 = "Solar"
        ylabel_top = "Terawatt hours (TWh)"
        ylabel = "TWh"
        footer_text = ("The summation of fuel quantities may not equal 'Total' due to unpublished data for some \
countries.\nFor "
                       + country
                       + ", the unpublished quantity in year "
                       + str(energy_system.elecgen_TWh.index[-1])
                       + " was "
                       + f"{(round(energy_system.elecgen_TWh["Unpublished"].iloc[-1], 2)):,}"
                       + "TWh, or "
                       + f"{(round(energy_system.elecgen_TWh["Unpublished Share"].iloc[-1], 0))}"
                       .rstrip("0").rstrip(".")
                       + "\nTotal = Fossil Fuels + Renewables + Nuclear + Bio, Geo and Other + \
any unpublished quantity above. Fossil Fuels = Coal + Oil + Gas.\nRenewables = Hydro + Wind + Solar. \
Quantities are gross generation that don't account for imports or exports.\n"
                       + str(energy_system.elecgen_TWh.index[-1])
                       + " values: \n"
                       + "Total = "
                       + f"{(round(energy_system.elecgen_TWh["Total Country"].iloc[-1])):,}"
                       + " TWh\nNuclear = "
                       + f"{(round(energy_system.elecgen_TWh["Nuclear"].iloc[-1])):,}"
                       + " TWh\nFossil Fuels = "
                       + f"{(round(energy_system.elecgen_TWh["Fossil Fuels"].iloc[-1])):,}"
                       + " TWh\nCoal = "
                       + f"{(round(energy_system.elecgen_TWh["Coal"].iloc[-1])):,}"
                       + " TWh\nOil = "
                       + f"{(round(energy_system.elecgen_TWh["Oil"].iloc[-1])):,}"
                       + " TWh\nGas = "
                       + f"{(round(energy_system.elecgen_TWh["Gas"].iloc[-1])):,}"
                       + " TWh\nBio, Geo and Other = "
                       + f"{(round(energy_system.elecgen_TWh["Bio, Geo and Other"].iloc[-1])):,}"
                       + " TWh\nRenewables = "
                       + f"{(round(energy_system.elecgen_TWh["Renewables"].iloc[-1])):,}"
                       + " TWh\nHydro = "
                       + f"{(round(energy_system.elecgen_TWh["Hydro"].iloc[-1])):,}"
                       + " TWh\nWind = "
                       + f"{(round(energy_system.elecgen_TWh["Wind"].iloc[-1])):,}"
                       + " TWh\nSolar = "
                       + f"{(round(energy_system.elecgen_TWh["Solar"].iloc[-1])):,}"
                       + " TWh\nA plot with a maximum value of 0.5% of the maximum of all plots is displayed as a solid \
line at zero.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        chart.column_11_subplots(
            energy_system.elecgen_TWh["Total Country"],
            energy_system.elecgen_TWh["Nuclear"],
            energy_system.elecgen_TWh["Fossil Fuels"],
            energy_system.elecgen_TWh["Coal"],
            energy_system.elecgen_TWh["Oil"],
            energy_system.elecgen_TWh["Gas"],
            energy_system.elecgen_TWh["Bio, Geo and Other"],
            energy_system.elecgen_TWh["Renewables"],
            energy_system.elecgen_TWh["Hydro"],
            energy_system.elecgen_TWh["Wind"],
            energy_system.elecgen_TWh["Solar"],
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

    if energy_system.elecgen_TWh is not None:
        plt.savefig(
            os.path.join(fig_dir, "9 " + country + " elec fuel qty.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2, )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    ####################################################################################################################
    # ELECTRICITY: Annual change of generation by fuel.
    ####################################################################################################################
    if energy_system.elecgen_TWh is not None:
        title = "Annual Change of Electricity Generation"
        ylabel_top = "Terawatt hours per year (TWh/yr)"
        ylabel_bottom = "TWh/yr"
        footer_text = ("Values are rounded to nearest whole number, and those 0.5 or less are displayed as zero, \
so column values in upper chart may not equal total of those in lower chart for a given year.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        chart.column_grouped_2_subplots(
            country,
            title,
            ylabel_top,
            ylabel_bottom,
            footer_text,
            user_globals.Color.FOSSIL_FUELS.value,
            energy_system.elecgen_TWh["Fossil Fuels Change"],
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            user_globals.Color.NUCLEAR.value,
            user_globals.Color.HYDRO.value,
            user_globals.Color.WIND_AND_SOLAR.value,
            user_globals.Color.OTHER.value,
            series1=energy_system.elecgen_TWh["Coal Change"],
            series2=energy_system.elecgen_TWh["Oil Change"],
            series3=energy_system.elecgen_TWh["Gas Change"],
            series4=energy_system.elecgen_TWh["Nuclear Change"],
            series5=energy_system.elecgen_TWh["Hydro Change"],
            series6=energy_system.elecgen_TWh["Wind and Solar Change"],
            series8=energy_system.elecgen_TWh["Bio, Geo and Other Change"],
        )
        plt.savefig(
            os.path.join(fig_dir, "10 " + country + " elec fuel change.svg"),
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
    if energy_system.elecgen_TWh is not None:
        title = ("Annual Electricity Generation by share with " + str(energy_system.elecgen_TWh.index[-1]) +
                 " value shown after each fuel")
        title1 = ("Nuclear " +
                  f"{(round(energy_system.elecgen_TWh["Nuclear Share"].iloc[-1], 1)):,}" + "%")
        title2 = ("Fossil Fuels (Coal+Oil+Gas) " +
                  f"{(round(energy_system.elecgen_TWh["Fossil Fuels Share"].iloc[-1], 1)):,}" + "%")
        title3 = ("Coal " +
                  f"{(round(energy_system.elecgen_TWh["Coal Share"].iloc[-1], 1)):,}" + "%")
        title4 = ("Oil " +
                  f"{(round(energy_system.elecgen_TWh["Oil Share"].iloc[-1], 1)):,}" + "%")
        title5 = ("Gas " +
                  f"{(round(energy_system.elecgen_TWh["Gas Share"].iloc[-1], 1)):,}" + "%")
        title6 = ("Bio, Geo and Other " +
                  f"{(round(energy_system.elecgen_TWh["Bio, Geo and Other Share"].iloc[-1], 1)):,}" + "%")
        title7 = ("Renewables (Hydro+Wind+Solar) " +
                  f"{(round(energy_system.elecgen_TWh["Renewables Share"].iloc[-1], 1)):,}" + "%")
        title8 = ("Hydro " +
                  f"{(round(energy_system.elecgen_TWh["Hydro Share"].iloc[-1], 1)):,}" + "%")
        title9 = ("Wind " +
                  f"{(round(energy_system.elecgen_TWh["Wind Share"].iloc[-1], 1)):,}" + "%")
        title10 = ("Solar " +
                   f"{(round(energy_system.elecgen_TWh["Solar Share"].iloc[-1], 1)):,}" + "%")
        ylabel = "Annual Share (%)"
        footer_text = ("Shares may not total 100% for some countries due to unavailability of data. For "
                       + country
                       + ", the unpublished share in year "
                       + str(energy_system.elecgen_TWh.index[-1])
                       + " was "
                       + f"{(round(energy_system.elecgen_TWh["Unpublished Share"].iloc[-1], 0))}"
                       .rstrip("0").rstrip(".")
                       + "%.\n\
Total (100%) = Fossil Fuels + Renewables + Nuclear + Bio, Geo and Other + any unpublished share above. \
Fossil Fuels = Coal + Oil + Gas. Renewables = Hydro + Wind + Solar.\n\
Shares are calculated using gross generation quantities that don't account for imports or exports. While geothermal is \
renewable, the data groups geothermal with biofuels that may not be renewable.\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

        elec_share1 = energy_system.elecgen_TWh["Nuclear Share"]
        elec_share2 = energy_system.elecgen_TWh["Fossil Fuels Share"]
        elec_share3 = energy_system.elecgen_TWh["Coal Share"]
        elec_share4 = energy_system.elecgen_TWh["Oil Share"]
        elec_share5 = energy_system.elecgen_TWh["Gas Share"]
        elec_share6 = energy_system.elecgen_TWh["Bio, Geo and Other Share"]
        elec_share7 = energy_system.elecgen_TWh["Renewables Share"]
        elec_share8 = energy_system.elecgen_TWh["Hydro Share"]
        elec_share9 = energy_system.elecgen_TWh["Wind Share"]
        elec_share10 = energy_system.elecgen_TWh["Solar Share"]

        print(
            "Annual sum of electricity generation fuel shares = \n"
            + str(
                elec_share1 + elec_share3 + elec_share4 + elec_share5 + elec_share6 +
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
            os.path.join(fig_dir, "11 " + country + " elec fuel share trends.svg"),
            format="svg",
            bbox_inches="tight",
            pad_inches=0.2,
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()


########################################################################################################################
#
# Function: major_emitter_charts()
#
# Description:
# Plots fossil fuel CO2 emissions, national shares, and primary energy consumption of fossil fuels for countries
# emitting user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value or more of world fossil fuel CO2 emissions.
#
########################################################################################################################
def major_emitter_charts(energy_system, global_carbon, major_emitter_df):
    fig_dir = "charts Major Emitters" + "/"
    os.makedirs(fig_dir, exist_ok=True)  # Save charts in this directory.

    # Chart 0: World CO2 Emissions from fossil fuel combustion line plot and country share treemap.
    title1 = "Fossil Fuel CO\u2082 Emissions"
    title2 = "Fossil Fuel CO\u2082 Emissions by National Share"
    subplot1_title = "Annual"
    subplot2_title = "Year " + str(int(max(global_carbon.country_shares_fy["Year"])))
    x_interval = 10
    ylabel = "Gigatonne (Gt)"

    large_emitter_share = 100 - float(
        global_carbon.country_shares_fy[
            global_carbon.country_shares_fy["Name"] == "Other"
            ].Value.values
    )
    major_emitter_countries = global_carbon.country_shares_fy[
        global_carbon.country_shares_fy["Value"] >= user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value
        ]
    major_emitter_share = round(
        (sum(major_emitter_countries["Value"]) -
         major_emitter_countries[major_emitter_countries["Name"] == "Other"].Value.values[0]), 1)

    large_not_major_emitter_countries = global_carbon.country_shares_fy.loc[
        global_carbon.country_shares_fy["Value"] < user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value
        ].Name.values

    s = ""
    for i in large_not_major_emitter_countries:
        s += i
        s += "\n"

    additional_text1 = ("Shares total 100% of 2023 global\nfossil fuel CO\u2082 emissions.\n\n\n\
Segments excluding 'Other' represent\ncountries with a "
                        + str(user_globals.Constant.LARGE_EMITTER_SHARE_THRESHOLD.value)
                        + "% or greater share,\nof which there were "
                        + str(len(global_carbon.country_shares_fy) - 1)
                        + ", totalling "
                        + str(large_emitter_share)
                        + "%.\n\n\nLabelled segments are those with a 1%\nor greater share, of which there were\n"
                        # Subtract 1 so as not to include 'Other'.
                        + str(len(global_carbon.country_shares_fy[global_carbon.country_shares_fy["Value"] >= 1]) - 1)
                        + ", totalling "
                        + str(major_emitter_share)
                        + "%.\n\n\nUnlabelled segments in lower\nright corner are listed below. \
These\nhad shares greater than or equal\nto " + str(user_globals.Constant.LARGE_EMITTER_SHARE_THRESHOLD.value) +
                        "%, and less than " + str(user_globals.Constant.MAJOR_EMITTER_SHARE_THRESHOLD.value) + "% -\n"
                        + s
                        )

    footer_text = (str(energy_system.ffco2_Mt["Value"].index[-1]) + " fossil fuel CO\u2082 emissions = " +
                   f"{(round(energy_system.ffco2_Gt["Value"].values[-1], 1)):,}" + "Gt\n\
By Shane White, whitesha@protonmail.com, https://github.com/shanewhi/world-energy-data.\n\
Data: The Energy Institute Statistical Review of World Energy 2024,\n\
https://www.energyinst.org/statistical-review/resources-and-data-downloads.")

    chart.line_treemap(
        energy_system.ffco2_Gt["Value"],
        global_carbon.country_shares_fy,
        user_globals.Color.CO2_EMISSION.value,
        "Total World",
        title1,
        title2,
        subplot1_title,
        subplot2_title,
        user_globals.Constant.CHART_START_YR_FOR_MAJOR_EMITTERS.value,
        x_interval,
        ylabel,
        additional_text1,
        footer_text,
    )
    plt.savefig(
        os.path.join(fig_dir, "0 " + " ff co2.svg"),
        format="svg",
        bbox_inches="tight",
        pad_inches=0.2,
    )

    # CHARTS 1 and above: Major emitter national CO2 emission line plot and pairing coal, oil and gas primary energy
    # line plots.
    counter = 0  # Loop counter to append to chart filenames
    print("Major emitters:\n")
    for country in major_emitter_df.index.get_level_values('Country').drop_duplicates():
        counter += 1
        country_name = country
        if country_name == "US":
            country_name = "United States"
        chart.line_2_subplots(
            major_emitter_df.loc[(country, "ffco2_Mt")],
            major_emitter_df.loc[(country, "primary_PJ_coal")],
            major_emitter_df.loc[(country, "primary_PJ_oil")],
            major_emitter_df.loc[(country, "primary_PJ_gas")],
            user_globals.Color.CO2_EMISSION.value,
            user_globals.Color.COAL.value,
            user_globals.Color.OIL.value,
            user_globals.Color.GAS.value,
            country_name,
            1965,
            1965,
            10,
            10,
        )
        print(country_name)
        plt.savefig(
            os.path.join(fig_dir, str(counter) + " " + country_name + ".svg"),
            format="svg",
        )
        if user_globals.Constant.DISPLAY_CHARTS.value is True:
            plt.show()
        plt.close()

    chart.legend_for_major_emitter_charts(
        major_emitter_df.loc[(country, "ffco2_Mt")],
        major_emitter_df.loc[(country, "primary_PJ_coal")],
        major_emitter_df.loc[(country, "primary_PJ_oil")],
        major_emitter_df.loc[(country, "primary_PJ_gas")],
        user_globals.Color.CO2_EMISSION.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
    )
    counter += 1
    plt.savefig(
        os.path.join(fig_dir, str(counter) + " legend" + ".svg"),
        format="svg",
    )
    if user_globals.Constant.DISPLAY_CHARTS.value is True:
        plt.show()
    plt.close()
