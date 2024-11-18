Python script for generation of charts displaying CO2 emissions, and trends and statistics of energy systems.
Charts are displayed at -
1. https://www.worldenergydata.org/world-energy-trends/
2. https://www.worldenergydata.org/national-energy-trends/, and
3. https://www.worldenergydata.org/greenhouse-gas-emissions/

Requires installation of Python. Charts are output in SVG format.

This package consists of -
1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (calculations)
5. output.py (chart calls)
6. chart.py (chart functions)
7. countries.py (country name translations to make them compatible with IEA dataset)

Prerequisites  (all are provided in this repository) -
1. Global Carbon Budget in .xlsx format. The version in this repository is required as 2024 GCP projected values have 
been included, obtained from https://essd.copernicus.org/preprints/essd-2024-519/essd-2024-519.pdf. Original GCB was
downloaded from https://globalcarbonbudgetdata.org/latest-data.html.
2. NOAA ESRL CO2 data in CSV format from https://gml.noaa.gov/ccgg/trends/gl_data.html
3. Energy Institute Statistical Review of World Energy data from
   https://www.energyinst.org/statistical-review/resources-and-data-downloads
(Direct link is https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv)
4. IEA annual energy balances in JSON format.

Instructions (code below is within single quotes) -
1. Choose a country to profile from those listed in the Energy Institute's data listed above.
2. Edit the existing profile commands in world_energy_data.py to include 'profile("Country_Name")', 
where Country_Name is an exact duplicate of the name of the country selected in (1).
3. Browse one of the IEA JSON files listed in (4) above to identify the IEA's equivalent country name.
4. If the IEA version of Country_Name differs, edit countries.iea_country_name() to translate Country_Name to the 
IEA equivalent.
5. Save all, and in a terminal, enter the command 'python3 world_energy_data.py'
6. Folders will be created named 'charts CO2' for global CO2 charts (generated on each execution), and 
'charts Country_Name' for national, or World, energy charts.
7. If need be, edit flags in user_globals.py to suit user preferences.

Written by Shane White, whitesha@protonmail.com, using Python v3.12.2
