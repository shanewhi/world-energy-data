Generates charts of CO<sub>2</sub> emissions, fossil fuel production, energy consumption, and electricity trends for
the world and specified countries. Example charts are displayed at https://www.worldenergydata.org/.

Requires installation of Python and dependencies listed below. Charts are output in SVG format so there's no loss of
resolution when magnified.

Python files -

1. world_energy_data.py (main executable)
2. user_globals.py (global definitions)
3. collate.py (extracts and arranges country specific data from input dataset)
4. process.py (calculations)
5. output.py (chart calls)
6. chart.py (chart functions)

Dependencies -

1. Install a Python3 version from https://www.python.org/downloads/, scroll down to "Information about specific ports,
   and developer info" and select suitable platform.
2. Install the following Python libraries by entering the following commands in a terminal: <br>
   a) pip3 install openpyxl<br>
   b) pip3 install git+https://github.com/chenyulue/matplotlib-extra/<br>
   c) pip3 install matplotlib<br>
   d) pip3 install pandas<br>
3. Install font 'Inter'. Delete matplotlib's font cache files to force rebuilding of cache -
   in a terminal enter rm ~/.matplotlib/fontlist*
4. The following datasets are required, which are provided in this package and are listed below for reference only:<br>
   a) Global Carbon Budget in .xlsx format. The version in this repository is required as 2024 GCP projected values have
   been included, obtained from https://essd.copernicus.org/preprints/essd-2024-519/essd-2024-519.pdf. Original GCB was
   downloaded from https://globalcarbonbudgetdata.org/latest-data.html<br>
   b) NOAA ESRL CO2 data in CSV format from https://gml.noaa.gov/ccgg/trends/gl_data.html<br>
   c) Energy Institute Statistical Review of World Energy data from -<br>
   https://www.energyinst.org/statistical-review/resources-and-data-downloads<br>
   (Direct link
   is https://www.energyinst.org/__data/assets/file/0003/1055694/Consolidated-Dataset-Narrow-format.csv)<br>
   d) IEA CO2 Emissions by Sector and Total Final Consumption by source for each relevant country, in CSV format
   from <br>
   https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser
   i. Select Country
   ii. Select Energy Consumption
   iii. Select Total final consumption (TFC) by source
   iv. Select Download chart data
   v. Select Energy transition indicators
   vi. Select CO₂ emissions by sector
   vii. Select Download chart data
5. https://robbieandrew.github.io/GCB2024/CSV/s64_2024_LinearPathways.csv (datafile from slide 64 at<br>
   https://robbieandrew.github.io/GCB2024/

Instructions (code below is within single quotes) -

1. Choose a country to profile from those listed in the Energy Institute's data listed above.
2. Edit line 38 of world_energy_data.py to include the country name,
   as an exact duplicate of the name selected in (1), and followed by a comma in the case of a single country <br>
   (single element tuple must be followed by a comma).
3. Obtain and move the IEA datafiles from 4(d) above to the same folder as this Python code.
4. Folders will be created named 'charts CO2' for global CO2 charts (generated on each execution), and
   'charts country_name' for national, or World energy charts.
5. If need be, edit flags in user_globals.py to suit user preferences.

Written by Shane White, whitesha@protonmail.com, using Python v3.12
