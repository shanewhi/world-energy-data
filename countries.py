#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:25:39 2024

@author: shanewhite
"""

###############################################################################
#
# Function: iea_country_name()
#
# Description:
# Converts country name to version compliant with IEA JSON dataset.
#
# Input(s): Country name, string.
# Output(s): Country name, string.
#
###############################################################################
def iea_country_name(country_in):
    country = "'" + country_in.upper() + "'"
    if country == "'AUSTRALIA'":
        return("'AUSTRALI'")
    if country == "'UNITED ARAB EMIRATES'":
        return("'UAE'")
    if country == "'UNITED KINGDOM'":
        return("'UK'")
    else:
        return(country)
