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

    title = energy_system.name


    # CO2: Annual emissions over time.
    title_addition = "Annual Carbon Dioxide Emissions from Fossil Fuels"
    ylabel = "MtCO\u2082/year"
    footer_text = "Data: Energy Institute Statistical Review of World \
Energy 2023, \n\
(https://www.energyinst.org/statistical-review/resources-and-data-downloads)\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    color = user_globals.Color.CO2.value

    chart.line(
        energy_system.co2_Mt.index,
        energy_system.co2_Mt,
        title,
        color,
        title_addition,
        ylabel,
        footer_text
        )
    plt.show()


    # PRODUCTION: Fossil Fuel production over time.
    title_addition = "Annual Fossil Fuel Production"
    subplot1_title = "Coal"
    subplot2_title = "Oil"
    subplot3_title = "Gas"
    ylabel = "Exajoule"
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
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value
    equiv_scale = True

    chart.column_1x3(
        energy_system.ffprod_EJ["coal"],
        energy_system.ffprod_EJ["oil"],
        energy_system.ffprod_EJ["gas"],
        color1,
        color2,
        color3,
        title,
        title_addition,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabel,
        footer_text,
        equiv_scale
        )
    plt.show()


    # PRIMARY ENERGY: Annual change of fossil fuel category over time.
    if title == "World":
         ylabel = "Exajoule/year"
         series = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
    else:
         ylabel = "Annual Change (petajoules/year)"
         series = pd.Series(energy_system.primary_PJ["Fossil Fuels Change"])
    title_addition = "Annual Change of Fossil Fuel Category in Energy Supply \
(Primary Energy)"
    footer_text = "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nFor an explanation of \
primary energy, refer to \
https://www.worldenergydata.org/introduction/\n\
Data: The Energy Institute Statistical Review of World Energy 2023 \
(https://www.energyinst.org/statistical-review/resources-and-data-downloads)\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    plot_start_yr = \
        user_globals.Constant.PRIMARY_ENERGY_CHANGE_START_YEAR.value
    color = user_globals.Color.FOSSIL_FUELS.value

    chart.column_grouped(
        title,
        title_addition,
        ylabel,
        footer_text,
        plot_start_yr,
        color,
        series1 = series
        )
    plt.show()

    # PRIMARY ENERGY: Annual change of fossil fuels over time.
    if title == "World":
        ylabel = "Exajoule/year"
        s1 = pd.Series(energy_system.primary_PJ["Coal Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        s2 = pd.Series(energy_system.primary_PJ["Oil Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        s3 = pd.Series(energy_system.primary_PJ["Gas Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
    else:
         ylabel = "Petajoule/year"
         s1 = pd.Series(energy_system.primary_PJ["Coal Change"])
         s2 = pd.Series(energy_system.primary_PJ["Oil Change"])
         s3 = pd.Series(energy_system.primary_PJ["Gas Change"])

    title_addition = "Annual Change of Fossil Fuels in Energy Supply \
(Primary Energy)"
    footer_text = "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nFor an explanation of \
primary energy, refer to \
https://www.worldenergydata.org/introduction/\n\
Data: The Energy Institute Statistical Review of World Energy 2023 \
(https://www.energyinst.org/statistical-review/resources-and-data-downloads)\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    plot_start_yr = \
        user_globals.Constant.PRIMARY_ENERGY_CHANGE_START_YEAR.value
    color1 = user_globals.Color.COAL.value
    color2 = user_globals.Color.OIL.value
    color3 = user_globals.Color.GAS.value

    chart.column_grouped(
         title,
         title_addition,
         ylabel,
         footer_text,
         plot_start_yr,
         color1,
         color2,
         color3,
         series1 = s1,
         series2 = s2,
         series3 = s3
         )
    plt.show()

    # PRIMARY ENERGY: Annual shares of most recent year.
    suptitle = title
    suptitle_addition = "Energy Supply by share (Primary Energy), \
year " + str(energy_system.primary_PJ.index[-1])
    title1 = "Category Shares"
    title2 = "Fuel Shares"
    footer_text = "For clarity: (1) Values are rounded, so shares may not \
total 100%, (2) Shares <1% aren't shown,\n(3) Labels may not be shown due to \
a lack of space, in which case refer to the legend.\n\
For an explanation of primary energy, refer to \
https://www.worldenergydata.org/introduction/\n\
Data: The Energy Institute Statistical Review of World Energy 2023 \
(https://www.energyinst.org/statistical-review/resources-and-data-downloads)\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data)\n"
    
    chart.treemap(
        energy_system.primary_category_shares,
        energy_system.primary_fuel_shares,
        title1,
        title2,
        suptitle,
        suptitle_addition,
        footer_text
        )
    plt.show()

    # FINAL ENERGY AND ELECTRICITY COMBINED: Shares for most recent year.
    suptitle = title
    suptitle_addition = "Share of Fuels in Energy Consumption, year" + \
        str(energy_system.consumption_PJ.index[-1]) + " and  Electricity \
Generation, year "+ str(energy_system.elecprod_TWh.index[-1])
    title1 = "Energy Consumption"
    title2 = "Electricity Generation"
    footer_text = "For clarity: (1) Values are rounded, so shares may not \
total 100%, (2) Shares <1% aren't shown,\n(3) Labels may not be shown due to \
a lack of space, in which case refer to the legend.\n\
For an explanation of Energy Consumption (also known as Final Energy or Total \
Final Consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Shares shown in the left hand chart of coal, oil, gas, biofuels, and waste \
were consumed for purposes other than electricity generation, such as steel \
maufacture or internal combustion etc.\nTFC data labelled 'Wind, solar etc' \
were for purposes other than electricity production, small and omitted for \
clarity.\nEnergy Consumption data: IEA 2023 World Energy Balances \
(https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances). Latest year of data as of 4/2024 is 2021.\n\
Electricity Generation data: The Energy Institute Statistical Review of World \
Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data).\n"

    chart.treemap(
        energy_system.consumption_final_shares,
        energy_system.elecprod_final_fuel_shares,
        title1,
        title2,
        suptitle,
        suptitle_addition,
        footer_text)
    plt.show()
    
    # FINAL ENERGY: Annual quantities over time.
    if title == "World":
         ylabel = "Exajoules"
         series1 = pd.Series(energy_system.consumption_PJ["Coal"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         series2 = pd.Series(energy_system.consumption_PJ["Oil"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         series3 = pd.Series(energy_system.consumption_PJ["Gas"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         series4 = \
             pd.Series(energy_system.consumption_PJ["Biofuels and Waste"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         series5 = pd.Series(energy_system.consumption_PJ["Electricity"] * \
             user_globals.Constant.PJ_TO_EJ.value)
         series6 = pd.Series(energy_system.consumption_PJ["Heat"] * \
             user_globals.Constant.PJ_TO_EJ.value)
    else:
        ylabel = "Petajoules"
        series1 = energy_system.consumption_PJ["Coal"]
        series2 = energy_system.consumption_PJ["Oil"]
        series3 = energy_system.consumption_PJ["Gas"]
        series4 = energy_system.consumption_PJ["Biofuels and Waste"]
        series5 = energy_system.consumption_PJ["Electricity"]
        series6 = energy_system.consumption_PJ["Heat"]

    title_addition = "Annual Energy Consumption (Total Final \
Consumption or Final Energy) - final forms of consumed energy"

    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Biofuels and Waste"
    title5 = "Electricity"
    title6 = "Heat"

    footer_text = "For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel maufacture or \
internal combustion etc. Additional fossil fuels were combusted to produce \
electricity.\nData labelled 'Wind, solar etc' were consumed for purposes \
other than electricity production, small and omitted for clarity.\n\
Data: IEA 2023 World Energy Balances \
(https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances). Latest year of data as of 4/2024 is 2021.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data).\n"

    chart.column_2x3(
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        user_globals.Color.COAL.value,
        user_globals.Color.OIL.value,
        user_globals.Color.GAS.value,
        user_globals.Color.BIOFUELS_AND_WASTE.value,
        user_globals.Color.ELECTRICITY.value,
        user_globals.Color.HEAT.value,
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


    # FINAL ENERGY: Annual change of quantity over time.
    if title == "World":
        ylabel = "Exajoule/year"
        s1 = pd.Series(energy_system.consumption_PJ["Coal Change"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        s2 = pd.Series(energy_system.consumption_PJ["Oil Change"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        s3 = pd.Series(energy_system.consumption_PJ["Gas Share"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        s4 = pd.Series( \
                   energy_system.consumption_PJ["Biofuels and Waste Share"] * \
             user_globals.Constant.PJ_TO_EJ.value)
        s5 = pd.Series(energy_system.consumption_PJ["Electricity Share"] * \
            user_globals.Constant.PJ_TO_EJ.value)
        s6 = pd.Series(energy_system.consumption_PJ["Heat Share"] * \
            user_globals.Constant.PJ_TO_EJ.value)
    else:
        ylabel = "Petajoule/year"
        s1 = pd.Series(energy_system.consumption_PJ["Coal Change"])
        s2 = pd.Series(energy_system.consumption_PJ["Oil Change"])
        s3 = pd.Series(energy_system.consumption_PJ["Gas Share"])
        s4 = pd.Series( \
                   energy_system.consumption_PJ["Biofuels and Waste Share"])
        s5 = pd.Series(energy_system.consumption_PJ["Electricity Share"])
        s6 = pd.Series(energy_system.consumption_PJ["Heat Share"])

    title_addition = "Annual Additions and Subtractions of Energy Consumption \
- final forms of consumed energy"
    footer_text = "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\n\
For an explanation of total final consumption (TFC), refer \
to https://www.worldenergydata.org/introduction/\n\
Quantities of coal, oil, gas, biofuels, and waste shown were consumed for \
purposes other than electricity generation, such as steel maufacture or \
internal combustion etc. Additional fossil fuels were combusted to produce \
electricity.\nTFC data labelled 'Wind, solar etc' were for purposes other \
than electricity production, small and omitted for clarity.\n\
Data: IEA 2023 World Energy Balances \
(https://www.iea.org/data-and-statistics/data-product/world-energy-\
statistics-and-balances). Latest year of data as of 4/2024 is 2021.\n\
By shanewhite@worldenergydata.org using Python \
(https://github.com/shanewhi/world-energy-data).\n"

    chart.column_grouped(
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
        series1 = s1,
        series2 = s2,
        series3 = s3,
        series4 = s4,
        series5 = s5,
        series6 = s6
        )
    plt.show()


    # FINAL ENERGY: Annual share over time.
    title_addition = "Annual Energy Consumption (Total Final \
Consumption or Final Energy) by share - final forms of consumed energy"
    ylabel = ("Annual Share (%)")
    chart.line_2x3(energy_system.consumption_PJ["Coal Share"],
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


    # ELECTRICITY: Annual generation quantity by category over time.
    title_addition = "Annual Electricity Generation by category"
    title1 = "Fossil Fuels"
    title2 = "Nuclear"
    title3 = "Renewables"
    title4 = "Geo Bio and Other"
    ylabel = "TWh"
    footer_text = "Quantities are gross production and don't account for \
imports or exports.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
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
                    title,
                    title_addition,
                    title1,
                    title2,
                    title3,
                    title4,
                    ylabel,
                    footer_text,
                    True
                    )
    plt.show()

    # ELECTRICITY: Annual generation quantity by fuel over time.
    title_addition = "Annual Electricity Generation by fuel"
    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Wind"
    title7 = "Solar"
    title8 = "Geo Bio and Other"
    ylabel = "TWh"
    footer_text = "Quantities are gross production and don't account for \
imports or exports.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
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
        title,
        title_addition,
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

    # ELECTRICITY: Annual share of generation by category.
    title_addition = "Annual share of Electricity Generation by category"
    ylabel = "Annual Share (%)"
    title1 = "Fossil Fuels"
    title2 = "Nuclear"
    title3 = "Renewables"
    title4 = "Geo Bio and Other"
    chart.line_1x4(energy_system.elecprod_TWh["Fossil Fuels Share"],
                    energy_system.elecprod_TWh["Nuclear Share"],
                    energy_system.elecprod_TWh["Renewables Share"],
                    energy_system.elecprod_TWh["Bio Geo and Other Share"],
                    user_globals.Color.FOSSIL_FUELS.value,
                    user_globals.Color.NUCLEAR.value,
                    user_globals.Color.RENEWABLES.value,
                    user_globals.Color.OTHER.value,
                     title, title_addition, title1, title2, title3, title4,
                     ylabel, footer_text, True)
    plt.show()

    title1 = "Coal"
    title2 = "Oil"
    title3 = "Gas"
    title4 = "Nuclear"
    title5 = "Hydro"
    title6 = "Wind"
    title7 = "Solar"
    title8 = "Geo Bio and Other"
    title_addition = "Annual share of Electricity Generation by share of fuel"
    ylabel = "Annual Share (%)"
    chart.line_2x4(energy_system.elecprod_TWh["Coal Share"],
                   energy_system.elecprod_TWh["Oil Share"],
                   energy_system.elecprod_TWh["Gas Share"],
                   energy_system.elecprod_TWh["Nuclear Share"],
                   energy_system.elecprod_TWh["Hydro Share"],
                   energy_system.elecprod_TWh["Wind Share"],
                   energy_system.elecprod_TWh["Solar Share"],
                   energy_system.elecprod_TWh["Bio Geo and Other Share"],
                   user_globals.Color.COAL.value,
                   user_globals.Color.OIL.value,
                   user_globals.Color.GAS.value,
                   user_globals.Color.NUCLEAR.value,
                   user_globals.Color.HYDRO.value,
                   user_globals.Color.WIND.value,
                   user_globals.Color.SOLAR.value,
                   user_globals.Color.OTHER.value,
                   title,
                   title_addition,
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


    # ELECTRICITY: Change of generation by category over time.
    title_addition = "Annual Additions and Subtractions of Electricity \
Generation by category"
    ylabel = "TWh/year"
    footer_text = "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nShares of 'other' are \
small and omitted for clarity. Renewables consists of solar, wind, \
geothermal, biofuels and other renewables.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data"

    chart.column_grouped(
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

    # ELECTRICITY: Change of generation by fuel over time.
    title_addition = "Annual Additions and Subtractions of Electricity \
Generation by fuel"
    ylabel = "TWh/year"
    footer_text = "For clarity: (1) Values of change at tops of columns are \
rounded to nearest whole number, (2) Values that round to zero are not shown, \
(3) When the value of a column is zero, the column is not \
shown resulting in a gap between plotted columns.\nShares of 'other' are \
small and omitted for clarity. Renewables consists of solar, wind, \
geothermal, biofuels and other renewables.\n\
Data: The Energy Institute Statistical Review of World Energy 2023, \
https://www.energyinst.org/statistical-review/resources-and-data-downloads\n\
By shanewhite@worldenergydata.org using Python, \
https://github.com/shanewhi/world-energy-data"

    chart.column_grouped(
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

