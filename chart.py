#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""


###############################################################################
#
# Module: chart.py
#
# Description:
# Generic chart drawing functions -
# line()
# line_1x4()
# line_2x3()
# line 2x4()
# column_1x3()
# column_1x4()
# column_2x3()
# column_2x4()
# column_grouped()
# treemap()
#
###############################################################################


# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np
import mpl_extra.treemap as tr #https://github.com/chenyulue/matplotlib-extra
import matplotlib.ticker


# Import user modules.
import user_globals


###############################################################################
#
# Function: line()
#
# Description:
# Plots a single series.
#
###############################################################################
def line(x, y, country_name, color, title, ylabel, footer_text):

    # Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in x:
        if year % 10 == 0: # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(x)

    # Create figure and axes.
    fig, ax = plt.subplots(1, 1,
                figsize = (user_globals.Constant.FIG_HSIZE_1x1.value,
                           user_globals.Constant.FIG_VSIZE_1x1.value))
    ax.plot(x, y, color, linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 6, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = 0.3)

    # Add comma as thousand seperator.
    ax.yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax.autoscale(axis = "y")
    ax.set_ylim(bottom = 0)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Year")

    # Set aspect ratio 1:1.
    ax.set_box_aspect(1)

    # Figure title.
    fig.suptitle(
        country_name,
        x = 0.13,
        y = 0.95,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
        )
    # Text beneath figure title.
    fig.text(
        0.13,
        0.905,
        title,
        horizontalalignment = "left",
       fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
       fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value,
       )
   # Text in footer.
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
       fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
       fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
       )
    plt.subplots_adjust(bottom=0.14)


