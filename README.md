Purpose:
-
Python script to create charts of the trends of fuels in energy systems
of countries and the world. This will be used to generate content at 
https://www.worldenergydata.org, and replace the spreadsheet currently
used.

Required Input:
-
https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv
(from https://www.energyinst.org/statistical-review/resources-and-data-downloads)


Consists of the following files:
-
1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (data processing)
5. chart.py (generic chart functions)

Output (as of March 21, 2024):
-
Country (or World) specific charts of fossil fuel production and primary
energy.
