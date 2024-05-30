#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################
#
# Module: collate.py
#
# Description:
# Collates all input data (EI and IEA).
#
########################################################################################

# Import Python modules.
import pandas as pd
import json as js
import jmespath as jp
import numpy as np

# Import user modules.
import user_globals
import countries
import process


########################################################################################
#
# Function: import_data()
#
# Description:
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported
# as single files by this function.
# The Internaitonal Energy Agency (IEA) dataset is stored in multiple JSON
# files, and therefore country specific data is searched for within these,
# rather than imported as a single file. This is done within the function
# populate_energy_system().
#
########################################################################################
def import_data():
    # Import Energy Institute's dataset.
    imported_ei_data = pd.read_csv(
        "Statistical Review of World Energy Narrow File.csv",
        index_col=["Year"],
        usecols=["Country", "Year", "Var", "Value"],
    )

    # Import Gobal Carbon Project dataset.
    gcp_ff_emissions = pd.read_excel(
        io="Global_Carbon_Budget_2023v1.1.xlsx",
        sheet_name="Fossil Emissions by Category",
        header=8,
        names=[
            "FF And Cement",
            "Coal",
            "Oil",
            "Gas",
            "Cement",
            "Flaring",
            "Other",
            "Per Capita",
        ],
        index_col=0,
    )
    gcp_budget = pd.read_excel(
        io="Global_Carbon_Budget_2023v1.1.xlsx",
        sheet_name="Global Carbon Budget",
        header=21,
        names=[
            "FF And Cement",
            "Land Use Change",
            "Atmospheric Growth",
            "Ocean Sink",
            "Land Sink",
            "Cement Carbonation Sink",
            "Budget Imbalance",
        ],
        index_col=0,
    )
    gcp_budget = gcp_budget.mul(user_globals.Constant.G_TO_M.value)

    gcp_ff_emissions = gcp_ff_emissions.drop(columns=["Per Capita"])
    gcp_budget = gcp_budget.drop(columns=["FF And Cement"])
    imported_gcp_data = gcp_ff_emissions.join(gcp_budget)

    esrl_co2_conc = pd.read_csv(
        "co2_annmean_gl.csv", header=37, index_col=["year"], usecols=["year", "mean"]
    )

    esrl_co2_growth = pd.read_csv(
        "co2_gr_gl.csv", header=43, index_col=["year"], usecols=["year", "ann inc"]
    )

    imported_esrl_data = esrl_co2_conc.join(esrl_co2_growth)
    imported_esrl_data = imported_esrl_data.rename(
        columns={"mean": "Mean", "ann inc": "Ann Inc"}
    )
    imported_esrl_data.index.names = ["Year"]

    return (imported_ei_data, imported_gcp_data, imported_esrl_data)


########################################################################################
#
# Function: organise_gcp_data()
#
# Description:
# Organises Global Carbon Project data into a user defined class.
#
########################################################################################
def organise_gcp_data(emissions_data, conc_data):
    emission_categories, emissions = process.carbon_emissions(emissions_data)
    country = "World"
    return user_globals.Global_Carbon(
        country, emissions_data, emission_categories, emissions, conc_data
    )


########################################################################################
#
# Function: organise_energy()
#
# Description:
# Calls all functions required to organise data for a specified energy system.
#
########################################################################################
def organise_energy(country, ei_data):
    country_energy_system = populate_energy_system(country, ei_data)
    if country_energy_system.incl_ei_flag is True:
        process.primary_energy(country_energy_system)
        process.electricity(country_energy_system)
    if country_energy_system.incl_iea_flag is True:
        process.consumption(country_energy_system)
    return country_energy_system


