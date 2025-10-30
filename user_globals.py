# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################################################
#
# Module: user_globals.py
#
# Description:
# Globals definitions for script world_energy_data.py.
#
########################################################################################################################

# Import Python modules.
from enum import Enum
import matplotlib.pyplot as plt


# Define custom class for organising fossil fuel CO2 emissions and atmospheric CO2 data
class Global_Carbon:
    def __init__(
            self,
            name,  # 'World' label used on plots.
            c_budget,  # Copy of Global Carbon Budget.
            emission_category_shares_fy,  # Final year shares of global CO2 emissions by category using Global Carbon
            # Budget organised into format for plotting treemap.
            emission_source_shares_fy,  # Final year shares of global CO2 emissions by source using Global Carbon Budget
            # organised into format for plotting treemap.
            remaining_c_budget_data,  # Global CO2 pathways using remaining carbon budgets.
            co2_conc,  # Copy of NOAA ESRL data for atmospheric CO2 concentration.
            country_shares_fy,  # Country shares of fossil fuel CO2 emissions for final year.
    ):
        self.name = name
        self.c_budget = c_budget
        self.emission_category_shares_fy = emission_category_shares_fy
        self.emission_source_shares_fy = emission_source_shares_fy
        self.remaining_c_budget_data = remaining_c_budget_data
        self.co2_conc = co2_conc
        self.country_shares_fy = country_shares_fy


# Define custom class of a country, or the world's energy system.
class Energy_System:
    def __init__(self,
                 country,  # Country name.
                 incl_ei_flag,  # True if country appears in EI data.
                 ffco2_Mt,  # Annual national fossil fuel CO2 emissions in units of megatonnes.
                 ffco2_Gt,  # Annual national fossil fuel CO2 emissions in units of gigatonnes.
                 pc_tco2,  # Final year per capita fossil fuel CO2 emissions for all countries.
                 country_pc_tco2,  # Final year per capita fossil fuel CO2 emissions for country.
                 pc_associated_data,  # Data used for footer text in per capita fossil fuel CO2 chart.
                 sector_co2_Mt,  # Annual national CO2 emissions by sector in units of megatonnes.
                 ffprod_PJ,  # Annual fossil fuel production in units of peta joules.
                 primary_PJ,  # Annual primary energy in units of peta joules.
                 elecgen_TWh,  # Annual electricity generation in units of tera Watt hours.
                 elecgen_PWh,  # Annual electricity generation in units of peta Watt hours.
                 elecgen_category_fy_shares,  # Electricity generation by category share for final year.
                 elecgen_fuel_fy_shares,  # Electricity generation by fuel share for final year.
                 finalenergy_PJ,  # Annual final energy in units of peta joules.
                 finalenergy_fy_shares,  # Final energy by share of fuel for final year.
                 ):
        self.country = country
        self.incl_ei_flag = incl_ei_flag
        self.ffco2_Mt = ffco2_Mt
        self.ffco2_Gt = ffco2_Gt
        self.pc_tco2 = pc_tco2
        self.country_pc_tco2 = country_pc_tco2
        self.pc_associated_data = pc_associated_data
        self.sector_co2_Mt = sector_co2_Mt
        self.ffprod_PJ = ffprod_PJ
        self.primary_PJ = primary_PJ
        self.elecgen_TWh = elecgen_TWh
        self.elecgen_PWh = elecgen_PWh
        self.elecgen_category_fy_shares = elecgen_category_fy_shares
        self.elecgen_fuel_fy_shares = elecgen_fuel_fy_shares
        self.finalenergy_PJ = finalenergy_PJ
        self.finalenergy_fy_shares = finalenergy_fy_shares