###############################################################################
#
# Function: line_1x4()
#
# Description:
# 1x4 line subplots.
#
###############################################################################
def line_1x4(
        series1,
        series2,
        series3,
        series4,
        color1,
        color2,
        color3,
        color4,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        ylabel,
        footer_text,
        equiv_yscale
        ):

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(1, 4, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_1X4.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_1X4.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.925,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )

    ax[0].plot(
        series1.index,
        series1,
        color1,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0].set_title(
            subplot1_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabel)
    ax[0].yaxis.grid(True)
    ax[0].margins(x = 0, tight = True)
    ax[0].set_xticks(x_ticks)
    ax[0].set_box_aspect(1)
    ax[0].autoscale(axis = "y")
    ylim1 = ax[0].get_ylim()[1]

    ax[1].plot(
        series2.index,
        series2,
        color2,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1].set_title(
            subplot2_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].margins(x = 0, tight = True)
    ax[1].set_xticks(x_ticks)
    ax[1].set_box_aspect(1)
    ax[1].autoscale(axis = "y")
    ylim2 = ax[1].get_ylim()[1]

    ax[2].plot(
        series3.index,
        series3,
        color3,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[2].set_title(
            subplot3_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[2].set_xlabel("Year")
    ax[2].yaxis.grid(True)
    ax[2].margins(x = 0, tight = True)
    ax[2].set_xticks(x_ticks)
    ax[2].set_box_aspect(1)
    ax[2].autoscale(axis = "y")
    ylim3 = ax[2].get_ylim()[1]

    ax[3].plot(
        series4.index,
        series4,
        color4,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[3].set_title(
            subplot4_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[3].set_xlabel("Year")
    ax[3].yaxis.grid(True)
    ax[3].margins(x = 0, tight = True)
    ax[3].set_xticks(x_ticks)
    ax[3].set_box_aspect(1)
    ax[3].autoscale(axis = "y")
    ylim4 = ax[3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)
        ax[3].set_ylim(0, y_max)

    plt.subplots_adjust(bottom=0.13)


###############################################################################
#
# Function: line_2x3()
#
# Description:
# 2x3 line subplots.
#
###############################################################################
def line_2x3(
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        ylabel,
        footer_text,
        equiv_yscale
        ):

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(2, 3, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.925,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )
    ax[0, 0].plot(
        series1.index,
        series1,
        color1,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 0].set_title(
            subplot1_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].margins(x = 0, tight = True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis = "y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.index,
        series2,
        color2,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 1].set_title(
            subplot2_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].margins(x = 0, tight = True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis = "y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.index,
        series3,
        color3,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 2].set_title(
            subplot3_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].margins(x = 0, tight = True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis = "y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[1, 0].plot(
        series4.index,
        series4,
        color4,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 0].set_title(
            subplot4_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].margins(x = 0, tight = True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis = "y")
    ylim4 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series5.index,
        series5,
        color5,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 1].set_title(
            subplot5_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].margins(x = 0, tight = True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis = "y")
    ylim5 = ax[1, 1].get_ylim()[1]

    ax[1, 2].plot(
        series6.index,
        series6,
        color6,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 2].set_title(
            subplot6_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].margins(x = 0, tight = True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis = "y")
    ylim6 = ax[1, 2].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)

    plt.subplots_adjust(bottom = 0.14)


###############################################################################
#
# Function: line_2x4()
#
# Description:
# 2x4 line subplots.
#
###############################################################################
def line_2x4(
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        series8,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        color7,
        color8,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        subplot7_title,
        subplot8_title,
        ylabel,
        footer_text,
        equiv_yscale
        ):

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(2, 4, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X4.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X4.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.925,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )
    ax[0, 0].plot(
        series1.index,
        series1,
        color1,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 0].set_title(
            subplot1_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].margins(x = 0, tight = True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis = "y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.index,
        series2,
        color2,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 1].set_title(
            subplot2_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 1].margins(x = 0, tight = True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis = "y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.index,
        series3,
        color3,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 2].set_title(
            subplot3_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 2].margins(x = 0, tight = True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis = "y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[0, 3].plot(
        series4.index,
        series4,
        color4,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[0, 3].set_title(
            subplot4_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 3].set_xlabel("Year")
    ax[0, 3].margins(x = 0, tight = True)
    ax[0, 3].set_xticks(x_ticks)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis = "y")
    ylim4 = ax[0, 3].get_ylim()[1]

    ax[1, 0].plot(
        series5.index,
        series5,
        color5,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 0].set_title(
            subplot5_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].margins(x = 0, tight = True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis = "y")
    ylim5 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series6.index,
        series6,
        color6,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 1].set_title(
            subplot6_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].margins(x = 0, tight = True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis = "y")
    ylim6 = ax[1, 1].get_ylim()[1]

    ax[1, 2].plot(
        series7.index,
        series7,
        color7,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 2].set_title(
            subplot7_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].margins(x = 0, tight = True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis = "y")
    ylim7 = ax[1, 2].get_ylim()[1]

    ax[1, 3].plot(
        series8.index,
        series8,
        color8,
        linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
        )
    ax[1, 3].set_title(
            subplot8_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[1, 3].set_xlabel("Year")
    ax[1, 3].margins(x = 0, tight = True)
    ax[1, 3].set_xticks(x_ticks)
    ax[1, 3].set_box_aspect(1)
    ax[1, 3].autoscale(axis = "y")
    ylim8 = ax[1, 3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6, ylim7, ylim8)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)
        ax[1, 3].set_ylim(0, y_max)

    plt.subplots_adjust(bottom=0.13)


###############################################################################
#
# Function: column_1x3()
#
# Description:
# 1x3 column subplots.
#
###############################################################################
def column_1x3(
        series1,
        series2,
        series3,
        color1,
        color2,
        color3,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabels,
        footer_text,
        equiv_yscale
        ):

    # Create figure and axes.
    fig, ax = plt.subplots(1, 3,
                figsize = (user_globals.Constant.FIG_HSIZE_SUBPLOT_1X3.value,
                           user_globals.Constant.FIG_VSIZE_SUBPLOT_1X3.value))

    # Set space between subplots.
    plt.subplots_adjust(wspace = 0.25, hspace = 0.4)

    # Figure title.
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.94,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    # Text beneath figure title.
    fig.text(
        0.125,
        0.875,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    # Text in footer.
    fig.text(
        0.125,
        0.007,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )

    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[2].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))

    # Grey edges for black columns.
    if color1 == "black":
        edge_color1 = "dimgrey"
    else:
        edge_color1 = "black"
    if color2 == "black":
        edge_color2 = "dimgrey"
    else:
        edge_color2 = "black"
    if color3 == "black":
        edge_color3 = "dimgrey"
    else:
        edge_color3 = "black"

    # x_ticks only for start of each decade.
    x_ticks1 = []
    x_ticks2 = []
    x_ticks3 = []
    for year in series1.index:
        if year % 10 == 0: # Modulus.
            x_ticks1.append(year)
    # Replace final value with most recent year.
    x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    ax[0].set_xticks(x_ticks1)
    for year in series2.index:
        if year % 10 == 0: # Modulus.
            x_ticks2.append(year)
    # Replace final value with most recent year.
    x_ticks2[len(x_ticks2) - 1] = max(series2.index)
    ax[1].set_xticks(x_ticks2)
    for year in series3.index:
        if year % 10 == 0: # Modulus.
            x_ticks3.append(year)
    # Replace final value with most recent year.
    x_ticks3[len(x_ticks3) - 1] = max(series3.index)
    ax[2].set_xticks(x_ticks3)

    # Subplot 1
   # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.index,
            series1, color1,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0].bar(
            series1.index,
            series1,
            width = 1,
            align = 'edge',
            color = color1,
            edgecolor = edge_color1,
            linewidth = 0.2
            )
    ax[0].set_title(
        subplot1_title,
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
        loc = "left"
        )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_box_aspect(1)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    # Autoscale and get max y for setting equiv y scale at end of function.
    ax[0].autoscale(axis = "y")
    # Remove margins.
    ax[0].margins(x = 0, tight = True)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for second and third suboplots.
    if  max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2, color2,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1].bar(
            series2.index,
            series2,
            width = 1,
            align = 'edge',
            color = color2,
            edgecolor = edge_color2,
            linewidth = 0.2
            )
    ax[1].set_title(
            subplot2_title,
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
            loc = "left"
            )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis = "y")
    ax[1].margins(x = 0, tight = True)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.index,
            series3,
            color3,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[2].bar(
            series3.index,
            series3,
            width = 1,
            align = 'edge',
            color = color3,
            edgecolor = edge_color3,
            linewidth = 0.2
            )
    ax[2].set_title(
            subplot3_title,
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
            loc = "left")
    ax[2].set_xlabel("Year")
    ax[2].yaxis.grid(True)
    ax[2].set_box_aspect(1)
    ax[2].set_axisbelow(True)
    ax[2].autoscale(axis = "y")
    ax[2].margins(x = 0, tight = True)
    ylim3 = ax[2].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)

    # Move subplots up on page to provide space for footer text.
    plt.subplots_adjust(bottom = 0.13)


