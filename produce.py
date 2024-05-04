#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:20:13 2024

@author: shanewhite
"""


###############################################################################
#
# Module: produce.py
#
# Description:
# Controls calling of chart functions.
#
###############################################################################


# Import Python modules.
import matplotlib.pyplot as plt


# Import user modules.
import user_globals
import chart


def charts(energy_system):

    title = energy_system.name

###############################################################################
# CO2 line plot.
###############################################################################
    chart.line(
        energy_system.co2_Mt.index,
        energy_system.co2_Mt,
        title,
        user_globals.Color.CO2.value,
        "Annual Carbon Dioxide Emissions from Fossil Fuels",
        "MtCO\u2082/year",
        "Data: Energy Institute Statistical Review of World Energy 2023,\n\
(https://www.energyinst.org/statistical-review/resources-and-data-downloads)\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n")
    plt.show()


###############################################################################
# Fossil Fuel Production 1x3 column plot with equiv y scale.
###############################################################################
    ylabel = "exajoules/year"
    if energy_system.name == "World":
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2023 (EI(2023)), \
https://www.energyinst.org/statistical-review/resources-and-data-downloads \
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe.\n\
Initial year of data for each fuel differs: coal 1981, oil 1965, and gas \
1970.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    else:
        footer_text = "Data: The Energy Institute Statistical Review of \
World Energy 2023 (EI(2023)), \
https://www.energyinst.org/statistical-review/resources-and-data-downloads \
\nOil production calculated by converting units of Mt to \
Joules using EI's approximate conversion factor of 41.868 GJ/toe.\n\
Initial year of data for each fuel differs: coal 1981, oil 1965, and gas \
1970.\n\
For comparison, EI(2023) listed 2022 World production values as: \
coal 175 EJ, oil 185 EJ, and gas 146 EJ.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    chart.column_1x3_equiv_scale(
        energy_system.ffprod_EJ["coal"],
        energy_system.ffprod_EJ["oil"],
        energy_system.ffprod_EJ["gas"],
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        title,
        "Annual Fossil Fuel Production",
        "Coal",
        "Oil",
        "Gas",
        ylabel,
        footer_text,
        True)

    plt.show()

###############################################################################
# Total Final Consumption Quantity 2x3 column plots with equiv y scale.
###############################################################################
    title_addition = "Annual Energy Consumption (Total Final \
Consumption or Final Energy). Final forms of consumed energy."

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"

    # Additional text.
    ylabel = ("petajoules/year")
    footer_text = "For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity production, such as steel maufacture or \
internal combustion etc.\nTFC data labelled 'Wind, solar etc' \
were for purposes other than electricity production, small and omitted for \
clarity.\nData: IEA 2023 World Energy Balances \
(https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances). Latest year of data as of 4/2024 is 2021.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data).\n"
    chart.column_subplot_2x3(
        energy_system.consumption_PJ["Coal"],
        energy_system.consumption_PJ["Oil"],
        energy_system.consumption_PJ["Gas"],
        energy_system.consumption_PJ["Biofuels and Waste"],
        energy_system.consumption_PJ["Electricity"],
        energy_system.consumption_PJ["Heat"],
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        title, title_addition, title1, title2, title3,
        title4, title5, title6, ylabel, footer_text, True)

    plt.show()


###############################################################################
# Total Final Consumption by share 2x3 column plots with equiv y scale.
###############################################################################
    title_addition = "Annual Energy Consumption by share"
    ylabel = ("Annual Share (%)")
    chart.line_subplot(energy_system.consumption_PJ["Coal Share"],
                     energy_system.consumption_PJ["Oil Share"],
                     energy_system.consumption_PJ["Gas Share"],
                     energy_system.consumption_PJ["Biofuels and Waste Share"],
                     energy_system.consumption_PJ["Electricity Share"],
                     energy_system.consumption_PJ["Heat Share"],
                     user_globals.Color.COAL.value,
                     user_globals.Color.OIL.value,
                     user_globals.Color.GAS.value,
                     user_globals.Color.BIOFUELS_AND_WASTE.value,
                     user_globals.Color.ELECTRICITY.value,
                     user_globals.Color.HEAT.value,
                    title, title_addition, title1, title2, title3,
                    title4, title5, title6, ylabel, footer_text, True)
    plt.show()

###############################################################################
# Total Final Consumption additions and subtractions of categories and fuels.
###############################################################################
    chart.column_grouped(
        title,
        "Annual Additions and Subtractions of Energy Consumption",
        "petajoules/year",
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nShares of 'other' are \
small and omitted for clarity. Renewables consists of solar, wind, \
geothermal, biofuels and other renewables.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data",
        user_globals.Constant.CHANGE_START_YEAR.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
        series1 = energy_system.consumption_PJ["Coal Change"],
        series2 = energy_system.consumption_PJ["Oil Change"],
        series3 = energy_system.consumption_PJ["Gas Change"],
        series4 = energy_system.consumption_PJ["Biofuels and Waste Change"],
        series5 = energy_system.consumption_PJ["Electricity Change"],
        series6 = energy_system.consumption_PJ["Heat Change"])
    plt.show()


###############################################################################
# Electricity Production 2x3 column plots with equiv y scale.
###############################################################################
    # Chart title.
    title_addition = "Annual Electricity Production"

    # Subplot titles.
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Renewables"

    # Additional text.
    ylabel = ("TWh/year")
    footer_text = "Shares of 'other' are small and omitted for clarity.\n\
Renewables consists of solar, wind, geothermal, biofuels and other \
renewables.\nData: The Energy Institute Statistical Review of World Energy \
2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data\n"
    chart.column_subplot_2x3(
        energy_system.elecprod_TWh["Coal"],
        energy_system.elecprod_TWh["Oil"],
        energy_system.elecprod_TWh["Gas"],
        energy_system.elecprod_TWh["Nuclear"],
        energy_system.elecprod_TWh["Hydro"],
        energy_system.elecprod_TWh["Renew"],
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.RENEW.value,
        title, title_addition, title1, title2, title3,
        title4, title5, title6, ylabel, footer_text, True)

    plt.show()

###############################################################################
# Electricity Production by share 2x3 column plots with equiv y scale.
###############################################################################
    title_addition = "Annual Electricity Production by share"
    ylabel = ("Annual Share (%)")
    chart.line_subplot(energy_system.elecprod_TWh["Coal Share"],
                       energy_system.elecprod_TWh["Oil Share"],
                       energy_system.elecprod_TWh["Gas Share"],
                       energy_system.elecprod_TWh["Nuclear Share"],
                       energy_system.elecprod_TWh["Hydro Share"],
                       energy_system.elecprod_TWh["Renew Share"],
                       user_globals.Color.COAL.value,
                       user_globals.Color.OIL.value,
                       user_globals.Color.GAS.value,
                       user_globals.Color.NUCLEAR.value,
                       user_globals.Color.HYDRO.value,
                       user_globals.Color.RENEW.value,
                       title, title_addition, title1, title2, title3,
                       title4, title5, title6, ylabel, footer_text, True)
    plt.show()

###############################################################################
# Annual Electricity additions and subtractions of categories and fuels
###############################################################################
    chart.column_grouped(
        energy_system.name.upper(),
        "Annual Additions and Subtractions of Electricity Production: By \
Category",
        "TWh/year",
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nShares of 'other' are \
small and omitted for clarity. Renewables consists of solar, wind, \
geothermal, biofuels and other renewables.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data",
        user_globals.Constant.CHANGE_START_YEAR.value,
        user_globals.Color.FOSSIL_FUELS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.RENEW.value,
        series1 = energy_system.elecprod_TWh["Fossil Fuels Change"],
        series2 = energy_system.elecprod_TWh["Nuclear Change"],
        series3 = energy_system.elecprod_TWh["Hydro Change"],
        series4 = energy_system.elecprod_TWh["Renew Change"])
    plt.show()

    chart.column_grouped(
        energy_system.name.upper(),
        "Annual Additions and Subtractions of Electricity Production: By Fuel",
        "TWh/year",
        "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nShares of 'other' are \
small and omitted for clarity. Renewables consists of solar, wind, \
geothermal, biofuels and other renewables.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data",
        user_globals.Constant.CHANGE_START_YEAR.value,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.NUCLEAR.value,
        user_globals.Color.HYDRO.value,
        user_globals.Color.RENEW.value,
        series1 = energy_system.elecprod_TWh["Coal Change"],
        series2 = energy_system.elecprod_TWh["Oil Change"],
        series3 = energy_system.elecprod_TWh["Gas Change"],
        series4 = energy_system.elecprod_TWh["Nuclear Change"],
        series5 = energy_system.elecprod_TWh["Hydro Change"],
        series6 = energy_system.elecprod_TWh["Renew Change"])
    plt.show()


###############################################################################
# Total Final Consumption and Electricity Treemaps for 1990 and final year
###############################################################################








'''

    # Consumption
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
    footer_text = "For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Shares of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity production, such as steel maufacture or \
internal combustion etc.\nTFC data labelled 'Wind, solar etc' \
were for purposes other than electricity production, small and omitted for \
clarity.\nData: IEA 2023 World Energy Balances \
(https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances). Latest year of data as of 4/2024 is 2021.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data).\n"

    #Plot
    chart.line_subplot(energy_system.consumption_PJ["Coal Share"],
                       energy_system.consumption_PJ["Oil Share"],
                       energy_system.consumption_PJ["Gas Share"],
                       energy_system.consumption_PJ["Biofuels and Waste \
Share"],
                       energy_system.consumption_PJ["Electricity Share"],
                       energy_system.consumption_PJ["Heat Share"],
                       user_globals.Color.COAL.value,
                       user_globals.Color.OIL.value,
                       user_globals.Color.GAS.value,
                       user_globals.Color.GEO_BIO.value,
                       user_globals.Color.ELECTRICITY.value,
                       user_globals.Color.HEAT.value,
                       title, title_addition, title1, title2, title3,
                       title4, title5, title6, ylabel, footer_text, True)

    plt.show()
'''
