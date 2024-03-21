#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:19:37 2024

@author: shanewhite
"""

from enum import Enum


# Define conversions (multiply for conversion).
class Constant(Enum):
    THOUSAND_TO_MILLION = 1 / 1000
    FIG_SIZE = 8


# Define fuel colors for charts.
class Color(Enum):
     COAL = 'black'
     OIL = 'firebrick'
     GAS = 'orange'
     NUCLEAR = 'violet'
     HYDRO = 'dodgerblue'
     WIND = 'blue'
     SOLAR = 'red'
     GEO_BIO_OTHER = 'sienna'
     OTHER = 'tan'
     FOSSIL_FUELS = 'grey'
     LOW_C = 'forestgreen'
     WIND_SOLAR = 'lime'
     ELECTRICITY = 'teal'


# Custom class of country specific energy system.
class Energy_System:
    def __init__(
            self,
            name, #country name
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm,
            coal_primary_EJ,
            oil_primary_EJ,
            gas_primary_EJ,
            nuclear_primary_EJ,
            hydro_primary_EJ,
            wind_primary_EJ,
            solar_primary_EJ,
            geo_bio_other_primary_EJ,
            primary_EJ):
        self.name = name
        self.coalprod_Mt = coalprod_Mt
        self.oilprod_Mbpd = oilprod_Mbpd
        self.gasprod_bcm = gasprod_bcm
        self.coal_primary_EJ = coal_primary_EJ
        self.oil_primary_EJ = oil_primary_EJ
        self.gas_primary_EJ = gas_primary_EJ
        self.nuclear_primary_EJ = nuclear_primary_EJ
        self.hydro_primary_EJ = hydro_primary_EJ
        self.wind_primary_EJ = wind_primary_EJ
        self.solar_primary_EJ = solar_primary_EJ
        self.geo_bio_other_primary_EJ = geo_bio_other_primary_EJ
        self.primary_EJ = primary_EJ