# Define conversion coefficients (multiply for conversion) and presets.
class Constant(Enum):
    DISPLAY_CHARTS = False  # Whether charts are output to monitor.
    CHART_START_YR_FOR_MAJOR_EMITTERS = 1965  # Start year for plots of major emitter emissions and fossil fuel primary
    # energy.
    CHART_START_YR = 2000  # Start year for all charts except change charts
    CHANGE_CHART_START_YR = 2010

    C_TO_CO2 = 44 / 12
    k_TO_M = 1e-3
    G_TO_M = 1e3
    TJ_TO_PJ = 1e-3
    EJ_TO_PJ = 1e3
    PJ_TO_EJ = 1e-3
    GJ_TO_PJ = 1e-6
    GJ_TO_EJ = 1e-9
    TWH_TO_PWH = 1e-3
    TOE_TO_GJ = 41.87  # https://www.iea.org/data-and-statistics/data-tools/unit-converter

    LARGE_EMITTER_SHARE_THRESHOLD = 0.5  # Percent of global FF CO2 emissions. Defines country as large CO2 emitter.
    # This includes the following 'Major' emitting countries below.
    # Such countries are designated individual tiles in the treemap of fossil fuel CO2 emissions by country share.
    MAJOR_EMITTER_SHARE_THRESHOLD = 1  # Percent of global FF CO2 emissions. Defines country as a major emitter of
    # fossil fuel CO2. Such countries are designated individual tiles and have their name displayed in the treemap of
    # fossil fuel CO2 emissions by country share, and have their fossil fuel primary energy trends plotted and saved in
    # the Major Emitters folder.
    PER_CAPITA_THRESHOLD = 0  # tCO2/per-capita. Values greater than or equal to this threshold are plotted individually
    # and the remainder are plotted as 'Other'.
    COAL_SHARE_RANK_THRESHOLD = 5  # Percent of global coal production. Defines large coal producer.
    OIL_SHARE_RANK_THRESHOLD = 2  # Percent of global oil production. Defines large oil producer.
    GAS_SHARE_RANK_THRESHOLD = 1.5  # Percent of global gas production. Defines large gas producer.

    # Threshold below which column chart displayed as solid line instead for visibility.
    COL_TO_LINE = 0.005

    # FONT SIZES:
    # Named options: 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'
    SUPTITLE_FONT_SIZE = 'large'
    TITLE_FONT_SIZE = 'xx-large'
    TITLE_ADDITION_FONT_SIZE = 'medium'
    SUBPLOT_TITLE_FONT_SIZE = 'large'
    SUBPLOT_2ROW_TITLE_FONT_SIZE = 'large'
    FOOTER_TEXT_FONT_SIZE = 'small'
    MAJOR_EMITTER_TITLE_FONT_SIZE = 40
    MAJOR_EMITTER_SUB_TITLE_FONT_SIZE = 'large'
    MAJOR_EMITTER_TICK_FONT_SIZE = 'small'
    MAJOR_EMITTER_AXIS_LABEL_FONT_SIZE = 'small'

    # FONT WEIGHTS:
    SUPTITLE_FONT_WEIGHT = 'regular'
    TITLE_FONT_WEIGHT = 'bold'
    TITLE_ADDITION_FONT_WEIGHT = 'regular'
    SUBPLOT_TITLE_FONT_WEIGHT = 'regular'
    TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT = 'bold'
    SUBPLOT_2ROW_TITLE_FONT_WEIGHT = 'regular'
    SUBPLOT_3ROW_TITLE_FONT_WEIGHT = 'regular'
    FOOTER_TEXT_FONT_WEIGHT = 'regular'
    MAJOR_EMITTER_TITLE_FONT_WEIGHT = 'bold'
    MAJOR_EMITTER_SUB_TITLE_FONT_WEIGHT = 'regular'

    # FIGURE SIZES.
    # To inspect, set DISPLAY_CHARTS True, and use the chart sliders. Set ALL parameters.
    FIG_HSIZE_SINGLE_PLOT = 10
    FIG_VSIZE_SINGLE_PLOT = 10

    FIG_HSIZE_1_ROW = 17
    FIG_VSIZE_1_ROW = 5.5
    FIG_VSIZE_1_ROW_TALL = 7
    FIG_VSIZE_1_ROW_TALLER = 7.5

    FIG_HSIZE_2_ROW = 17
    FIG_VSIZE_2_ROW = 9

    FIG_HSIZE_3_ROW = 17
    FIG_VSIZE_3_ROW = 10

    FIG_HSIZE_1_TREE = 8
    FIG_VSIZE_1_TREE = 9.2

    FIG_HSIZE_2_TREE = 15
    FIG_VSIZE_2_TREE = 9.2

    FIG_HSIZE_3_TREE = 17
    FIG_VSIZE_3_TREE = 6.4

    FIG_HSIZE_CHANGE_SS_COLUMN_PLOT = 12  # For single series plot.

    FIG_HSIZE_CHANGE_COLUMN_PLOT = 17
    FIG_VSIZE_CHANGE_COLUMN_PLOT = 7
    FIG_VSIZE_CHANGE_COLUMN_2_PLOT = 10

    FIG_VSIZE_2x5 = 8

    MAJOR_EMITTER_FIG_HSIZE_1_ROW = 13.5

    LINE_WIDTH_SUBPLOT = 2.2
    LINE_WIDTH_0_SUBPLOT = 2.2
    LINE_WIDTH_10_SUBPLOT = 2.2
    LINE_MARKER_SIZE = 5
    LINE_WIDTH_PLOT_1x1 = 4
    MAJOR_EMITTER_LINE_WIDTH_PLOT = 7
    LINE_PLOT_WIDTH = 5
    MAJOR_EMITTER_LINE_MARKER_SIZE = 8

    COLUMN_11_SUBPLOT_TITLE_YPOS = 0.95


