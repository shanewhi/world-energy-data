#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:36 2024
#@author: shanewhite


# Import Python modules.
import pandas as pd
import json as js
import jmespath as jp
import numpy as np


# Import user modules.
import user_globals


###############################################################################
#
# Function: populate_energy_system(country)
#
# Description:
# Collate CO2, energy production, primary energy, and electricity data using
# the Energy Institute's dataset.
# Collate total final consumption data using the IEA's dataset.
#
# Input(s): Country name, string.
# Output(s): Instance of user class user_globals.energy_system.
#
###############################################################################
def populate_energy_system(country):
    ei_data = user_globals.ei_data_import
    if country in ei_data["Country"].values:
        country_data = ei_data.loc[ei_data["Country"] == country]

        #######################################################################
        # CO2
        #######################################################################
        co2_combust_mtco2 = country_data.loc[country_data["Var"] ==
                                             "co2_combust_mtco2"]

        #######################################################################
        # Production
        #######################################################################
        coalprod_Mt = country_data.loc[country_data["Var"] == "coalprod_mt"]
        coalprod_Mt.replace("coalprod_mt", "coalprod_Mt")
        oilprod_kbpd = country_data.loc[country_data["Var"] == "oilprod_kbd"]
        oilprod_Mbpd = pd.DataFrame(index = oilprod_kbpd.index,
                                    columns = ["Country", "Var", "Value"])
        oilprod_Mbpd["Country"] = oilprod_kbpd["Country"]
        oilprod_Mbpd["Var"] = "oilprod_Mbpd"
        oilprod_Mbpd["Value"] = oilprod_kbpd["Value"] *\
            user_globals.Constant.k_TO_M.value
        gasprod_bcm = country_data.loc[country_data["Var"] == "gasprod_bcm"]

        #######################################################################
        # Primary Energy
        #######################################################################
        total_primary_EJ = country_data.loc[country_data["Var"] ==
                                            "primary_ej"]
        coal_primary_EJ = country_data.loc[country_data["Var"] ==
                                           "coalcons_ej"]
        oil_primary_EJ = country_data.loc[country_data["Var"] == "oilcons_ej"]
        gas_primary_EJ = country_data.loc[country_data["Var"] == "gascons_ej"]
        nuclear_primary_EJ = country_data.loc[country_data["Var"] ==
                                              "nuclear_ej"]
        hydro_primary_EJ = country_data.loc[country_data["Var"] == "hydro_ej"]
        wind_primary_EJ = country_data.loc[country_data["Var"] == "wind_ej"]
        solar_primary_EJ = country_data.loc[country_data["Var"] == "solar_ej"]
        biogeo_primary_EJ = country_data.loc[country_data["Var"] ==
                                             "biogeo_ej"]
        biofuels_primary_PJ = country_data.loc[country_data["Var"] ==
                                               "biofuels_cons_pj"]
        # Drop "Var" and "country" index from dataframes and convert value to
        # PJ.
        total_primary_PJ = total_primary_EJ
        total_primary_PJ = total_primary_PJ.drop(["Var"], axis = 'columns')
        total_primary_PJ["Value"] = total_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        coal_primary_PJ = coal_primary_EJ
        coal_primary_PJ = coal_primary_PJ.drop(["Var"], axis = 'columns')
        coal_primary_PJ["Value"] = coal_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        oil_primary_PJ = oil_primary_EJ
        oil_primary_PJ = oil_primary_PJ.drop(["Var"], axis = 'columns')
        oil_primary_PJ["Value"] = oil_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        gas_primary_PJ = gas_primary_EJ
        gas_primary_PJ = gas_primary_PJ.drop(["Var"], axis = 'columns')
        gas_primary_PJ["Value"] = gas_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        nuclear_primary_PJ = nuclear_primary_EJ
        nuclear_primary_PJ = nuclear_primary_PJ.drop(["Var"], axis = 'columns')
        nuclear_primary_PJ["Value"] = nuclear_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        hydro_primary_PJ = hydro_primary_EJ
        hydro_primary_PJ = hydro_primary_PJ.drop(["Var"], axis = 'columns')
        hydro_primary_PJ["Value"] = hydro_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        wind_primary_PJ = wind_primary_EJ
        wind_primary_PJ = wind_primary_PJ.drop(["Var"], axis = 'columns')
        wind_primary_PJ["Value"] = wind_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        solar_primary_PJ = solar_primary_EJ
        solar_primary_PJ = solar_primary_PJ.drop(["Var"], axis = 'columns')
        solar_primary_PJ["Value"] = solar_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        biogeo_primary_PJ = biogeo_primary_EJ
        biogeo_primary_PJ = biogeo_primary_PJ.drop(["Var"], axis = 'columns')
        biogeo_primary_PJ["Value"] = biogeo_primary_PJ["Value"] * \
            user_globals.Constant.EJ_TO_PJ.value

        # Liquid biofuels in dataset has units PJ.
        biofuels_primary_PJ = biofuels_primary_PJ.drop(["Var"], axis =\
                                                       'columns')

        # Construct geo_bio_other dataframe to combine biogeo_cons and
        # biofuels_cons (i.e. combine solid and liquid biofuels).
        geo_bio_other_primary_PJ = pd.DataFrame(index =\
                                                biogeo_primary_PJ.index,
                                                columns = ["Value"])
        geo_bio_other_primary_PJ["Value"] = biogeo_primary_PJ["Value"] + \
            biofuels_primary_PJ["Value"]

        # Ensure all dataframes comsist of the same range of years.
        # Fill any missing values with 0.
        co2_combust_mtco2  = \
            co2_combust_mtco2.reindex(total_primary_PJ.index, fill_value = 0)
        coalprod_Mt = \
            coalprod_Mt.reindex(total_primary_PJ.index, fill_value = 0)
        oilprod_Mbpd = \
            oilprod_Mbpd.reindex(total_primary_PJ.index, fill_value = 0)
        gasprod_bcm = \
            gasprod_bcm.reindex(total_primary_PJ.index, fill_value = 0)
        coal_primary_PJ = \
            coal_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        oil_primary_PJ = \
            oil_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        gas_primary_PJ = \
            gas_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        nuclear_primary_PJ = \
            nuclear_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        hydro_primary_PJ = \
            hydro_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        wind_primary_PJ = \
            wind_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        solar_primary_PJ = \
            solar_primary_PJ.reindex(total_primary_PJ.index, fill_value = 0)
        geo_bio_other_primary_PJ = \
            geo_bio_other_primary_PJ.reindex(total_primary_PJ.index,
                                             fill_value = 0)

        # Replace "Total World" label for chart titles.
        if country == "Total World":
            country = "World"
    else:
        print("Country not in EI data.\n")

    ###########################################################################
    # Total Final Consumption
    ###########################################################################

    # Make country name JSON compliant for use with IEA dataset.
    country_upper = "'" + country.upper() + "'"

    # Create year array for new TFC dataframe derived from IEA Balances.
    tfc_years = np.array(range(user_globals.Constant.TFC_START_YEAR.value,
                         user_globals.Constant.TFC_END_YEAR.value + 1))
    tf_consumption_PJ = pd.DataFrame(index = tfc_years, columns = \
                        ["Country", "Coal", "Oil", "Gas", "Wind solar etc",
                         "Bio and Waste", "Electricity", "Heat", "Total"])
    # Collate TFC data.
    for year in tfc_years:
        with open("iea" + str(year) + ".json") as iea:
            iea_data = js.load(iea)
        if jp.search(f"balances[?(short == {country_upper})].value", iea_data):
            tf_consumption_PJ["Country"] = country
            tf_consumption_PJ.at[year, "Coal"] = \
                np.array(jp.search(f"balances[?(short == {country_upper}\
                                   && flow == 'TFC' && \
                                   product == 'COAL')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Oil"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'MTOTOIL')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            # MTOTOIL is the addition of Crude Oil and Oil Products.
            tf_consumption_PJ.at[year, "Gas"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'NATGAS')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Wind solar etc"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'GEOTHERM')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Bio and Waste"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'COMRENEW')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Electricity"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'ELECTR')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Heat"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'NATGAS')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            tf_consumption_PJ.at[year, "Total"] = \
             np.array(jp.search(f"balances[?(short == {country_upper} && \
                                flow == 'TFC' && \
                                product == 'TOTAL')].value", iea_data),
                                dtype = float) * \
                                user_globals.Constant.TJ_TO_PJ.value
        else:
            print("Country not in IEA data.\n")
            break
        
    ###########################################################################
    # Return national energy system data.
    ###########################################################################
    return (user_globals.Energy_System(
            country,
            co2_combust_mtco2,
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm,
            total_primary_PJ,
            coal_primary_PJ,
            oil_primary_PJ,
            gas_primary_PJ,
            nuclear_primary_PJ,
            hydro_primary_PJ,
            wind_primary_PJ,
            solar_primary_PJ,
            geo_bio_other_primary_PJ,
            tf_consumption_PJ))
