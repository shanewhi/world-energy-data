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