###############################################################################
#
# Function: column_1x4()
#
# Description:
# 1x4 column subplots.
#
###############################################################################
def column_1x4(
        series1,
        series2,
        series3,
        series4,
        color1,
        color2,
        color3,
        color4,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        ylabels,
        footer_text,
        equiv_yscale
        ):

    # Create figure and axes.
    fig, ax = plt.subplots(1, 4,
                figsize = (user_globals.Constant.FIG_HSIZE_SUBPLOT_1X4.value,
                           user_globals.Constant.FIG_VSIZE_SUBPLOT_1X4.value))

    # Set space between subplots.
    plt.subplots_adjust(wspace = 0.25, hspace = 0.4)

    # Figure title.
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.93,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    # Text beneath figure title.
    fig.text(
        0.125,
        0.865,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    # Text in footer.
    fig.text(
        0.125,
        0.007,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )

    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[2].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[3].yaxis.set_major_formatter( \
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))

    # Grey edges for black columns.
    if color1 == "black":
        edge_color1 = "dimgrey"
    else:
        edge_color1 = "black"
    if color2 == "black":
        edge_color2 = "dimgrey"
    else:
        edge_color2 = "black"
    if color3 == "black":
        edge_color3 = "dimgrey"
    else:
        edge_color3 = "black"
    if color4 == "black":
        edge_color4 = "dimgrey"
    else:
        edge_color4 = "black"

    # x_ticks only for start of each decade.
    x_ticks1 = []
    x_ticks2 = []
    x_ticks3 = []
    x_ticks4 = []
    for year in series1.index:
        if year % 10 == 0: # Modulus.
            x_ticks1.append(year)
    # Replace final value with most recent year.
    x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    ax[0].set_xticks(x_ticks1)
    for year in series2.index:
        if year % 10 == 0: # Modulus.
            x_ticks2.append(year)
    # Replace final value with most recent year.
    x_ticks2[len(x_ticks2) - 1] = max(series2.index)
    ax[1].set_xticks(x_ticks2)
    for year in series3.index:
        if year % 10 == 0: # Modulus.
            x_ticks3.append(year)
    # Replace final value with most recent year.
    x_ticks3[len(x_ticks3) - 1] = max(series3.index)
    ax[2].set_xticks(x_ticks3)
    for year in series4.index:
        if year % 10 == 0: # Modulus.
            x_ticks4.append(year)
    # Replace final value with most recent year.
    x_ticks4[len(x_ticks4) - 1] = max(series4.index)
    ax[3].set_xticks(x_ticks4)

    # Subplots
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.index,
            series1,
            color1,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0].bar(
            series1.index,
            series1,
            width = 1,
            align = 'edge',
            color = color1,
            edgecolor = edge_color1,
            linewidth = 0.2
            )
    ax[0].set_title(
        subplot1_title,
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
        loc = "left"
        )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_box_aspect(1)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    # Autoscale and get max y for setting equiv y scale at end of function.
    ax[0].autoscale(axis = "y")
    ax[0].margins(x = 0, tight = True)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for remaining suboplots.

    if  max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2, color2,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[1].bar(series2.index,
                  series2,
                  width = 1,
                  align = 'edge',
                  color = color2,
                  edgecolor = edge_color2,
                  linewidth = 0.2
                  )
    ax[1].set_title(
            subplot2_title,
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
            loc = "left"
            )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis = "y")
    ax[1].margins(x = 0, tight = True)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.index,
            series3,
            color3,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[2].bar(
            series3.index,
            series3,
            width = 1,
            align = 'edge',
            color = color3,
            edgecolor = edge_color3,
            linewidth = 0.2
            )
    ax[2].set_title(
        subplot3_title,
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
        loc = "left"
        )
    ax[2].yaxis.grid(True)
    ax[2].set_xlabel("Year")
    ax[2].set_box_aspect(1)
    ax[2].set_axisbelow(True)
    ax[2].autoscale(axis = "y")
    ax[2].margins(x = 0, tight = True)
    ylim3 = ax[2].get_ylim()[1]

    if max(series4) == 0:
        ax[3].plot(
            series3.index,
            series4,
            color4,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[3].bar(
            series4.index,
            series4,
            width = 1,
            align = 'edge',
            color = color4,
            edgecolor = edge_color4,
            linewidth = 0.2
            )
    ax[3].set_title(
            subplot4_title,
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value,
            loc = "left"
            )
    ax[3].set_xlabel("Year")
    ax[3].yaxis.grid(True)
    ax[3].set_box_aspect(1)
    ax[3].set_axisbelow(True)
    ax[3].autoscale(axis = "y")
    ax[3].margins(x = 0, tight = True)
    ylim4 = ax[3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)
        ax[3].set_ylim(0, y_max)

    # Move subplots up on page to provide space for footer text.
    plt.subplots_adjust(bottom=0.13)


###############################################################################
#
# Function: column_2x3()
#
# Description:
# 2x3 column subplots with optional equivalent y scale
#
###############################################################################
def column_2x3(
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        ylabel,
        footer_text,
        equiv_yscale
        ):

    # Grey edges for black columns.
    if color1 == "black":
        edge_color1 = "dimgrey"
    else:
        edge_color1 = "black"
    if color2 == "black":
        edge_color2 = "dimgrey"
    else:
        edge_color2 = "black"
    if color3 == "black":
        edge_color3 = "dimgrey"
    else:
        edge_color3 = "black"
    if color4 == "black":
        edge_color4 = "dimgrey"
    else:
        edge_color4 = "black"
    if color5 == "black":
        edge_color5 = "dimgrey"
    else:
        edge_color5 = "black"
    if color6 == "black":
        edge_color6 = "dimgrey"
    else:
        edge_color6 = "black"

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(2, 3, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.925,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )

    # Add comma thousands seperator.
    ax[0, 0].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 1].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 2].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 0].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 1].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 2].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))

    if  max(series1) == 0:
        ax[0, 0].plot(
            series1.index,
            series1,
            color1,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0, 0].bar(
            series1.index,
            series1,
            width = 1,
            align = 'edge',
            color = color1,
            edgecolor = edge_color1,
            linewidth = 0.2,
            )
    ax[0, 0].set_axisbelow(True)
    ax[0, 0].set_title(
            subplot1_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].margins(x = 0, tight = True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis = "y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if  max(series2) == 0:
      ax[0, 1].plot(
          series2.index,
          series2,
          color2,
          linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
          )
    else:
        ax[0, 1].bar(
            series2.index,
            series2,
            align = 'edge',
            width = 1,
            color = color2,
            edgecolor = edge_color2,
            linewidth = 0.2
            )
    ax[0, 1].set_axisbelow(True)
    ax[0, 1].set_title(
            subplot2_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].margins(x = 0, tight = True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis = "y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if  max(series3) == 0:
        ax[0, 2].plot(
            series3.index,
            series3,
            color3,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0, 2].bar(
            series3.index,
            series3,
            width = 1,
            align = 'edge',
            color = color3,
            edgecolor = edge_color3,
            linewidth = 0.2
            )
    ax[0, 2].set_axisbelow(True)
    ax[0, 2].set_title(
            subplot3_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].margins(x = 0, tight = True)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis = "y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if  max(series4) == 0:
        ax[1, 0].plot(
            series4.index,
            series4, color4,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 0].bar(
            series4.index,
            series4,
            width = 1,
            align = 'edge',
            color = color4,
            edgecolor = edge_color4,
            linewidth = 0.2
            )
    ax[1, 0].set_axisbelow(True)
    ax[1, 0].set_title(
        subplot4_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].margins(x = 0, tight = True)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis = "y")
    ylim4 = ax[1, 0].get_ylim()[1]

    if  max(series5) == 0:
        ax[1, 1].plot(
            series5.index,
            series5,
            color5,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 1].bar(
            series5.index,
            series5,
            width = 1,
            align = 'edge',
            color = color5,
            edgecolor = edge_color5,
            linewidth = 0.2
            )
    ax[1, 1].set_axisbelow(True)
    ax[1, 1].set_title(
        subplot5_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].margins(x = 0, tight = True)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis = "y")
    ylim5 = ax[1, 1].get_ylim()[1]

    if  max(series6) == 0:
        ax[1, 2].plot(
            series6.index,
            series6,
            color6,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 2].bar(
            series6.index,
            series6,
            width = 1,
            align = 'edge',
            color = color6,
            edgecolor = edge_color6,
            linewidth = 0.2
            )
    ax[1, 2].set_axisbelow(True)
    ax[1, 2].set_title(
        subplot6_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].margins(x = 0, tight = True)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis = "y")
    ylim6 = ax[1, 2].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)

    plt.subplots_adjust(bottom=0.13)