########################################################################################
#
# Function: populate_energy_system(country)
#
# Description:
# Collates CO2, energy production, primary energy, and electricity data using
# the Energy Institute's dataset.
# Collates total final consumption data using the IEA's dataset.
#
########################################################################################
def populate_energy_system(country, ei_data):
    if country in ei_data["Country"].values:
        incl_ei_flag = True
        country_data = ei_data.loc[ei_data["Country"] == country]

        # Replace "Total World" label for chart titles.
        if country == "Total World":
            country = "World"

        total_primary_EJ = country_data.loc[
            country_data["Var"] == "primary_ej", "Value"
        ]

        # CO2.
        co2_Mt = country_data.loc[country_data["Var"] == "co2_combust_mtco2", "Value"]

        # FOSSIL FUEL PRODUCTION.
        ffprod_PJ = pd.DataFrame(
            index=total_primary_EJ.index, columns=["Coal", "Oil", "Gas"]
        )

        ffprod_PJ["Coal"] = (
            country_data.loc[country_data["Var"] == "coalprod_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        oil_Mt = country_data.loc[country_data["Var"] == "oilprod_mt", "Value"]
        ffprod_PJ["Oil"] = (
            oil_Mt
            * 1e6
            * user_globals.Constant.TONNES_TO_GJ.value
            * user_globals.Constant.GJ_TO_EJ.value
            * user_globals.Constant.EJ_TO_PJ.value
        )
        ffprod_PJ["Gas"] = (
            country_data.loc[country_data["Var"] == "gasprod_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        # If nil production, create 0 series in order for chart function to
        # plot correctly.
        if ffprod_PJ["Coal"].empty or ffprod_PJ["Coal"].dropna().empty:
            ffprod_PJ["Coal"] = pd.Series(data=0, index=total_primary_EJ.index)
        if ffprod_PJ["Oil"].empty or ffprod_PJ["Oil"].dropna().empty:
            ffprod_PJ["Oil"] = pd.Series(data=0, index=total_primary_EJ.index)
        if ffprod_PJ["Gas"].empty or ffprod_PJ["Gas"].dropna().empty:
            ffprod_PJ["Gas"] = pd.Series(data=0, index=total_primary_EJ.index)

        # PRIMARY ENERGY.
        primary_PJ = pd.DataFrame(
            index=total_primary_EJ.index,
            columns=[
                "Coal",
                "Oil",
                "Gas",
                "Nuclear",
                "Hydro",
                "Wind",
                "Solar",
                "Bio, Geo and Other",
                "Fossil Fuels",
                "Renewables",
                "Total",
            ],
        )

        primary_PJ["Coal"] = (
            country_data.loc[country_data["Var"] == "coalcons_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Oil"] = (
            country_data.loc[country_data["Var"] == "oilcons_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Gas"] = (
            country_data.loc[country_data["Var"] == "gascons_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Nuclear"] = (
            country_data.loc[country_data["Var"] == "nuclear_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Hydro"] = (
            country_data.loc[country_data["Var"] == "hydro_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Wind"] = (
            country_data.loc[country_data["Var"] == "wind_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Solar"] = (
            country_data.loc[country_data["Var"] == "solar_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ["Bio, Geo and Other"] = (
            country_data.loc[country_data["Var"] == "biogeo_ej", "Value"]
            * user_globals.Constant.EJ_TO_PJ.value
            + country_data.loc[country_data["Var"] == "biofuels_cons_pj", "Value"]
        )

        # Replace any NaNs with 0 in fields imported into primary_PJ.
        with pd.option_context("future.no_silent_downcasting", True):
            primary_PJ.fillna(0, inplace=True)

        # Calculate categories.
        primary_PJ["Fossil Fuels"] = (
            primary_PJ["Coal"] + primary_PJ["Oil"] + primary_PJ["Gas"]
        )
        primary_PJ["Renewables"] = (
            primary_PJ["Hydro"] + primary_PJ["Wind"] + primary_PJ["Solar"]
        )
        primary_PJ["Total"] = total_primary_EJ * user_globals.Constant.EJ_TO_PJ.value

        # ELECTRICITY.
        total_elecprod_TWh = country_data.loc[
            country_data["Var"] == "electbyfuel_total"
        ]

        elecprod_TWh = pd.DataFrame(
            index=total_elecprod_TWh.index,
            columns=[
                "Coal",
                "Oil",
                "Gas",
                "Nuclear",
                "Hydro",
                "Wind",
                "Solar",
                "Bio, Geo Other",
                "Fossil Fuels",
                "Wind and Solar",
                "Renewables",
                "Total",
            ],
        )

        elecprod_TWh["Coal"] = country_data.loc[
            country_data["Var"] == "electbyfuel_coal", "Value"
        ]
        elecprod_TWh["Oil"] = country_data.loc[
            country_data["Var"] == "electbyfuel_oil", "Value"
        ]
        elecprod_TWh["Gas"] = country_data.loc[
            country_data["Var"] == "electbyfuel_gas", "Value"
        ]
        elecprod_TWh["Nuclear"] = country_data.loc[
            country_data["Var"] == "electbyfuel_nuclear", "Value"
        ]
        elecprod_TWh["Hydro"] = country_data.loc[
            country_data["Var"] == "electbyfuel_hydro", "Value"
        ]
        elecprod_TWh["Wind"] = country_data.loc[
            country_data["Var"] == "wind_twh", "Value"
        ]
        elecprod_TWh["Solar"] = country_data.loc[
            country_data["Var"] == "solar_twh", "Value"
        ]
        elecprod_TWh["Bio, Geo and Other"] = (
            country_data.loc[country_data["Var"] == "biogeo_twh", "Value"]
            + country_data.loc[country_data["Var"] == "electbyfuel_other", "Value"]
        )
        elecprod_TWh["Fossil Fuels"] = (
            elecprod_TWh["Coal"] + elecprod_TWh["Oil"] + elecprod_TWh["Gas"]
        )
        elecprod_TWh["Wind and Solar"] = elecprod_TWh["Wind"] + elecprod_TWh["Solar"]
        elecprod_TWh["Renewables"] = (
            elecprod_TWh["Wind"] + elecprod_TWh["Solar"] + elecprod_TWh["Hydro"]
        )
        elecprod_TWh["Total"] = country_data.loc[
            country_data["Var"] == "electbyfuel_total", "Value"
        ]

        with pd.option_context("future.no_silent_downcasting", True):
            elecprod_TWh.fillna(0, inplace=True)

        elecprod_TWh["Coal"] = np.where(
            elecprod_TWh["Coal"] < 0.1, 0, elecprod_TWh["Coal"]
        )
        elecprod_TWh["Oil"] = np.where(
            elecprod_TWh["Oil"] < 0.1, 0, elecprod_TWh["Oil"]
        )
        elecprod_TWh["Gas"] = np.where(
            elecprod_TWh["Gas"] < 0.1, 0, elecprod_TWh["Gas"]
        )
        elecprod_TWh["Nuclear"] = np.where(
            elecprod_TWh["Nuclear"] < 0.1, 0, elecprod_TWh["Nuclear"]
        )
        elecprod_TWh["Hydro"] = np.where(
            elecprod_TWh["Hydro"] < 0.1, 0, elecprod_TWh["Hydro"]
        )
        elecprod_TWh["Wind"] = np.where(
            elecprod_TWh["Wind"] < 0.1, 0, elecprod_TWh["Wind"]
        )
        elecprod_TWh["Solar"] = np.where(
            elecprod_TWh["Solar"] < 0.1, 0, elecprod_TWh["Solar"]
        )
        elecprod_TWh["Bio, Geo and Other"] = np.where(
            elecprod_TWh["Bio, Geo and Other"] < 0.1,
            0,
            elecprod_TWh["Bio, Geo and Other"],
        )
    else:
        print("Country not in EI data.\n")
        incl_ei_flag = False
        co2_Mt = None
        ffprod_PJ = None
        primary_PJ = None
        elecprod_TWh = None

    # FINAL ENERGY.
    # Convert country name to IEA JSON equivalent.
    iea_country = countries.iea_country_name(country)
    # Create year array for new TFC dataframe derived from IEA Balances.
    tfc_years = np.array(
        range(
            user_globals.Constant.TFC_START_YEAR.value,
            user_globals.Constant.TFC_END_YEAR.value + 1,
        )
    )
    consumption_PJ = pd.DataFrame(
        index=tfc_years,
        columns=[
            "Coal",
            "Oil",
            "Gas",
            "Wind Solar Etc",
            "Biofuels and Waste",
            "Electricity",
            "Heat",
            "Total",
        ],
    )
    # Collate data.
    for year in tfc_years:
        with open("iea" + str(year) + ".json") as iea:
            iea_data = js.load(iea)
        if jp.search(f"balances[?(short == {iea_country})].value", iea_data):
            incl_iea_flag = True
            consumption_PJ.at[year, "Coal"] = (
                np.array(
                    jp.search(
                        f"(balances[?(short == {iea_country}\
                                   && flow == 'TFC' && \
                                   product == 'COAL')].value)",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Coal"]:
                consumption_PJ.at[year, "Coal"] = 0

            # "MTOTOIL" is the addition of Crude Oil and Oil Products.
            consumption_PJ.at[year, "Oil"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'MTOTOIL')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Oil"]:
                consumption_PJ.at[year, "Oil"] = 0

            consumption_PJ.at[year, "Gas"] = (
                np.array(
                    jp.search(
                        f"(balances[?(short == {iea_country}\
                                   && flow == 'TFC' && \
                                   product == 'NATGAS')].value)",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Gas"]:
                consumption_PJ.at[year, "Gas"] = 0

            consumption_PJ.at[year, "Wind Solar Etc"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'GEOTHERM')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Wind Solar Etc"]:
                consumption_PJ.at[year, "Wind Solar Etc"] = 0

            consumption_PJ.at[year, "Biofuels and Waste"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'COMRENEW')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Biofuels and Waste"]:
                consumption_PJ.at[year, "Biofuels and Waste"] = 0

            consumption_PJ.at[year, "Electricity"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'ELECTR')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Electricity"]:
                consumption_PJ.at[year, "Electricity"] = 0

            consumption_PJ.at[year, "Heat"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'HEAT')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Heat"]:
                consumption_PJ.at[year, "Heat"] = 0

            consumption_PJ.at[year, "Total"] = (
                np.array(
                    jp.search(
                        f"balances[?(short == {iea_country} && \
                                   flow == 'TFC' && \
                                   product == 'TOTAL')].value",
                        iea_data,
                    ),
                    dtype=float,
                )
                * user_globals.Constant.TJ_TO_PJ.value
            )
            if not consumption_PJ.at[year, "Total"]:
                consumption_PJ.at[year, "Total"] = 0
        else:
            print("Country not in IEA data.\n")
            incl_iea_flag = False
            consumption_PJ = None

    # Return national energy system data as object.
    return user_globals.Energy_System(
        country,
        incl_ei_flag,
        incl_iea_flag,
        co2_Mt,
        ffprod_PJ,
        primary_PJ,
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        elecprod_TWh,
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        consumption_PJ,
        pd.DataFrame(),
    )  # Populated in process.py
