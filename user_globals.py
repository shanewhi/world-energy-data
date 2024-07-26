# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""


########################################################################################
#
# Module: user_globals.py
#
# Description:
# Globals definitions for application world_energy_data.py.
#
########################################################################################

# Import Python modules.
from enum import Enum
import matplotlib.pyplot as plt


# Define custom class of an energy system.
class Global_Carbon:
    def __init__(
        self,
        name,
        data,
        final_emission_category_shares,
        final_emission_shares,
        co2_conc,
    ):
        self.name = name
        self.data = data
        self.final_emission_category_shares = final_emission_category_shares
        self.final_emission_shares = final_emission_shares
        self.co2_conc = co2_conc

    # Final share dataframes are required by treemap function.
    # Better to seperate in this class than to place within another dataframe.


# Define custom class of an energy system.
class Energy_System:
    def __init__(
        self,
        name,  # Country name.
        incl_ei_flag,  # True if country appears in EI data.
        incl_iea_flag,  # True if country appears in IEA data.
        ffco2,
        ffprod_PJ,
        primary_PJ,
        primary_final_category_shares,
        primary_final_fuel_shares,
        elecprod_TWh,
        elecprod_final_category_shares,
        elecprod_final_fuel_shares,
        consumption_PJ,
        consumption_final_shares,
    ):
        self.name = name
        self.incl_ei_flag = incl_ei_flag
        self.incl_iea_flag = incl_iea_flag
        self.ffco2 = ffco2
        self.ffprod_PJ = ffprod_PJ
        self.primary_PJ = primary_PJ
        self.primary_final_category_shares = primary_final_category_shares
        self.primary_final_fuel_shares = primary_final_fuel_shares
        self.elecprod_TWh = elecprod_TWh
        self.elecprod_final_category_shares = elecprod_final_category_shares
        self.elecprod_final_fuel_shares = elecprod_final_fuel_shares
        self.consumption_PJ = consumption_PJ
        self.consumption_final_shares = consumption_final_shares

    # Final share dataframes are required by treemap function.
    # Better to seperate than to place within another dataframe.


# Define conversion coefficeints (multiply for conversion).
class Constant(Enum):

    DISPLAY_CHARTS = True  # Whether charts are output to display.
    CHART_START_YR = 2000  # Start year for all charts.

    C_TO_CO2 = 44 / 12
    k_TO_M = 1e-3
    G_TO_M = 1e3
    TJ_TO_PJ = 1e-3
    EJ_TO_PJ = 1e3
    PJ_TO_EJ = 1 / EJ_TO_PJ
    GJ_TO_PJ = 1e-6
    GJ_TO_EJ = 1e-9
    TONNES_TO_GJ = 41.868  # EI Conversion Factors sheet.
    COAL_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large coal producer.
    OIL_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large oil producer.
    GAS_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large gas producer.

    # Processing of IEA data takes a noticeably long time.
    # To shorten execution time during testing, set TFC_START_YEAR to 1999
    # and TFC_END_YEAR to 2000 or later. This assumes CHART_START_YR = 2000.
    # Default values as of 6/2024 are:
    #    TFC_START_YEAR = 1990
    #    TFC_END_YEAR = 2021
    TFC_START_YEAR = 1999
    TFC_END_YEAR = 2001  # End year of IEA data iw 2021 in 6/2024.

    # FONT SIZES:
    # Options: 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    SUPTITLE_FONT_SIZE = "large"
    TITLE_FONT_SIZE = "xx-large"
    TITLE_ADDITION_FONT_SIZE = "medium"
    SUBPLOT_TITLE_FONT_SIZE = "large"
    FOOTER_TEXT_FONT_SIZE = "small"

    # FONT WEIGHTS:
    # Options -
    # 'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman',
    # 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'
    SUPTITLE_FONT_WEIGHT = "normal"
    TITLE_FONT_WEIGHT = "bold"
    TITLE_ADDITION_FONT_WEIGHT = "normal"
    SUBPLOT_TITLE_FONT_WEIGHT = "semibold"
    FOOTER_TEXT_FONT_WEIGHT = "normal"

    FIG_HSIZE_1x1 = 10
    FIG_HSIZE_SUBPLOT_1X2 = 17
    FIG_HSIZE_SUBPLOT_1X3 = 17
    FIG_HSIZE_TREE_1X3 = 17
    FIG_HSIZE_SUBPLOT_2X3 = 17
    FIG_HSIZE_SUBPLOT_1X4 = 17
    FIG_HSIZE_SUBPLOT_2X4 = 17
    FIG_HSIZE_TREE_1X1 = 8
    FIG_HSIZE_TREE_1X2 = 15
    FIG_HSIZE_CHANGE_SS_COLUMN_PLOT = 12  # For single series plot.
    FIG_HSIZE_CHANGE_COLUMN_PLOT = 17

    FIG_VSIZE_1x1 = 7
    FIG_VSIZE_SUBPLOT_1X2 = 7
    FIG_VSIZE_SUBPLOT_1X3 = 7
    FIG_VSIZE_TREE_1X3 = 6.4
    FIG_VSIZE_SUBPLOT_2X3 = 10
    FIG_VSIZE_SUBPLOT_1X4 = 5.5
    FIG_VSIZE_SUBPLOT_2X4 = 9
    FIG_VSIZE_TREE_1X1 = 9.2
    FIG_VSIZE_TREE_1X2 = 9.2
    FIG_VSIZE_CHANGE_COLUMN_PLOT = 7

    LINE_WIDTH_PLOT_1x1 = 4
    LINE_WIDTH_SUBPOLT = 2.5
    LINE_MARKER_SIZE = 5


# Define colors for charts.
# Color library: https://matplotlib.org/stable/gallery/color/named_colors.html
class Color(Enum):
    CO2_CONC = "cornflowerblue"
    CO2_EMISSION = "slategrey"
    FOSSIL_FUELS = "grey"
    CEMENT = "cadetblue"
    LUC = "olivedrab"
    COAL = "black"
    OIL = "brown"
    GAS = "darkorange"
    FLARING = "hotpink"
    NUCLEAR = "darkviolet"
    HYDRO = "dodgerblue"
    WIND = "blue"
    SOLAR = "crimson"
    BIOFUELS_AND_WASTE = "saddlebrown"
    OTHER = "peru"
    HEAT = "rebeccapurple"
    RENEWABLES = "green"
    WIND_AND_SOLAR = "limegreen"
    ELECTRICITY = "teal"
    UNPUBLISHED = "steelblue"


# All prebuilt chart styles: https://python-charts.com/matplotlib/styles/#list
# Python chart gallery: https://python-graph-gallery.com/
# Matplotlib universal settings:
# https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams
rc = {
    # "axes.edgecolor": "gray",
    # "axes.linewidth": 0.5,
    "xtick.direction": "out",
    "xtick.color": "grey",
    "xtick.labelcolor": "black",
    "ytick.direction": "out",
    "ytick.color": "grey",
    "ytick.labelcolor": "black",
}
plt.style.use(("bmh", rc))

# Set global font parameters.
# If you add a font to the OS, be sure to delete all matplotlib's font cache files in
# ~/.matplotlib.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["SF Pro Display"]