###############################################################################
#
# Function: column_2x4()
#
# Description:
# 2x4 column subplots with optional equivalent y scale
#
###############################################################################
def column_2x4(
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        series8,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        color7,
        color8,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        subplot7_title,
        subplot8_title,
        ylabel,
        footer_text,
        equiv_yscale
        ):

    # Grey edges for black columns.
    if color1 == "black":
        edge_color1 = "dimgrey"
    else:
        edge_color1 = "black"
    if color2 == "black":
        edge_color2 = "dimgrey"
    else:
        edge_color2 = "black"
    if color3 == "black":
        edge_color3 = "dimgrey"
    else:
        edge_color3 = "black"
    if color4 == "black":
        edge_color4 = "dimgrey"
    else:
        edge_color4 = "black"
    if color5 == "black":
        edge_color5 = "dimgrey"
    else:
        edge_color5 = "black"
    if color6 == "black":
        edge_color6 = "dimgrey"
    else:
        edge_color6 = "black"
    if color7 == "black":
        edge_color7 = "dimgrey"
    else:
        edge_color7 = "black"
    if color8 == "black":
        edge_color8 = "dimgrey"
    else:
        edge_color8 = "black"

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(2, 4, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X4.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X4.value))

    plt.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.925,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    fig.text(
        0.125,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )

    # Add comma thousands seperator.
    ax[0, 0].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 1].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 2].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 3].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 0].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 1].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[1, 2].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax[0, 3].yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))

    if  max(series1) == 0:
        ax[0, 0].plot(
            series1.index,
            series1,
            color1,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0, 0].bar(
            series1.index,
            series1,
            width = 1,
            align = 'edge',
            color = color1,
            edgecolor = edge_color1,
            linewidth = 0.2,
            )
    ax[0, 0].set_axisbelow(True)
    ax[0, 0].set_title(
            subplot1_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].margins(x = 0, tight = True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis = "y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if  max(series2) == 0:
      ax[0, 1].plot(
          series2.index,
          series2,
          color2,
          linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
          )
    else:
        ax[0, 1].bar(
            series2.index,
            series2,
            align = 'edge',
            width = 1,
            color = color2,
            edgecolor = edge_color2,
            linewidth = 0.2
            )
    ax[0, 1].set_axisbelow(True)
    ax[0, 1].set_title(
            subplot2_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].margins(x = 0, tight = True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis = "y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if  max(series3) == 0:
        ax[0, 2].plot(
            series3.index,
            series3,
            color3,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0, 2].bar(
            series3.index,
            series3,
            width = 1,
            align = 'edge',
            color = color3,
            edgecolor = edge_color3,
            linewidth = 0.2
            )
    ax[0, 2].set_axisbelow(True)
    ax[0, 2].set_title(
            subplot3_title,
            loc = "left",
            weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
            )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].margins(x = 0, tight = True)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis = "y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if  max(series4) == 0:
        ax[0, 3].plot(
            series4.index,
            series4, color4,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[0, 3].bar(
            series4.index,
            series4,
            width = 1,
            align = 'edge',
            color = color4,
            edgecolor = edge_color4,
            linewidth = 0.2
            )
    ax[0, 3].set_axisbelow(True)
    ax[0, 3].set_title(
        subplot4_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[0, 3].set_xlabel("Year")
    ax[0, 3].yaxis.grid(True)
    ax[0, 3].set_xticks(x_ticks)
    ax[0, 3].margins(x = 0, tight = True)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis = "y")
    ylim4 = ax[0, 3].get_ylim()[1]

    if  max(series5) == 0:
        ax[1, 0].plot(
            series5.index,
            series5,
            color5,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 0].bar(
            series5.index,
            series5,
            width = 1,
            align = 'edge',
            color = color5,
            edgecolor = edge_color5,
            linewidth = 0.2
            )
    ax[1, 0].set_axisbelow(True)
    ax[1, 0].set_title(
        subplot5_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].margins(x = 0, tight = True)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis = "y")
    ylim5 = ax[1, 0].get_ylim()[1]

    if  max(series6) == 0:
        ax[1, 1].plot(
            series6.index,
            series6,
            color6,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 1].bar(
            series6.index,
            series6,
            width = 1,
            align = 'edge',
            color = color6,
            edgecolor = edge_color6,
            linewidth = 0.2
            )
    ax[1, 1].set_axisbelow(True)
    ax[1, 1].set_title(
        subplot6_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].margins(x = 0, tight = True)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis = "y")
    ylim6 = ax[1, 1].get_ylim()[1]

    if  max(series7) == 0:
        ax[1, 2].plot(
            series7.index,
            series7,
            color6,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 2].bar(
            series7.index,
            series7,
            width = 1,
            align = 'edge',
            color = color7,
            edgecolor = edge_color7,
            linewidth = 0.2
            )
    ax[1, 2].set_axisbelow(True)
    ax[1, 2].set_title(
        subplot6_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].margins(x = 0, tight = True)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis = "y")
    ylim7 = ax[1, 2].get_ylim()[1]

    if  max(series8) == 0:
        ax[1, 3].plot(
            series8.index,
            series8,
            color6,
            linewidth = user_globals.Constant.LINE_WIDTH_SUBPOLT.value
            )
    else:
        ax[1, 3].bar(
            series8.index,
            series8,
            width = 1,
            align = 'edge',
            color = color8,
            edgecolor = edge_color8,
            linewidth = 0.2
            )
    ax[1, 3].set_axisbelow(True)
    ax[1, 3].set_title(
        subplot6_title,
        loc = "left",
        weight = user_globals.Constant.TITLE_FONT_WEIGHT.value
        )
    ax[1, 3].set_xlabel("Year")
    ax[1, 3].yaxis.grid(True)
    ax[1, 3].set_xticks(x_ticks)
    ax[1, 3].margins(x = 0, tight = True)
    ax[1, 3].set_box_aspect(1)
    ax[1, 3].autoscale(axis = "y")
    ylim8 = ax[1, 3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6, ylim7, ylim8)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)
        ax[1, 3].set_ylim(0, y_max)

    plt.subplots_adjust(bottom=0.13)


