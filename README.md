<h2>world-energy-data</h2>

<h3>Purpose</h3>
<p>
Generates charts of annual CO<sub>2</sub> emissions, fossil fuel production, 
energy consumption, and electricity generation of the world and specified 
countries.<br>Output is displayed at <code>https://www.worldenergydata.org/</code></p>

<h3>Description</h3>
<p>
This package consists of the following files -</p>
<ul>
   <li>world_energy_data.py (main executable)</li>
   <li>user_globals.py (global definitions)</li>
   <li>collate.py (extracts and arranges country specific data from input dataset)</li>
   <li>process.py (calculations)</li>
   <li>output.py (chart calls)</li>
   <li>chart.py (chart functions)</li>
   <li>countries.py (country name translations between datasets)</li>
</ul>

<h3>Software Installation Requirements</h3>
<p>
Requires installation of Python v3.12.7, and library versions listed below, which can 
be done using the terminal commands shown alongside -</p>
<ul>
    <li><a href="https://www.python.org/downloads/">Python v3.12.7</a></li>
    <li>Matplotlib v3.10.3 <code>pip3.12 install matplotlib==3.10.3</code></li>
    <li>Matplotlib-extra v0.1.0 <code>pip3.12 install git+https://github.com/chenyulue/matplotlib-extra/</code></li>
    <li>Numpy v2.3.1 <code>pip3.12 install numpy==2.3.1</code></li>
    <li>Openpyxl v3.1.5 <code>pip3.12 install openpyxl==3.1.5</code></li>
    <li>Pandas v2.3.0 <code>pip3.12 install pandas==2.3.0</code></li>
</ul>

<h3>Input Data Requirements</h3>
<p>
The following datasets are required, and are included in this package -</p>
<ol>
    <li><a href="https://www.icos-cp.eu/impact/science/global-carbon-budget/2025">Global Carbon Budget 2025 v1.0 in XLSX format</a>. 
    Modify this to include the cement carbonation sink and projected values for 2025, as follows -</li>
    <ol>
        <li>In sheet titled <code>'Global Carbon Budget'</code>, create a new column named <code>'fossil emissions including cement carbonation’</code> and fill with the values of<br>
            <code>'fossil emissions excluding cement carbonation'</code> minus <code>'cement carbonation sink'</code><br>
            Add the row <code>2025</code> and fill the same column with the projected value from <a href="https://globalcarbonbudget.org/"> Table 1 of Key Messages from GCB 2025</a>.</li>
        <li>In sheet titled <code>'Fossil Emissions by Category'</code>, add the row <code>2025</code> and fill with the projected values for coal, oil and gas from the same document above.</li>
    </ol>
    <li><code>Globally averaged marine surface annual mean data</code> and <code>Globally averaged marine surface annual mean growth rates</code> in CSV format from <a href="https://gml.noaa.gov/ccgg/trends/gl_data.html">NOAA Global Monitoring Laboratory</a>.</li>
    <li>The <a href="https://www.energyinst.org/statistical-review/resources-and-data-downloads">2026 Energy Institute Statistical Review of World Energy</a> in consolidated narrow CSV format.<br>
    <li><a href="https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser">IEA CO<sub>2</sub> Emissions by Sector and Total Final Consumption by Source</a> for the world and each selected country.
    Data is obtained by -
    <ol>
        <li>Select Country</li>
        <li>Select Energy Consumption</li>
        <li> Select Total final consumption (TFC) by source</li>
        <li>Select Download chart data</li>
        <li>Select Energy transition indicators</li>
        <li>Select CO<sub>2</sub> emissions by sector</li>
        <li>Select Download chart data</li>
    </ol></li>
    <li><a href="https://robbieandrew.github.io/GCB2024/CSV/s64_2024_LinearPathways.csv">Linear emission reduction pathways</a>.
    This is the datafile from slide 64 of <a href="https://robbieandrew.github.io/GCB2024/">Figures from the Global Carbon Budget 2024</a>.</li>
    <li><a href="https://data.worldbank.org/indicator/SP.POP.TOTL">World Bank Group Total Population dataset in CSV format</a>.<br>
    Unzip the downloaded archive and rename the CSV file <code>'world_pop.csv'</code>.</li>
</ol>

<h3>Instructions</h3>
<ol>
   <li>Choose a country to profile from those listed in the Energy Institute's Statistical Review. This package does attempt to check that a<br>
compatible country name has been input, but it's coarse and some may break at run-time (e.g. Yemen, which the Energy Institute<br>
dataset includes, but only for oil production). This may be improved later.</li>
   <li>Edit line 38 of world_energy_data.py (shown below), to include the country name, followed by a comma in the case of a single country<br>
(a single element tuple must be followed by a comma) -<br>
<code># Define countries to profile using tuple.<br>countries = ('Total World',)</code>
   <li>For data not already included in this repository, obtain and move the IEA datafiles from (4) in Input Data Requirements above, to the<br>
same folder as this package. If needed, add the IEA's country name to -<br>
<code>countries.translate_country_name()</code> in <code>countries.py</code>.</li>
   <li>Folders will be created named <code>charts CO2</code>, <code>charts country_name</code> and <code>charts Major Emitters</code></li>
   <li>Flags in <code>user_globals.py</code> can be edited to suit preferences.</li>
</ol>
