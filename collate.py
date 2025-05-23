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
import output


########################################################################################
#
# Function: profile(nation, global_carbon, ei_data)
#
# Description:
# Top level function that calls collation and chart functions for a specified
# nation.
#
########################################################################################
def profile(nation, global_carbon, ei_data):
    energy_system = energy(nation, ei_data)

    # Generate global fossil fuel production charts using EI data.
    if energy_system.incl_ei_flag is True:
        output.country_co2_charts(energy_system, global_carbon)

    coal_producers, oil_producers, gas_producers = ffproducer_shares(ei_data)
    output.world_ffprod_charts(coal_producers, oil_producers, gas_producers, energy_system.name)
    print("\nLarge coal producers:\n", str(coal_producers))
    print("\nLarge oil producers:\n", str(oil_producers))
    print("\nLarge gas producers:\n", str(gas_producers), "\n")

    output.country_prod_primary_energy_charts(energy_system)
    output.country_consumption_elec_charts(energy_system)
    output.country_consumption_charts(energy_system)
    output.country_elec_charts(energy_system)

    # Print warnings to console.
    if energy_system.incl_ei_flag is False:
        print("Nation was not found in EI data. Check the nations listed in The Statistical Review of World Energy \
included in this package.")

    if energy_system.incl_iea_flag is False:
        print("Nation was not found in IEA data. Its IEA translation name may need to be added to nations.py. \
See this package's README for instructions.")


