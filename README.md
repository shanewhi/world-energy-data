Purpose:
-
Python script to create charts of the trends of global carbon dioxide
emissions, and energy systems of countries and the world. This will be
used to generate content at https://www.worldenergydata.org,
replacing the spreadsheet currently used.

Required Input:
-
1. https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv
(from https://www.energyinst.org/statistical-review/resources-and-data-downloads)
2. IEA annual energy balances in JSON format (included in the latest release of this code)
3. Global Carbon Budget in .xlsx format from https://globalcarbonbudgetdata.org/latest-data.html
   (included in the latest release of this code).



Consists of the following files:
-
1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (calculations)
5. output.py (chart calls)
6. chart.py (generic chart functions)
7. countries.py (country name translations to make them compatible with IEA dataset)

Notes:
-
1. To reduce execution time, in user_globals.py reduce the difference between TFC_START_YEAR and TFC_END_YEAR