###############################################################################
#
# Function: column_grouped()
#
# Description:
# Single figure plot of grouped columns. Plotted values are input as a variable
# number of series and matching colors.
#
###############################################################################
def column_grouped(
        country_name,
        title,
        y_label,
        footer_text,
        start_yr,
        *colors,
        **series
        ):

    # Create figure and axes.
    fig, ax = plt.subplots(1, 1, figsize =
                  (user_globals.Constant.FIG_HSIZE_GROUPED_COLUMN_PLOT.value,
                   user_globals.Constant.FIG_VSIZE_GROUPED_COLUMN_PLOT.value))
    label_pad = 2
    series_qty = (len(series))
    column_width = 1 / series_qty
    multiplier = 0
    offset = column_width * multiplier
    plot_names = []

    # Cycle through and plot input series.
    for key, value in series.items():
        series = value
        offset = column_width * multiplier
        p = ax.bar(
            series.truncate(before = start_yr).index.astype("float") + offset,
            series.truncate(before = start_yr),
            width = column_width * 0.9,
            color = colors[multiplier],
            edgecolor = "black",
            linewidth = 0.4
            )
        # Disable displaying of zero labels on top of columns.
        labels = [round(v.get_height()) if v.get_height() > 1 or
                  v.get_height() < -1 else "" for v in p]
        ax.bar_label(p, labels = labels, fmt = "%.0f", padding = label_pad)
        # Extract fuel names from each sataframe, for use in chart legend.
        plot_names.append(series.name.replace(" Change", ""))
        multiplier += 1

    # Derive list of x_ticks from first dataframe and fill with start of each
    # decade.
    x_ticks_major = []
    end_yr = series.index[-1]
    for year in range(start_yr, end_yr):
        if year % 5 == 0: # Modulus.
            x_ticks_major.append(year)
    # Replace final value with most recent year.
    x_ticks_major[len(x_ticks_major) - 1] = end_yr

    # Align major ticks, minor ticks and grid with left hand edge of columns.
    ax.set_xticks(np.array(x_ticks_major) - column_width / 2,
                  labels = x_ticks_major)
    ax.xaxis.grid(True, which="major", alpha = 1)
    ax.xaxis.grid(True, which="minor", alpha = 0.5)
    ax.set_xticks(np.arange(start_yr - column_width / 2,
                            (end_yr - column_width / 2), 1), minor = True)

    plt.tight_layout(pad = 6)
    # Figure text.
    fig.suptitle(
        country_name,
        x = 0.065,
        y = 0.96,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value
        )
    # Text beneath figure title.
    fig.text(
        0.065,
        0.915,
        title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value
        )
    # Text in footer.
    fig.text(
        0.065,
        0.005,
        footer_text,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value
        )
    ax.autoscale(axis = "y")
    ax.set_ylabel(y_label)
    ax.yaxis.grid(False)
    ax.set_xlabel("Year")
    ax.legend(
        plot_names,
        loc = "best",
        frameon = False,
        handlelength = 2,
        ncol = 6,
        fontsize = "large"
        )
    # Show x axis line.
    plt.axhline(0, color="black", lw = 0.4)

    # Insert space at bottom of plot.
    plt.subplots_adjust(bottom=0.15)

    plt.margins(x = 0, tight = True)


