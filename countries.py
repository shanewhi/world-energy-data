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
    else:
        return country
