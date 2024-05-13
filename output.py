#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:20:13 2024

@author: shanewhite
"""


###############################################################################
#
# Module: output.py
#
# Description:
# Controls chart plotting sequence.
#
###############################################################################


# Import Python modules.
import matplotlib.pyplot as plt
import pandas as pd


# Import user modules.
import user_globals
import chart


def charts(energy_system):

    country = energy_system.name

###############################################################################
# CO2: Annual emissions.
###############################################################################
   
    title = "Carbon Dioxide Emissions - Annual quantity"
    ylabel = "MtCO\u2082/year"
    footer_text = "Data: Energy Institute Statistical Review of World \
Energy 2023,\n\
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"
    color = user_globals.Color.CO2.value

    chart.column_1x1(
        energy_system.co2_Mt,
        color,
        country,
        title,
        ylabel,
        footer_text
        )
    plt.show()


###############################################################################
# PRODUCTION: Annual Fossil Fuel production.
###############################################################################

    title = "Fossil Fuel Production - Annual quantities"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    ylabel = "Petajoule"

    if country == "World":
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads \
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe.\n\
Initial year of data for each fuel differs: coal 1981, oil 1965, and gas \
1970.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"
    else:
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads \
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe.\n\
Initial year of data for each fuel differs: coal 1981, oil 1965, and gas \
1970.\n\
For comparison, EI(2023) listed 2022 World production values as: \
coal 175,000 PJ, oil 185,000 PJ, and gas 146,000 PJ.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    equiv_scale = True

    chart.column_1x3(
        energy_system.ffprod_PJ["coal"],
        energy_system.ffprod_PJ["oil"],
        energy_system.ffprod_PJ["gas"],
        color1,
        color2,
        color3,
        country,
        title,
        "",
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabel,
        footer_text,
        equiv_scale
        )
    plt.show()


###############################################################################
# PRIMARY ENERGY: Annual quantities of fossil fuels.
###############################################################################

    title = "Energy Supply (Primary Energy) - \
Annual quantities of Fossil Fuels"
    title_addition = "Primary Energy accounts for fuels input to a national, \
or the world energy system, prior to conversion to electricity or combusted \
for non-electric purposes."

    if country == "World":
         ylabel = "Exajoule"
         peq1 = pd.Series(energy_system.primary_PJ["Coal"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         peq2 = pd.Series(energy_system.primary_PJ["Oil"] * \
                 user_globals.Constant.PJ_TO_EJ.value)
         peq3 = pd.Series(energy_system.primary_PJ["Gas"] * \
                 user_globals.Constant.PJ_TO_EJ.value)
    else:
         ylabel = "Petajoule"
         peq1 = pd.Series(energy_system.primary_PJ["Coal"])
         peq2 = pd.Series(energy_system.primary_PJ["Oil"])
         peq3 = pd.Series(energy_system.primary_PJ["Gas"])

    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data"

    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value

    chart.column_1x3(
        peq1,
        peq2,
        peq3,
        color1,
        color2,
        color3,
        country,
        title,
        title_addition,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabel,
        footer_text,
        True
        )
    plt.show()


###############################################################################
# PRIMARY ENERGY: Annual change of fossil fuel category.
###############################################################################

    title = "Energy Supply (Primary Energy) - Annual change of Fossil Fuels"

    if country == "World":
         ylabel = "Exajoule/year"
         series = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
    else:
         ylabel = "Petajoule/year"
         series = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"])

    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
For clarity: (1) Values of change at tops of columns are rounded to nearest \
whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not shown resulting in \
a gap between plotted columns.\nFor an explanation of primary energy, refer \
to https://www.worldenergydata.org/introduction/\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    plot_start_yr = \
        user_globals.Constant.PRIMARY_ENERGY_CHANGE_START_YEAR.value
    color = user_globals.Color.FOSSIL_FUELS.value

    chart.column_grouped(
        country,
        title,
        title_addition,
        ylabel,
        footer_text,
        plot_start_yr,
        color,
        series1 = series
        )
    plt.show()


###############################################################################
# PRIMARY ENERGY: Annual change of fossil fuels.
###############################################################################
    
    title = "Energy Supply (Primary Energy) - Annual change of Coal, Oil \
and Gas"

    if country == "World":
        ylabel = "Exajoule/year"
        pe1 = pd.Series(energy_system.primary_PJ["Coal Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        pe2 = pd.Series(energy_system.primary_PJ["Oil Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        pe3 = pd.Series(energy_system.primary_PJ["Gas Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
    else:
         ylabel = "Petajoule/year"
         pe1 = pd.Series(energy_system.primary_PJ["Coal Change"])
         pe2 = pd.Series(energy_system.primary_PJ["Oil Change"])
         pe3 = pd.Series(energy_system.primary_PJ["Gas Change"])

    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
For clarity: (1) Values of change at tops of columns are rounded to nearest \
whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not shown resulting in \
a gap between plotted columns.\nFor an explanation of primary energy, refer \
to https://www.worldenergydata.org/introduction/\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    plot_start_yr = \
        user_globals.Constant.PRIMARY_ENERGY_CHANGE_START_YEAR.value
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value

    chart.column_grouped(
         country,
         title,
         title_addition,
         ylabel,
         footer_text,
         plot_start_yr,
         color1,
         color2,
         color3,
         series1 = pe1,
         series2 = pe2,
         series3 = pe3
         )
    plt.show()


###############################################################################
# PRIMARY ENERGY: Annual shares.
###############################################################################

    title = "Energy Supply (Primary Energy) - Share of fuels"
    title_addition = "Primary Energy accounts for fuels input to a national, \
or the world energy system, prior to conversion to electricity or combusted \
for non-electric purposes.\nEquivalents are shown for non-combustible fuels."

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Renewables"
    title6 = "Bio Geo and Other"

    pes1 = pd.Series(energy_system.primary_PJ["Coal Share"])
    pes2 = pd.Series(energy_system.primary_PJ["Oil Share"])
    pes3 = pd.Series(energy_system.primary_PJ["Gas Share"])
    pes4 = pd.Series(energy_system.primary_PJ["Nuclear Share"])
    pes5 = pd.Series(energy_system.primary_PJ["Renewables Share"])
    pes6 = pd.Series(energy_system.primary_PJ["Bio Geo and Other Share"])

    # Additional text.
    ylabel = ("Annual Share (%)")
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Renewables is the sum of hydro, wind and solar.\n\
For an explanation of primary energy, refer to \
https://www.worldenergydata.org/introduction/\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    #Plot
    chart.line_2x3(
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
        title_addition,
        title1,
        title2,
        title3,
        title4,
        title5,
        title6,
        ylabel,
        footer_text,
        True
        )
    plt.show()


###############################################################################
# PRIMARY ENERGY: Annual shares of most recent year.
###############################################################################

    title = "Energy Supply (Primary Energy) - Shares in Year " \
        + str(energy_system.primary_PJ.index[-1])
    title_addition = "Primary Energy accounts for fuels input to a national, \
or the world energy system, prior to conversion to electricity or combusted \
for non-electric purposes.\nEquivalents are shown for non-combustible fuels."
    title1 = "By Category"
    title2 = "By Fuel"
    footer_text = "For clarity: (1) Values are rounded, so shares may not \
total 100%, (2) Shares <1% aren't shown,\n(3) Labels may not be shown due to \
a lack of space, in which case refer to the legend.\n\
For an explanation of primary energy, refer to \
https://www.worldenergydata.org/introduction/\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    print(
        "Sum of primary energy shares = \n" + \
        str(energy_system.primary_PJ["Coal Share"] + \
            energy_system.primary_PJ["Oil Share"] + \
            energy_system.primary_PJ["Gas Share"] + \
            energy_system.primary_PJ["Nuclear Share"] + \
            energy_system.primary_PJ["Hydro Share"] + \
            energy_system.primary_PJ["Wind Share"] + \
            energy_system.primary_PJ["Solar Share"] + \
            energy_system.primary_PJ["Bio Geo and Other Share"] \
            ) + "%\n")

    chart.treemap(
        energy_system.primary_category_shares,
        energy_system.primary_fuel_shares,
        title1,
        title2,
        country,
        title,
        title_addition,
        footer_text
        )
    plt.show()


###############################################################################
# FINAL ENERGY AND ELECTRICITY COMBINED: Shares for most recent year.
###############################################################################

    title = "Energy Consumption and Electricity Generation by share for most \
recent year of data"
    title_addition = "Energy Consumption is also known as Total Final \
Consumption or Final Energy. This accounts for energy in the form that it's \
consumed."
    title1 = "Energy Consumption by share in year "+ \
        str(energy_system.consumption_PJ.index[-1]) + \
        "\n(Electricity shares are shown in the righthand chart)"
    title2 = "Electricity Generation by share in year " + \
str(energy_system.elecprod_TWh.index[-1])
    footer_text = \
"Energy Consumption data: IEA 2023 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances\n\
Electricity Generation data: The Energy Institute Statistical Review of World \
Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Latest years of data shown as of May 2024. For clarity: \
(1) Shares are rounded & may not total 100%, \
(2) Shares <1% not shown, and \
(3) Labels may not be shown due to a lack of space; refer to legend.\n\
For an explanation of Energy Consumption (also known as Final Energy or Total \
Final Consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Energy Consumption data labelled 'Wind, solar etc' were for purposes other \
than electricity generation, small and omitted for clarity.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data."

    chart.treemap(
        energy_system.consumption_final_shares,
        energy_system.elecprod_final_fuel_shares,
        title1,
        title2,
        country,
        title,
        title_addition,
        footer_text
        )
    plt.show()


###############################################################################
# FINAL ENERGY: Annual quantities.
###############################################################################

    title = "Energy Consumption - Annual quantities"
    if country == "World":
         ylabel = "Exajoules"
         feq1 = pd.Series(energy_system.consumption_PJ["Coal"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         feq2 = pd.Series(energy_system.consumption_PJ["Oil"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         feq3 = pd.Series(energy_system.consumption_PJ["Gas"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         feq4 = \
             pd.Series(energy_system.consumption_PJ["Biofuels and Waste"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         feq5 = pd.Series(energy_system.consumption_PJ["Electricity"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         feq6 = pd.Series(energy_system.consumption_PJ["Heat"] * \
             user_globals.Constant.PJ_TO_EJ.value)
    else:
        ylabel = "Petajoule"
        feq1 = energy_system.consumption_PJ["Coal"]
        feq2 = energy_system.consumption_PJ["Oil"]
        feq3 = energy_system.consumption_PJ["Gas"]
        feq4 = energy_system.consumption_PJ["Biofuels and Waste"]
        feq5 = energy_system.consumption_PJ["Electricity"]
        feq6 = energy_system.consumption_PJ["Heat"]

    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"

    footer_text = \
"Data: IEA 2023 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances. Latest year of data as of 4/2024 is 2021.\n\
For an explanation of total final consumption (TFC), refer to \
https://www.worldenergydata.org/introduction/\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel maufacture or \
internal combustion etc. Additional fossil fuels were combusted to produce \
electricity.\nData labelled 'Wind, solar etc' were consumed for purposes \
other than electricity production, small and omitted for clarity.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    chart.column_2x3(
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
        title_addition,
        title1,
        title2,
        title3,
        title4,
        title5,
        title6,
        ylabel,
        footer_text,
        True
        )
    plt.show()


###############################################################################
# FINAL ENERGY: Annual change.
###############################################################################

    title = "Energy Consumption - Annual changes"
    if country == "World":
        ylabel = "Exajoule/year"
        fec1 = pd.Series(energy_system.consumption_PJ["Coal Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        fec2 = pd.Series(energy_system.consumption_PJ["Oil Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        fec3 = pd.Series(energy_system.consumption_PJ["Gas Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        fec4 = pd.Series( \
                   energy_system.consumption_PJ["Biofuels and Waste Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        fec5 = pd.Series(energy_system.consumption_PJ["Electricity Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        fec6 = pd.Series(energy_system.consumption_PJ["Heat Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
    else:
        ylabel = "Petajoule/year"
        fec1 = pd.Series(energy_system.consumption_PJ["Coal Change"])
        fec2 = pd.Series(energy_system.consumption_PJ["Oil Change"])
        fec3 = pd.Series(energy_system.consumption_PJ["Gas Change"])
        fec4 = pd.Series( \
                   energy_system.consumption_PJ["Biofuels and Waste Change"])
        fec5 = pd.Series(energy_system.consumption_PJ["Electricity Change"])
        fec6 = pd.Series(energy_system.consumption_PJ["Heat Change"])

    footer_text = \
"Data: IEA 2023 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances. Latest year of data as of 4/2024 is 2021.\n\
For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel maufacture or \
internal combustion etc. Additional fossil fuels were combusted to produce \
electricity.\nTFC data labelled 'Wind, solar etc' were for purposes other \
than electricity production, small and omitted for clarity.\n\
For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/ By \
shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data.\n"

    chart.column_grouped(
        country,
        title,
        title_addition,
        ylabel,
        footer_text,
        user_globals.Constant.TFC_START_YEAR.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        series1 = fec1,
        series2 = fec2,
        series3 = fec3,
        series4 = fec4,
        series5 = fec5,
        series6 = fec6
        )
    plt.show()


###############################################################################
# FINAL ENERGY: Annual shares.
###############################################################################

    title = "Energy Consumption - Annual shares"
    ylabel = ("Annual Share (%)")
    footer_text = \
"Data: IEA 2023 World Energy Balances, \
https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances. Latest year of data as of 4/2024 is 2021.\n\
Quantities of coal, oil, gas, biofuels, and waste shown \
were consumed for purposes other than electricity generation, such as steel \
maufacture or internal combustion etc. Additional fossil fuels were combusted \
to produce electricity.\nTFC data labelled 'Wind, solar etc' were for\
purposes other than electricity production, small and omitted for clarity.\n\
For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/ By \
shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data.\n"

    fes1 = energy_system.consumption_PJ["Coal Share"]
    fes2 = energy_system.consumption_PJ["Oil Share"]
    fes3 = energy_system.consumption_PJ["Gas Share"]
    fes4 = energy_system.consumption_PJ["Biofuels and Waste Share"]
    fes5 = energy_system.consumption_PJ["Electricity Share"]
    fes6 = energy_system.consumption_PJ["Heat Share"]

    print(
        "Sum of annual consumption shares = \n" +
        str(fes1 + fes2 + fes3 + fes4 + fes5 + fes6)
        + "\n")
    
    chart.line_2x3(
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
                   title_addition,
                   title1,
                   title2,
                   title3,
                   title4,
                   title5,
                   title6,
                   ylabel,
                   footer_text,
                   True
                   )
    plt.show()


###############################################################################
# ELECTRICITY: Annual generation quantity by category.
###############################################################################

    title = "Electricity Generation - Annual quantities of categories"
    title1 = "Fossil Fuels"
    title2 = "Nuclear"
    title3 = "Renewables"
    title4 = "Geo Bio and Other"
    ylabel = "TWh"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Renewables is the sum of hydro, wind and solar. Quantities are gross \
generation that don't account for imports or exports.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    chart.column_1x4(energy_system.elecprod_TWh["Fossil Fuels"],
                    energy_system.elecprod_TWh["Nuclear"],
                    energy_system.elecprod_TWh["Renewables"],
                    energy_system.elecprod_TWh["Bio Geo and Other"],
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
                    ylabel,
                    footer_text,
                    True
                    )
    plt.show()


###############################################################################
# ELECTRICITY: Annual generation quantity by fuel.
###############################################################################

    title = "Electricity Generation - Annual quantities of fuels"
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Wind"
    title7 = "Solar"
    title8 = "Geo Bio and Other"
    ylabel = "TWh"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Quantities are gross generation that don't account for imports or exports.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    chart.column_2x4(
        energy_system.elecprod_TWh["Coal"],
        energy_system.elecprod_TWh["Oil"],
        energy_system.elecprod_TWh["Gas"],
        energy_system.elecprod_TWh["Nuclear"],
        energy_system.elecprod_TWh["Hydro"],
        energy_system.elecprod_TWh["Wind"],
        energy_system.elecprod_TWh["Solar"],
        energy_system.elecprod_TWh["Bio Geo and Other"],
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
        ylabel,
        footer_text,
        True
        )
    plt.show()


###############################################################################
# ELECTRICITY: Annual change of generation by category.
###############################################################################

    title = "Electricity Generation - Annual change of categories"
    title_addition = ""
    ylabel = "TWh/year"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
For clarity: (1) Values of change at tops of columns are rounded to nearest \
whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not shown resulting in \
a gap between plotted columns.\nRenewables is the sum of hydro, wind and \
solar.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data"

    chart.column_grouped(
        country,
        title,
        title_addition,
        ylabel,
        footer_text,
        user_globals.Constant.ELEC_CHANGE_START_YEAR.value,
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.RENEWABLES.value,
        user_globals.Color.OTHER.value,
        series1 = energy_system.elecprod_TWh["Fossil Fuels Change"],
        series2 = energy_system.elecprod_TWh["Nuclear Change"],
        series3 = energy_system.elecprod_TWh["Renewables Change"],
        series4 = energy_system.elecprod_TWh["Bio Geo and Other Change"]
        )
    plt.show()


###############################################################################
# ELECTRICITY: Annual change of generation by fuel.
###############################################################################

    title = "Electricity Generation - Annual change of fuels"
    title_addition = ""
    ylabel = "TWh/year"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
For clarity: (1) Values of change at tops of columns are rounded to nearest \
whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data"

    chart.column_grouped(
        country,
        title,
        title_addition,
        ylabel,
        footer_text,
        user_globals.Constant.ELEC_CHANGE_START_YEAR.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.WIND_AND_SOLAR.value,
        user_globals.Color.OTHER.value,
        series1 = energy_system.elecprod_TWh["Coal Change"],
        series2 = energy_system.elecprod_TWh["Oil Change"],
        series3 = energy_system.elecprod_TWh["Gas Change"],
        series4 = energy_system.elecprod_TWh["Nuclear Change"],
        series5 = energy_system.elecprod_TWh["Hydro Change"],
        series6 = energy_system.elecprod_TWh["Wind and Solar Change"],
        series8 = energy_system.elecprod_TWh["Bio Geo and Other Change"]
        )
    plt.show()


###############################################################################
# ELECTRICITY: Annual share of generation by category.
###############################################################################

    title = "Electricity Generation - Annual share of categories"
    ylabel = "Annual Share (%)"
    title1 = "Fossil Fuels"
    title2 = "Nuclear"
    title3 = "Renewables"
    title4 = "Geo Bio and Other"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Renewables is the sum of hydro, wind and solar.\nShares are calculated using \
gross generation quantities that don't account for imports or exports.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    esc1 = energy_system.elecprod_TWh["Fossil Fuels Share"]
    esc2 = energy_system.elecprod_TWh["Nuclear Share"]
    esc3 = energy_system.elecprod_TWh["Renewables Share"]
    esc4 = energy_system.elecprod_TWh["Bio Geo and Other Share"]

    print(
        "Sum of annual electricity generation category shares = \n" +
        str(esc1 + esc2 + esc3 + esc4)
        + "\n"
        )

    chart.line_1x4(
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
        ylabel,
        footer_text,
        True
        )
    plt.show()


###############################################################################
# ELECTRICITY: Annual share of generation by fuel.
###############################################################################

    title = "Electricity Generation - Annual share of fuels"
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Wind"
    title7 = "Solar"
    title8 = "Geo Bio and Other"
    ylabel = "Annual Share (%)"
    footer_text = \
"Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
Shares are calculated using gross generation quantities that don't account \
for imports or exports.\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"

    esf1 = energy_system.elecprod_TWh["Coal Share"]
    esf2 = energy_system.elecprod_TWh["Oil Share"]
    esf3 = energy_system.elecprod_TWh["Gas Share"]
    esf4 = energy_system.elecprod_TWh["Nuclear Share"]
    esf5 = energy_system.elecprod_TWh["Hydro Share"]
    esf6 = energy_system.elecprod_TWh["Wind Share"]
    esf7 = energy_system.elecprod_TWh["Solar Share"]
    esf8 = energy_system.elecprod_TWh["Bio Geo and Other Share"]

    print(
        "Sum of annual electricity generation fuel shares = \n" +
        str(esf1 + esf2 + esf3 + esf4 + esf5 + esf6 + esf7 + esf8)
        + "\n"
        )

    chart.line_2x4(
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
                   ylabel,
                   footer_text,
                   True
                   )
    plt.show()
