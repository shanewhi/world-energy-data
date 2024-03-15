# Creates charts of national energy systems.
# Written by Shane White using Python v3.11.5 and Spyder IDE.
# https://github.com/shanewhi
# https://www.worldenergydata.org

# Choose a country at bottom of script. If that country has never produced a
# specific fuel, then a corresponding chart isn't created. Entered country
# name must match that used by The Energry Institute's dataset.


# Import Python modules.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import inspect


# Define conversions (multiply for conversion).
class ConstantsNamespace:
    __slots__ = ()
    THOUSAND_TO_MILLION = 1 / 1000
    FIG_SIZE = 8


# Define fuel colors for charts.
class Color(Enum):
     COAL = '#000000'
     OIL = '#A62B17'
     GAS = '#F09937'
     NUCLEAR = '#F900FF'
     HYDRO = '#479FF8'
     WIND = '#1432F5'
     SOLAR = '#DA3B26'
     GEO_BIO_OTHER = '#92902C'
     OTHER = '#9F6622'
     FOSSIL_FUELS = '#5E5E5E'
     LOW_C = '#53AE32'
     WIND_SOLAR = '#72F54A'
     ELECTRICITY = '#3F8F91'


# Custom class of country specific energy system.
class Energy_System:
    def __init__(
            self,
            name, #country name
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm):
        self.name = name
        self.coalprod_Mt = coalprod_Mt
        self.oilprod_Mbpd = oilprod_Mbpd
        self.gasprod_bcm = gasprod_bcm

    # Class method charts fuel trends.
    def chart(energy_system):
        # Identify attributes in object of custom class Energy_System.
        a = id_attributes(energy_system)
        # 1. Fossil fuel production charts.
        # Identifies production specific attributes by searching for
        # substring in a list.
        prod_attrs = [item for item in a if 'prod' in item]
        for item in prod_attrs:
            if 'coal' in item and energy_system.coalprod_Mt.empty == False:

                title = energy_system.name + ' Annual Coal Production'
                ylabel = ('Annual Production (Mt)')
                Energy_System.column_chart(energy_system.coalprod_Mt,
                    Color.COAL.value,
                    title,
                    ylabel)
            if 'oil' in item and energy_system.oilprod_Mbpd.empty == False:
                title = energy_system.name + ' Annual Oil Production'
                ylabel = ('Annual Production (Mbpd)')
                Energy_System.column_chart(energy_system.oilprod_Mbpd,
                    Color.OIL.value,
                    title,
                    ylabel)
            if 'gas' in item and energy_system.gasprod_bcm.empty == False:
                title = energy_system.name + ' Annual Gas Production'
                ylabel = ('Annual Production (bcm)')
                Energy_System.column_chart(energy_system.gasprod_bcm,
                    Color.GAS.value,
                    title,
                    ylabel)

    # Class method creates bar chart.
    def column_chart(data, column_color, title, ylabel):
        fig = plt.figure(figsize=(constant.FIG_SIZE, constant.FIG_SIZE))
        ax = fig.add_subplot()
        if column_color == Color.COAL.value:
            edge_color = 'grey'
        else:
            edge_color = 'black'
        ax.bar(
            data['Year'],
            data['Value'],
            width=1,
            color = column_color,
            edgecolor = edge_color,
            linewidth=0.7)
        ax.set_autoscaley_on(True)
        # On x-axis, display every second year, and display final year
        # irrespective of whether the start year is odd or even.
        ax.tick_params('x', labelrotation = 90)
        if (float(min(data['Year']) % 2) != 0.0):
            ax.set_xticks(np.arange(
                min(data['Year'] + 1),
                max(data['Year'] + 1),
                2))
        else:
            ax.set_xticks(np.arange(
                min(data['Year']),
                max(data['Year'] + 2),
                2))
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        #plt.savefig(title, dpi=300)

#End custom class Energy_System.


# Function extracts attributes from instance of Energy_System custom class.
def id_attributes(instance):
    # create empty list to hold attributes
    attr_list = []
    # iterate through instance attributes and exclude non-custom attributes
    for attr, value in inspect.getmembers(instance):
        if not inspect.ismethod(value) and not attr.startswith('__'):
            attr_list.append(attr)
            # uncomment next line to append values
            # attr_list.append(value)
    return(attr_list)


# Function extracts country specific data from Energy Institute's dataset.
# Returns instance of custom class Energy_System.
def populate_energy_system(country):
    country_data = ei_data.loc[country]
    coalprod_Mt = country_data.loc[country_data['Var'] == 'coalprod_mt']
    oilprod_kbpd = country_data.loc[country_data['Var'] == 'oilprod_kbd']
    gasprod_bcm = country_data.loc[country_data['Var'] == 'gasprod_bcm']
    #create new empty pandas dataframe for oil unit conversion kbpd -> Mpbd
    oilprod_Mbpd = pd.DataFrame(columns = ['Year', 'Var', 'Value'])
    oilprod_Mbpd['Year'] = oilprod_kbpd['Year']
    oilprod_Mbpd['Var'] = 'oilprod_Mbpd'
    oilprod_Mbpd['Value'] = oilprod_kbpd['Value'] * \
        constant.THOUSAND_TO_MILLION
    if country == 'Total World':
        country = 'World'
    return (Energy_System(
        country,
        coalprod_Mt,
        oilprod_Mbpd,
        gasprod_bcm))


# Function creates profile of a country's energy system by creating an
# instance of custom class Energy_System, populating that object with data,
# and creating charts.
def profile(country):
    country_energy_system = populate_energy_system(country)
    Energy_System.chart(country_energy_system)


# Main function.
constant = ConstantsNamespace()
ei_data = pd.read_csv(
    "Statistical Review of World Energy Narrow File.csv",
    index_col=['Country'],
    usecols=['Country', 'Year', 'Var', 'Value'])
# Create energy system charts for the following countries:
profile('Total World')
profile('Germany')
profile('United Arab Emirates')
profile('United Kingdom')
plt.show()
