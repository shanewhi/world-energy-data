# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Mar 20 14:19:37 2024
# @author: shanewhite


# Import Python modules.
from enum import Enum


# Define conversion coefficeints (multiply for conversion).
# Chart sizes suit 16" MBP screen
class Constant(Enum):
    k_TO_M = 1E-3
    TJ_TO_PJ = 1E-3
    EJ_TO_PJ = 1E3
    PJ_TO_EJ = 1 / EJ_TO_PJ
    COAL_PROD_START_YEAR = 1981
    OIL_PROD_START_YEAR = 1965
    GAS_PROD_START_YEAR = 1970
    CHANGE_START_YEAR = 1995
    TFC_START_YEAR = 1990
    TFC_END_YEAR = 1991
    SUPTITLE_FONT_SIZE = "large"
    SUPTITLE_FONT_WEIGHT = "normal"
    SUPTITLE_ADDITION_FONT_SIZE = "x-large"
    SUPTITLE_ADDITION_FONT_WEIGHT = "bold"
    TITLE_FONT_SIZE = "normal"
    TITLE_FONT_WEIGHT = "normal"
    FOOTER_TEXT_FONT_SIZE = "small"
    FOOTER_TEXT_FONT_WEIGHT = "normal"
    FIG_VSIZE = 8.2
    FIG_HSIZE = 8
    FIG_VSIZE_SUBPLOT_1X3 = 5.5
    FIG_HSIZE_SUBPLOT_1X3 = 15
    FIG_VSIZE_SUBPLOT_2X3 = 10
    FIG_HSIZE_SUBPLOT_2X3 = 15
    FIG_VSIZE_COLUMN_PLOT = 8
    FIG_HSIZE_COLUMN_PLOT = 18
    FIG_VSIZE_TREE_1X2 = 7
    FIG_HSIZE_TREE_1X2 = 12
    LINE_WIDTH_PLOT_1x1 = 4
    LINE_WIDTH_SUBPOLT = 2.5
    LINE_MARKER_SIZE = 5
    CHART_DPI = 100
    CHART_FONT = "Open Sans" #all: matplotlib.font_manager.get_font_names()
    CHART_STYLE = "bmh"     #"default", "seaborn-darkgrid"
# All prebuilt chart styles: https://python-charts.com/matplotlib/styles/#list


# Define fuel colors for charts.
# https://matplotlib.org/stable/gallery/color/named_colors.html
class Color(Enum):
     COAL = "black"
     OIL = "brown"
     GAS = "darkorange"
     NUCLEAR = "darkmagenta"
     HYDRO = "dodgerblue"
     WIND = "blue"
     SOLAR = "crimson"
     GEO_BIO = "sienna"
     OTHER = "tan"
     HEAT = "purple"
     FOSSIL_FUELS = "dimgray"
     RENEW = "forestgreen"
     WIND_SOLAR = "limegreen"
     ELECTRICITY = "teal"
     CO2 = "black"
# Python chart gallery: https://python-graph-gallery.com/


# Define dataset as global.
global ei_data_import
ei_data_import = []


# Define custom class for a national energy system.
class Energy_System:
    def __init__(
            self,
            name, # Country name.
            co2_combust_Mt,
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm,
            primary_PJ,
            elec_gen_TWh,
            tf_consumption_PJ):
        self.name = name
        self.co2_combust_Mt = co2_combust_Mt
        self.coalprod_Mt = coalprod_Mt
        self.oilprod_Mbpd = oilprod_Mbpd
        self.gasprod_bcm = gasprod_bcm
        self.primary_PJ = primary_PJ
        self.elec_gen_TWh = elec_gen_TWh
        self.tf_consumption_PJ = tf_consumption_PJ
