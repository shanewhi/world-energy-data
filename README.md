Python script that generates the following charts -

Global charts:
1. Annual atmospheric CO₂ concentration and change
2. CO₂ emission sources by share
3. Annual CO₂ emissions from fossil fuels and cement
4. Annual change of CO₂ emissions from fossil fuels and cement
5. Annual coal, oil and gas CO₂ emissions

Global or national charts (for the country or countries specified):
1. Annual CO₂ emissions from fossil fuels and national shares of CO₂ emissions
2. Change of annual CO₂ emissions from fossil fuels
3. Global annual production of coal, oil and gas by country
4. Annual national production of coal, oil and gas 
5. Shares of fuels in energy supply for latest year (primary energy)
6. Annual shares of fuels in energy supply
7. Annual quantity of coal, oil and gas in energy supply
8. Annual change of quantity of fossil fuels in energy supply
9. Annual change of quantity of coal, oil and gas in energy supply
10. Shares of fuels in final energy and electricity generation for latest year
11. Annual shares of fuels in final energy
12. Annual quantity of fuels in final energy
13. Annual change of quantity of fuels in final energy
14. Annual shares of categories in electricity generation
15. Annual shares of fuels in electricity generation
16. Annual quantity of categories in electricity generation
17. Annual quantity of fuels in electricity generation
18. Annual change of categories in electricity generation
19. Annual change of fuels in electricity generation
20. Recent annual change of fuels in electricity generation

   
Written by Shane White using Python v3.12.2 for the site https://www.worldenergydata.org

Consists of the following files:
1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (calculations)
5. output.py (chart calls)
6. chart.py (generic chart functions)
7. countries.py (country name translations to make them compatible with IEA dataset)

Required input (all are provided in this repository):
1. Global Carbon Budget in .xlsx format from https://globalcarbonbudgetdata.org/latest-data.html
2. NOAA ESRL CO2 data in CSV format from https://gml.noaa.gov/ccgg/trends/gl_data.html
3. Energy Institute Statistical Review of World Energy data from
   https://www.energyinst.org/statistical-review/resources-and-data-downloads
(Direct link is https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv)
4. IEA annual energy balances in JSON format. Instructions to obtain this are lengthy and listed in the comments of
   world_energy_data.py, within this repository.

Instructions for use (code below is within single quotes):
1. Choose a country to profile from those listed in the Energy Institute's data listed above.
2. Edit the existing profile commands in world_energy_data.py to include 'profile("Country_Name")', where Country_Name is an exact
   duplicate of the name of the country selected in (1).
3. Browse one of the IEA JSON files listed in (4) above to identify the IEA's equivalent country name.
4. If the IEA version of Country_Name differs, edit countries.iea_country_name() to translate Country_Name to the IEA equivalent.
5. Save all and using a terminal, enter the command 'python3 world_energy_data.py'
6. Folders will be created named 'charts CO2' for global CO2 charts (generated on each execution), and
   'charts Country_Name' for national, or World, energy charts.