# Define colors for charts.
# Color library: https://matplotlib.org/stable/gallery/color/named_colors.html
class Color(Enum):
    CO2_CONC = 'cornflowerblue'
    CO2_EMISSION = 'slategrey'
    FOSSIL_FUELS = 'grey'
    CEMENT = 'cadetblue'
    LUC = 'olivedrab'

    COAL = 'black'
    OIL = 'brown'
    GAS = 'darkorange'
    FLARING = 'hotpink'
    NUCLEAR = 'darkviolet'
    HYDRO = 'dodgerblue'
    WIND = 'blue'
    SOLAR = 'crimson'
    BIOFUELS_AND_WASTE = 'saddlebrown'
    OTHER = 'peru'
    HEAT = 'rebeccapurple'
    RENEWABLES = 'green'
    WIND_AND_SOLAR = 'limegreen'
    ELECTRICITY = 'teal'
    UNPUBLISHED = 'steelblue'

    SECTOR_ELEC = 'firebrick'
    SECTOR_OTHER_ENERGY = 'coral'
    SECTOR_INDUSTRY = 'darkmagenta'
    SECTOR_TRANSPORT = 'cadetblue'
    SECTOR_COM_PUBLIC_SERV = 'midnightblue'
    SECTOR_RESD = 'mediumslateblue'
    SECTOR_AG = 'green'
    SECTOR_OTHER = 'purple'

    ALL = 'mediumpurple'
    CHINA = 'crimson'
    OTHER_COUNTRIES = 'darkslategrey'
    US = 'blue'
    INDIA = 'darkorange'
    RUSSIA = 'darkgreen'
    JAPAN = 'darkgoldenrod'
    INDONESIA = 'indianred'
    IRAN = 'sienna'
    SAUDI_ARABIA = 'darkred'
    SOUTH_KOREA = 'deeppink'
    GERMANY = 'green'
    CANADA = 'dodgerblue'
    MEXICO = 'chocolate'
    BRAZIL = 'forestgreen'
    TURKIYE = 'red'
    SOUTH_AFRICA = 'indigo'
    AUS = 'black'
    PER_CAPITA_HIGHLIGHT = 'magenta'

# All prebuilt chart styles: https://python-charts.com/matplotlib/styles/#list
# Python chart gallery: https://python-graph-gallery.com/
# Matplotlib universal settings:
# https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rcParams


rc = {
    'xtick.direction': 'out',
    'xtick.color': 'grey',
    'xtick.labelcolor': 'black',
    'ytick.direction': 'out',
    'ytick.color': 'grey',
    'ytick.labelcolor': 'black',
}
plt.style.use(('bmh', rc))

# Set global font parameters.
# If you add a font to the OS, be sure to delete all matplotlib's font cache files in ~/.matplotlib.
plt.rcParams['font.sans-serif'] = 'Helvetica'