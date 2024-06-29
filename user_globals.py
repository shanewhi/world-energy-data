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
import matplotlib as mpl
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
        co2_Mt,
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
    # Better to seperate than to place within primary_PJ dataframe.


# Define conversion coefficeints (multiply for conversion).
class Constant(Enum):
    C_TO_CO2 = 44 / 12
    k_TO_M = 1e-3
    G_TO_M = 1e3
    TJ_TO_PJ = 1e-3
    EJ_TO_PJ = 1e3
    PJ_TO_EJ = 1 / EJ_TO_PJ
    GJ_TO_PJ = 1e-6
    GJ_TO_EJ = 1e-9
    TONNES_TO_GJ = 41.868  # EI Conversion Factors sheet.
    CO2_RECENT_YEAR = 1980
    CO2_CHANGE_START_YEAR = 1950
    COAL_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large coal producer.
    OIL_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large oil producer.
    GAS_SHARE_RANK_THRESHOLD = 4  # Percent. Defines large gas producer.
    PRIMARY_ENERGY_CHANGE_START_YEAR = 1966
    ELEC_CHANGE_START_YEAR = 1995
    TFC_START_YEAR = 1990
    TFC_END_YEAR = 2021  # Final year of IEA data.

    # FONT SIZES:
    # 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    SUPTITLE_FONT_SIZE = "large"
    TITLE_FONT_SIZE = "xx-large"
    TITLE_ADDITION_FONT_SIZE = "medium"
    SUBPLOT_TITLE_FONT_SIZE = "large"
    FOOTER_TEXT_FONT_SIZE = "small"

    # FONT WEIGHTS:
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
    FIG_HSIZE_GROUPED_COLUMN_PLOT = 17

    FIG_VSIZE_1x1 = 6
    FIG_VSIZE_SUBPLOT_1X2 = 7
    FIG_VSIZE_SUBPLOT_1X3 = 7
    FIG_VSIZE_TREE_1X3 = 6.4
    FIG_VSIZE_SUBPLOT_2X3 = 10
    FIG_VSIZE_SUBPLOT_1X4 = 5.5
    FIG_VSIZE_SUBPLOT_2X4 = 9
    FIG_VSIZE_TREE_1X1 = 9.2
    FIG_VSIZE_TREE_1X2 = 9.2
    FIG_VSIZE_GROUPED_COLUMN_PLOT = 7

    LINE_WIDTH_PLOT_1x1 = 4
    LINE_WIDTH_SUBPOLT = 2.5
    LINE_MARKER_SIZE = 5
    DISPLAY_CHARTS = False

    # To install a font:
    # Copy .ttf files to ~/Library/Fonts
    # Then delete matplotlib's font cache using rm ~/.matplotlib/fontlist-v330.json
    # Finally restart IDE.
    #
    # To view all accessible fonts, enter:
    # sorted(matplotlib.font_manager.get_font_names())
    #
    # Not all fonts support Unicode subscript '2' and have a bold style.
    # To view fonts that support a subscript '2':
    # https://www.fileformat.info/info/unicode/char/2082/fontsupport.htm
    # Path to FreeSans:
    # https://ftp.gnu.org/gnu/freefont/
    CHART_FONT = "FreeSans"

    # All prebuilt chart styles: https://python-charts.com/matplotlib/styles/#list
    # Python chart gallery: https://python-graph-gallery.com/
    CHART_STYLE = "bmh"


# Define fuel colors for charts.
# Color library: https://matplotlib.org/stable/gallery/color/named_colors.html
class Color(Enum):
    CO2_EMISSION = "dimgray"  # "slategrey"#"lightsteelblue"
    CO2_CONC = "cornflowerblue"
    COAL = "black"
    OIL = "brown"
    GAS = "darkorange"
    FLARING = "hotpink"  # "violet"
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
    FOSSIL_FUELS = "grey"  # "dimgray"
    CEMENT = "cadetblue"  # "lightslategrey"
    LUC = "olivedrab"  # "saddlebrown"


# Set global font parameters.
plt.style.use(Constant.CHART_STYLE.value)
plt.rcParams["font.family"] = Constant.CHART_FONT.value
