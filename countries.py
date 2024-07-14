#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:25:39 2024

@author: shanewhite
"""

########################################################################################
#
# Module: countries.py
#
# Description:
# Functions that peform country name lookups and modifications.
#
########################################################################################


########################################################################################
#
# Function: iea_country_name()
#
# Description:
# Converts country name to version compliant with IEA JSON dataset.
#
########################################################################################
def iea_country_name(country_in):
    country = "'" + country_in.upper() + "'"
    if country == "'AUSTRALIA'":
        return "'AUSTRALI'"
    if country == "'UNITED ARAB EMIRATES'":
        return "'UAE'"
    if country == "'UNITED KINGDOM'":
        return "'UK'"
    if country == "'US'":
        return "'USA'"
    if country == "'RUSSIAN FEDERATION'":
        return "'RUSSIA'"
    if country == "'SAUDI ARABIA'":
        return "'SAUDIARABI'"
    if country == "'UNITED ARAB EMIRATES'":
        return "'UAE'"
    else:
        return country


########################################################################################
#
# Function: ffprod_shorten_country()
#
# Description:
# Shortens country name for chart.treemap().
#
########################################################################################
def ffprod_shorten_country(df1, df2, df3):

    df1.replace("Russian Federation", "Russia", inplace=True)
    df2.replace("Russian Federation", "Russia", inplace=True)
    df3.replace("Russian Federation", "Russia", inplace=True)
    df1.replace("United Arab Emirates", "UAE", inplace=True)
    df2.replace("United Arab Emirates", "UAE", inplace=True)
    df3.replace("United Arab Emirates", "UAE", inplace=True)
    return (df1, df2, df3)
