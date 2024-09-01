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


###############################################################################
#
# Function: column_2_subplots()
#
# Description:
# 2 column subplots in 1 row.
#
###############################################################################

def column_2_subplots(
        series1,
        series2,
        color1,
        color2,
        country,
        title,
        subplot1_title,
        subplot2_title,
        start_yr1,
        start_yr2,
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
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
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

    x_ticks1 = [start_yr1]
    x_ticks2 = [start_yr2]

    # x_ticks only for period defined by x_axis_interval
    for year in series1.truncate(before=start_yr1).index:
        if year % x_axis1_interval == 0:  # Modulus.
            x_ticks1.append(year)
    for year in series2.truncate(before=start_yr2).index:
        if year % x_axis2_interval == 0:
            x_ticks2.append(year)

    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks1) >= 3:
        x_ticks1.append(series1.index.max())
    else:
        x_ticks1[len(x_ticks1) - 1] = series1.index.max()

    if series2.index.max() - max(x_ticks2) >= 3:
        x_ticks2.append(series2.index.max())
    else:
        x_ticks2[len(x_ticks2) - 1] = series2.index.max()

    ax[0].set_xticks(x_ticks1, labels=x_ticks1)
    ax[1].set_xticks(x_ticks2, labels=x_ticks2)

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.truncate(before=start_yr1).index,
            series1.truncate(before=start_yr1),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0].bar(
            series1.truncate(before=start_yr1).index,
            series1.truncate(before=start_yr1),
            width=1,
            align="center",
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
    ax[0].margins(x=0)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for second subplot.
    if max(series2) == 0:
        ax[1].plot(
            series2.truncate(before=start_yr2).index,
            series2.truncate(before=start_yr2),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1].bar(
            series2.truncate(before=start_yr2).index,
            series2.truncate(before=start_yr2),
            width=1,
            align="center",
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
    ax[1].margins(x=0)
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
        y=0.965,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.915,
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
# Function: line_column()
#
# Description:
# Line chart on the left, column chart on the right.
#
########################################################################################


def line_column(
        series1,
        series2,
        color1,
        color2,
        country,
        title,
        subplot1_title,
        subplot2_title,
        start_yr1,
        start_yr2,
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
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        ),
    )

    # Grey edges for black columns.
    if color2 == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"

    x_ticks1 = [start_yr1]
    x_ticks2 = [start_yr2]

    # x_ticks only for period defined by x_axis_interval
    for year in series1.truncate(before=start_yr1).index:
        if year % x_axis1_interval == 0:  # Modulus.
            x_ticks1.append(year)
    for year in series2.truncate(before=start_yr2).index:
        if year % x_axis2_interval == 0:
            x_ticks2.append(year)

    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks1) >= 3:
        x_ticks1.append(series1.index.max())
    else:
        x_ticks1[len(x_ticks1) - 1] = series1.index.max()

    if series2.index.max() - max(x_ticks2) >= 3:
        x_ticks2.append(series2.index.max())
    else:
        x_ticks2[len(x_ticks2) - 1] = series2.index.max()

    ax[0].set_xticks(x_ticks1, labels=x_ticks1)
    ax[1].set_xticks(x_ticks2, labels=x_ticks2)

    # Subplot 1. Line chart.
    ax[0].plot(
        series1.truncate(before=start_yr1).index,
        series1.truncate(before=start_yr1),
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
    if max(series2) == 0:
        ax[1].plot(
            series2.index,
            series2,
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        p = ax[1].bar(
            series2.truncate(before=start_yr2).index,
            series2.truncate(before=start_yr2),
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

    ax[0].margins(x=0)
    ax[1].margins(x=0)

    # Force uppermost y-tick to be equal to autoscale max + grid interval
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    plt.subplots_adjust(left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02)
    fig.suptitle(
        country,
        x=0.18,
        y=0.97,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.92,
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
# Function: column_treemap()
#
# Description:
# Column chart on the left, treemap chart on the right.
#
########################################################################################
def column_treemap(
        series1,
        df,
        color1,
        country1,
        title1,
        title2,
        subplot1_title,
        subplot2_title,
        start_yr,
        x_axis1_interval,
        ylabel1,
        additional_text1,
        footer_text,
):
    fig = plt.figure(
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        )
    )
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, adjustable="box", aspect=1)

    # Add comma thousands seperator.
    ax1.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    # Grey edges for black columns.
    if color1 == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"

    x_ticks1 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series1.index:
        if year % x_axis1_interval == 0:  # Modulus.
            x_ticks1.append(year)

    # Include most recent year. If period between ticks is >= 25 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis1_interval >= 25:
        x_ticks1.append(max(series1.index))
    else:
        x_ticks1[len(x_ticks1) - 1] = max(series1.index)
    ax1.set_xticks(x_ticks1)

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax1.plot(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax1.bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            color=color1,
            edgecolor=edge_color,
            linewidth=0.2,
        )

    ax1.set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel(ylabel1)
    ax1.yaxis.grid(True)
    ax1.set_box_aspect(1)
    # Place grid behind columns.
    ax1.set_axisbelow(True)
    ax1.autoscale(axis="y")

    # Force uppermost tick to be equal to autoscale max + grid interval
    ax1.set_ylim(0, max(ax1.get_yticks()))

    tr.treemap(
        ax2,
        df,
        area="Value",
        labels="Label",
        cmap=df["Color"].to_list(),
        fill="Name",
        top=True,
        rectprops=dict(ec="white", lw=0.6),
        textprops=dict(
            c="white", place="top left", padx=3, pady=6, reflow=False, max_fontsize=100
        ),
    )
    country2 = "World"
    ax2.axis("off")
    ax2.set_title(
        subplot2_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )
    ax1.margins(x=0)
    plt.subplots_adjust(
        left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02, hspace=0.05
    )
    fig.suptitle(
        country1,
        x=0.18,
        y=0.965,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.947,
        country2,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.915,
        title1,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.915,
        title2,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.825,
        0.87,
        additional_text1,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
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
# Function: column_3_subplots()
#
# Description:
# 3 column subplots in 1 row.
#
########################################################################################


def column_3_subplots(
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
        start_yr,
        x_axis_interval,
        ylabels,
        footer_text,
        equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        3,
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
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

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % x_axis_interval == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks, labels=x_ticks)
    ax[1].set_xticks(x_ticks, labels=x_ticks)
    ax[2].set_xticks(x_ticks, labels=x_ticks)

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0].margins(x=0)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for second and third subplots.
    if max(series2) == 0:
        ax[1].plot(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1].margins(x=0)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[2].margins(x=0)
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

    plt.subplots_adjust(left=0.06, right=0.97, wspace=0.14, top=1, bottom=0)
    fig.suptitle(
        country,
        x=0.06,
        y=0.935,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.06,
        0.885,
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
# Function: line_4_subplots()
#
# Description:
# 4 line subplots in 1 row.
#
########################################################################################


def line_4_subplots(
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
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW.value,
        ),
    )
    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks, labels=x_ticks)
    ax[1].set_xticks(x_ticks, labels=x_ticks)
    ax[2].set_xticks(x_ticks, labels=x_ticks)
    ax[3].set_xticks(x_ticks, labels=x_ticks)

    ax[0].plot(
        series1.truncate(before=start_yr).index,
        series1.truncate(before=start_yr),
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel(ylabel)
    ax[0].yaxis.grid(True)
    ax[0].margins(x=0)
    ax[0].set_box_aspect(1)
    ax[0].autoscale(axis="y")
    ylim1 = ax[0].get_ylim()[1]

    ax[1].plot(
        series2.truncate(before=start_yr).index,
        series2.truncate(before=start_yr),
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1].set_xlabel("Year")
    ax[1].yaxis.grid(True)
    ax[1].margins(x=0)
    ax[1].set_box_aspect(1)
    ax[1].autoscale(axis="y")
    ylim2 = ax[1].get_ylim()[1]

    ax[2].plot(
        series3.truncate(before=start_yr).index,
        series3.truncate(before=start_yr),
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[2].set_xlabel("Year")
    ax[2].yaxis.grid(True)
    ax[2].margins(x=0)
    ax[2].set_box_aspect(1)
    ax[2].autoscale(axis="y")
    ylim3 = ax[2].get_ylim()[1]

    ax[3].plot(
        series4.truncate(before=start_yr).index,
        series4.truncate(before=start_yr),
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[3].set_xlabel("Year")
    ax[3].yaxis.grid(True)
    ax[3].margins(x=0)
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

    plt.subplots_adjust(left=0.05, right=0.97, wspace=0.12, top=0.94, bottom=0.09)
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
# Function: column_4_subplots()
#
# Description:
# Single row of 4 column subplots.
#
########################################################################################


def column_4_subplots(
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
        start_yr,
        ylabels,
        footer_text,
        equiv_yscale,
):
    fig, ax = plt.subplots(
        1,
        4,
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW.value,
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

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.truncate(before=start_yr).index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks, labels=x_ticks)
    ax[1].set_xticks(x_ticks, labels=x_ticks)
    ax[2].set_xticks(x_ticks, labels=x_ticks)
    ax[3].set_xticks(x_ticks, labels=x_ticks)

    # Subplots
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[0].plot(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0].margins(x=0)
    ylim1 = ax[0].get_ylim()[1]

    # Repeat above for remaining subplots.
    if max(series2) == 0:
        ax[1].plot(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1].margins(x=0)
    ylim2 = ax[1].get_ylim()[1]

    if max(series3) == 0:
        ax[2].plot(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[2].margins(x=0)
    ylim3 = ax[2].get_ylim()[1]

    if max(series4) == 0:
        ax[3].plot(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[3].margins(x=0)
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
        y=0.94,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    # Text beneath figure title.
    fig.text(
        0.06,
        0.875,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    # Text in footer.
    fig.text(
        0.06,
        0.105,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


# 2 row charts.
########################################################################################
#
# Function: column_5_subplots()
#
# Description:
# 5 column subplots, 4 on first row, 1 on second.
#
########################################################################################


def column_5_subplots(

        series1,
        series2,
        series3,
        series4,
        series5,
        color1,
        color2,
        color3,
        color4,
        color5,
        country,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)

    ax[1, 1].set_visible(False)
    ax[1, 2].set_visible(False)
    ax[1, 3].set_visible(False)

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

    if max(series1) == 0:
        ax[0, 0].plot(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 0].tick_params(labelsize=8)
    ax[0, 0].margins(x=0)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if max(series2) == 0:
        ax[0, 1].plot(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            align="center",
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
    ax[0, 1].tick_params(labelsize=8)
    ax[0, 1].margins(x=0)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if max(series3) == 0:
        ax[0, 2].plot(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 2].tick_params(labelsize=8)
    ax[0, 2].margins(x=0)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if max(series4) == 0:
        ax[0, 3].plot(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 3].tick_params(labelsize=8)
    ax[0, 3].margins(x=0)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    if max(series5) == 0:
        ax[1, 0].plot(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 0].tick_params(labelsize=8)
    ax[1, 0].margins(x=0)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)

        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))

    plt.subplots_adjust(
        left=0.052, right=0.97, top=0.92, bottom=0.1, wspace=0, hspace=0.15
    )
    fig.suptitle(
        country,
        x=0.065,
        y=0.99,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.955,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.05,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: line_6_subplots()
#
# Description:
# Line subplots, 4 on first line, 2 on second.
#
########################################################################################
def line_6_subplots(
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
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)

    ax[1, 2].set_visible(False)
    ax[1, 3].set_visible(False)

    ax[0, 0].plot(
        series1.truncate(before=start_yr).index,
        series1.truncate(before=start_yr),
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.truncate(before=start_yr).index,
        series2.truncate(before=start_yr),
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.truncate(before=start_yr).index,
        series3.truncate(before=start_yr),
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].margins(x=0)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[0, 3].plot(
        series4.truncate(before=start_yr).index,
        series4.truncate(before=start_yr),
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 3].margins(x=0)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    ax[1, 0].plot(
        series5.truncate(before=start_yr).index,
        series5.truncate(before=start_yr),
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 0].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].margins(x=0)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series6.truncate(before=start_yr).index,
        series6.truncate(before=start_yr),
        color6,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 1].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].margins(x=0)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)

        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))

    plt.subplots_adjust(
        left=0.09, right=0.95, top=0.94, bottom=0.08, wspace=0.12, hspace=0.01
    )
    fig.suptitle(
        country,
        x=0.09,
        y=0.985,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.09,
        0.945,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.09,
        0.05,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column_6_subplots()
#
# Description:
# 6 column subplots, 4 on first row, 2 on second.
#
########################################################################################


def column_6_subplots(
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
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)

    ax[1, 2].set_visible(False)
    ax[1, 3].set_visible(False)

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
    ax[0, 3].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax[1, 1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    if max(series1) == 0:
        ax[0, 0].plot(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 0].tick_params(labelsize=8)
    ax[0, 0].margins(x=0)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if max(series2) == 0:
        ax[0, 1].plot(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            align="center",
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
    ax[0, 1].tick_params(labelsize=8)
    ax[0, 1].margins(x=0)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if max(series3) == 0:
        ax[0, 2].plot(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 2].tick_params(labelsize=8)
    ax[0, 2].margins(x=0)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if max(series4) == 0:
        ax[0, 3].plot(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 3].tick_params(labelsize=8)
    ax[0, 3].margins(x=0)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    if max(series5) == 0:
        ax[1, 0].plot(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 0].tick_params(labelsize=8)
    ax[1, 0].margins(x=0)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    if max(series6) == 0:
        ax[1, 1].plot(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 1].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 1].tick_params(labelsize=8)
    ax[1, 1].margins(x=0)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim1, ylim2, ylim3, ylim4, ylim5, ylim6)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)

        # Force uppermost tick to be equal to autoscale max + grid interval
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))

    plt.subplots_adjust(
        left=0.052, right=0.97, top=0.92, bottom=0.1, wspace=0, hspace=0.14
    )
    fig.suptitle(
        country,
        x=0.065,
        y=0.99,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.955,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.05,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: line_8_subplots()
#
# Description:
# 8 line subplots, 4 on each of two rows.
#
########################################################################################


def line_8_subplots(
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
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 3].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].plot(
        series1.truncate(before=start_yr).index,
        series1.truncate(before=start_yr),
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 0].set_title(
        subplot1_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].margins(x=0, tight=True)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    ax[0, 1].plot(
        series2.truncate(before=start_yr).index,
        series2.truncate(before=start_yr),
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 1].set_title(
        subplot2_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    ax[0, 2].plot(
        series3.truncate(before=start_yr).index,
        series3.truncate(before=start_yr),
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 2].set_title(
        subplot3_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].margins(x=0)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    ax[0, 3].plot(
        series4.truncate(before=start_yr).index,
        series4.truncate(before=start_yr),
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 3].set_title(
        subplot4_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 3].margins(x=0)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    ax[1, 0].plot(
        series5.truncate(before=start_yr).index,
        series5.truncate(before=start_yr),
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 0].set_title(
        subplot5_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].margins(x=0)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    ax[1, 1].plot(
        series6.truncate(before=start_yr).index,
        series6.truncate(before=start_yr),
        color6,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 1].set_title(
        subplot6_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].margins(x=0)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    ax[1, 2].plot(
        series7.truncate(before=start_yr).index,
        series7.truncate(before=start_yr),
        color7,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 2].set_title(
        subplot7_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].margins(x=0)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
    ylim7 = ax[1, 2].get_ylim()[1]

    ax[1, 3].plot(
        series8.truncate(before=start_yr).index,
        series8.truncate(before=start_yr),
        color8,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 3].set_title(
        subplot8_title,
        loc="left",
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 3].set_xlabel("Year")
    ax[1, 3].margins(x=0)
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
        left=0.09, right=0.95, top=0.94, bottom=0.08, wspace=0.12, hspace=0.01
    )
    fig.suptitle(
        country,
        x=0.09,
        y=0.985,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.09,
        0.945,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.09,
        0.05,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################
#
# Function: column_8_subplots()
#
# Description:
# 8 column subplots, 4 on each of two rows.
#
########################################################################################


def column_8_subplots(
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
        start_yr,
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
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series1.index:
        if year % 5 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then
    # there's room to append most recent year.
    # Else replace final value with most recent year.
    if series1.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series1.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series1.index.max()

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 3].set_xticks(x_ticks, labels=x_ticks)

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
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 0].tick_params(labelsize=8)
    ax[0, 0].margins(x=0)
    ax[0, 0].set_box_aspect(1)
    ax[0, 0].autoscale(axis="y")
    ylim1 = ax[0, 0].get_ylim()[1]

    if max(series2) == 0:
        ax[0, 1].plot(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            align="center",
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
    ax[0, 1].tick_params(labelsize=8)
    ax[0, 1].margins(x=0)
    ax[0, 1].set_box_aspect(1)
    ax[0, 1].autoscale(axis="y")
    ylim2 = ax[0, 1].get_ylim()[1]

    if max(series3) == 0:
        ax[0, 2].plot(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 2].tick_params(labelsize=8)
    ax[0, 2].margins(x=0)
    ax[0, 2].set_box_aspect(1)
    ax[0, 2].autoscale(axis="y")
    ylim3 = ax[0, 2].get_ylim()[1]

    if max(series4) == 0:
        ax[0, 3].plot(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[0, 3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[0, 3].tick_params(labelsize=8)
    ax[0, 3].margins(x=0)
    ax[0, 3].set_box_aspect(1)
    ax[0, 3].autoscale(axis="y")
    ylim4 = ax[0, 3].get_ylim()[1]

    if max(series5) == 0:
        ax[1, 0].plot(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 0].tick_params(labelsize=8)
    ax[1, 0].margins(x=0)
    ax[1, 0].set_box_aspect(1)
    ax[1, 0].autoscale(axis="y")
    ylim5 = ax[1, 0].get_ylim()[1]

    if max(series6) == 0:
        ax[1, 1].plot(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 1].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 1].tick_params(labelsize=8)
    ax[1, 1].margins(x=0)
    ax[1, 1].set_box_aspect(1)
    ax[1, 1].autoscale(axis="y")
    ylim6 = ax[1, 1].get_ylim()[1]

    if max(series7) == 0:
        ax[1, 2].plot(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            color7,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 2].bar(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 2].tick_params(labelsize=8)
    ax[1, 2].margins(x=0)
    ax[1, 2].set_box_aspect(1)
    ax[1, 2].autoscale(axis="y")
    ylim7 = ax[1, 2].get_ylim()[1]

    if max(series8) == 0:
        ax[1, 3].plot(
            series8.truncate(before=start_yr).index,
            series8.truncate(before=start_yr),
            color8,
            linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
        )
    else:
        ax[1, 3].bar(
            series8.truncate(before=start_yr).index,
            series8.truncate(before=start_yr),
            width=1,
            align="center",
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
    ax[1, 3].tick_params(labelsize=8)
    ax[1, 3].margins(x=0)
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
        left=0.052, right=0.97, top=0.92, bottom=0.1, wspace=0, hspace=0.14
    )
    fig.suptitle(
        country,
        x=0.065,
        y=0.99,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.955,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.05,
        footer_text,
        horizontalalignment="left",
        verticalalignment="top",
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
            user_globals.Constant.FIG_HSIZE_CHANGE_COLUMN_PLOT.value,
            user_globals.Constant.FIG_VSIZE_CHANGE_COLUMN_PLOT.value,
        ),
    )

    label_pad = 2
    series_qty = len(series)
    column_width = 1 / series_qty
    series_number = 0
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
                else "0"  # So that 0 is displayed instead of "-0" if negative values
                # between -0.5 and 0 are rounded.
            )
            for v in p
        ]
        if series_qty > 1:
            ax.bar_label(p, labels=labels, fmt="%.0f", padding=label_pad, rotation=90)
        else:
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
    x_ticks_major.append(end_yr)

    # If more than one series is plotted, align major ticks, minor ticks and grid with
    # the left hand edge of set of columns, and enable minor as well as major grid
    # lines.
    if series_qty > 1:
        ax.set_xticks(np.array(x_ticks_major) - column_width / 2, labels=x_ticks_major)
        ax.set_xticks(
            np.arange(start_yr - column_width / 2, (end_yr - column_width / 2), 1),
            minor=True,
        )
        ax.xaxis.grid(
            True, which="major", alpha=1, linestyle="--", linewidth=0.5, color="black"
        )
        ax.xaxis.grid(
            True, which="minor", alpha=1, linestyle="--", linewidth=0.5, color="black"
        )
        plt.margins(x=0.006)
    else:
        ax.set_xticks(np.array(x_ticks_major), labels=x_ticks_major)
        ax.set_xticks(np.arange(start_yr, end_yr, 1), minor=True)
        ax.xaxis.grid(
            True, which="major", alpha=1, linestyle="--", linewidth=0.5, color="black"
        )
        plt.margins(x=0)

    ax.autoscale(axis="y")
    ax.set_ylim(min(ax.get_yticks()), max(ax.get_yticks()))
    ax.set_ylabel(y_label)
    ax.yaxis.grid(False)
    # Add comma thousands seperator.
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
    )
    ax.set_xlabel("Year")
    if series_qty > 1:
        ax.legend(
            plot_names,
            loc="lower left",
            frameon=False,
            handlelength=2,
            ncol=7,
            fontsize="large",
        )
    # Show x-axis line.
    plt.axhline(0, color="black", lw=0.4)
    ax.set_axisbelow(True)

    plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.18)
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
        0.91,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.12,
        footer_text,
        verticalalignment="top",
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


