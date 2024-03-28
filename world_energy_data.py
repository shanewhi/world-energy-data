#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite

#Creates charts of national energy systems.
#Written by Shane White using Python v3.11.5 and Spyder IDE.
#https://github.com/shanewhi
#https://www.worldenergydata.org

#Required input:
#https://www.energyinst.org/__data/assets/file/0003/1055694/ ...
#Consolidated-Dataset-Narrow-format.csv

#Choose a country at bottom of script. If that country has never produced a
#specific fuel, then a corresponding chart isn't created. Entered country
#name must match that used by The Energry Institute's dataset.

#import Python modules
import pandas as pd

#import user modules
import collate
import process

#profile a country's energy system by creating an instance of user class
#Energy_System, populate that object with data, and draw charts
def profile(country):
    country_energy_system = collate.populate_energy_system(ei_data, country)
    process.production(country_energy_system)
    process.primary_energy(country_energy_system)

#main function
ei_data = pd.read_csv(
    "Statistical Review of World Energy Narrow File.csv",
	index_col = ['Country'],
    usecols = ['Country', 'Year', 'Var', 'Value'])
#profile following countries:
#profile('Mexico')
#profile('Germany')
profile('United Arab Emirates')
#profile('United Kingdom')
#profile('Total World')
