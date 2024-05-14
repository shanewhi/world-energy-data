# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""


###############################################################################
#
# Module: user_globals.py
#
# Description:
# Globals definitions for application world_energy_data.py.
#
###############################################################################


# Import Python modules.
from enum import Enum


# Define custom class of an energy system.
class Energy_System:
    def __init__(
            self,
            name, # Country name.
            co2_Mt,
            ffprod_PJ,
            primary_PJ,
            primary_final_category_shares,
            primary_final_fuel_shares,
            elecprod_TWh,
            elecprod_final_category_shares,
            elecprod_final_fuel_shares,
            consumption_PJ,
            consumption_final_shares
            ):
        self.name = name
        self.co2_Mt = co2_Mt
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
        # Better to seperate than place within primary_PJ dataframe.


# Define conversion coefficeints (multiply for conversion).
class Constant(Enum):
    k_TO_M = 1E-3
    TJ_TO_PJ = 1E-3
    EJ_TO_PJ = 1E3
    PJ_TO_EJ = 1 / EJ_TO_PJ
    GJ_TO_PJ = 1E-6
    GJ_TO_EJ = 1E-9
    TONNES_TO_GJ = 41.868 # EI Conversion Factors sheet.
    PRIMARY_ENERGY_CHANGE_START_YEAR = 1966
    ELEC_CHANGE_START_YEAR = 1995
    TFC_START_YEAR = 1990
    TFC_END_YEAR = 2021

    # FONT SIZES:
    # 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    SUPTITLE_FONT_SIZE = "large"
    TITLE_FONT_SIZE = "xx-large"
    TITLE_ADDITION_FONT_SIZE = "medium"
    SUBPLOT_TITLE_FONT_SIZE = "large"
    FOOTER_TEXT_FONT_SIZE = "small"

    # FONT WEIGHTS:
    #'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman',
    #'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'
    SUPTITLE_FONT_WEIGHT = "normal"
    TITLE_FONT_WEIGHT = "bold"
    TITLE_ADDITION_FONT_WEIGHT = "normal"
    SUBPLOT_TITLE_FONT_WEIGHT = "semibold"
    FOOTER_TEXT_FONT_WEIGHT = "normal"

    FIG_HSIZE_1x1 = 8
    FIG_HSIZE_SUBPLOT_1X3 = 15
    FIG_HSIZE_SUBPLOT_2X3 = 15
    FIG_HSIZE_SUBPLOT_1X4 = 18
    FIG_HSIZE_SUBPLOT_2X4 = 18
    FIG_HSIZE_TREE_1X1 = 8
    FIG_HSIZE_TREE_1X2 = 15

    FIG_VSIZE_1x1 = 8
    FIG_VSIZE_SUBPLOT_1X3 = 6
    FIG_VSIZE_SUBPLOT_2X3 = 10
    FIG_VSIZE_SUBPLOT_1X4 = 5
    FIG_VSIZE_SUBPLOT_2X4 = 9
    FIG_VSIZE_TREE_1X1 = 9.2
    FIG_VSIZE_TREE_1X2 = 9.2

    FIG_VSIZE_GROUPED_COLUMN_PLOT = 9
    FIG_HSIZE_GROUPED_COLUMN_PLOT = 18

    LINE_WIDTH_PLOT_1x1 = 4
    LINE_WIDTH_SUBPOLT = 2.5
    LINE_MARKER_SIZE = 5
    CHART_DPI = 100

    # IBM Plex Sans font installed manually by copying Google font ttf files to
    # Python's font directory.
    CHART_FONT = "IBM Plex Sans" #all: matplotlib.font_manager.get_font_names()
    CHART_STYLE = "bmh"     #"default", "seaborn-darkgrid"
# All prebuilt chart styles: https://python-charts.com/matplotlib/styles/#list
# Python chart gallery: https://python-graph-gallery.com/


# Define fuel colors for charts.
class Color(Enum):
    BOLD = '\033[1m'
    CO2 = "slategrey"#"lightsteelblue"
    COAL = "black"
    OIL = "brown"
    GAS = "darkorange"
    NUCLEAR = "darkviolet"
    HYDRO = "dodgerblue"
    WIND = "blue"
    SOLAR = "crimson"
    BIOFUELS_AND_WASTE = "sienna"
    OTHER = "peru"
    HEAT = "darkmagenta"
    RENEWABLES = "green"
    WIND_AND_SOLAR = "limegreen"
    ELECTRICITY = "teal"
    FOSSIL_FUELS = "dimgray"
# Color library: https://matplotlib.org/stable/gallery/color/named_colors.html


# Define dataset as global.
global ei_data_import
ei_data_import = []



