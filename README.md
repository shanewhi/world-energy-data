Python script that generates the following charts -

Global charts:
1. Annual atmospheric CO₂ concentration and change
2. CO₂ emission sources by share
3. Annual CO₂ emissions from fossil fuels and cement
4. Annual change of CO₂ emissions from fossil fuels and cement
5. Annual coal, oil and gas CO₂ emissions

Global or national charts (for user-specified countries):
1. Annual Fossil Fuel (FF) CO₂ emissions and national shares of FF CO₂ emissions
2. Change of annual FF CO₂ emissions
3. Annual coal, oil and gas production
4. Country shares of coal, oil and gas production
5. Shares of Energy consumption prior to partial conversions to Electricity (Primary Energy) for most recent year
6. Annual Energy Consumption by share prior to partial conversions to Electricity (Primary Energy)
7. Annual FF consumption prior to partial conversions to Electricity (Primary Energy)
8. Annual change of FF consumption prior to partial conversions to Electricity (Primary Energy)
9. Shares of Energy Consumption after partial conversions to Electricity (Final Energy), & Electricity Generation for the most recent year.
10. Annual Energy Consumption by share after partial conversions to Electricity (Final Energy)
Annual Energy Consumption by share prior to partial conversions to Electricity (Primary Energy)
11. Annual Energy Consumption after partial conversions to Electricity (Final Energy)
12. Annual change of Energy Consumption after partial conversions to Electricity (Final Energy)
13. Annual Electricity Generation by share
14. Annual Electricity Generation
15. Annual change of Electricity Generation
   
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
4. IEA annual energy balances in JSON format.

Instructions for use (code below is within single quotes):
1. Choose a country to profile from those listed in the Energy Institute's data listed above.
2. Edit the existing profile commands in world_energy_data.py to include 'profile("Country_Name")', where Country_Name is an exact duplicate of the name of the country selected in (1).
3. Browse one of the IEA JSON files listed in (4) above to identify the IEA's equivalent country name.
4. If the IEA version of Country_Name differs, edit countries.iea_country_name() to translate Country_Name to the IEA equivalent.
5. Save all and using a terminal, enter the command 'python3 world_energy_data.py'
6. Folders will be created named 'charts CO2' for global CO2 charts (generated on each execution), and 'charts Country_Name' for national, or World, energy charts.
7. If need be, edit flags in user_globals.py to suit user preferences.

Written by Shane White, whitesha@protonmail.com, using Python v3.12.2
