#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite

###############################################################################
#
# Application world_energy_data.py
#
# Description:
# Creates charts of national energy systems.
# Written by Shane White using Python v3.11.5 and Spyder IDE.
# https://github.com/shanewhi/world-energy-data
# https://www.worldenergydata.org
#
# Files:
# world_energy_data.py (this file)
# user_globals.py (defs)
# collate.py (called by world_energy_data.py)
# process.py (called by world_energy_data.py)
# chart.py (called by process.py)
#
# Choose a country at bottom of script.
# Name must match that used by The Energry Institute's (EI) dataset and or
# IEA's.
#
# Input(s):
# 1. Country name, string.
# 2. EI's dataset. Download from -
# https://www.energyinst.org/statistical-review/resources-and-data-downloads
# 3. IEA's annual energy balances. To download an annual IEA World Energy
# Balance -
# Load https://www.iea.org/data-and-statistics/data-tools/ \
#      energy-statistics-data-browser?country=WORLD&fuel= \
#      Energy%20supply&indicator=TESbySource
# 2. Right click on chart -> Inspect
# 3. Select Network tab
# 5. Click XHR button
# 6. Select Browse as Tables
# 7. Select year from dropdown (ensure this is done manually)
# 8. Reload page
# 9. Double click on the following result (using 2021 as an example)
# https://api.iea.org/stats?year=2021&countries=[object+Object]&series=BALANCES
# 10. Save as JSON format with name 'iea<yr>.json', where <yr> is relevant
# year.
# 11. Add to start of file: {"balances":
# 12. Add to the end of the file: }
#
# Output(s): Charts.
#
###############################################################################


# Import Python modules.
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# Import user modules.
import user_globals
import collate


# Import Energy Institute's dataset, once only.
user_globals.ei_data_import = pd.read_csv(
    "Statistical Review of World Energy Narrow File.csv",
	index_col = ["Year"],
    usecols = ["Country", "Year", "Var", "Value"])
# IEA's dataset is imported in collate.populate_energy_system(). This is
# because it's imported as annual Energy Balances stored in separate JSON
# files, because their Highlights dataset omits some countries.

# Set plot globals
plt.style.use(user_globals.Constant.CHART_STYLE.value)
plt.rcParams["font.family"] = user_globals.Constant.CHART_FONT.value
plt.rcParams["font.weight"] = "regular"
mpl.rcParams['figure.dpi']= user_globals.Constant.CHART_DPI.value

# Profile following countries or "Total World".
#collate.profile("Mexico")
#collate.profile("Germany")
#collate.profile("United Arab Emirates")
collate.profile("United Kingdom")
#collate.profile("Sweden")
#collate.profile("Australia")
#collate.profile("Total World")
#collate.profile("Algeria")
#collate.profile("Vietnam")