###############################################################################
#
# Function: treemap()
#
# Description:
# 1x2 treemap subplots.
#
###############################################################################
def treemap(
        df1, # Dataframe 1
        df2, # Dataframe 2
        subplot1_title, # Title above LH plot
        subplot2_title, # Title above RH plot
        country_name,
        title,
        footer_text
        ):

    fig, ax = plt.subplots(1, 2, figsize = (
                           user_globals.Constant.FIG_HSIZE_TREE_1X2.value,
                           user_globals.Constant.FIG_VSIZE_TREE_1X2.value),
                           subplot_kw = dict(aspect = 1.1))

    # Plot lefthand treemap.
    tr.treemap(
        ax[0],
        df1,
        area = "Value",
        labels ="Label",
        cmap = df1["Color"].to_list(),
        fill = "Name",
        rectprops = dict(ec = "#eeeeee", lw = 1),
        textprops = dict(c = "white",
                         place = "top left",
                         reflow = True,
                         max_fontsize = 80)
        )
    ax[0].legend(
        df1["Name"],
        loc = "upper left", bbox_to_anchor=(0, 0),
        frameon = False,
        handlelength = 2,
        ncol = 2,
        fontsize = "large"
        )
    ax[0].axis("off")
    ax[0].set_title(subplot1_title, fontsize = "large",
                    fontweight = "demibold", loc = 'left')

    # Plot righthand treemap.
    tr.treemap(ax[1],
               df2,
               area = "Value",
               labels ="Label",
               cmap = df2["Color"].to_list(),
               fill = "Name",
               rectprops = dict(ec = "#eeeeee", lw = 1),
               textprops = dict(
                   c = "white",
                   place = "top left",
                   reflow = True,
                   max_fontsize = 50)
               )
    ax[1].legend(
        df2["Name"],
        loc = "upper left", bbox_to_anchor = (0, 0),
        frameon = False,
        handlelength = 2,
        ncol = 3,
        fontsize = "large"
        )
    ax[1].axis("off")
    ax[1].set_title(subplot2_title, fontsize = "large",
                    fontweight = "demibold", loc = 'left')
    fig.suptitle(country_name, x = 0.125, y = 0.98,
             horizontalalignment = "left",
             fontsize = user_globals.Constant.SUPTITLE_FONT_SIZE.value,
             fontweight = user_globals.Constant.SUPTITLE_FONT_WEIGHT.value)
    fig.text(0.125, 0.93, title,
        horizontalalignment = "left",
        fontsize = user_globals.Constant.SUPTITLE_ADDITION_FONT_SIZE.value,
        fontweight = user_globals.Constant.SUPTITLE_ADDITION_FONT_WEIGHT.value)
    fig.text(0.125, 0, footer_text,
             horizontalalignment = "left",
             fontsize = user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
             fontweight = user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value)
    plt.subplots_adjust(bottom=0.19)

