import pandas as pd
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn
import seaborn.objects as so


# conversions
class ConstantsNamespace:
    __slots__ = ()
    THOUSAND_TO_MILLION = 1 / 1000
    COLOR_COAL = '#000000'
    COLOR_OIL = '#A62B17'
    COLOR_GAS = '#F09937'
    COLOR_NUCLEAR = '#F900FF'
    COLOR_HYDRO = '#479FF8'
    COLOR_WIND = '#1432F5'
    COLOR_SOLAR = '#DA3B26'
    COLOR_GEO_BIO_OTHER = '#92902C'
    COLOR_OTHER = '#9F6622'
    COLOR_FOSSIL_FUELS = '#5E5E5E'
    COLOR_LOW_C = '#53AE32'
    COLOR_WIND_SOLAR = '#72F54A'
    COLOR_ELECTRICITY = '#3F8F91'
    FIG_SIZE = 8
    OIL_PROD_INTERVAL = 20.0


def import_energy_inst_data():
    return(pd.read_csv("Statistical Review of World Energy Narrow File.csv", index_col=['Country'],
                       usecols=['Country', 'Year', 'Var', 'Value']))


def fossil_fuel_production(data):
    oil_production = data.loc[data['Var'] == 'oilprod_kbd']
    oilprod_Mbpd = oil_production.copy()
    oilprod_Mbpd['Value'] = oilprod_Mbpd['Value'] * constant.THOUSAND_TO_MILLION

    # Matplotlib plot:
    fig = plt.figure(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
    ax1 = fig.add_subplot()
    ax1.bar(oilprod_Mbpd['Year'], oilprod_Mbpd['Value'], width=1, color=constant.COLOR_OIL,
                             edgecolor='black', linewidth=0.7)
    ax1.minorticks_off()
    ax1.tick_params('x', labelrotation = 90)
    ax1.set_xticks(np.arange(min(oilprod_Mbpd['Year'])+1, max(oilprod_Mbpd['Year'])+1, 2.0))
    ax1.set_yticks(np.arange(0, max(oilprod_Mbpd['Value'])+constant.OIL_PROD_INTERVAL, constant.OIL_PROD_INTERVAL))
    ax1.set_title('Oil Production')
    ax1.set_ylabel('Oil Production (million barrels/day)')

    # Pandas plot:
    oilprod_Mbpd.plot(
        kind='bar',
        x='Year',
        y='Value',
        color=constant.COLOR_OIL,
        title='pandas',
        edgecolor='black',
        width=1,
        figsize=(constant.FIG_SIZE, constant.FIG_SIZE))

    # Seaborn plot:
    fig, ax = plt.subplots(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
    seaborn.barplot(
        data=oilprod_Mbpd,
        x='Year',
        y='Value',
        saturation = 1,
        color=constant.COLOR_OIL,
        edgecolor='black',
        width=1)
    ax.set_title('seaborn')
    ax.set_ylabel('Annual Production (million barrels per day (Mpbd)')
    #plt.setp(ax.axes.get_xticklabels(), visible=False)
    #plt.setp(ax.axes.get_xticklabels()[::5], visible=True)
    plt.show()
 

def profile(country):
    ei_country_data = ei_data.loc[country]
    fossil_fuel_production(ei_country_data)


# world
# Use non-default matlabplot backend for testing due to macOS Sonoma bug; this causes charts to look pixelated.
# Enable default version for high res charts but causes program to hang when displaying charts.
# matplotlib.use('Tkagg')
constant = ConstantsNamespace()
ei_data = import_energy_inst_data()
country = 'Total World'
profile(country)

# ei_country_data = import_energy_inst_data('Russian Federation')
# profile(ei_country_data)


























# trash
# oilprod_chart1 = plt.bar(oilprod_Mbpd['Year'], oilprod_Mbpd['Value'], width = 1, color = constant.COLOR_OIL, edgecolor = 'black', linewidth = 0.7)
# oilprod_chart2 = oilprod_Mbpd.plot.bar(x = 'Year', y = 'Value', color = {constant.COLOR_OIL}, edgecolor = 'black', linewidth = 1)
# for x in oilprod_Mbpd['Var']:
#    oilprod_Mbpd['Var'] = 'oilprod_Mbpd'
# print(oil_production)
# print(oilprod_Mbpd)
# oilprod_chart = oilprod_Mbpd.plot.bar(x = 'Year', y = 'Value', color = {constant.COLOR_OIL}, edgecolor = 'black', linewidth = 1)
#
# oilprod_chart = plt.bar(oilprod_Mbpd['Year'], oilprod_Mbpd['Value'], width = 1, color = constant.COLOR_OIL, edgecolor = 'black', linewidth = 0.7)
# for label in oilprod_chart.set_xticklabels.get_ticklabels()[::2]:
#    label.set_visible(False)
# for x in oilprod_Mbpd['Year']:
#    if x % 2 != 0:
#        year =
# plt.xticks(oilprod_Mbpd['Year'], oilprod_Mbpd['Year'], rotation = 'vertical')
# plt.xticks(year, year, rotation = 'vertical')
# print(year)
#    ticks=list(range(int(len(oilprod_Mbpd['Year'].tolist())/2)))

