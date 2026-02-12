#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Fri Apr 26 14:25:39 2024

@author: shanewhite
"""

########################################################################################################################
#
# Module: countries.py
#
# Description:
# Functions that perform country name lookups and modifications.
#
########################################################################################################################
# Import user modules.
import user_globals

########################################################################################################################
#
# Function: translate_country_name()
#
# Description:
# Translates country name used by Energy Institute to that used by the IEA.
#
########################################################################################################################
def translate_country_name(ei_name):
    if ei_name == 'Total World':
        iea_name = 'World'
    elif ei_name == 'China':
        iea_name = "People's Republic of China"
    elif ei_name == 'US':
        iea_name = 'United States'
    elif ei_name == 'Iran':
        iea_name = 'Islamic Republic of Iran'
    elif ei_name == 'South Korea':
        iea_name = 'Korea'
    elif ei_name == 'Turkiye':
        iea_name = 'Republic of Turkiye'
    else:
        iea_name = ei_name
    return iea_name
########################################################################################################################
#
# Function: ffprod_shorten_country()
#
# Description:
# Shortens country name for chart.treemap() functions.
#
########################################################################################################################
def ffprod_shorten_country(df1, df2, df3):
    df1.replace('Russian Federation', 'Russia', inplace=True)
    df2.replace('Russian Federation', 'Russia', inplace=True)
    df3.replace('Russian Federation', 'Russia', inplace=True)
    df1.replace('United Arab Emirates', 'UAE', inplace=True)
    df2.replace('United Arab Emirates', 'UAE', inplace=True)
    df3.replace('United Arab Emirates', 'UAE', inplace=True)
    return df1, df2, df3

########################################################################################################################
#
# Function: restore_original_country_name()
#
# Description:
# Replaces original country name for those shortened by ffprod_shorten_country()
#
########################################################################################################################
def restore_original_country_name(names):
    names.replace('Russia', 'Russian Federation', inplace=True)
    names.replace('UAE', 'United Arab Emirates', inplace=True)
    return names

########################################################################################################################
#
# Function: assign_chart_colors()
#
# Description:
# Assigns colors to country names
#
########################################################################################################################
def assign_chart_colors(input_series):
    output_colors = []
    for index, country in input_series.items():
        match country:
            case 'China':
                output_colors.append(user_globals.Color.CHINA.value)
            case 'US':
                output_colors.append(user_globals.Color.US.value)
            case 'India':
                output_colors.append(user_globals.Color.INDIA.value)
            case 'Russia':
                output_colors.append(user_globals.Color.RUSSIA.value)
            case 'Japan':
                output_colors.append(user_globals.Color.JAPAN.value)
            case 'Indonesia':
                output_colors.append(user_globals.Color.INDONESIA.value)
            case 'Iran':
                output_colors.append(user_globals.Color.IRAN.value)
            case 'Saudi Arabia':
                output_colors.append(user_globals.Color.SAUDI_ARABIA.value)
            case 'South Korea':
                output_colors.append(user_globals.Color.SOUTH_AFRICA.value)
            case 'Germany':
                output_colors.append(user_globals.Color.GERMANY.value)
            case 'Canada':
                output_colors.append(user_globals.Color.CANADA.value)
            case 'Mexico':
                output_colors.append(user_globals.Color.MEXICO.value)
            case 'Brazil':
                output_colors.append(user_globals.Color.BRAZIL.value)
            case 'Turkiye':
                output_colors.append(user_globals.Color.TURKIYE.value)
            case 'South Africa':
                output_colors.append(user_globals.Color.SOUTH_AFRICA.value)
            case 'Australia':
                output_colors.append(user_globals.Color.AUS.value)
            case 'Kuwait':
                output_colors.append(user_globals.Color.KUWAIT.value)
            case 'Iraq':
                output_colors.append(user_globals.Color.IRAQ.value)
            case 'UAE':
                output_colors.append(user_globals.Color.UAE.value)
            case 'Norway':
                output_colors.append(user_globals.Color.NORWAY.value)
            case 'Algeria':
                output_colors.append(user_globals.Color.ALGERIA.value)
            case 'Qatar':
                output_colors.append(user_globals.Color.QATAR.value)
            case 'Other':
                output_colors.append(user_globals.Color.OTHER_COUNTRIES.value)
            case _:
                output_colors.append(user_globals.Color.COUNTRY_WITHOUT_ASSIGNED_COLOR.value)
    return output_colors
