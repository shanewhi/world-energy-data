import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#define immutable conversions
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
    OIL_PROD_YAXIS_INTERVAL = 20
    COAL_PROD_YAXIS_INTERVAL = 1000
    GAS_PROD_YAXIS_INTERVAL = 1000


#import energy institute data from csv file
def import_energy_inst_data():
    return(pd.read_csv(
        "Statistical Review of World Energy Narrow File.csv",
        index_col=['Country'],
        usecols=['Country', 'Year', 'Var', 'Value']))


#fossil fuel production charts
def fossil_fuel_production(profile_country, data):

    #for chart titles
    if profile_country == 'Total World':
        profile_country = 'World'

    #locate production values
    coalprod_mt = data.loc[data['Var'] == 'coalprod_mt']
    oilprod_kbd = data.loc[data['Var'] == 'oilprod_kbd']
    gasprod_bcm = data.loc[data['Var'] == 'gasprod_bcm']

    #coal
    fig = plt.figure(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
    ax = fig.add_subplot()
    ax.bar(
        coalprod_mt['Year'],
        coalprod_mt['Value'],
        width=1,
        color=constant.COLOR_COAL,
        edgecolor='grey',
        linewidth=0.7)
    ax.tick_params('x', labelrotation = 90)
    if (float(min(coalprod_mt['Year']) % 2) != 0.0):
       ax.set_xticks(np.arange(
           min(coalprod_mt['Year'] + 1),
           max(coalprod_mt['Year'] + 1),
           2))
    else:
        ax.set_xticks(np.arange(
            min(coalprod_mt['Year']),
            max(coalprod_mt['Year'] + 2),
            2))
    ax.set_yticks(np.arange(
        0,
        max(coalprod_mt['Value']) + constant.COAL_PROD_YAXIS_INTERVAL,
        constant.COAL_PROD_YAXIS_INTERVAL))
    title = profile_country + ' Annual Coal Production'
    ax.set_title(title)
    ax.set_ylabel('Annual Production (million tonnes (Mt))')
    plt.savefig(title, dpi=300)

    #oil
    #create new empty dataframe to accomodate conversion kbpd -> Mpbd
    oilprod_Mbpd = pd.DataFrame(columns = ['Year', 'Var', 'Value'])
    oilprod_Mbpd['Year'] = oilprod_kbd['Year']
    oilprod_Mbpd['Var'] = 'oil_prodMpd'
    oilprod_Mbpd['Value'] = oilprod_kbd['Value'] * \
        constant.THOUSAND_TO_MILLION
    fig = plt.figure(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
    ax = fig.add_subplot()
    ax.bar(
        oilprod_Mbpd['Year'],
        oilprod_Mbpd['Value'],
        width=1,
        color=constant.COLOR_OIL,
        edgecolor='black',
        linewidth=0.7)
    ax.tick_params('x', labelrotation = 90)
    if (float(min(oilprod_Mbpd['Year']) % 2) != 0):
       ax.set_xticks(np.arange(
           min(oilprod_Mbpd['Year'] + 1),
           max(oilprod_Mbpd['Year'] + 1),
           2))
    else:
        ax.set_xticks(np.arange(
            min(oilprod_Mbpd['Year']),
            max(oilprod_Mbpd['Year'] + 2),
            2))
    ax.set_yticks(np.arange(
        0,
        max(oilprod_Mbpd['Value']) + constant.OIL_PROD_YAXIS_INTERVAL,
        constant.OIL_PROD_YAXIS_INTERVAL))
    title = profile_country + ' Annual Oil Production'
    ax.set_title(title)
    ax.set_ylabel('Annual Production (million barrels/day (Mbpd))')
    plt.savefig(title, dpi=300)
    #chart full width if preferred
    #ax1.set_xlim(min(oilprod_Mbpd['Year']) - 1, max(oilprod_Mbpd['Year']) + 1)

    #gas
    fig = plt.figure(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
    ax = fig.add_subplot()
    ax.bar(
        gasprod_bcm['Year'],
        gasprod_bcm['Value'],
        width=1,
        color=constant.COLOR_GAS,
        edgecolor='black',
        linewidth=0.7)
    ax.tick_params('x', labelrotation = 90)
    if (float(min(gasprod_bcm['Year'] % 2)) != 0):
       ax.set_xticks(np.arange(
           min(gasprod_bcm['Year'] + 1),
           max(gasprod_bcm['Year'] + 1),
           2))
    else:
        ax.set_xticks(np.arange(
            min(gasprod_bcm['Year']),
            max(gasprod_bcm['Year'] + 2),
            2))
    ax.set_yticks(np.arange(
        0,
        max(gasprod_bcm['Value'])+constant.GAS_PROD_YAXIS_INTERVAL,
        constant.GAS_PROD_YAXIS_INTERVAL))
    title = profile_country + ' Annual Gas Production'
    ax.set_title(title)
    ax.set_ylabel('Annual Production (billion cubic metres (bcm))')
    plt.savefig(title, dpi=300)

#call functons to source country specific data, and plot charts of that data
def profile(country):
    ei_country_data = ei_data.loc[country]
    fossil_fuel_production(country, ei_country_data)


#Profile1: World
constant = ConstantsNamespace()
ei_data = import_energy_inst_data()
profile('Total World')