###############################################################################
#
# Function: treemap_1_subplot()
#
# Description:
# Single treemap plot
#
###############################################################################


def treemap_1_subplot(
        df, subplot_title, country, title, title_addition, footer_text  # Dataframe
):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_TREE.value,
            user_globals.Constant.FIG_VSIZE_1_TREE.value,
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
        rectprops=dict(ec="darkslategray", lw=0.6),
        textprops=dict(
            c="white", place="top left", padx=3, pady=6, reflow=True, max_fontsize=60
        ),
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
# Function: treemap_2_subplots()
#
# Description:
# 2 treemap subplots in 1 row.
#
###############################################################################


def treemap_2_subplots(
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
            user_globals.Constant.FIG_HSIZE_2_TREE.value,
            user_globals.Constant.FIG_VSIZE_2_TREE.value,
        ),
        subplot_kw=dict(aspect=1.1),
    )

    # Plot left-hand treemap.
    tr.treemap(
        ax[0],
        df1,
        area="Value",
        labels="Label",
        cmap=df1["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="darkslategray", lw=0.6),
        textprops=dict(
            c="white",
            place="top left",
            padx=3,
            pady=6,
            reflow=True,
            max_fontsize=60,
            grow=True,
        ),
    )
    ax[0].legend(
        df1["Name"],
        loc="upper left",
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=3,
        fontsize="large",
    )
    ax[0].axis("off")
    ax[0].set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    # Plot right-hand treemap.
    tr.treemap(
        ax[1],
        df2,
        area="Value",
        labels="Label",
        cmap=df2["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="black", lw=0.4),
        textprops=dict(
            c="white",
            place="top left",
            padx=3,
            pady=6,
            reflow=True,
            max_fontsize=60,
        ),
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
            position=(0.011, 1),
            pad=7.5,
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


###############################################################################
#
# Function: treemap_3_subplots()
#
# Description:
# 3 treemap subplots in 1 row, without legend.
#
###############################################################################


def treemap_3_subplots(
        df1,  # Dataframe 1
        df2,  # Dataframe 2
        df3,  # Dataframe 3
        subplot1_title,  # Title above LH plot
        subplot2_title,  # Title above centre plot
        subplot3_title,  # Title above RH plot
        country,
        title,
        title_addition,
        footer_text,
):
    fig, ax = plt.subplots(
        1,
        3,
        figsize=(
            user_globals.Constant.FIG_HSIZE_3_TREE.value,
            user_globals.Constant.FIG_VSIZE_3_TREE.value,
        ),
        subplot_kw=dict(aspect=1.1),
    )

    # Plot left-hand treemap.
    tr.treemap(
        ax[0],
        df1,
        area="Value",
        labels="Label",
        cmap=df1["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="white", lw=0.6),
        textprops=dict(
            c="white", place="top left", padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[0].axis("off")
    ax[0].set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    # Plot centre treemap.
    tr.treemap(
        ax[1],
        df2,
        area="Value",
        labels="Label",
        cmap=df2["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="white", lw=0.6),
        textprops=dict(
            c="white", place="top left", padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[1].axis("off")
    ax[1].set_title(
        subplot2_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    # Plot RH treemap.
    tr.treemap(
        ax[2],
        df3,
        area="Value",
        labels="Label",
        cmap=df3["Color"].to_list(),
        fill="Name",
        rectprops=dict(ec="darkslategray", lw=0.6),
        textprops=dict(
            c="white", place="top left", padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[2].axis("off")
    ax[2].set_title(
        subplot3_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc="left",
    )

    plt.subplots_adjust(left=0.125, top=0.9, bottom=0.09)
    fig.suptitle(
        country,
        x=0.125,
        y=0.95,
        horizontalalignment="left",
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.895,
        title,
        horizontalalignment="left",
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.885,
        title_addition,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.04,
        footer_text,
        horizontalalignment="left",
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )
