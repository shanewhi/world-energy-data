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

        # Replace "Total World" label for chart titles.
        if country == "Total World":
            country = "World"

        #######################################################################
        # CO2
        #######################################################################
        co2_combust_Mt = country_data.loc[country_data["Var"] ==
                                          "co2_combust_mtco2", "Value"]

        #######################################################################
        # Production
        #######################################################################
        coalprod_Mt = country_data.loc[country_data["Var"] ==
                                       "coalprod_mt", "Value"]
        oilprod_kbpd = country_data.loc[country_data["Var"] ==
                                        "oilprod_kbd", "Value"]
        oilprod_Mbpd = oilprod_kbpd * user_globals.Constant.k_TO_M.value
        gasprod_bcm = country_data.loc[country_data["Var"] ==
                                       "gasprod_bcm", "Value"]

        #######################################################################
        # Primary Energy
        #######################################################################
        total_primary_EJ = country_data.loc[country_data["Var"] ==
                                        "primary_ej", "Value"]

        primary_PJ = pd.DataFrame(index = total_primary_EJ.index,
            columns = \
            ["Coal", "Oil", "Gas", "Nuclear", "Hydro", "Wind",
             "Solar", "Bio Geo", "Fossil Fuels", "Wind and Solar", "Total"])

        primary_PJ["Coal"] = country_data.loc[country_data["Var"] ==
                                        "coalcons_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Oil"] = country_data.loc[country_data["Var"] ==
                                        "oilcons_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Gas"] = country_data.loc[country_data["Var"] ==
                                        "gascons_ej", "Value"] *\
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Nuclear"] = country_data.loc[country_data["Var"] ==
                                        "nuclear_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Hydro"] = country_data.loc[country_data["Var"] ==
                                        "hydro_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Wind"] = country_data.loc[country_data["Var"] ==
                                        "wind_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Solar"] = country_data.loc[country_data["Var"] ==
                                        "solar_ej", "Value"] * \
                                        user_globals.Constant.EJ_TO_PJ.value
        primary_PJ["Bio Geo"] = country_data.loc[country_data["Var"] ==
                                    "biogeo_ej", "Value"] * \
                                    user_globals.Constant.EJ_TO_PJ.value + \
                                    country_data.loc[country_data["Var"] ==
                                    "biofuels_cons_pj", "Value"]

        # Replace any NaNs with 0 in fields imported into primary_PJ.
        primary_PJ.fillna(0, inplace = True)

        # Calculate categories.
        primary_PJ["Fossil Fuels"] = primary_PJ["Coal"] + \
                                     primary_PJ["Oil"] + \
                                     primary_PJ["Gas"]
        primary_PJ["Wind and Solar"] = primary_PJ["Wind"] + primary_PJ["Solar"]
        primary_PJ["Total"] = total_primary_EJ * \
                              user_globals.Constant.EJ_TO_PJ.value

        # Make years production consistent and fill any missing values with 0.
        coalprod_Mt = \
            coalprod_Mt.reindex(primary_PJ.index, fill_value = 0)
        oilprod_Mbpd = \
            oilprod_Mbpd.reindex(primary_PJ.index, fill_value = 0)
        gasprod_bcm = \
            gasprod_bcm.reindex(primary_PJ.index, fill_value = 0)

        #######################################################################
        # Electricity
        #######################################################################
        total_elec_gen_TWh = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_total"]

        elec_gen_TWh = pd.DataFrame(index = total_elec_gen_TWh.index,
            columns = \
            ["Coal", "Oil", "Gas", "Nuclear", "Hydro", "Renew",
             "Other", "Fossil Fuels", "Low C", "Hydro Renew", "Total"])

        elec_gen_TWh["Coal"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_coal", "Value"]
        elec_gen_TWh["Oil"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_oil", "Value"]
        elec_gen_TWh["Gas"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_gas", "Value"]
        elec_gen_TWh["Nuclear"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_nuclear", "Value"]
        elec_gen_TWh["Hydro"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_hydro", "Value"]
        elec_gen_TWh["Renew"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_ren_power", "Value"]
        elec_gen_TWh["Other"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_other", "Value"]
        elec_gen_TWh["Fossil Fuels"] = elec_gen_TWh["Coal"] + \
                                       elec_gen_TWh["Oil"] + \
                                       elec_gen_TWh["Gas"]
        elec_gen_TWh["Low C"] = elec_gen_TWh["Nuclear"] + \
                                elec_gen_TWh["Hydro"] + \
                                elec_gen_TWh["Renew"]
        elec_gen_TWh["Hydro Renew"] = elec_gen_TWh["Hydro"] + \
                                      elec_gen_TWh["Renew"]
        elec_gen_TWh["Total"] = country_data.loc[country_data["Var"] ==
                                              "electbyfuel_total", "Value"]
        elec_gen_TWh.fillna(0, inplace = True)

    else:
        print("Country not in EI data.\n")

    ###########################################################################
    # Total Final Consumption
    ###########################################################################
    # Make country name JSON compliant for use with IEA dataset.
    country_upper = "'" + country.upper() + "'"

    # Make country names compatible with IEA dataset when needed.
    if country_upper == "'AUSTRALIA'":
        country_upper = "'AUSTRALI'"
    if country_upper == "'UNITED ARAB EMIRATES'":
        country_upper = "'UAE'"
    if country_upper == "'UNITED KINGDOM'":
        country_upper = "'UK'"

    # Create year array for new TFC dataframe derived from IEA Balances.
    tfc_years = np.array(range(user_globals.Constant.TFC_START_YEAR.value,
                         user_globals.Constant.TFC_END_YEAR.value + 1))
    tf_consumption_PJ = pd.DataFrame(index = tfc_years, columns = \
                        ["Coal", "Oil", "Gas", "Wind Solar Etc",
                         "Biofuels and Waste", "Electricity", "Heat", "Total"])
    # Collate TFC data.
    for year in tfc_years:
        with open("iea" + str(year) + ".json") as iea:
            iea_data = js.load(iea)
        if jp.search(f"balances[?(short == {country_upper})].value", iea_data):

            tf_consumption_PJ.at[year, "Coal"] = \
                np.array(jp.search(f"(balances[?(short == {country_upper}\
                                   && flow == 'TFC' && \
                                   product == 'COAL')].value)", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Coal"]:
                tf_consumption_PJ.at[year, "Coal"] = 0

            # "MTOTOIL" is the addition of Crude Oil and Oil Products.
            tf_consumption_PJ.at[year, "Oil"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'MTOTOIL')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Oil"]:
                tf_consumption_PJ.at[year, "Oil"] = 0

            tf_consumption_PJ.at[year, "Gas"] = \
                np.array(jp.search(f"(balances[?(short == {country_upper}\
                                   && flow == 'TFC' && \
                                   product == 'NATGAS')].value)", iea_data),
                                   dtype = float) *\
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Gas"]:
                tf_consumption_PJ.at[year, "Gas"] = 0

            tf_consumption_PJ.at[year, "Wind Solar Etc"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'GEOTHERM')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Wind Solar Etc"]:
                tf_consumption_PJ.at[year, "Wind Solar Etc"] = 0

            tf_consumption_PJ.at[year, "Biofuels and Waste"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'COMRENEW')].value",
                                   iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Biofuels and Waste"]:
                tf_consumption_PJ.at[year, "Biofuels and Waste"] = 0

            tf_consumption_PJ.at[year, "Electricity"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'ELECTR')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Electricity"]:
                tf_consumption_PJ.at[year, "Electricity"] = 0

            tf_consumption_PJ.at[year, "Heat"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'HEAT')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Heat"]:
                tf_consumption_PJ.at[year, "Heat"] = 0

            tf_consumption_PJ.at[year, "Total"] = \
                np.array(jp.search(f"balances[?(short == {country_upper} && \
                                   flow == 'TFC' && \
                                   product == 'TOTAL')].value", iea_data),
                                   dtype = float) * \
                                   user_globals.Constant.TJ_TO_PJ.value
            if not tf_consumption_PJ.at[year, "Total"]:
                tf_consumption_PJ.at[year, "Total"] = 0
        else:
            print("Country not in IEA data.\n")
            break

    ###########################################################################
    # Return national energy system data.
    ###########################################################################
    return (user_globals.Energy_System(
            country,
            co2_combust_Mt,
            coalprod_Mt,
            oilprod_Mbpd,
            gasprod_bcm,
            primary_PJ,
            elec_gen_TWh,
            tf_consumption_PJ))