########################################################################################
#
# Function: import_data()
#
# Description:
# Data importation differs between sources:
# Energy Institute (EI) and Global Carbon Project (GCP) datasets are imported
# as single files by this function.
# The International Energy Agency (IEA) dataset is stored in multiple JSON
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

    # Import Global Carbon Project dataset.
    gcp_ff_emissions_MtC = pd.read_excel(
        io="Global_Carbon_Budget_2024_v1.0.xlsx",
        sheet_name="Fossil Emissions by Category",
        header=8,
        names=[
            "FF and Cement",
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
    gcp_ff_emissions_MtCO2 = gcp_ff_emissions_MtC.mul(
        user_globals.Constant.C_TO_CO2.value
    )
    gcp_ff_emissions_MtCO2 = gcp_ff_emissions_MtCO2.drop(columns=["Per Capita"])

    gcp_budget_MtC = pd.read_excel(
        io="Global_Carbon_Budget_2024_v1.0.xlsx",
        sheet_name="Global Carbon Budget",
        header=21,
        names=[
            "FF and Cement Exc Cement Carb",
            "Land Use Change",
            "Atmospheric Growth",
            "Ocean Sink",
            "Land Sink",
            "Cement Carbonation Sink",
            "Budget Imbalance",
            "Net FF and Cement",
        ],
        index_col=0,
    )
    gcp_budget_MtC = gcp_budget_MtC.mul(user_globals.Constant.G_TO_M.value)
    gcp_budget_MtC02 = gcp_budget_MtC.mul(user_globals.Constant.C_TO_CO2.value)
    gcp_budget_MtC02 = gcp_budget_MtC02.drop(columns=["FF and Cement Exc Cement Carb"])
    imported_gcp_data = gcp_ff_emissions_MtCO2.join(gcp_budget_MtC02)

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

    return imported_ei_data, imported_gcp_data, imported_esrl_data


########################################################################################
#
# Function: co2_data()
#
# Description:
# Organises Global Carbon Project and NOAA ESRL data into a user defined class.
#
########################################################################################
def co2_data(energy_data, emissions_data, conc_data):
    country_shares_fy_data = calc_country_shares_fy(energy_data)
    emission_categories, emissions, country_shares_fy = process.carbon_emissions(
        emissions_data, country_shares_fy_data
    )
    country = "World"
    return user_globals.Global_Carbon(
        country,
        emissions_data,
        emission_categories,
        emissions,
        conc_data,
        country_shares_fy,
    )


########################################################################################
#
# Function: calc_country_shares_fy()
#
# Description:
# For all countries, calculate shares of CO2 emissions from fossil fuel combustion for
# the final year of data.
#
########################################################################################
def calc_country_shares_fy(data):
    # Extract CO2 emissions from fossil fuel combustion for all years.
    ffco2_Mt = data.loc[data["Var"] == "co2_combust_mtco2"]

    # Identify most recent year.
    final_yr = max(data.index)

    # Filter for data of most recent year.
    ffco2_Mt_fy = ffco2_Mt.loc[ffco2_Mt.index == final_yr]

    # Reindex dataframe to country so that those starting with "Total" can be
    # dropped. Record World total prior.
    ffco2_Mt_fy.set_index(["Country"], inplace=True)
    total_ffco2_Mt = ffco2_Mt_fy.loc[ffco2_Mt_fy.index == "Total World", "Value"].values
    ffco2_Mt_fy = ffco2_Mt_fy.drop(
        index=ffco2_Mt_fy[ffco2_Mt_fy.index.str.startswith("Total")].index
    )
    # Calculate shares.
    ffco2_Mt_fy["Share"] = round(ffco2_Mt_fy["Value"] / total_ffco2_Mt * 100, 2)
    # TDrop "Other" regions, which are collections of low emitting countries.
    # Dropping them only prevents any being tallied as a relatively large emitter. The
    # share is still included in the chart as 1-large_emitters.
    ffco2_Mt_fy = ffco2_Mt_fy.drop(
        index=ffco2_Mt_fy[ffco2_Mt_fy.index.str.startswith("Other")].index
    )
    # Record final year for later usage.
    ffco2_Mt_fy["Year"] = final_yr
    # Clean up.
    ffco2_Mt_fy = ffco2_Mt_fy.reset_index()
    ffco2_Mt_fy = ffco2_Mt_fy.drop(["Var", "Value"], axis=1)
    return ffco2_Mt_fy


########################################################################################
#
# Function: ffprod_country_shares()
#
# Description:
# Identifies and organises the major fossil fuel producers.
#
########################################################################################
def ffproducer_shares(data):
    # coal_producers, oil_producers, gas_producers = process.id_ffprods(ei_data)

    # Extract fossil fuel production data.
    coal_prod = data.loc[data["Var"] == "coalprod_ej"]
    oil_prod = data.loc[data["Var"] == "oilprod_mt"]
    gas_prod = data.loc[data["Var"] == "gasprod_ej"]

    # Obtain latest global production value of each fossil fuel,
    # in order to calculate shares.
    # 1. Coal
    world_coal_prod = coal_prod.loc[coal_prod["Country"] == "Total World"]
    world_coal_prod_latest = world_coal_prod.loc[
        world_coal_prod.index == max(world_coal_prod.index), "Value"
    ]
    total_coal = float(world_coal_prod_latest.values)
    # 2. Oil
    world_oil_prod = oil_prod.loc[oil_prod["Country"] == "Total World"]
    world_oil_prod_latest = world_oil_prod.loc[
        world_oil_prod.index == max(world_oil_prod.index), "Value"
    ]
    total_oil = float(world_oil_prod_latest.values)
    # 3. Gas
    world_gas_prod = gas_prod.loc[gas_prod["Country"] == "Total World"]
    world_gas_prod_latest = world_gas_prod.loc[
        world_gas_prod.index == max(world_gas_prod.index), "Value"
    ]
    total_gas = float(world_gas_prod_latest.values)

    coal_producers, oil_producers, gas_producers = process.world_ffprod(
        coal_prod, oil_prod, gas_prod, total_coal, total_oil, total_gas
    )

    return coal_producers, oil_producers, gas_producers


########################################################################################
#
# Function: energy()
#
# Description:
# Calls all functions required to organise data for a specified energy system.
#
########################################################################################
def energy(country, ei_data):
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

        # Fossil Fuel CO2
        ffco2_Mt = country_data.loc[country_data["Var"] == "co2_combust_mtco2", "Value"]
        ffco2 = pd.DataFrame(index=ffco2_Mt.index, columns=["Value", "Change"])
        ffco2["Value"] = ffco2_Mt
        process.ffco2_change(ffco2)

        # Fossil Fuel Production
        ffprod_PJ = pd.DataFrame(
            index=total_primary_EJ.index, columns=["Coal", "Oil", "Gas"]
        )

        ffprod_PJ["Coal"] = (
                country_data.loc[country_data["Var"] == "coalprod_ej", "Value"]
                * user_globals.Constant.EJ_TO_PJ.value
        )
        oil_mt = country_data.loc[country_data["Var"] == "oilprod_mt", "Value"]
        ffprod_PJ["Oil"] = (
                oil_mt
                * 1e6
                * user_globals.Constant.TONNES_TO_GJ.value
                * user_globals.Constant.GJ_TO_PJ.value
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

        # Primary Energy.
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

        # Electricity.
        total_elecprod_TWh = country_data.loc[country_data["Var"] == "elect_twh"]

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
                "Bio, Geo and Other",
                "Fossil Fuels",
                "Wind and Solar",
                "Renewables",
                "Sum Fuels",
                "Total Fuels",
                "Total Country",
                "Unpublished",
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
            country_data["Var"] == "nuclear_twh", "Value"
        ]
        elecprod_TWh["Hydro"] = country_data.loc[
            country_data["Var"] == "hydro_twh", "Value"
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

        # Replace any NaNs with 0
        with pd.option_context("future.no_silent_downcasting", True):
            elecprod_TWh.fillna(0, inplace=True)

        elecprod_TWh["Fossil Fuels"] = (
                elecprod_TWh["Coal"] + elecprod_TWh["Oil"] + elecprod_TWh["Gas"]
        )
        elecprod_TWh["Wind and Solar"] = elecprod_TWh["Wind"] + elecprod_TWh["Solar"]
        elecprod_TWh["Renewables"] = (
                elecprod_TWh["Wind"] + elecprod_TWh["Solar"] + elecprod_TWh["Hydro"]
        )
        # For some countries (e.g. Norway), EI data contains a total for the country ("elect_twh"),
        # but not a value for every fuel. In such cases, "electbyfuel_total" will be
        # zero, but "elect_twh" will have a value. Values may also be provided for
        # non-combustible fuels, in which case these can be plotted and totalled. Any difference between
        # this "Sum_Fuels" and "elect_twh" will be classified as "Unpublished".

        elecprod_TWh["Total Fuels"] = country_data.loc[
            country_data["Var"] == "electbyfuel_total", "Value"
        ]
        elecprod_TWh["Total Country"] = country_data.loc[
            country_data["Var"] == "elect_twh", "Value"
        ]

        elecprod_TWh["Sum Fuels"] = (
                elecprod_TWh["Coal"]
                + elecprod_TWh["Oil"]
                + elecprod_TWh["Gas"]
                + elecprod_TWh["Nuclear"]
                + elecprod_TWh["Hydro"]
                + elecprod_TWh["Wind"]
                + elecprod_TWh["Solar"]
                + elecprod_TWh["Bio, Geo and Other"]
        )

        elecprod_TWh["Unpublished"] = (
                elecprod_TWh["Total Country"] - elecprod_TWh["Sum Fuels"]
        )

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
        elecprod_TWh["Unpublished"] = np.where(
            elecprod_TWh["Unpublished"] < 0.1, 0, elecprod_TWh["Unpublished"]
        )
    else:
        print("Country not in EI data.\n")
        incl_ei_flag = False
        ffco2 = None
        ffprod_PJ = None
        primary_PJ = None
        elecprod_TWh = None

    # Final Energy,
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
    incl_iea_flag = False
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
            if not consumption_PJ.at[year, "Coal"].size > 0:
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
            if not consumption_PJ.at[year, "Oil"].size > 0:
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
            if not consumption_PJ.at[year, "Gas"].size > 0:
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
            if not consumption_PJ.at[year, "Wind Solar Etc"].size > 0:
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
            if not consumption_PJ.at[year, "Biofuels and Waste"].size > 0:
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
            if not consumption_PJ.at[year, "Electricity"].size > 0:
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
            if not consumption_PJ.at[year, "Heat"].size > 0:
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
            if not consumption_PJ.at[year, "Total"].size > 0:
                consumption_PJ.at[year, "Total"] = 0

    if incl_iea_flag is False:
        print("Country not in IEA data.\n")
        consumption_PJ = None
    else:
        consumption_PJ = consumption_PJ.astype(float)

    # Return country energy system data as object.
    return user_globals.Energy_System(
        country,
        incl_ei_flag,
        incl_iea_flag,
        ffco2,
        ffprod_PJ,
        primary_PJ,
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        elecprod_TWh,
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        pd.DataFrame(),  # Populated in process.py
        consumption_PJ,
        pd.DataFrame(),  # Populated in process.py
    )


########################################################################################
#
# Function: populate_major_emitter_co2_energy_dataframe()
#
# Description:
# For major emitters, construct dataframe of fossil fuel CO2 emissions and primary
# energy data.
#
########################################################################################
def populate_major_emitter_co2_energy_dataframe(major_emitters, ei_data):
    # Initialise loop counter
    n = 0
    # For each large emitting country -
    for country in major_emitters:
        # Generate multi index indices for dataframe
        parameters = ["ffco2_Mt", "primary_PJ_coal", "primary_PJ_oil", "primary_PJ_gas"]
        country_name = []
        for i in range(4):
            country_name = country_name + [country]
        arrays = [country_name, parameters]
        indices = pd.MultiIndex.from_arrays(arrays, names=('Country', 'Parameter'))

        # Assemble data
        country_energy_data = ei_data.loc[ei_data["Country"] == country]
        ffco2_Mt = country_energy_data.loc[country_energy_data["Var"] == "co2_combust_mtco2", "Value"]
        primary_PJ_coal = (
                country_energy_data.loc[country_energy_data["Var"] == "coalcons_ej", "Value"]
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ_oil = (
                country_energy_data.loc[country_energy_data["Var"] == "oilcons_ej", "Value"]
                * user_globals.Constant.EJ_TO_PJ.value
        )
        primary_PJ_gas = (
                country_energy_data.loc[country_energy_data["Var"] == "gascons_ej", "Value"]
                * user_globals.Constant.EJ_TO_PJ.value
        )

        # Name each data series
        ffco2_Mt.name = 'ffco2_Mt'
        primary_PJ_coal.name = 'primary_PJ_coal'
        primary_PJ_oil.name = 'primary_PJ_oil'
        primary_PJ_gas.name = 'primary_PJ_gas'

        # Concatenate series to create a dataframe
        dataframe = pd.concat([ffco2_Mt, primary_PJ_coal, primary_PJ_oil, primary_PJ_gas], axis=1)
        # Transpose
        dataframe = dataframe.T
        # Replace index with multi index generated above
        dataframe.index = indices
        # Create parent dataframe
        if n == 0:
            major_emitter_co2_energy_dataframe = dataframe
        else:
            major_emitter_co2_energy_dataframe = pd.concat([major_emitter_co2_energy_dataframe, dataframe])
        # Increment loop counter
        n += 1
    return major_emitter_co2_energy_dataframe
