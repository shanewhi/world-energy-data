Generates charts of CO<sub>2</sub> emissions, fossil fuel production, energy consumption, and electricity trends for the world and specified countires. Charts are displayed at https://www.worldenergydata.org/.

Requires installation of Python and dependancies listed below. Charts are output in SVG format so there's no loss of resolution when magnified.

Python files -
1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (calculations)
5. output.py (chart calls)
6. chart.py (chart functions)
7. countries.py (country name translations to make them compatible with IEA dataset)

Dependencies -
1. Install the latest Python from https://www.python.org/downloads/, scroll down to "Information about specific ports, 
and developer info" and select suitable platform.
2. Install the following Python libraries by entering the following commands in a terminal: <br>
a) pip3 install openpyxl<br>
b) pip3 install git+https://github.com/chenyulue/matplotlib-extra/<br>
c) pip3 install mpl_extra<br>
d) pip3 install matplotlib<br>
e) pip3 install jmespath<br>
f) pip3 install pandas<br>
3. Install font 'SF Pro' from  https://developer.apple.com/fonts/. Delete matplotlib's font cache files to force
rebuilding of cache and inclusion of 'SF Pro' - in a terminal enter rm ~/.matplotlib/fontlist*
4. The following datasets are required, which are provided in this package and are listed below for reference only:<br>
a) Global Carbon Budget in .xlsx format. The version in this repository is required as 2024 GCP projected values have 
been included, obtained from https://essd.copernicus.org/preprints/essd-2024-519/essd-2024-519.pdf. Original GCB was
downloaded from https://globalcarbonbudgetdata.org/latest-data.html<br>
b) NOAA ESRL CO2 data in CSV format from https://gml.noaa.gov/ccgg/trends/gl_data.html<br>
c) Energy Institute Statistical Review of World Energy data from -<br>
https://www.energyinst.org/statistical-review/resources-and-data-downloads<br>
(Direct link is https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv)<br>
d) IEA annual energy balances in JSON format obtained from -<br>
   https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser<br>
5. https://robbieandrew.github.io/GCB2024/CSV/s64_2024_LinearPathways.csv (datafile from slide 64 at<br>
https://robbieandrew.github.io/GCB2024/

Instructions (code below is within single quotes) -
1. Choose a country to profile from those listed in the Energy Institute's data listed above.
2. Edit line 75 of world_energy_data.py (first line of code) to include the country name,
as an exact duplicate of the name selected in (1).
3. Browse one of the IEA JSON files listed in (4) above to identify the IEA's equivalent country name.
4. If the IEA version differs, edit countries.iea_country_name() to translate the country name to the 
IEA equivalent.
5. Save all, and in a terminal, enter the command 'python3 world_energy_data.py'
6. Folders will be created named 'charts CO2' for global CO2 charts (generated on each execution), and 
'charts country_name' for national, or World energy charts.
7. If need be, edit flags in user_globals.py to suit user preferences.

Written by Shane White, whitesha@protonmail.com, using Python v3.12.2
