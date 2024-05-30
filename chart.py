#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################
#
# Module: chart.py
#
# Description:
# Generic chart drawing functions.
#
########################################################################################

# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np
import mpl_extra.treemap as tr

# Location:
# https://github.com/chenyulue/matplotlib-extra
# Install command:
# pip3 install git+https://github.com/chenyulue/matplotlib-extra/
import matplotlib.ticker

# Import user modules.
import user_globals


# 1x charts.
########################################################################################
#
# Function: line1x1()
#
# Description:
# Plots a single series.
#
########################################################################################


def line1x1(x, y, country, color, title, ylabel, footer_text):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_1x1.value,
            user_globals.Constant.FIG_VSIZE_1x1.value,
        ),
    )
    ax.plot(
        x,
        y,
        color,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker=".",
        markersize=6,
        markerfacecolor="white",
        markeredgecolor="black",
        markeredgewidth=0.3,
    )
    # Set aspect ratio 1:1.
    ax.set_box_aspect(1)

    # Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in x:
        if year % 10 == 0:  # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(x)
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Year")

    # Add comma as thousand seperator.
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax.autoscale(axis="y")
    ax.set_ylim(0, max(ax.get_yticks()))
    ax.set_ylabel(ylabel)

    plt.subplots_adjust(left=0.06, right=1, top=0.89, bottom=0.13)
    fig.suptitle(
        country,
        x=0.135,
        y=0.945,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.135,
        0.9,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.135,
        0.005,
        footer_text,
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


###############################################################################
#
# Function: column1x1()
#
# Description:
# 1x1 column plot.
#
###############################################################################


def column1x1(
    series,
    color,
    country,
    title,
    x_axis_interval,
    ylabel,
    footer_text,
):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_VSIZE_1x1.value,
            user_globals.Constant.FIG_VSIZE_1x1.value,
        ),
    )
    if color == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"
    # if nil data remove y-axis detail, else plot bar chart
    if max(series) == 0:
        ax.plot(
            series.index,
            series,
            color,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax.bar(
            series.index,
            series,
            width=1,
            align="edge",
            color=color,
            edgecolor=edge_color,
            linewidth=0.2,
        )
    ax.set_box_aspect(1)
    # grid behind columns
    ax.set_axisbelow(True)

    # x_ticks only for start of each decade
    x_ticks = []
    for year in series.index:
        if year % x_axis_interval == 0:  # modulus
            x_ticks.append(year)
    # Include most recent year. If period between ticks is >= 25 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis_interval >= 25:
        x_ticks.append(max(series.index))
    else:
        x_ticks[len(x_ticks) - 1] = max(series.index)
    ax.set_xticks(x_ticks)
    ax.set_xlabel("Year")
    # remove margins
    ax.margins(x=0, tight=True)

    ax.autoscale(axis="y")
    # force uppermost y-tick to be equal to autoscale max + grid interval
    ax.set_ylim(0, max(ax.get_yticks()))
    # add comma thousands seperator
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax.yaxis.grid(True)
    ax.set_ylabel(ylabel)

    plt.subplots_adjust(left=0.03, right=1, top=0.89, bottom=0.13)
    fig.suptitle(
        country,
        x=0.135,
        y=0.95,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.135,
        0.905,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.135,
        0.075,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


###############################################################################
#
# Function: column1x2()
#
# Description:
# 1x2 column subplots.
#
###############################################################################


def column1x2(
    series1,
    series2,
    color1,
    color2,
    country,
    title,
    subplot1_title,
    subplot2_title,
    x_axis1_interval,
    x_axis2_interval,
    ylabels,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_1X2.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_1X2.value,
        ),
    )

    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    # Grey edges for black columns.
    if color1 == "black":
        edge_color1 = "dimgrey"
    else:
        edge_color1 = "black"
    if color2 == "black":
        edge_color2 = "dimgrey"
    else:
        edge_color2 = "black"

    x_ticks1 = []
    x_ticks2 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series1.index:
        if year % x_axis1_interval == 0:  # Modulus.
            x_ticks1.append(year)
    for year in series2.index:
        if year % x_axis2_interval == 0:
            x_ticks2.append(year)

    # Include most recent year. If period between ticks is >= 25 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis1_interval >= 25:
        x_ticks1.append(max(series1.index))
    else:
        x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    if x_axis2_interval >= 25:
        x_ticks2.append(max(series2.index))
    else:
        x_ticks2[len(x_ticks2) - 1] = max(series2.index)
    ax[0].set_xticks(x_ticks1)
    ax[1].set_xticks(x_ticks2)

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0].bar(
            series1.index,
            series1,
            width=1,
            align="edge",
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    ax[0].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_box_aspect(1)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    # Autoscale and get max y for setting equiv y scale at end of function.
    ax[0].autoscale(axis="y")
    # Remove margins.
    ax[0].margins(x=0, tight=True)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for second suboplot.
    if max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1].bar(
            series2.index,
            series2,
            width=1,
            align="edge",
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    ax[1].set_title(
        subplot2_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis="y")
    ax[1].margins(x=0, tight=True)
    ylim2 = ax[1].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
    # Force uppermost tick to be equal to autoscale max + grid interval
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    plt.subplots_adjust(left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02)
    fig.suptitle(
        country,
        x=0.18,
        y=0.975,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.925,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: line_column1x2()
#
# Description:
# Column chart on the left, line chart on the right.
#
########################################################################################


def line_column1x2(
    series1,
    series2,
    color1,
    color2,
    country,
    title,
    subplot1_title,
    subplot2_title,
    x_axis1_interval,
    x_axis2_interval,
    ylabel1,
    ylabel2,
    chart_text,
    footer_text,
):
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_1X2.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_1X2.value,
        ),
    )

    # Grey edges for black columns.
    if color2 == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"

    x_ticks1 = []
    x_ticks2 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series1.index:
        if year % x_axis1_interval == 0:  # Modulus.
            x_ticks1.append(year)
    for year in series2.index:
        if year % x_axis2_interval == 0:
            x_ticks2.append(year)

    # Include most recent year. If period between ticks is >= 25 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis1_interval >= 25:
        x_ticks1.append(max(series1.index))
    else:
        x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    if x_axis2_interval >= 25:
        x_ticks2.append(max(series2.index))
    else:
        x_ticks2[len(x_ticks2) - 1] = max(series2.index)
    ax[0].set_xticks(x_ticks1)
    ax[1].set_xticks(x_ticks2)

    # Subplot 1. Line chart.
    ax[0].plot(
        series1.index,
        series1,
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker=".",
        markersize=6,
        markerfacecolor="white",
        markeredgecolor="black",
        markeredgewidth=0.3,
    )
    ax[0].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    # Set aspect ratio 1:1.
    ax[0].set_box_aspect(1)
    ax[0].set_xlabel("Year")
    ax[0].autoscale(axis="y")
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[0].set_ylabel(ylabel1)
    # Add text to chart
    ax[0].text(2005, 425, chart_text)
    # Subplot 2
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[1].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        p = ax[1].bar(
            series2.index,
            series2,
            width=1,
            color=color2,
            edgecolor=edge_color,
            linewidth=0.2,
        )
    ax[1].bar_label(p, fmt="%.1f", padding=2)

    ax[1].set_title(
        subplot2_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[1].set_xlabel("Year")
    ax[1].set_ylabel(ylabel2)
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    # Place grid behind columns.
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis="y")
    # Remove margins.
    ax[1].margins(x=0, tight=True)

    # Force uppermost tick to be equal to autoscale max + grid interval
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    plt.subplots_adjust(left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02)
    fig.suptitle(
        country,
        x=0.18,
        y=0.975,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.925,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column1x3()
#
# Description:
# 1x3 column subplots.
#
########################################################################################


def column1x3(
    series1,
    series2,
    series3,
    color1,
    color2,
    color3,
    country,
    title,
    subplot1_title,
    subplot2_title,
    subplot3_title,
    x_axis_interval,
    ylabels,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        3,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_1X3.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_1X3.value,
        ),
    )

    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

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

    x_ticks1 = []
    x_ticks2 = []
    x_ticks3 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series1.index:
        if year % x_axis_interval == 0:  # Modulus.
            x_ticks1.append(year)
    for year in series2.index:
        if year % x_axis_interval == 0:
            x_ticks2.append(year)
    for year in series3.index:
        if year % x_axis_interval == 0:
            x_ticks3.append(year)
    # Include most recent year. If period between ticks is >= 25 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis_interval >= 25:
        x_ticks1.append(max(series1.index))
        x_ticks2.append(max(series2.index))
        x_ticks3.append(max(series3.index))
    else:
        x_ticks1[len(x_ticks1) - 1] = max(series1.index)
        x_ticks2[len(x_ticks2) - 1] = max(series2.index)
        x_ticks3[len(x_ticks3) - 1] = max(series3.index)
    ax[0].set_xticks(x_ticks1)
    ax[1].set_xticks(x_ticks2)
    ax[2].set_xticks(x_ticks3)

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0].bar(
            series1.index,
            series1,
            width=1,
            align="edge",
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    ax[0].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_box_aspect(1)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    # Autoscale and get max y for setting equiv y scale at end of function.
    ax[0].autoscale(axis="y")
    # Remove margins.
    ax[0].margins(x=0, tight=True)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for second and third suboplots.
    if max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1].bar(
            series2.index,
            series2,
            width=1,
            align="edge",
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    ax[1].set_title(
        subplot2_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis="y")
    ax[1].margins(x=0, tight=True)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.index,
            series3,
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[2].bar(
            series3.index,
            series3,
            width=1,
            align="edge",
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    ax[2].set_title(
        subplot3_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[2].set_xlabel("Year")
    ax[2].yaxis.grid(True)
    ax[2].set_box_aspect(1)
    ax[2].set_axisbelow(True)
    ax[2].autoscale(axis="y")
    ax[2].margins(x=0, tight=True)
    ylim3 = ax[2].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)
    # Force uppermost tick to be equal to autoscale max + grid interval
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))
    ax[2].set_ylim(0, max(ax[2].get_yticks()))

    plt.subplots_adjust(left=0.06, right=0.97, wspace=0.115, top=1, bottom=0)
    fig.suptitle(
        country,
        x=0.06,
        y=0.96,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.06,
        0.9,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.06,
        0.09,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: line1x4()
#
# Description:
# 1x4 line subplots.
#
########################################################################################


def line1x4(
    series1,
    series2,
    series3,
    series4,
    color1,
    color2,
    color3,
    color4,
    country,
    title,
    subplot1_title,
    subplot2_title,
    subplot3_title,
    subplot4_title,
    ylabel,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        4,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_1X4.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_1X4.value,
        ),
    )
    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    ax[0].plot(
        series1.index,
        series1,
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabel)
    ax[0].yaxis.grid(True)
    ax[0].margins(x=0, tight=True)
    ax[0].set_xticks(x_ticks)
    ax[0].set_box_aspect(1)
    ax[0].autoscale(axis="y")
    ylim1 = ax[0].get_ylim()[1]

    ax[1].plot(
        series2.index,
        series2,
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].margins(x=0, tight=True)
    ax[1].set_xticks(x_ticks)
    ax[1].set_box_aspect(1)
    ax[1].autoscale(axis="y")
    ylim2 = ax[1].get_ylim()[1]

    ax[2].plot(
        series3.index,
        series3,
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[2].set_xlabel("Year")
    ax[2].yaxis.grid(True)
    ax[2].margins(x=0, tight=True)
    ax[2].set_xticks(x_ticks)
    ax[2].set_box_aspect(1)
    ax[2].autoscale(axis="y")
    ylim3 = ax[2].get_ylim()[1]

    ax[3].plot(
        series4.index,
        series4,
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[3].set_xlabel("Year")
    ax[3].yaxis.grid(True)
    ax[3].margins(x=0, tight=True)
    ax[3].set_xticks(x_ticks)
    ax[3].set_box_aspect(1)
    ax[3].autoscale(axis="y")
    ylim4 = ax[3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)
        ax[3].set_ylim(0, y_max)
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0].set_ylim(0, max(ax[0].get_yticks()))
        ax[1].set_ylim(0, max(ax[1].get_yticks()))
        ax[2].set_ylim(0, max(ax[2].get_yticks()))
        ax[3].set_ylim(0, max(ax[3].get_yticks()))

    plt.subplots_adjust(left=0.05, right=0.97, wspace=0.09, top=0.94, bottom=0.09)
    fig.suptitle(
        country,
        x=0.05,
        y=0.965,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.9,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.11,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column1x4()
#
# Description:
# 1x4 column subplots.
#
########################################################################################


def column1x4(
    series1,
    series2,
    series3,
    series4,
    color1,
    color2,
    color3,
    color4,
    country,
    title,
    subplot1_title,
    subplot2_title,
    subplot3_title,
    subplot4_title,
    ylabels,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        4,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_1X4.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_1X4.value,
        ),
    )

    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[3].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

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
        if year % 10 == 0:  # Modulus.
            x_ticks1.append(year)
    # Replace final value with most recent year.
    x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    ax[0].set_xticks(x_ticks1)
    for year in series2.index:
        if year % 10 == 0:  # Modulus.
            x_ticks2.append(year)
    # Replace final value with most recent year.
    x_ticks2[len(x_ticks2) - 1] = max(series2.index)
    ax[1].set_xticks(x_ticks2)
    for year in series3.index:
        if year % 10 == 0:  # Modulus.
            x_ticks3.append(year)
    # Replace final value with most recent year.
    x_ticks3[len(x_ticks3) - 1] = max(series3.index)
    ax[2].set_xticks(x_ticks3)
    for year in series4.index:
        if year % 10 == 0:  # Modulus.
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
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0].bar(
            series1.index,
            series1,
            width=1,
            align="edge",
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    ax[0].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_box_aspect(1)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    # Autoscale and get max y for setting equiv y scale at end of function.
    ax[0].autoscale(axis="y")
    ax[0].tick_params(labelsize=8)
    ax[0].margins(x=0, tight=True)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for remaining suboplots.
    if max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1].bar(
            series2.index,
            series2,
            width=1,
            align="edge",
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    ax[1].set_title(
        subplot2_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].set_box_aspect(1)
    ax[1].set_axisbelow(True)
    ax[1].autoscale(axis="y")
    ax[1].tick_params(labelsize=8)
    ax[1].margins(x=0, tight=True)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.index,
            series3,
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[2].bar(
            series3.index,
            series3,
            width=1,
            align="edge",
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    ax[2].set_title(
        subplot3_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[2].yaxis.grid(True)
    ax[2].set_xlabel("Year")
    ax[2].set_box_aspect(1)
    ax[2].set_axisbelow(True)
    ax[2].autoscale(axis="y")
    ax[2].tick_params(labelsize=8)
    ax[2].margins(x=0, tight=True)
    ylim3 = ax[2].get_ylim()[1]

    if max(series4) == 0:
        ax[3].plot(
            series3.index,
            series4,
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[3].bar(
            series4.index,
            series4,
            width=1,
            align="edge",
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    ax[3].set_title(
        subplot4_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax[3].set_xlabel("Year")
    ax[3].yaxis.grid(True)
    ax[3].set_box_aspect(1)
    ax[3].set_axisbelow(True)
    ax[3].autoscale(axis="y")
    ax[3].tick_params(labelsize=8)
    ax[3].margins(x=0, tight=True)
    ylim4 = ax[3].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
        ax[2].set_ylim(0, y_max)
        ax[3].set_ylim(0, y_max)
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0].set_ylim(0, max(ax[0].get_yticks()))
        ax[1].set_ylim(0, max(ax[1].get_yticks()))
        ax[2].set_ylim(0, max(ax[2].get_yticks()))
        ax[3].set_ylim(0, max(ax[3].get_yticks()))

    plt.subplots_adjust(left=0.06, right=0.97, wspace=0.14, top=1, bottom=0)
    # Figure title.
    fig.suptitle(
        country,
        x=0.06,
        y=0.935,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    # Text beneath figure title.
    fig.text(
        0.06,
        0.87,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    # Text in footer.
    fig.text(
        0.06,
        0.11,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


# 2x charts.
########################################################################################
#
# Function: line2x3()
#
# Description:
# 2x3 line subplots.
#
########################################################################################
def line2x3(
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
    country,
    title,
    subplot1_title,
    subplot2_title,
    subplot3_title,
    subplot4_title,
    subplot5_title,
    subplot6_title,
    ylabel,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        2,
        3,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    ax[0, 0].plot(
        series1.index,
        series1,
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.index,
        series2,
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.index,
        series3,
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].margins(x=0, tight=True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[1, 0].plot(
        series4.index,
        series4,
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 0].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].margins(x=0, tight=True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim4 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series5.index,
        series5,
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 1].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].margins(x=0, tight=True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim5 = ax[1, 1].get_ylim()[1]

    ax[1, 2].plot(
        series6.index,
        series6,
        color6,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 2].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].margins(x=0, tight=True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
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
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))

    plt.subplots_adjust(
        left=0.125, right=0.9, hspace=0.14, wspace=0, top=0.91, bottom=0.125
    )
    fig.suptitle(
        country,
        x=0.145,
        y=0.975,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.145,
        0.94,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.145,
        0.075,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column2x3()
#
# Description:
# 2x3 column subplots with optional equivalent y scale
#
########################################################################################


def column2x3(
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
    country,
    title,
    subplot1_title,
    subplot2_title,
    subplot3_title,
    subplot4_title,
    subplot5_title,
    subplot6_title,
    ylabel,
    footer_text,
    equiv_yscale,
):
    fig, ax = plt.subplots(
        2,
        3,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

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

    # Add comma thousands seperator.
    ax[0, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[0, 1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[0, 2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    if max(series1) == 0:
        ax[0, 0].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 0].bar(
            series1.index,
            series1,
            width=1,
            align="edge",
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    ax[0, 0].set_axisbelow(True)
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if max(series2) == 0:
        ax[0, 1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 1].bar(
            series2.index,
            series2,
            align="edge",
            width=1,
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    ax[0, 1].set_axisbelow(True)
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if max(series3) == 0:
        ax[0, 2].plot(
            series3.index,
            series3,
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 2].bar(
            series3.index,
            series3,
            width=1,
            align="edge",
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    ax[0, 2].set_axisbelow(True)
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].margins(x=0, tight=True)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if max(series4) == 0:
        ax[1, 0].plot(
            series4.index,
            series4,
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 0].bar(
            series4.index,
            series4,
            width=1,
            align="edge",
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    ax[1, 0].set_axisbelow(True)
    ax[1, 0].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].margins(x=0, tight=True)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim4 = ax[1, 0].get_ylim()[1]

    if max(series5) == 0:
        ax[1, 1].plot(
            series5.index,
            series5,
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 1].bar(
            series5.index,
            series5,
            width=1,
            align="edge",
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
    ax[1, 1].set_axisbelow(True)
    ax[1, 1].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].margins(x=0, tight=True)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim5 = ax[1, 1].get_ylim()[1]

    if max(series6) == 0:
        ax[1, 2].plot(
            series6.index,
            series6,
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 2].bar(
            series6.index,
            series6,
            width=1,
            align="edge",
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
    ax[1, 2].set_axisbelow(True)
    ax[1, 2].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].margins(x=0, tight=True)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
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
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))

    plt.subplots_adjust(
        left=0.125, right=0.9, hspace=0.125, wspace=0, top=0.91, bottom=0.125
    )
    fig.suptitle(
        country,
        x=0.145,
        y=0.975,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.145,
        0.94,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.145,
        0.075,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: line2x4()
#
# Description:
# 2x4 line subplots.
#
########################################################################################


def line2x4(
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
    country,
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
    equiv_yscale,
):

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

    fig, ax = plt.subplots(
        2,
        4,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_2X4.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_2X4.value,
        ),
    )

    ax[0, 0].plot(
        series1.index,
        series1,
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.index,
        series2,
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.index,
        series3,
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].margins(x=0, tight=True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[0, 3].plot(
        series4.index,
        series4,
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[0, 3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 3].margins(x=0, tight=True)
    ax[0, 3].set_xticks(x_ticks)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    ax[1, 0].plot(
        series5.index,
        series5,
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 0].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].margins(x=0, tight=True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series6.index,
        series6,
        color6,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 1].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].margins(x=0, tight=True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    ax[1, 2].plot(
        series7.index,
        series7,
        color7,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 2].set_title(
        subplot7_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].margins(x=0, tight=True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
    ylim7 = ax[1, 2].get_ylim()[1]

    ax[1, 3].plot(
        series8.index,
        series8,
        color8,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
    )
    ax[1, 3].set_title(
        subplot8_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 3].set_xlabel("Year")
    ax[1, 3].margins(x=0, tight=True)
    ax[1, 3].set_xticks(x_ticks)
    ax[1, 3].set_box_aspect(1)
    ax[1, 3].autoscale(axis="y")
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
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))
        ax[1, 3].set_ylim(0, max(ax[1, 3].get_yticks()))

    plt.subplots_adjust(
        left=0.08, right=0.9, wspace=0.1, hspace=0, top=0.9, bottom=0.07
    )
    fig.suptitle(
        country,
        x=0.08,
        y=0.94,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.08,
        0.9,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.08,
        0.05,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column2x4()
#
# Description:
# 2x4 column subplots with optional equivalent y scale
#
########################################################################################


def column2x4(
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
    country,
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
    equiv_yscale,
):
    fig, ax = plt.subplots(
        2,
        4,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SUBPLOT_2X4.value,
            user_globals.Constant.FIG_VSIZE_SUBPLOT_2X4.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in series1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(series1.index)

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

    # Add comma thousands seperator.
    ax[0, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[0, 1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[0, 2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[0, 3].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 3].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    if max(series1) == 0:
        ax[0, 0].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 0].bar(
            series1.index,
            series1,
            width=1,
            align="edge",
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    ax[0, 0].set_axisbelow(True)
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].tick_params(labelsize=8)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if max(series2) == 0:
        ax[0, 1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 1].bar(
            series2.index,
            series2,
            align="edge",
            width=1,
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    ax[0, 1].set_axisbelow(True)
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].tick_params(labelsize=8)
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if max(series3) == 0:
        ax[0, 2].plot(
            series3.index,
            series3,
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 2].bar(
            series3.index,
            series3,
            width=1,
            align="edge",
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    ax[0, 2].set_axisbelow(True)
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].tick_params(labelsize=8)
    ax[0, 2].margins(x=0, tight=True)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if max(series4) == 0:
        ax[0, 3].plot(
            series4.index,
            series4,
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[0, 3].bar(
            series4.index,
            series4,
            width=1,
            align="edge",
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    ax[0, 3].set_axisbelow(True)
    ax[0, 3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 3].yaxis.grid(True)
    ax[0, 3].set_xticks(x_ticks)
    ax[0, 3].tick_params(labelsize=8)
    ax[0, 3].margins(x=0, tight=True)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    if max(series5) == 0:
        ax[1, 0].plot(
            series5.index,
            series5,
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 0].bar(
            series5.index,
            series5,
            width=1,
            align="edge",
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
    ax[1, 0].set_axisbelow(True)
    ax[1, 0].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].tick_params(labelsize=8)
    ax[1, 0].margins(x=0, tight=True)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    if max(series6) == 0:
        ax[1, 1].plot(
            series6.index,
            series6,
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 1].bar(
            series6.index,
            series6,
            width=1,
            align="edge",
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
    ax[1, 1].set_axisbelow(True)
    ax[1, 1].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].tick_params(labelsize=8)
    ax[1, 1].margins(x=0, tight=True)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    if max(series7) == 0:
        ax[1, 2].plot(
            series7.index,
            series7,
            color7,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 2].bar(
            series7.index,
            series7,
            width=1,
            align="edge",
            color=color7,
            edgecolor=edge_color7,
            linewidth=0.2,
        )
    ax[1, 2].set_axisbelow(True)
    ax[1, 2].set_title(
        subplot7_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].tick_params(labelsize=8)
    ax[1, 2].margins(x=0, tight=True)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
    ylim7 = ax[1, 2].get_ylim()[1]

    if max(series8) == 0:
        ax[1, 3].plot(
            series8.index,
            series8,
            color8,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPOLT.value,
        )
    else:
        ax[1, 3].bar(
            series8.index,
            series8,
            width=1,
            align="edge",
            color=color8,
            edgecolor=edge_color8,
            linewidth=0.2,
        )
    ax[1, 3].set_axisbelow(True)
    ax[1, 3].set_title(
        subplot8_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 3].set_xlabel("Year")
    ax[1, 3].yaxis.grid(True)
    ax[1, 3].set_xticks(x_ticks)
    ax[1, 3].tick_params(labelsize=8)
    ax[1, 3].margins(x=0, tight=True)
    ax[1, 3].set_box_aspect(1)
    ax[1, 3].autoscale(axis="y")
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
        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))
        ax[1, 3].set_ylim(0, max(ax[1, 3].get_yticks()))

    plt.subplots_adjust(left=0.08, wspace=0.15, top=0.87, bottom=0.12)
    fig.suptitle(
        country,
        x=0.08,
        y=0.95,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.08,
        0.91,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.08,
        0.07,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


# Other charts.
###############################################################################
#
# Function: columngrouped()
#
# Description:
# Single figure plot of grouped columns. Plotted values are input as a variable
# number of series and matching colors.
#
###############################################################################
def columngrouped(country, title, y_label, footer_text, start_yr, *colors, **series):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_GROUPED_COLUMN_PLOT.value,
            user_globals.Constant.FIG_VSIZE_GROUPED_COLUMN_PLOT.value,
        ),
    )

    label_pad = 2
    series_qty = len(series)
    column_width = 1 / series_qty
    series_number = 0
    offset = column_width * series_number
    plot_names = []

    # Cycle through and plot input series.
    for key, value in series.items():
        offset = column_width * series_number
        p = ax.bar(
            value.truncate(before=start_yr).index.astype("float") + offset,
            value.truncate(before=start_yr),
            width=column_width * 0.9,
            color=colors[series_number],
            edgecolor="black",
            linewidth=0.4,
        )
        # Round column value labels and disable displaying of zero.
        labels = [
            (
                round(v.get_height())
                if v.get_height() >= 0.5 or v.get_height() <= -0.5
                else ""
            )
            for v in p
        ]
        ax.bar_label(p, labels=labels, fmt="%.0f", padding=label_pad)
        # Extract fuel names from each dataframe, for use in chart legend.
        plot_names.append(value.name.replace(" Change", ""))
        series_number += 1

    # Derive list of x_ticks from final dataframe and fill with start of each
    # decade.
    x_ticks_major = []
    end_yr = value.index[-1]
    for year in range(start_yr, end_yr):
        if year % 5 == 0:  # Modulus.
            x_ticks_major.append(year)
    # Replace final value with most recent year.
    x_ticks_major[len(x_ticks_major) - 1] = end_yr

    # Align major ticks, minor ticks and grid with left hand edge of set of
    # columns if more than one series being plotted.
    if series_qty > 1:
        ax.set_xticks(np.array(x_ticks_major) - column_width / 2, labels=x_ticks_major)
        ax.set_xticks(
            np.arange(start_yr - column_width / 2, (end_yr - column_width / 2), 1),
            minor=True,
        )
    else:
        ax.set_xticks(np.array(x_ticks_major), labels=x_ticks_major)
        ax.set_xticks(np.arange(start_yr, end_yr, 1), minor=True)

    ax.xaxis.grid(True, which="major", alpha=1)
    ax.xaxis.grid(True, which="minor", alpha=0.5)

    plt.tight_layout(pad=6)
    ax.autoscale(axis="y")
    ax.set_ylim(min(ax.get_yticks()), max(ax.get_yticks()))
    ax.set_ylabel(y_label)
    ax.yaxis.grid(False)
    ax.set_xlabel("Year")
    ax.legend(
        plot_names,
        loc="best",
        frameon=False,
        handlelength=2,
        ncol=6,
        fontsize="large",
    )
    # Show x axis line.
    plt.axhline(0, color="black", lw=0.4)
    plt.margins(x=0, tight=True)

    plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.16)
    fig.suptitle(
        country,
        x=0.05,
        y=0.96,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.92,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.105,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


###############################################################################
#
# Function: treemap1x1()
#
# Description:
# Single treemap plot
#
###############################################################################


def treemap1x1(
    df, subplot_title, country, title, title_addition, footer_text  # Dataframe
):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_TREE_1X1.value,
            user_globals.Constant.FIG_VSIZE_TREE_1X1.value,
        ),
        subplot_kw=dict(aspect=1.1),
    )
    tr.treemap(
        ax,
        df,
        area="Value",
        labels="Label",
        cmap=df["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="darkslategray", lw=0.4),
        textprops=dict(c="white", place="top left", reflow=True, max_fontsize=80),
    )
    ax.legend(
        df["Name"],
        loc="upper left",
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=2,
        fontsize="large",
    )
    ax.axis("off")
    ax.set_title(
        subplot_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    plt.subplots_adjust(left=0.125, top=0.83, bottom=0.22)
    fig.suptitle(
        country,
        x=0.125,
        y=0.96,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.92,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.91,
        title_addition,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.025,
        footer_text,
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


###############################################################################
#
# Function: treemap1x2()
#
# Description:
# 1x2 treemap subplots.
#
###############################################################################


def treemap1x2(
    df1,  # Dataframe 1
    df2,  # Dataframe 2
    subplot1_title,  # Title above LH plot
    subplot2_title,  # Title above RH plot
    country,
    title,
    title_addition,
    footer_text,
):
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(
            user_globals.Constant.FIG_HSIZE_TREE_1X2.value,
            user_globals.Constant.FIG_VSIZE_TREE_1X2.value,
        ),
        subplot_kw=dict(aspect=1.1),
    )

    # Plot lefthand treemap.
    tr.treemap(
        ax[0],
        df1,
        area="Value",
        labels="Label",
        cmap=df1["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="darkslategray", lw=0.4),
        textprops=dict(c="white", place="top left", reflow=True, max_fontsize=80),
    )
    ax[0].legend(
        df1["Name"],
        loc="upper left",
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=2,
        fontsize="large",
    )
    ax[0].axis("off")
    ax[0].set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    # Plot righthand treemap.
    tr.treemap(
        ax[1],
        df2,
        area="Value",
        labels="Label",
        cmap=df2["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="darkslategray", lw=0.4),
        textprops=dict(c="white", place="top left", reflow=True, max_fontsize=50),
    )
    ax[1].legend(
        df2["Name"],
        loc="upper left",
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=3,
        fontsize="large",
    )
    ax[1].axis("off")
    if "Electricity Generation" in subplot2_title:
        ax[1].set_title(
            subplot2_title,
            fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
            fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
            loc="left",
            color="white",
            backgroundcolor="teal",
            position=(0.012, 1.2),
        )
    else:
        ax[1].set_title(
            subplot2_title,
            fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
            fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
            loc="left",
        )

    plt.subplots_adjust(left=0.125, top=0.86, bottom=0.18)
    fig.suptitle(
        country,
        x=0.125,
        y=0.96,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.92,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.91,
        title_addition,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.025,
        footer_text,
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )
