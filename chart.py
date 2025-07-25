#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#Created on Wed Mar 20 13:56:43 2024

#@author: shanewhite
"""

########################################################################################################################
#
# Module: chart.py
#
# Description:
# Generic chart drawing functions.
#
########################################################################################################################

# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np
import mpl_extra.treemap as tr
# Location:
# https://github.com/chenyulue/matplotlib-extra
# Install command:
# pip3 install git+https://github.com/chenyulue/matplotlib-extra/
import matplotlib.ticker
import decimal
import pandas as pd

# Import user modules.
import user_globals


########################################################################################################################
#
# Function: line_plot()
#
# Description:
# Single line plot of user selected quantity of series. Line markers appear every 10 so will appear every decade if
# data begins at start of a decade.
#
########################################################################################################################
def line_plot(title, x_label, y_label, footer_text, text, series_labels, *colors, **series):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_SINGLE_PLOT.value,
            user_globals.Constant.FIG_VSIZE_SINGLE_PLOT.value,
        ),
    )
    # Cycle through and plot input series.
    series_number = 0
    series_qty = len(series)
    plot_names = []
    min_all_series_x = min(series['series1'].index)  # Preset min of x-axis. Final value is assigned in loop below.
    max_all_series_x = max(series['series1'].index)  # Preset max of x-axis. Final value is assigned in loop below.

    for key, value in series.items():
        if series_number == 0:
            ax.plot(
                value.index,
                value,
                color=colors[series_number],
                linewidth=user_globals.Constant.LINE_PLOT_WIDTH.value,
                marker='.',
                markersize=15,
                markerfacecolor='white',
                markeredgecolor=colors[series_number],
                markeredgewidth=1,
                markevery=10,
                zorder=1,
                solid_capstyle='round'
            )
        else:
            ax.plot(
                value.index,
                value,
                color=colors[series_number],
                linewidth=user_globals.Constant.LINE_PLOT_WIDTH.value,
                marker='.',
                markersize=15,
                markerfacecolor='white',
                markeredgecolor=colors[series_number],
                markeredgewidth=1,
                markevery=10,
                zorder=0,
                solid_capstyle='round'
            )
        plot_names.append(value.name)
        min_series_x = min(value.index)
        if min_series_x < min_all_series_x:
            min_all_series_x = min_series_x
        max_series_x = max(value.index)
        if max_series_x > max_all_series_x:
            max_all_series_x = max_series_x
        series_number += 1

    ax.set_facecolor('whitesmoke')

    # Show legend if more than one series,
    if series_qty > 1:
        ax.legend(
            labels=series_labels,
            loc='upper left',
            handlelength=2,
            fontsize='large',
            facecolor='white',
            framealpha=1,
            fancybox=False,
            labelspacing=1,
        )
    ax.set_box_aspect(1)

    # Create list x_ticks and fill with start year of each decade.
    x_axis_years = np.arange(min_all_series_x, max_all_series_x + 1, 1)
    x_ticks = [min_all_series_x]
    for year in x_axis_years:
        if year % 10 == 0:
            x_ticks.append(year)

    ax.set_xticks(x_ticks)
    plt.xticks(rotation=90)
    ax.set_xlim(min_all_series_x, max_all_series_x)
    ax.set_xlabel(x_label)
    ax.margins(x=0)

    ax.set_ylim(0, max(ax.get_yticks()))
    ax.set_ylabel(y_label)

    plt.subplots_adjust(left=0, right=1, top=0.96, bottom=0.09)

    fig.text(
        0.065,
        0.97,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.065,
        0.025,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )
    t = fig.text(
        0.32,
        0.945,
        text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
    )
    t.set_bbox(dict(facecolor='white', edgecolor='lightgrey', pad=5))


########################################################################################################################
#
# Function: line_2_subplots()
#
# Description:
# 2 line subplots in 1 row. First is a plot of a single series and the second of 3 series. No subplot labels, axes or
# tick labels.
#
########################################################################################################################
def line_2_subplots(
        series0,
        series1,
        series2,
        series3,
        color0,
        color1,
        color2,
        color3,
        country,
        start_yr0,
        start_yr1,
        x_axis0_interval,
        x_axis1_interval,
):
    fig, ax = plt.subplots(
        1,
        2,
        figsize=(
            user_globals.Constant.MAJOR_EMITTER_FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        ),
    )

    # Subplot0, line plot, series0
    ax[0].plot(
        series0.truncate(before=start_yr0).index,
        series0.truncate(before=start_yr0),
        color0,
        linewidth=user_globals.Constant.MAJOR_EMITTER_LINE_WIDTH_PLOT.value,
        marker='.',
        markersize=user_globals.Constant.MAJOR_EMITTER_LINE_MARKER_SIZE.value,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )

    # Subplot1, line plot, series 1
    ax[1].plot(
        series1.truncate(before=start_yr1).index,
        series1.truncate(before=start_yr1),
        color1,
        linewidth=user_globals.Constant.MAJOR_EMITTER_LINE_WIDTH_PLOT.value,
        marker='.',
        markersize=user_globals.Constant.MAJOR_EMITTER_LINE_MARKER_SIZE.value,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    # Subplot2
    ax[1].plot(
        series2.truncate(before=start_yr1).index,
        series2.truncate(before=start_yr1),
        color2,
        linewidth=user_globals.Constant.MAJOR_EMITTER_LINE_WIDTH_PLOT.value,
        marker='.',
        markersize=user_globals.Constant.MAJOR_EMITTER_LINE_MARKER_SIZE.value,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    # Subplot3
    ax[1].plot(
        series3.truncate(before=start_yr1).index,
        series3.truncate(before=start_yr1),
        color3,
        linewidth=user_globals.Constant.MAJOR_EMITTER_LINE_WIDTH_PLOT.value,
        marker='.',
        markersize=user_globals.Constant.MAJOR_EMITTER_LINE_MARKER_SIZE.value,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )

    ax[0].set_facecolor('whitesmoke')
    ax[1].set_facecolor('whitesmoke')

    x_ticks0 = [start_yr0]
    x_ticks1 = [start_yr1]

    # x_ticks only for period defined by x_axis_interval
    for year in series0.truncate(before=start_yr0).index:
        if year % x_axis0_interval == 0:  # Modulus.
            x_ticks0.append(year)
    for year in series1.truncate(before=start_yr1).index:
        if year % x_axis1_interval == 0:
            x_ticks1.append(year)

    # If period between final tick and year of final value is >= 4 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if series0.index.max() - max(x_ticks0) >= 4:
        x_ticks0.append(series0.index.max())
    else:
        x_ticks0[len(x_ticks0) - 1] = series0.index.max()

    if series1.index.max() - max(x_ticks1) >= 4:
        x_ticks1.append(series1.index.max())
    else:
        x_ticks1[len(x_ticks1) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks0, labels=x_ticks0, color='white')
    ax[1].set_xticks(x_ticks1, labels=x_ticks1, color='white')

    ax[0].tick_params(axis='both', which='major', labelcolor='white', colors='white')
    ax[1].tick_params(axis='both', which='major', labelcolor='white', colors='white')
    ax[0].tick_params(axis='both', which='minor', labelcolor='white', colors='white')
    ax[1].tick_params(axis='both', which='minor', labelcolor='white', colors='white')

    ax[0].margins(x=0)
    ax[0].autoscale(axis='y')
    ax[0].xaxis.grid(False)
    ax[0].yaxis.grid(False)

    ax[1].margins(x=0)
    ax[1].autoscale(axis='y')
    ax[1].xaxis.grid(False)
    ax[1].yaxis.grid(False)

    # Force uppermost x-tick to be equal to next tick after ylim
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    # Set aspect ratio 1:1.
    ax[0].set_box_aspect(1)
    ax[1].set_box_aspect(1)

    for axis in ['top', 'bottom', 'left', 'right']:
        ax[0].spines[axis].set_linewidth(.5)
        ax[0].spines[axis].set_color('black')
        ax[1].spines[axis].set_linewidth(.5)
        ax[1].spines[axis].set_color('black')

    # Adjust whitespace around plot area.
    plt.subplots_adjust(left=0, right=1, wspace=0, top=0.91, bottom=0.04)

    if country == 'Russian Federation':
        country = 'USSR & Russian Federation'
    fig.suptitle(
        country,
        x=0.5,
        y=0.985,
        horizontalalignment='center',
        fontsize=user_globals.Constant.MAJOR_EMITTER_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.MAJOR_EMITTER_TITLE_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: legend_for_major_emitter_charts()
#
# Description:
# Generates legend for use on webpage
#
########################################################################################################################
def legend_for_major_emitter_charts(
        series0,
        series1,
        series2,
        series3,
        color0,
        color1,
        color2,
        color3,
):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.MAJOR_EMITTER_FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        ),
    )

    # Subplot0, line plot, series0
    ax.plot(
        series0.index,
        series0,
        color0,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )

    # Subplot1, line plot, series 1
    ax.plot(
        series1.index,
        series1,
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    # Subplot2
    ax.plot(
        series2.index,
        series2,
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    # Subplot3
    ax.plot(
        series3.index,
        series3,
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    ax.set_axis_off()  # turn off the axis

    ax.legend(['Fossil Fuel CO\u2082 Emissions (tonne)',
               'Coal Consumption (joule)',
               'Oil Consumption (joule)',
               'Gas Consumption (joule)'],
              loc='upper left', frameon=True, prop={'size': 14}, framealpha=1, facecolor='white',
              ncols=1, mode='expand', borderpad=2)


########################################################################################################################
#
# Function: column_2_subplots()
#
# Description:
# 2 column subplots in 1 row.
#
########################################################################################################################
def column_2_subplots(
        series0,
        series1,
        color0,
        color1,
        country,
        title,
        subplot0_title,
        subplot1_title,
        start_yr0,
        start_yr1,
        x_axis0_interval,
        x_axis1_interval,
        ylabels,
        chart_text,
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
    # Grey edges for black columns.
    if color0 == 'black':
        edge_color0 = 'dimgrey'
    else:
        edge_color0 = 'black'
    if color1 == 'black':
        edge_color1 = 'dimgrey'
    else:
        edge_color1 = 'black'

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series0) == 0:
        ax[0].plot(
            series0.truncate(before=start_yr0).index,
            pd.Series(0, series0.truncate(before=start_yr0).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0].bar(
            series0.truncate(before=start_yr0).index,
            series0.truncate(before=start_yr0),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )

    # Repeat above for second subplot.
    if max(series1) == 0:
        ax[1].plot(
            series1.truncate(before=start_yr1).index,
            pd.Series(0, series1.truncate(before=start_yr1).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1].bar(
            series1.truncate(before=start_yr1).index,
            series1.truncate(before=start_yr1),
            width=1,
            align='center',
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )

    ax[0].set_facecolor('whitesmoke')
    ax[1].set_facecolor('whitesmoke')

    # Configure x-axes.
    # Create list x_ticks and fill with start year of each decade.
    x_ticks0 = [start_yr0]
    x_ticks1 = [start_yr1]
    # x_ticks only for period defined by x_axis_interval
    for year in series0.truncate(before=start_yr0).index:
        if year % x_axis0_interval == 0:  # Modulus.
            x_ticks0.append(year)
    for year in series0.truncate(before=start_yr1).index:
        if year % x_axis1_interval == 0:
            x_ticks1.append(year)
    # If period between final tick and year of final value is >= 3 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if series0.index.max() - max(x_ticks0) >= 3:
        x_ticks0.append(series0.index.max())
    else:
        x_ticks0[len(x_ticks0) - 1] = series0.index.max()

    if series1.index.max() - max(x_ticks1) >= 3:
        x_ticks1.append(series1.index.max())
    else:
        x_ticks1[len(x_ticks1) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks0, labels=x_ticks0)
    ax[1].set_xticks(x_ticks1, labels=x_ticks1)

    ax[0].set_xlabel('Year')
    ax[1].set_xlabel('Year')

    ax[0].margins(x=0)
    ax[1].margins(x=0)

    # Configure y-axes.
    # Autoscale and get max-y for setting equiv y-axis scale.
    ax[0].autoscale(axis='y')
    ax[1].autoscale(axis='y')
    ylim0 = ax[0].get_ylim()[1]
    ylim1 = ax[1].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim0, ylim1)
        ax[0].set_ylim(0, y_max)
        ax[1].set_ylim(0, y_max)
    # Force uppermost tick to be equal to next tick after ylim
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    ax[0].yaxis.grid(True)
    ax[1].yaxis.grid(True)

    ax[0].set_box_aspect(1)
    ax[1].set_box_aspect(1)

    ax[0].set_axisbelow(True)
    ax[1].set_axisbelow(True)

    # Remove ticks from y-axis
    ax[1].tick_params(axis='y', labelleft=False, length=0)

    # If series max is zero, display only a zero on the y-axis, otherwise add comma thousands seperator to y-labels.
    if max(series0) == 0:
        ax[0].set_yticks([0])
    else:
        ax[0].set_ylabel(ylabels)
        ax[0].yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
        )
    if max(series1) == 0:
        ax[1].set_yticks([0])
    else:
        ax[1].yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
        )

    # Adjust whitespace around plot area.
    plt.subplots_adjust(left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02)

    # Add plot text.
    ax[0].text(1960, 37000, chart_text)

    ax[0].set_title(
        subplot0_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    ax[1].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    fig.suptitle(
        country,
        x=0.18,
        y=0.965,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.915,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: line_column()
#
# Description:
# Line chart on the left, column chart on the right.
#
########################################################################################################################
def line_column(
        series0,
        series1,
        color0,
        color1,
        country,
        title,
        subplot0_title,
        subplot1_title,
        start_yr0,
        start_yr1,
        x_axis0_interval,
        x_axis1_interval,
        ylabel0,
        ylabel1,
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
    if color1 == 'black':
        edge_color = 'dimgrey'
    else:
        edge_color = 'black'

    x_ticks0 = [start_yr0]
    x_ticks1 = [start_yr1]

    # x_ticks only for period defined by x_axis_interval
    for year in series0.truncate(before=start_yr0).index:
        if year % x_axis0_interval == 0:  # Modulus.
            x_ticks0.append(year)
    for year in series1.truncate(before=start_yr1).index:
        if year % x_axis1_interval == 0:
            x_ticks1.append(year)

    # If period between final tick and year of final value is >= 3 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if series0.index.max() - max(x_ticks0) >= 3:
        x_ticks0.append(series0.index.max())
    else:
        x_ticks0[len(x_ticks0) - 1] = series0.index.max()

    if series1.index.max() - max(x_ticks1) >= 3:
        x_ticks1.append(series1.index.max())
    else:
        x_ticks1[len(x_ticks1) - 1] = series1.index.max()

    ax[0].set_xticks(x_ticks0, labels=x_ticks0)
    ax[1].set_xticks(x_ticks1, labels=x_ticks1)

    # Subplot 1, line plot.
    ax[0].plot(
        series0.truncate(before=start_yr0).index,
        series0.truncate(before=start_yr0),
        color0,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )

    # Subplot 2, column plot.
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series1) == 0:
        ax[1].plot(
            series1.index,
            series1,
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        p = ax[1].bar(
            series1.truncate(before=start_yr1).index,
            series1.truncate(before=start_yr1),
            width=1,
            color=color1,
            edgecolor=edge_color,
            linewidth=0.2,
        )
    ax[1].bar_label(p, fmt='%.1f', padding=2)

    ax[0].set_facecolor('whitesmoke')
    ax[1].set_facecolor('whitesmoke')

    ax[0].margins(x=0)
    ax[1].margins(x=0)
    ax[0].set_xlabel('Year')
    ax[1].set_xlabel('Year')

    ax[0].set_ylabel(ylabel0)
    ax[1].set_ylabel(ylabel1)
    ax[0].autoscale(axis='y')
    ax[1].autoscale(axis='y')
    ax[1].yaxis.grid(True)

    # Force uppermost tick to be equal to next tick after ylim
    ax[0].set_ylim(0, max(ax[0].get_yticks()))
    ax[1].set_ylim(0, max(ax[1].get_yticks()))

    # Set aspect ratio 1:1.
    ax[0].set_box_aspect(1)
    ax[1].set_box_aspect(1)

    # Place grid behind columns.
    ax[1].set_axisbelow(True)

    # Adjust whitespace around plot area.
    plt.subplots_adjust(left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02)

    # Add text to chart and after force the uppermost tick to be equal to next tick after.
    ax[0].text(2005, 425, chart_text)
    ax[0].set_ylim(0, max(ax[0].get_yticks()))

    ax[0].set_title(
        subplot0_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    ax[1].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    fig.suptitle(
        country,
        x=0.18,
        y=0.97,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.92,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: line_treemap()
#
# Description:
# Line chart on the left (subplot0), treemap chart on the right (subplot1).
#
########################################################################################################################
def line_treemap(
        series0,
        df,
        color0,
        country0,
        title0,
        title1,
        subplot0_title,
        subplot1_title,
        start_yr0,
        x_axis_interval0,
        ylabel0,
        additional_text0,
        footer_text,
):
    fig = plt.figure(
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        )
    )
    ax0 = fig.add_subplot(1, 2, 1)
    ax1 = fig.add_subplot(1, 2, 2, adjustable='box', aspect=1)

    # Subplot 0 line plot.
    ax0.plot(
        series0.truncate(before=start_yr0).index,
        series0.truncate(before=start_yr0),
        color0,
        linewidth=user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
        marker='.',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='black',
        markeredgewidth=0.3,
    )
    ax0.set_facecolor('whitesmoke')

    # x-axis of subplot0:
    x_ticks0 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series0.truncate(before=start_yr0).index:
        if year % x_axis_interval0 == 0:  # Modulus.
            x_ticks0.append(year)

    # Make initial x_tick initial year of data
    x_ticks0[0] = min(series0.index)

    # Make final x_tick final year of data
    x_ticks0[len(x_ticks0) - 1] = max(series0.index)

    ax0.set_xticks(x_ticks0)
    ax0.set_xlabel('Year')
    ax0.set_ylabel(ylabel0)
    ax0.yaxis.grid(True)
    ax0.set_box_aspect(1)
    # Place grid behind line.
    ax0.set_axisbelow(True)
    ax0.autoscale(axis='y')
    # If series max is zero, display only a zero on the y-axis, otherwise add comma thousands seperator to y-labels.
    if max(series0) == 0:
        ax0.set_yticks([0])
    else:
        ax0.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
        )
    # Force uppermost tick to be equal to next tick after ylim
    ax0.set_ylim(0, max(ax0.get_yticks()))

    tr.treemap(
        ax1,
        df,
        area='Value',
        labels='Label',
        cmap=df['Color'].to_list(),
        fill='Name',
        top=True,
        rectprops=dict(ec='white', lw=0.6),
        textprops=dict(
            c='white', place='top left', padx=3, pady=6, reflow=False, max_fontsize=100
        ),
    )

    country1 = 'World'
    ax1.axis('off')
    ax1.set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    ax0.margins(x=0)
    plt.subplots_adjust(
        left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02, hspace=0.05
    )
    ax0.set_title(
        subplot0_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    fig.suptitle(
        country0,
        x=0.18,
        y=0.965,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.947,
        country1,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.915,
        title0,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.915,
        title1,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.825,
        0.87,
        additional_text0,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: column_treemap()
#
# Description:
# Column chart on the left, treemap chart on the right.
#
########################################################################################################################
def column_treemap(
        series0,
        df,
        color0,
        country0,
        title0,
        title1,
        subplot0_title,
        subplot1_title,
        start_yr,
        x_axis0_interval,
        ylabel0,
        additional_text0,
        footer_text,
):
    fig = plt.figure(
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        )
    )
    ax0 = fig.add_subplot(1, 2, 1)
    ax1 = fig.add_subplot(1, 2, 2, adjustable='box', aspect=1)

    # Grey edges for black columns.
    if color0 == 'black':
        edge_color = 'dimgrey'
    else:
        edge_color = 'black'

    # Subplot 1
    # If nil data remove y-axis detail, else plot bar chart.
    if max(series0) == 0:
        ax0.plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax0.bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            color=color0,
            edgecolor=edge_color,
            linewidth=0.2,
        )

    ax0.set_facecolor('whitesmoke')

    x_ticks0 = []
    # x_ticks only for period defined by x_axis_interval
    for year in series0.index:
        if year % x_axis0_interval == 0:  # Modulus.
            x_ticks0.append(year)

    # Include most recent year. If period between ticks is >= 25 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if x_axis0_interval >= 25:
        x_ticks0.append(max(series0.index))
    else:
        x_ticks0[len(x_ticks0) - 1] = max(series0.index)
    ax0.set_xticks(x_ticks0)
    ax0.set_xlabel('Year')
    ax0.set_ylabel(ylabel0)
    ax0.yaxis.grid(True)
    ax0.set_box_aspect(1)
    # Place grid behind columns.
    ax0.set_axisbelow(True)
    ax0.autoscale(axis='y')
    # If series max is zero, display only a zero on the y-axis, otherwise add comma thousands seperator to y-labels.
    if max(series0) == 0:
        ax0.set_yticks([0])
    else:
        ax0.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
        )
    # Force uppermost tick to be equal to next tick after ylim
    ax0.set_ylim(0, max(ax0.get_yticks()))

    tr.treemap(
        ax1,
        df,
        area='Value',
        labels='Label',
        cmap=df['Color'].to_list(),
        fill='Name',
        top=True,
        rectprops=dict(ec='white', lw=0.6),
        textprops=dict(
            c='white', place='top left', padx=3, pady=6, reflow=False, max_fontsize=100
        ),
    )

    country1 = 'World'
    ax1.axis('off')
    ax1.set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    ax0.margins(x=0)
    plt.subplots_adjust(
        left=0.18, right=0.82, wspace=0.13, top=1, bottom=0.02, hspace=0.05
    )
    ax0.set_title(
        subplot0_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )
    fig.suptitle(
        country0,
        x=0.18,
        y=0.965,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.947,
        country1,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.915,
        title0,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.52,
        0.915,
        title1,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.825,
        0.87,
        additional_text0,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.18,
        0.08,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: column_3_subplots()
#
# Description:
# 3 column subplots in 1 row.
#
########################################################################################################################
def column_3_subplots(
        series0,
        series1,
        series2,
        color0,
        color1,
        color2,
        country,
        title,
        subplot0_title,
        subplot1_title,
        subplot2_title,
        start_yr,
        x_axis_interval,
        ylabels,
        footer_text,
        equiv_yscale,
        x_tick_label_size
):
    fig, ax = plt.subplots(
        1,
        3,
        figsize=(
            user_globals.Constant.FIG_HSIZE_1_ROW.value,
            user_globals.Constant.FIG_VSIZE_1_ROW_TALL.value,
        ),
    )

    # Grey edges for black columns.
    if color0 == 'black':
        edge_color0 = 'dimgrey'
    else:
        edge_color0 = 'black'
    if color1 == 'black':
        edge_color1 = 'dimgrey'
    else:
        edge_color1 = 'black'
    if color2 == 'black':
        edge_color2 = 'dimgrey'
    else:
        edge_color2 = 'black'

    max_val = max(series0.max(), series1.max(), series2.max())
    # Subplot 1
    # If nil data plot line, else plot column chart.
    if series0.max() == 0:
        ax[0].plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    elif series0.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0].plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )

    # Repeat above for second and third subplots.
    if series1.max() == 0:
        ax[1].plot(
            series1.truncate(before=start_yr).index,
            pd.Series(0, series1.truncate(before=start_yr).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    elif series1.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1].plot(
            series1.truncate(before=start_yr).index,
            pd.Series(0, series1.truncate(before=start_yr).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            width=1,
            align='center',
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )

    if series2.max() == 0:
        ax[2].plot(
            series2.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    elif series2.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2].plot(
            series2.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )

    ax[0].set_facecolor('whitesmoke')
    ax[1].set_facecolor('whitesmoke')
    ax[2].set_facecolor('whitesmoke')

    # Configure x-axes.
    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series0.index:
        if year % x_axis_interval == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if series0.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series0.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series0.index.max()

    ax[0].set_xticks(x_ticks, labels=x_ticks)
    ax[1].set_xticks(x_ticks, labels=x_ticks)
    ax[2].set_xticks(x_ticks, labels=x_ticks)

    ax[0].tick_params(axis='x', labelsize=x_tick_label_size)
    ax[1].tick_params(axis='x', labelsize=x_tick_label_size)
    ax[2].tick_params(axis='x', labelsize=x_tick_label_size)

    ax[1].set_xlabel('Year')

    # Remove margins.
    ax[0].margins(x=0)
    ax[1].margins(x=0)
    ax[2].margins(x=0)

    # Configure y-axes.
    if max_val == 0:
        ax[0].set_ylim(0, 5)
        ax[1].set_ylim(0, 5)
        ax[2].set_ylim(0, 5)
    else:
        # Autoscale and get max-y for setting equiv y-axis scale.
        ax[0].autoscale(axis='y')
        ax[1].autoscale(axis='y')
        ax[2].autoscale(axis='y')
        ylim0 = ax[0].get_ylim()[1]
        ylim1 = ax[1].get_ylim()[1]
        ylim2 = ax[2].get_ylim()[1]

        # Apply equivalent scale to all subplots if set.
        if equiv_yscale:
            y_max = max(ylim0, ylim1, ylim2)
            ax[0].set_ylim(0, y_max)
            ax[1].set_ylim(0, y_max)
            ax[2].set_ylim(0, y_max)
        # Force uppermost tick to be equal to next tick after ylim
        ax[0].set_ylim(0, max(ax[0].get_yticks()))
        ax[1].set_ylim(0, max(ax[1].get_yticks()))
        ax[2].set_ylim(0, max(ax[2].get_yticks()))

        ax[0].yaxis.grid(True)
        ax[1].yaxis.grid(True)
        ax[2].yaxis.grid(True)

    ax[0].set_box_aspect(1)
    ax[1].set_box_aspect(1)
    ax[2].set_box_aspect(1)

    # Place grid behind columns.
    ax[0].set_axisbelow(True)
    ax[1].set_axisbelow(True)
    ax[2].set_axisbelow(True)

    ax[0].set_ylabel(ylabels)

    # Add comma thousands seperator to y-labels.
    ax[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[2].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))

    # Remove ticks from y-axis
    ax[1].tick_params(axis='y', labelleft=False, length=0)
    ax[2].tick_params(axis='y', labelleft=False, length=0)

    # Adjust whitespace around plot area.
    plt.subplots_adjust(left=0.05, right=0.98, top=0.99, bottom=0.065, wspace=0.15)

    # Add plot text.
    ax[0].set_title(
        subplot0_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='center',
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1].set_title(
        subplot1_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='center',
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2].set_title(
        subplot2_title,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='center',
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    fig.suptitle(
        country,
        x=0.05,
        y=0.93,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.88,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.12,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: line_6_subplots()
#
# Description:
# 2 rows of 3 line subplots
#
########################################################################################################################
def line_6_subplots(
        series0,
        series1,
        series2,
        series3,
        series4,
        series5,
        color0,
        color1,
        color2,
        color3,
        color4,
        color5,
        country,
        title,
        subplot0_title,
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
        3,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )

    ax[0, 0].plot(
        series0.truncate(before=start_yr).index,
        series0.truncate(before=start_yr),
        color0,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 1].plot(
        series1.truncate(before=start_yr).index,
        series1.truncate(before=start_yr),
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[0, 2].plot(
        series2.truncate(before=start_yr).index,
        series2.truncate(before=start_yr),
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 0].plot(
        series3.truncate(before=start_yr).index,
        series3.truncate(before=start_yr),
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 1].plot(
        series4.truncate(before=start_yr).index,
        series4.truncate(before=start_yr),
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )
    ax[1, 2].plot(
        series5.truncate(before=start_yr).index,
        series5.truncate(before=start_yr),
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_SUBPLOT.value,
    )

    ax[0, 0].set_facecolor('whitesmoke')
    ax[0, 1].set_facecolor('whitesmoke')
    ax[0, 2].set_facecolor('whitesmoke')
    ax[0, 3].set_facecolor('whitesmoke')
    ax[0, 4].set_facecolor('whitesmoke')
    ax[0, 5].set_facecolor('whitesmoke')

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = [start_yr]
    for year in series0.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # If period between final tick and year of final value is >= 3 years, then there's room to append most recent year.
    # Else replace final value with most recent year.
    if series0.index.max() - max(x_ticks) >= 3:
        x_ticks.append(series0.index.max())
    else:
        x_ticks[len(x_ticks) - 1] = series0.index.max()
    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].margins(x=0, tight=True)
    ax[0, 1].margins(x=0, tight=True)
    ax[0, 2].margins(x=0, tight=True)
    ax[1, 0].margins(x=0, tight=True)
    ax[1, 1].margins(x=0, tight=True)
    ax[1, 2].margins(x=0, tight=True)

    ax[1, 0].set_xlabel('Year')
    ax[1, 1].set_xlabel('Year')
    ax[1, 2].set_xlabel('Year')

    ax[0, 0].autoscale(axis='y')
    ax[0, 1].autoscale(axis='y')
    ax[0, 2].autoscale(axis='y')
    ax[1, 0].autoscale(axis='y')
    ax[1, 1].autoscale(axis='y')
    ax[1, 2].autoscale(axis='y')

    ylim0 = ax[0, 0].get_ylim()[1]
    ylim1 = ax[0, 1].get_ylim()[1]
    ylim2 = ax[0, 2].get_ylim()[1]
    ylim3 = ax[1, 0].get_ylim()[1]
    ylim4 = ax[1, 1].get_ylim()[1]
    ylim5 = ax[1, 2].get_ylim()[1]

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim0, ylim1, ylim2, ylim3, ylim4, ylim5)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)

        # Force uppermost tick to be equal to next tick after ylim
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))

    ax[0, 0].set_ylabel(ylabel)
    ax[1, 0].set_ylabel(ylabel)

    ax[0, 0].set_box_aspect(1)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].set_box_aspect(1)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].set_box_aspect(1)

    plt.subplots_adjust(
        left=0, right=0.68, top=0.92, bottom=0.1, wspace=0, hspace=0.14
    )

    ax[0, 0].set_title(
        subplot0_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 1].set_title(
        subplot1_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[0, 2].set_title(
        subplot2_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 0].set_title(
        subplot3_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 1].set_title(
        subplot4_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    ax[1, 2].set_title(
        subplot5_title,
        loc='left',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
    )

    fig.suptitle(
        country,
        x=0.012,
        y=0.99,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.012,
        0.955,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.012,
        0.05,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: column_6_subplots()
#
# Description:
# 2 rows of 3 column subplots
#
########################################################################################################################
def column_6_subplots(
        series0,
        series1,
        series2,
        series3,
        series4,
        series5,
        color0,
        color1,
        color2,
        color3,
        color4,
        color5,
        country,
        title,
        subplot0_title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        start_yr,
        ylabel_top,
        ylabel_bottom,
        footer_text,
        equiv_yscale,
):
    fig, ax = plt.subplots(
        2,
        3,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2_ROW.value,
        ),
    )
    if color0 == 'black':
        edge_color0 = 'dimgrey'
    else:
        edge_color0 = 'black'
    if color1 == 'black':
        edge_color1 = 'dimgrey'
    else:
        edge_color1 = 'black'
    if color2 == 'black':
        edge_color2 = 'dimgrey'
    else:
        edge_color2 = 'black'
    if color3 == 'black':
        edge_color3 = 'dimgrey'
    else:
        edge_color3 = 'black'
    if color4 == 'black':
        edge_color4 = 'dimgrey'
    else:
        edge_color4 = 'black'
    if color5 == 'black':
        edge_color5 = 'dimgrey'
    else:
        edge_color5 = 'black'

    max_val = max(series0.max(), series1.max(), series2.max(), series3.max(), series4.max(), series5.max())

    # If the max value of a series is less than user_globals.Constant.COL_TO_LINE.value, first plot a bar to position
    # x-ticks in centre of columns, and then plot a line at 0 to show a line. A bar of zero height doesn't display, and
    # if a line only is plotted, then x-ticks are aligned at edges of axes, interfering with adjacent chart(s).

    if series0.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
        ax[0, 0].plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
    if series1.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 1].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
        ax[0, 1].plot(
            series1.truncate(before=start_yr).index,
            pd.Series(0, series1.truncate(before=start_yr).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 1].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    if series2.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 2].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
        ax[0, 2].plot(
            series2.truncate(before=start_yr).index,
            pd.Series(0, series2.truncate(before=start_yr).index),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 2].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    if series3.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 0].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
        ax[1, 0].plot(
            series3.truncate(before=start_yr).index,
            pd.Series(0, series3.truncate(before=start_yr).index),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    if series4.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 1].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
        ax[1, 1].plot(
            series4.truncate(before=start_yr).index,
            pd.Series(0, series4.truncate(before=start_yr).index),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 1].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    if series5.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 2].bar(
            series5.truncate(before=start_yr).index,
            0,
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,)
        ax[1, 2].plot(
            series5.truncate(before=start_yr).index,
            pd.Series(0, series5.truncate(before=start_yr).index),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 2].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )

    ax[0, 0].set_facecolor('whitesmoke')
    ax[0, 1].set_facecolor('whitesmoke')
    ax[0, 2].set_facecolor('whitesmoke')
    ax[1, 0].set_facecolor('whitesmoke')
    ax[1, 1].set_facecolor('whitesmoke')
    ax[1, 2].set_facecolor('whitesmoke')

    ax[0, 0].margins(x=0)
    ax[0, 1].margins(x=0)
    ax[0, 2].margins(x=0)
    ax[1, 0].margins(x=0)
    ax[1, 1].margins(x=0)
    ax[1, 2].margins(x=0)

    ax[1, 1].set_xlabel('Year', fontsize='medium', labelpad=4)

    # Create list x_ticks. For clarity include only year 2000, final year, and (about) the year halfway between.
    x_ticks = [start_yr, round((series0.index.max() - start_yr) / 2) + start_yr, series0.index.max()]

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].tick_params(axis='x', labelbottom=False, length=0)
    ax[0, 1].tick_params(axis='x', labelbottom=False, length=0)
    ax[0, 2].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 0].tick_params(axis='x', labelsize=8)
    ax[1, 1].tick_params(axis='x', labelsize=8)
    ax[1, 2].tick_params(axis='x', labelsize=8)

    ax[0, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[0, 2].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 2].tick_params(axis='y', labelleft=False, length=0)

    ax[0, 0].set_ylabel(ylabel_top)
    ax[1, 0].set_ylabel(ylabel_bottom)

    ax[0, 0].yaxis.grid(True)
    ax[0, 1].yaxis.grid(True)
    ax[0, 2].yaxis.grid(True)
    ax[1, 0].yaxis.grid(True)
    ax[1, 1].yaxis.grid(True)
    ax[1, 2].yaxis.grid(True)

    ax[0, 0].set_box_aspect(1)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].set_box_aspect(1)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].set_box_aspect(1)

    ax[0, 0].autoscale(axis='y')
    ax[0, 1].autoscale(axis='y')
    ax[0, 2].autoscale(axis='y')
    ax[1, 0].autoscale(axis='y')
    ax[1, 1].autoscale(axis='y')
    ax[1, 2].autoscale(axis='y')

    ylim0 = ax[0, 0].get_ylim()[1]
    ylim1 = ax[0, 1].get_ylim()[1]
    ylim2 = ax[0, 2].get_ylim()[1]
    ylim3 = ax[1, 0].get_ylim()[1]
    ylim4 = ax[1, 1].get_ylim()[1]
    ylim5 = ax[1, 2].get_ylim()[1]

    ax[0, 0].set_axisbelow(True)
    ax[0, 1].set_axisbelow(True)
    ax[0, 2].set_axisbelow(True)
    ax[1, 0].set_axisbelow(True)
    ax[1, 1].set_axisbelow(True)
    ax[1, 2].set_axisbelow(True)

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim0, ylim1, ylim2, ylim3, ylim4, ylim5)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)

        # Force uppermost tick to be equal to next tick after ylim
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))

    # Add comma thousands seperator to y-labels.
    ax[0, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))

    plt.subplots_adjust(left=0.04, right=0.72, top=0.945, bottom=0.105, hspace=0.03, wspace=0)

    ax[0, 0].set_title(
        subplot0_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[0, 1].set_title(
        subplot1_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[0, 2].set_title(
        subplot2_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 0].set_title(
        subplot3_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 1].set_title(
        subplot4_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 2].set_title(
        subplot5_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    fig.suptitle(
        country,
        x=0.045,
        y=0.995,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.045,
        0.955,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.045,
        0.06,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: column_8_subplots()
#
# Description:
# 2 rows of 4 column subplots
#
########################################################################################################################
def column_8_subplots(
        series0,
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        color0,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        color7,
        country,
        title,
        subplot0_title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        subplot7_title,
        start_yr,
        ylabel_top,
        ylabel_bottom,
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
    if color0 == 'black' or color0 == 'midnightblue':
        edge_color0 = 'dimgrey'
    else:
        edge_color0 = 'black'

    if color1 == 'black' or color1 == 'midnightblue':
        edge_color1 = 'dimgrey'
    else:
        edge_color1 = 'black'

    if color2 == 'black' or color2 == 'midnightblue':
        edge_color2 = 'dimgrey'
    else:
        edge_color2 = 'black'

    if color3 == 'black' or color3 == 'midnightblue':
        edge_color3 = 'dimgrey'
    else:
        edge_color3 = 'black'

    if color4 == 'black' or color4 == 'midnightblue':
        edge_color4 = 'dimgrey'
    else:
        edge_color4 = 'black'

    if color5 == 'black' or color5 == 'midnightblue':
        edge_color5 = 'dimgrey'
    else:
        edge_color5 = 'black'

    if color6 == 'black' or color6 == 'midnightblue':
        edge_color6 = 'dimgrey'
    else:
        edge_color6 = 'black'

    if color7 == 'black' or color7 == 'midnightblue':
        edge_color7 = 'dimgrey'
    else:
        edge_color7 = 'black'

    max_val = max(series0.max(), series1.max(), series2.max(), series3.max(), series4.max(), series5.max(),
                  series6.max(), series7.max())

    # If the max value of a series is less than user_globals.Constant.COL_TO_LINE.value, first plot a bar to position
    # x-ticks in centre of columns, and then plot a line at 0 to show a line. A bar of zero height doesn't display, and
    # if a line only is plotted, then x-ticks are aligned at edges of axes, interfering with adjacent chart(s).

    if series0.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
        ax[0, 0].plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
    if series1.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 1].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
        ax[0, 1].plot(
            series1.truncate(before=start_yr).index,
            pd.Series(0, series1.truncate(before=start_yr).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 1].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    if series2.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 2].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
        ax[0, 2].plot(
            series2.truncate(before=start_yr).index,
            pd.Series(0, series2.truncate(before=start_yr).index),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 2].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    if series3.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 3].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
        ax[0, 3].plot(
            series3.truncate(before=start_yr).index,
            pd.Series(0, series3.truncate(before=start_yr).index),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 3].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    if series4.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 0].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
        ax[1, 0].plot(
            series4.truncate(before=start_yr).index,
            pd.Series(0, series4.truncate(before=start_yr).index),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    if series5.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 1].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
        ax[1, 1].plot(
            series5.truncate(before=start_yr).index,
            pd.Series(0, series5.truncate(before=start_yr).index),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 1].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
    if series6.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 2].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align='center',
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
        ax[1, 2].plot(
            series6.truncate(before=start_yr).index,
            pd.Series(0, series6.truncate(before=start_yr).index),
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 2].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align='center',
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
    if series7.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 3].bar(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            width=1,
            align='center',
            color=color7,
            edgecolor=edge_color7,
            linewidth=0.2,
        )
        ax[1, 3].plot(
            series7.truncate(before=start_yr).index,
            pd.Series(0, series7.truncate(before=start_yr).index),
            color7,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 3].bar(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            width=1,
            align='center',
            color=color7,
            edgecolor=edge_color7,
            linewidth=0.2,
        )

    ax[0, 0].set_facecolor('whitesmoke')
    ax[0, 1].set_facecolor('whitesmoke')
    ax[0, 2].set_facecolor('whitesmoke')
    ax[0, 3].set_facecolor('whitesmoke')
    ax[1, 0].set_facecolor('whitesmoke')
    ax[1, 1].set_facecolor('whitesmoke')
    ax[1, 2].set_facecolor('whitesmoke')
    ax[1, 3].set_facecolor('whitesmoke')

    ax[0, 0].margins(x=0)
    ax[0, 1].margins(x=0)
    ax[0, 2].margins(x=0)
    ax[0, 3].margins(x=0)
    ax[1, 0].margins(x=0)
    ax[1, 1].margins(x=0)
    ax[1, 2].margins(x=0)
    ax[1, 3].margins(x=0)

    # Create list x_ticks. For clarity include only year 2000, final year, and (about) the year halfway between.
    x_ticks = [start_yr, round((series0.index.max() - start_yr) / 2) + start_yr, series0.index.max()]

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 3].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].tick_params(axis='x', labelbottom=False, length=0)
    ax[0, 1].tick_params(axis='x', labelbottom=False, length=0)
    ax[0, 2].tick_params(axis='x', labelbottom=False, length=0)
    ax[0, 3].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 0].tick_params(axis='x', labelsize=9)
    ax[1, 1].tick_params(axis='x', labelsize=9)
    ax[1, 2].tick_params(axis='x', labelsize=9)
    ax[1, 3].tick_params(axis='x', labelsize=9)

    ax[0, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[0, 2].tick_params(axis='y', labelleft=False, length=0)
    ax[0, 3].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 2].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 3].tick_params(axis='y', labelleft=False, length=0)

    ax[0, 0].set_ylabel(ylabel_top)
    ax[1, 0].set_ylabel(ylabel_bottom)

    ax[0, 0].yaxis.grid(True)
    ax[0, 1].yaxis.grid(True)
    ax[0, 2].yaxis.grid(True)
    ax[0, 3].yaxis.grid(True)
    ax[1, 0].yaxis.grid(True)
    ax[1, 1].yaxis.grid(True)
    ax[1, 2].yaxis.grid(True)
    ax[1, 3].yaxis.grid(True)

    ax[0, 0].set_box_aspect(1)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].set_box_aspect(1)
    ax[0, 3].set_box_aspect(1)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].set_box_aspect(1)
    ax[1, 3].set_box_aspect(1)

    ax[0, 0].autoscale(axis='y')
    ax[0, 1].autoscale(axis='y')
    ax[0, 2].autoscale(axis='y')
    ax[0, 3].autoscale(axis='y')
    ax[1, 0].autoscale(axis='y')
    ax[1, 1].autoscale(axis='y')
    ax[1, 2].autoscale(axis='y')
    ax[1, 3].autoscale(axis='y')

    ylim0 = ax[0, 0].get_ylim()[1]
    ylim1 = ax[0, 1].get_ylim()[1]
    ylim2 = ax[0, 2].get_ylim()[1]
    ylim3 = ax[0, 3].get_ylim()[1]
    ylim4 = ax[1, 0].get_ylim()[1]
    ylim5 = ax[1, 1].get_ylim()[1]
    ylim6 = ax[1, 2].get_ylim()[1]
    ylim7 = ax[1, 3].get_ylim()[1]

    ax[0, 0].set_axisbelow(True)
    ax[0, 1].set_axisbelow(True)
    ax[0, 2].set_axisbelow(True)
    ax[0, 3].set_axisbelow(True)
    ax[1, 0].set_axisbelow(True)
    ax[1, 1].set_axisbelow(True)
    ax[1, 2].set_axisbelow(True)
    ax[1, 3].set_axisbelow(True)

    # Apply equivalent y scale to all subplots if set.
    if equiv_yscale:
        y_max = max(ylim0, ylim1, ylim2, ylim3, ylim4, ylim5, ylim6, ylim7)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)
        ax[1, 3].set_ylim(0, y_max)

        # Force uppermost tick to be equal to next tick after ylim
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))
        ax[1, 3].set_ylim(0, max(ax[1, 2].get_yticks()))

    # Add comma thousands seperator to y-labels.
    ax[0, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))

    plt.subplots_adjust(left=0.04, right=0.96, top=0.945, bottom=0.105, hspace=0.03, wspace=0)

    ax[0, 0].set_title(
        subplot0_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[0, 1].set_title(
        subplot1_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[0, 2].set_title(
        subplot2_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[0, 3].set_title(
        subplot3_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 0].set_title(
        subplot4_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 1].set_title(
        subplot5_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 2].set_title(
        subplot6_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 3].set_title(
        subplot7_title,
        loc='center',
        size=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    fig.suptitle(
        country,
        x=0.045,
        y=0.995,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.045,
        0.955,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.045,
        0.06,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )
    fig.text(
        0.505,
        0.08,
        'Year',
        horizontalalignment='center',
        verticalalignment='top',
        fontsize='medium',
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: line_10_subplots()
#
# Description:
# 2 rows of 5 line subplots.
#
########################################################################################################################
def line_10_subplots(
        series0,
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        series8,
        series9,
        color0,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        color7,
        color8,
        color9,
        country,
        title,
        subplot0_title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        subplot7_title,
        subplot8_title,
        subplot9_title,
        start_yr,
        ylabel,
        footer_text,
        equiv_yscale,
):
    fig, ax = plt.subplots(
        2,
        5,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_2_ROW.value,
            user_globals.Constant.FIG_VSIZE_2x5.value,
        ),
    )
    ax[0, 0].plot(
        series0.truncate(before=start_yr).index,
        series0.truncate(before=start_yr),
        color0,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[0, 1].plot(
        series1.truncate(before=start_yr).index,
        series1.truncate(before=start_yr),
        color1,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[0, 2].plot(
        series2.truncate(before=start_yr).index,
        series2.truncate(before=start_yr),
        color2,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[0, 3].plot(
        series3.truncate(before=start_yr).index,
        series3.truncate(before=start_yr),
        color3,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[0, 4].plot(
        series4.truncate(before=start_yr).index,
        series4.truncate(before=start_yr),
        color4,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[1, 0].plot(
        series5.truncate(before=start_yr).index,
        series5.truncate(before=start_yr),
        color5,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[1, 1].plot(
        series6.truncate(before=start_yr).index,
        series6.truncate(before=start_yr),
        color6,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[1, 2].plot(
        series7.truncate(before=start_yr).index,
        series7.truncate(before=start_yr),
        color7,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[1, 3].plot(
        series8.truncate(before=start_yr).index,
        series8.truncate(before=start_yr),
        color8,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )
    ax[1, 4].plot(
        series9.truncate(before=start_yr).index,
        series9.truncate(before=start_yr),
        color9,
        linewidth=user_globals.Constant.LINE_WIDTH_10_SUBPLOT.value,
    )

    ax[0, 0].set_facecolor('whitesmoke')
    ax[0, 1].set_facecolor('whitesmoke')
    ax[0, 2].set_facecolor('whitesmoke')
    ax[0, 3].set_facecolor('whitesmoke')
    ax[0, 4].set_facecolor('whitesmoke')
    ax[1, 0].set_facecolor('whitesmoke')
    ax[1, 1].set_facecolor('whitesmoke')
    ax[1, 2].set_facecolor('whitesmoke')
    ax[1, 3].set_facecolor('whitesmoke')
    ax[1, 4].set_facecolor('whitesmoke')

    # Create list x_ticks. For clarity include only year 2000, final year, and the year (about) halfway between.
    x_ticks = [start_yr, round((series0.index.max() - start_yr) / 2) + start_yr, series0.index.max()]

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[0, 4].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 4].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].margins(x=0)
    ax[0, 1].margins(x=0)
    ax[0, 2].margins(x=0)
    ax[0, 3].margins(x=0)
    ax[0, 4].margins(x=0)
    ax[1, 0].margins(x=0)
    ax[1, 1].margins(x=0)
    ax[1, 2].margins(x=0)
    ax[1, 3].margins(x=0)
    ax[1, 4].margins(x=0)

    ax[1, 2].set_xlabel('Year')

    ax[0, 0].set_ylabel(ylabel)
    ax[1, 0].set_ylabel(ylabel)

    ax[0, 0].yaxis.grid(True)
    ax[0, 1].yaxis.grid(True)
    ax[0, 2].yaxis.grid(True)
    ax[0, 3].yaxis.grid(True)
    ax[0, 4].yaxis.grid(True)
    ax[1, 0].yaxis.grid(True)
    ax[1, 1].yaxis.grid(True)
    ax[1, 2].yaxis.grid(True)
    ax[1, 3].yaxis.grid(True)
    ax[1, 4].yaxis.grid(True)

    ax[0, 0].set_axisbelow(True)
    ax[0, 1].set_axisbelow(True)
    ax[0, 2].set_axisbelow(True)
    ax[0, 3].set_axisbelow(True)
    ax[0, 4].set_axisbelow(True)
    ax[1, 0].set_axisbelow(True)
    ax[1, 1].set_axisbelow(True)
    ax[1, 2].set_axisbelow(True)
    ax[1, 3].set_axisbelow(True)
    ax[1, 4].set_axisbelow(True)

    ax[0, 0].autoscale(axis='y')
    ax[0, 1].autoscale(axis='y')
    ax[0, 2].autoscale(axis='y')
    ax[0, 3].autoscale(axis='y')
    ax[0, 4].autoscale(axis='y')
    ax[1, 0].autoscale(axis='y')
    ax[1, 1].autoscale(axis='y')
    ax[1, 2].autoscale(axis='y')
    ax[1, 3].autoscale(axis='y')
    ax[1, 4].autoscale(axis='y')

    ylim0 = ax[0, 0].get_ylim()[1]
    ylim1 = ax[0, 1].get_ylim()[1]
    ylim2 = ax[0, 2].get_ylim()[1]
    ylim3 = ax[0, 3].get_ylim()[1]
    ylim4 = ax[0, 4].get_ylim()[1]
    ylim5 = ax[1, 0].get_ylim()[1]
    ylim6 = ax[1, 1].get_ylim()[1]
    ylim7 = ax[1, 2].get_ylim()[1]
    ylim8 = ax[1, 3].get_ylim()[1]
    ylim9 = ax[1, 4].get_ylim()[1]

    ax[0, 0].set_box_aspect(1)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].set_box_aspect(1)
    ax[0, 3].set_box_aspect(1)
    ax[0, 4].set_box_aspect(1)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].set_box_aspect(1)
    ax[1, 3].set_box_aspect(1)
    ax[1, 4].set_box_aspect(1)

    ax[0, 0].tick_params(labelsize=10, labelbottom=False)
    ax[0, 0].tick_params(axis='x', length=0)

    ax[1, 0].tick_params(axis='x', labelsize=7)
    ax[1, 1].tick_params(axis='x', labelsize=7)
    ax[1, 2].tick_params(axis='x', labelsize=7)
    ax[1, 3].tick_params(axis='x', labelsize=7)
    ax[1, 4].tick_params(axis='x', labelsize=7)

    ax[0, 1].tick_params(length=0, labelleft=False, labelbottom=False)
    ax[0, 2].tick_params(length=0, labelleft=False, labelbottom=False)
    ax[0, 3].tick_params(length=0, labelleft=False, labelbottom=False)
    ax[0, 4].tick_params(length=0, labelleft=False, labelbottom=False)

    ax[1, 1].tick_params(axis='y', length=0, labelleft=False)
    ax[1, 2].tick_params(axis='y', length=0, labelleft=False)
    ax[1, 3].tick_params(axis='y', length=0, labelleft=False)
    ax[1, 4].tick_params(axis='y', length=0, labelleft=False)

    # Apply equivalent y scale to all subplots if set except first subplot.
    if equiv_yscale:
        y_max = max(ylim0, ylim1, ylim2, ylim3, ylim4, ylim5, ylim6, ylim7, ylim8, ylim9)
        ax[0, 0].set_ylim(0, y_max)
        ax[0, 1].set_ylim(0, y_max)
        ax[0, 2].set_ylim(0, y_max)
        ax[0, 3].set_ylim(0, y_max)
        ax[0, 4].set_ylim(0, y_max)
        ax[1, 0].set_ylim(0, y_max)
        ax[1, 1].set_ylim(0, y_max)
        ax[1, 2].set_ylim(0, y_max)
        ax[1, 3].set_ylim(0, y_max)
        ax[1, 4].set_ylim(0, y_max)
        # Force uppermost tick to be equal to next tick after ylim
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[0, 1].set_ylim(0, max(ax[0, 1].get_yticks()))
        ax[0, 2].set_ylim(0, max(ax[0, 2].get_yticks()))
        ax[0, 3].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[0, 4].set_ylim(0, max(ax[0, 3].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))
        ax[1, 3].set_ylim(0, max(ax[1, 3].get_yticks()))
        ax[1, 4].set_ylim(0, max(ax[0, 3].get_yticks()))

    ax[0, 0].set_title(
        subplot0_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[0, 1].set_title(
        subplot1_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[0, 2].set_title(
        subplot2_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[0, 3].set_title(
        subplot3_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[0, 4].set_title(
        subplot4_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[1, 0].set_title(
        subplot5_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[1, 1].set_title(
        subplot6_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[1, 2].set_title(
        subplot7_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[1, 3].set_title(
        subplot8_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )
    ax[1, 4].set_title(
        subplot9_title,
        loc='center',
        fontsize=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_SIZE.value,
        weight=user_globals.Constant.SUBPLOT_2ROW_TITLE_FONT_WEIGHT.value,
        y=0.98,
    )

    plt.subplots_adjust(left=0.02, right=0.99, top=0.9, bottom=0.1, hspace=0.11, wspace=0)

    fig.suptitle(
        country,
        x=0.027,
        y=0.985,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )

    fig.text(
        0.027,
        0.94,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.027,
        0.05,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )

    fig.patches.extend([plt.Rectangle((0.027, 0.1), 0.38, 0.83, linewidth=1.8,
                                      fill=False, color='darkslateblue', alpha=0.9, ls='dashed',
                                      transform=fig.transFigure, figure=fig)])


########################################################################################################################
#
# Function: column_11_subplots()
#
# Description:
# 11 column subplots; 1 in first row, 5 in each of two rows underneath.
#
########################################################################################################################
def column_11_subplots(
        series0,
        series1,
        series2,
        series3,
        series4,
        series5,
        series6,
        series7,
        series8,
        series9,
        series10,
        color0,
        color1,
        color2,
        color3,
        color4,
        color5,
        color6,
        color7,
        color8,
        color9,
        color10,
        country,
        title,
        subplot0_title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        subplot4_title,
        subplot5_title,
        subplot6_title,
        subplot7_title,
        subplot8_title,
        subplot9_title,
        subplot10_title,
        start_yr,
        ylabel_top,
        ylabel,
        footer_text,
        equiv_yscale,
):
    fig, ax = plt.subplots(
        3,
        5,
        sharex=False,
        sharey=False,
        figsize=(
            user_globals.Constant.FIG_HSIZE_3_ROW.value,
            user_globals.Constant.FIG_VSIZE_3_ROW.value,
        ),
    )

    if color0 == 'black':
        edge_color0 = 'dimgrey'
    else:
        edge_color0 = 'black'
    if color1 == 'black':
        edge_color1 = 'dimgrey'
    else:
        edge_color1 = 'black'
    if color2 == 'black':
        edge_color2 = 'dimgrey'
    else:
        edge_color2 = 'black'
    if color3 == 'black':
        edge_color3 = 'dimgrey'
    else:
        edge_color3 = 'black'
    if color4 == 'black':
        edge_color4 = 'dimgrey'
    else:
        edge_color4 = 'black'
    if color5 == 'black':
        edge_color5 = 'dimgrey'
    else:
        edge_color5 = 'black'
    if color6 == 'black':
        edge_color6 = 'dimgrey'
    else:
        edge_color6 = 'black'
    if color7 == 'black':
        edge_color7 = 'dimgrey'
    else:
        edge_color7 = 'black'
    if color8 == 'black':
        edge_color8 = 'dimgrey'
    else:
        edge_color8 = 'black'
    if color9 == 'black':
        edge_color9 = 'dimgrey'
    else:
        edge_color9 = 'black'
    if color10 == 'black':
        edge_color10 = 'dimgrey'
    else:
        edge_color10 = 'black'

    max_val = max(series0.max(), series1.max(), series2.max(), series3.max(), series4.max(), series5.max(),
                  series6.max(), series7.max(), series8.max(), series9.max(), series10.max())
    # If a line must be plotted, first plot a bar chart in order to align x-axis ticks to prevent
    # clashing with those of adjacent subplots.
    if series0.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
        ax[0, 0].plot(
            series0.truncate(before=start_yr).index,
            pd.Series(0, series0.truncate(before=start_yr).index),
            color0,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[0, 0].bar(
            series0.truncate(before=start_yr).index,
            series0.truncate(before=start_yr),
            width=1,
            align='center',
            color=color0,
            edgecolor=edge_color0,
            linewidth=0.2,
        )
    if series1.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
        ax[1, 0].plot(
            series1.truncate(before=start_yr).index,
            pd.Series(0, series1.truncate(before=start_yr).index),
            color1,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 0].bar(
            series1.truncate(before=start_yr).index,
            series1.truncate(before=start_yr),
            align='center',
            width=1,
            color=color1,
            edgecolor=edge_color1,
            linewidth=0.2,
        )
    if series2.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
        ax[1, 1].plot(
            series2.truncate(before=start_yr).index,
            pd.Series(0, series2.truncate(before=start_yr).index),
            color2,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 1].bar(
            series2.truncate(before=start_yr).index,
            series2.truncate(before=start_yr),
            width=1,
            align='center',
            color=color2,
            edgecolor=edge_color2,
            linewidth=0.2,
        )
    if series3.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
        ax[1, 2].plot(
            series3.truncate(before=start_yr).index,
            pd.Series(0, series3.truncate(before=start_yr).index),
            color3,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 2].bar(
            series3.truncate(before=start_yr).index,
            series3.truncate(before=start_yr),
            width=1,
            align='center',
            color=color3,
            edgecolor=edge_color3,
            linewidth=0.2,
        )
    if series4.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
        ax[1, 3].plot(
            series4.truncate(before=start_yr).index,
            pd.Series(0, series4.truncate(before=start_yr).index),
            color4,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 3].bar(
            series4.truncate(before=start_yr).index,
            series4.truncate(before=start_yr),
            width=1,
            align='center',
            color=color4,
            edgecolor=edge_color4,
            linewidth=0.2,
        )
    if series5.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[1, 4].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
        ax[1, 4].plot(
            series5.truncate(before=start_yr).index,
            pd.Series(0, series5.truncate(before=start_yr).index),
            color5,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[1, 4].bar(
            series5.truncate(before=start_yr).index,
            series5.truncate(before=start_yr),
            width=1,
            align='center',
            color=color5,
            edgecolor=edge_color5,
            linewidth=0.2,
        )
    if series6.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2, 0].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align='center',
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
        ax[2, 0].plot(
            series6.truncate(before=start_yr).index,
            pd.Series(0, series6.truncate(before=start_yr).index),
            color6,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2, 0].bar(
            series6.truncate(before=start_yr).index,
            series6.truncate(before=start_yr),
            width=1,
            align='center',
            color=color6,
            edgecolor=edge_color6,
            linewidth=0.2,
        )
    if series7.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2, 1].bar(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            width=1,
            align='center',
            color=color7,
            edgecolor=edge_color7,
            linewidth=0.2,
        )
        ax[2, 1].plot(
            series7.truncate(before=start_yr).index,
            pd.Series(0, series7.truncate(before=start_yr).index),
            color7,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2, 1].bar(
            series7.truncate(before=start_yr).index,
            series7.truncate(before=start_yr),
            width=1,
            align='center',
            color=color7,
            edgecolor=edge_color7,
            linewidth=0.2,
        )
    if series8.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2, 2].bar(
            series8.truncate(before=start_yr).index,
            series8.truncate(before=start_yr),
            width=1,
            align='center',
            color=color8,
            edgecolor=edge_color8,
            linewidth=0.2,
        )
        ax[2, 2].plot(
            series8.truncate(before=start_yr).index,
            pd.Series(0, series8.truncate(before=start_yr).index),
            color8,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2, 2].bar(
            series8.truncate(before=start_yr).index,
            series8.truncate(before=start_yr),
            width=1,
            align='center',
            color=color8,
            edgecolor=edge_color8,
            linewidth=0.2,
        )
    if series9.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2, 3].bar(
            series9.truncate(before=start_yr).index,
            series9.truncate(before=start_yr),
            width=1,
            align='center',
            color=color9,
            edgecolor=edge_color9,
            linewidth=0.2,
        )
        ax[2, 3].plot(
            series9.truncate(before=start_yr).index,
            pd.Series(0, series9.truncate(before=start_yr).index),
            color9,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2, 3].bar(
            series9.truncate(before=start_yr).index,
            series9.truncate(before=start_yr),
            width=1,
            align='center',
            color=color9,
            edgecolor=edge_color9,
            linewidth=0.2,
        )
    if series10.max() / max_val < user_globals.Constant.COL_TO_LINE.value:
        ax[2, 4].bar(
            series10.truncate(before=start_yr).index,
            series10.truncate(before=start_yr),
            width=1,
            align='center',
            color=color10,
            edgecolor=edge_color10,
            linewidth=0.2,
        )
        ax[2, 4].plot(
            series10.truncate(before=start_yr).index,
            pd.Series(0, series10.truncate(before=start_yr).index),
            color10,
            linewidth=user_globals.Constant.LINE_WIDTH_0_SUBPLOT.value,
        )
    else:
        ax[2, 4].bar(
            series10.truncate(before=start_yr).index,
            series10.truncate(before=start_yr),
            width=1,
            align='center',
            color=color10,
            edgecolor=edge_color10,
            linewidth=0.2,
        )

    # Hide unused subplots.
    ax[0, 1].set_visible(False)
    ax[0, 2].set_visible(False)
    ax[0, 3].set_visible(False)
    ax[0, 4].set_visible(False)

    # Create list x_ticks. For clarity include only year 2000, final year, and (about) the year halfway between.
    x_ticks = [start_yr, round((series0.index.max() - start_yr) / 2) + start_yr, series0.index.max()]

    ax[0, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[1, 4].set_xticks(x_ticks, labels=x_ticks)
    ax[2, 0].set_xticks(x_ticks, labels=x_ticks)
    ax[2, 1].set_xticks(x_ticks, labels=x_ticks)
    ax[2, 2].set_xticks(x_ticks, labels=x_ticks)
    ax[2, 3].set_xticks(x_ticks, labels=x_ticks)
    ax[2, 4].set_xticks(x_ticks, labels=x_ticks)

    ax[0, 0].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 0].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 1].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 2].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 3].tick_params(axis='x', labelbottom=False, length=0)
    ax[1, 4].tick_params(axis='x', labelbottom=False, length=0)

    ax[0, 0].set_facecolor('whitesmoke')
    ax[1, 0].set_facecolor('whitesmoke')
    ax[1, 1].set_facecolor('whitesmoke')
    ax[1, 2].set_facecolor('whitesmoke')
    ax[1, 3].set_facecolor('whitesmoke')
    ax[1, 4].set_facecolor('whitesmoke')
    ax[2, 0].set_facecolor('whitesmoke')
    ax[2, 1].set_facecolor('whitesmoke')
    ax[2, 2].set_facecolor('whitesmoke')
    ax[2, 3].set_facecolor('whitesmoke')
    ax[2, 4].set_facecolor('whitesmoke')

    ax[0, 0].margins(x=0)
    ax[1, 0].margins(x=0)
    ax[1, 1].margins(x=0)
    ax[1, 2].margins(x=0)
    ax[1, 3].margins(x=0)
    ax[1, 4].margins(x=0)
    ax[2, 0].margins(x=0)
    ax[2, 1].margins(x=0)
    ax[2, 2].margins(x=0)
    ax[2, 3].margins(x=0)
    ax[2, 4].margins(x=0)

    ax[2, 2].set_xlabel('Year', fontsize='medium', labelpad=4)

    ax[1, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 2].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 3].tick_params(axis='y', labelleft=False, length=0)
    ax[1, 4].tick_params(axis='y', labelleft=False, length=0)
    ax[2, 1].tick_params(axis='y', labelleft=False, length=0)
    ax[2, 2].tick_params(axis='y', labelleft=False, length=0)
    ax[2, 3].tick_params(axis='y', labelleft=False, length=0)
    ax[2, 4].tick_params(axis='y', labelleft=False, length=0)

    ax[0, 0].set_ylabel(ylabel_top)
    ax[1, 0].set_ylabel(ylabel)
    ax[2, 0].set_ylabel(ylabel)

    ax[0, 0].yaxis.grid(True)
    ax[1, 0].yaxis.grid(True)
    ax[1, 1].yaxis.grid(True)
    ax[1, 2].yaxis.grid(True)
    ax[1, 3].yaxis.grid(True)
    ax[1, 4].yaxis.grid(True)
    ax[2, 0].yaxis.grid(True)
    ax[2, 1].yaxis.grid(True)
    ax[2, 2].yaxis.grid(True)
    ax[2, 3].yaxis.grid(True)
    ax[2, 4].yaxis.grid(True)

    ax[0, 0].set_axisbelow(True)
    ax[1, 0].set_axisbelow(True)
    ax[1, 1].set_axisbelow(True)
    ax[1, 2].set_axisbelow(True)
    ax[1, 3].set_axisbelow(True)
    ax[1, 4].set_axisbelow(True)
    ax[2, 0].set_axisbelow(True)
    ax[2, 1].set_axisbelow(True)
    ax[2, 2].set_axisbelow(True)
    ax[2, 3].set_axisbelow(True)
    ax[2, 4].set_axisbelow(True)

    ax[0, 0].set_box_aspect(1)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].set_box_aspect(1)
    ax[1, 3].set_box_aspect(1)
    ax[1, 4].set_box_aspect(1)
    ax[2, 0].set_box_aspect(1)
    ax[2, 1].set_box_aspect(1)
    ax[2, 2].set_box_aspect(1)
    ax[2, 3].set_box_aspect(1)
    ax[2, 4].set_box_aspect(1)

    ax[0, 0].tick_params(axis='y', labelsize=8)
    ax[1, 0].tick_params(axis='y', labelsize=8)
    ax[2, 0].tick_params(axis='y', labelsize=8)
    ax[2, 0].tick_params(axis='x', labelsize=7)
    ax[2, 1].tick_params(axis='x', labelsize=7)
    ax[2, 2].tick_params(axis='x', labelsize=7)
    ax[2, 3].tick_params(axis='x', labelsize=7)
    ax[2, 4].tick_params(axis='x', labelsize=7)

    ax[0, 0].autoscale(axis='y', tight=True)
    ax[1, 0].autoscale(axis='y')
    ax[1, 1].autoscale(axis='y')
    ax[1, 2].autoscale(axis='y')
    ax[1, 3].autoscale(axis='y')
    ax[1, 4].autoscale(axis='y')
    ax[2, 0].autoscale(axis='y')
    ax[2, 1].autoscale(axis='y')
    ax[2, 2].autoscale(axis='y')
    ax[2, 3].autoscale(axis='y')
    ax[2, 4].autoscale(axis='y')

    # Apply equivalent y scale to all subplots if set except first subplot.
    ylim1 = ax[0, 0].get_ylim()[1]
    if equiv_yscale:
        ax[0, 0].set_ylim(0, ylim1)
        ax[1, 0].set_ylim(0, ylim1)
        ax[1, 1].set_ylim(0, ylim1)
        ax[1, 2].set_ylim(0, ylim1)
        ax[1, 3].set_ylim(0, ylim1)
        ax[1, 4].set_ylim(0, ylim1)
        ax[2, 0].set_ylim(0, ylim1)
        ax[2, 1].set_ylim(0, ylim1)
        ax[2, 2].set_ylim(0, ylim1)
        ax[2, 3].set_ylim(0, ylim1)
        ax[2, 4].set_ylim(0, ylim1)
        # Force uppermost tick to be equal to next tick after ylim
        ax[0, 0].set_ylim(0, max(ax[0, 0].get_yticks()))
        ax[1, 0].set_ylim(0, max(ax[1, 0].get_yticks()))
        ax[1, 1].set_ylim(0, max(ax[1, 1].get_yticks()))
        ax[1, 2].set_ylim(0, max(ax[1, 2].get_yticks()))
        ax[1, 3].set_ylim(0, max(ax[1, 3].get_yticks()))
        ax[1, 4].set_ylim(0, max(ax[1, 4].get_yticks()))
        ax[2, 0].set_ylim(0, max(ax[2, 0].get_yticks()))
        ax[2, 1].set_ylim(0, max(ax[2, 1].get_yticks()))
        ax[2, 2].set_ylim(0, max(ax[2, 2].get_yticks()))
        ax[2, 3].set_ylim(0, max(ax[2, 3].get_yticks()))
        ax[2, 4].set_ylim(0, max(ax[2, 4].get_yticks()))

    ax[0, 0].set_title(
        subplot0_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 0].set_title(
        subplot1_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 1].set_title(
        subplot2_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 2].set_title(
        subplot3_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 3].set_title(
        subplot4_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[1, 4].set_title(
        subplot5_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2, 0].set_title(
        subplot6_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2, 1].set_title(
        subplot7_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2, 2].set_title(
        subplot8_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2, 3].set_title(
        subplot9_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )
    ax[2, 4].set_title(
        subplot10_title,
        loc='center',
        weight=user_globals.Constant.SUBPLOT_3ROW_TITLE_FONT_WEIGHT.value,
        y=user_globals.Constant.COLUMN_11_SUBPLOT_TITLE_YPOS.value,
        bbox={'facecolor': 'whitesmoke', 'alpha': 0.7},
        va='top',
    )

    # Add comma thousands seperator to y-labels.
    ax[0, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[1, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))
    ax[2, 0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ',')))

    plt.subplots_adjust(left=0.04, right=0.99, top=0.99, bottom=0.04, hspace=0.035, wspace=0)

    fig.suptitle(
        country,
        x=0.425,
        y=0.995,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.425,
        0.96,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.425,
        0.95,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )

    fig.patches.extend([plt.Rectangle((0.043, 0.04), 0.376, 0.954, linewidth=1.8,
                                      fill=False, color='darkslateblue', alpha=0.9, ls='dashed',
                                      transform=fig.transFigure, figure=fig)])


########################################################################################################################
#
# Function: column_grouped()
#
# Description:
# Single figure plot of grouped columns. Plotted values are input as a variable number of series and matching colors.
#
########################################################################################################################
def column_grouped(country, title, y_label, footer_text, *colors, **series):
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_CHANGE_COLUMN_PLOT.value,
            user_globals.Constant.FIG_VSIZE_CHANGE_COLUMN_PLOT.value,
        ),
    )
    start_yr = user_globals.Constant.CHANGE_CHART_START_YR.value
    label_pad = 2
    series_qty = len(series)
    # All columns to total 95% of an x-tick spacing.
    column_width = 0.95 / series_qty
    series_number = 0
    plot_names = []

    # Cycle through and plot input series.
    for key, value in series.items():
        offset = column_width * series_number
        p = ax.bar(
            value.truncate(before=start_yr).index.astype('float') + offset,
            value.truncate(before=start_yr),
            width=column_width,
            color=colors[series_number],
            edgecolor='black',
            linewidth=0.4,
        )

        if series_qty > 1:
            ax.bar_label(p, fmt='{:,.0f}', padding=label_pad, rotation=90)
        else:
            ax.bar_label(p, fmt='{:,.0f}', padding=label_pad)

        # Extract fuel names from each dataframe, for use in chart legend.
        plot_names.append(value.name.replace(' Change', ''))
        series_number += 1

    # Show legend if more than one series,
    if series_qty > 1:
        ax.legend(
            plot_names,
            loc='lower left',
            handlelength=2,
            ncol=7,
            fontsize='large',
            facecolor='whitesmoke',
            fancybox=False,
        )

    ax.set_facecolor('whitesmoke')

    # Derive list of x_ticks from final dataframe. Arrange ticks as to place label in centre of column along x-axis
    # and grid lines in between columns.
    end_yr = value.index[-1]
    x_ticks_major = np.arange(start_yr, end_yr + 1, 1)
    if series_qty > 1:
        ax.set_xticks(np.array(x_ticks_major) + column_width * ((series_qty - 1) / 2), labels=x_ticks_major)
        ax.set_xticks(np.arange(start_yr - column_width / 2 - ((1 - 0.95) / 2), end_yr + 1, 1), minor=True)
    else:
        ax.set_xticks(x_ticks_major)
        ax.set_xticks(np.arange(start_yr + .5, end_yr + .5, 1), minor=True)
    ax.xaxis.grid(False, which='major')
    ax.xaxis.grid(True, which='minor', color='dimgray')
    ax.tick_params(axis='x', length=0)
    ax.margins(x=0.002)
    # Show x-axis line.
    plt.axhline(0, color='black', lw=0.4)
    ax.set_axisbelow(True)
    ax.set_xlabel('Year')

    ax.autoscale(axis='y')
    ax.set_ylim(min(ax.get_yticks()), max(ax.get_yticks()))
    ax.set_ylabel(y_label)
    ax.yaxis.grid(False)

    # Add comma thousands seperator.
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, k: format(decimal.Decimal(x), ','))
    )

    plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.18)
    fig.suptitle(
        country,
        x=0.05,
        y=0.96,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.91,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.12,
        footer_text,
        verticalalignment='top',
        horizontalalignment='left',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: column_grouped_2_subplots()
#
# Description:
# 2 grouped column subplots. series1 is plotted in top subplot, **series in the bottom.
#
########################################################################################################################
def column_grouped_2_subplots(country, title, y_label_top, y_label_bottom, footer_text, color_top, series_top,
                              *colors, **series):
    fig, ax = plt.subplots(
        2,
        1,
        figsize=(
            user_globals.Constant.FIG_HSIZE_CHANGE_COLUMN_PLOT.value,
            user_globals.Constant.FIG_VSIZE_CHANGE_COLUMN_2_PLOT.value,
        ),
    )
    start_yr = user_globals.Constant.CHANGE_CHART_START_YR.value
    label_pad = 2

    # Top plot.
    p0 = ax[0].bar(
        series_top.truncate(before=start_yr).index.astype('float'),
        series_top.truncate(before=start_yr),
        width=0.95,
        color=color_top,
        edgecolor='black',
        linewidth=0.4,
    )

    ax[0].bar_label(p0, fmt='{:,.0f}', padding=label_pad)

    # Extract fuel names from each dataframe, for use in chart legend.
    series_name = [series_top.name.replace(' Change', '')]
    ax[0].legend(
        series_name,
        loc='upper left',
        handlelength=2,
        fontsize='large',
        facecolor='whitesmoke',
        fancybox=False,
    )
    ax[0].set_facecolor('whitesmoke')
    # Derive list of x_ticks from final dataframe. Arrange ticks as to place label in centre of column along x-axis
    # and grid lines in between columns.
    end_yr = series_top.index[-1]
    ax[0].set_xticks(np.arange(start_yr, end_yr + 1, 1))
    ax[0].set_xticks(np.arange(start_yr + .5, end_yr + .5, 1), minor=True)
    ax[0].xaxis.grid(False, which='major')
    ax[0].xaxis.grid(True, which='minor', color='dimgray')
    ax[0].tick_params(axis='x', length=0)
    # Show x-axis line.
    ax[0].axhline(0, color='black', lw=0.4)
    ax[0].set_axisbelow(True)
    ax[0].margins(x=0.002)
    ax[0].autoscale(axis='y')
    ax[0].set_ylim(min(ax[0].get_yticks()), max(ax[0].get_yticks()))
    ax[0].set_ylabel(y_label_top)
    ax[0].yaxis.grid(False)
    # Add comma thousands seperator.
    ax[0].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
    )

    if np.nanmax(abs(series_top)) < 0.5:
        ax[0].set_yticks([])
        ax[0].set_ylabel(y_label_top, labelpad=10)

    # Bottom plot.
    series_qty = len(series)
    column_width = 0.95 / series_qty
    series_number = 0
    series_names = []
    # Cycle through and plot input series.
    for key, value in series.items():
        offset = column_width * series_number
        p1 = ax[1].bar(
            value.truncate(before=start_yr).index.astype('float') + offset,
            value.truncate(before=start_yr),
            width=column_width,
            color=colors[series_number],
            edgecolor='black',
            linewidth=0.4,
        )
        if series_qty > 1:
            ax[1].bar_label(p1, fmt='{:,.0f}', padding=label_pad, rotation=90)
        else:
            ax[1].bar_label(p1, fmt='{:,.0f}', padding=label_pad)
        # Extract fuel names from each dataframe, for use in chart legend.
        series_names.append(value.name.replace(' Change', ''))
        series_number += 1

    ax[1].legend(
        series_names,
        loc='lower left',
        handlelength=2,
        ncol=7,
        fontsize='large',
        facecolor='whitesmoke',
        fancybox=False,
    )
    ax[1].set_facecolor('whitesmoke')

    # Derive list of x_ticks from final dataframe.
    end_yr = series_top.index[-1]
    x_ticks_major = (np.arange(start_yr, end_yr + 1, 1))
    ax[1].set_xticks(np.array(x_ticks_major) + column_width * ((series_qty - 1) / 2), labels=x_ticks_major)
    ax[1].set_xticks(np.arange(start_yr - column_width / 2 - ((1 - 0.95) / 2), end_yr + 1, 1), minor=True)
    ax[1].xaxis.grid(False, which='major')
    ax[1].xaxis.grid(True, which='minor', color='dimgray')
    ax[1].tick_params(axis='x', length=0)

    # Show x-axis line.
    ax[1].axhline(0, color='black', lw=0.4)
    ax[1].set_axisbelow(True)
    ax[1].set_xlabel('Year')
    ax[1].margins(x=0.002)

    ax[1].autoscale(axis='y')
    ax[1].set_ylim(min(ax[1].get_yticks()), max(ax[1].get_yticks()))
    ax[1].set_ylabel(y_label_bottom)
    ax[1].yaxis.grid(False)
    # Add comma thousands seperator.
    ax[1].yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(decimal.Decimal(x), ','))
    )

    plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.17, hspace=0.1)

    fig.suptitle(
        country,
        x=0.05,
        y=0.945,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.91,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.05,
        0.13,
        footer_text,
        verticalalignment='top',
        horizontalalignment='left',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: treemap_1_subplot()
#
# Description:
# Single treemap subplot
#
########################################################################################################################
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
        area='Value',
        labels='Label',
        cmap=df['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='white', lw=0.5),
        textprops=dict(
            c='white', place='top left', padx=3, pady=6, reflow=True, max_fontsize=60
        ),
    )
    ax.legend(
        df['Name'],
        loc='upper left',
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=2,
        fontsize='large',
    )
    ax.axis('off')
    ax.set_title(
        subplot_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    plt.subplots_adjust(left=0.125, top=0.83, bottom=0.22)

    fig.suptitle(
        country,
        x=0.125,
        y=0.955,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.92,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.91,
        title_addition,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.115,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: treemap_2_subplots()
#
# Description:
# 2 treemap subplots in 1 row.
#
########################################################################################################################
def treemap_2_subplots(
        df0,  # Dataframe 1
        df1,  # Dataframe 2
        subplot0_title,  # Title above LH plot
        subplot1_title,  # Title above RH plot
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
        df0,
        area='Value',
        labels='Label',
        cmap=df0['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='white', lw=0.5),
        textprops=dict(
            c='white',
            place='top left',
            padx=3,
            pady=6,
            reflow=False,
            max_fontsize=60,
            grow=True,
        ),
    )
    ax[0].legend(
        df0['Name'],
        loc='upper left',
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=3,
        fontsize='large',
    )
    ax[0].axis('off')
    ax[0].set_title(
        subplot0_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    # Plot right-hand treemap.
    tr.treemap(
        ax[1],
        df1,
        area='Value',
        labels='Label',
        cmap=df1['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='white', lw=0.5),
        textprops=dict(
            c='white',
            place='top left',
            padx=3,
            pady=6,
            reflow=False,
            max_fontsize=60,
        ),
    )
    ax[1].legend(
        df1['Name'],
        loc='upper left',
        bbox_to_anchor=(0, 0),
        frameon=False,
        handlelength=2,
        ncol=3,
        fontsize='large',
    )
    ax[1].axis('off')
    if 'ELECTRICITY GENERATION' in subplot1_title:
        ax[1].set_title(
            subplot1_title,
            fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
            fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
            loc='left',
            color='black',
            position=(0.011, 1),
            pad=7.5,
        )
    else:
        ax[1].set_title(
            subplot1_title,
            fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
            fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
            loc='left',
        )

    plt.subplots_adjust(left=0.125, top=0.86, bottom=0.18)

    fig.suptitle(
        country,
        x=0.125,
        y=0.955,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.915,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.905,
        title_addition,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.115,
        footer_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )


########################################################################################################################
#
# Function: treemap_3_subplots()
#
# Description:
# 3 treemap subplots in 1 row, without legend.
#
########################################################################################################################
def treemap_3_subplots(
        df0,  # Dataframe 1
        df1,  # Dataframe 2
        df2,  # Dataframe 3
        subplot0_title,  # Title above LH plot
        subplot1_title,  # Title above centre plot
        subplot2_title,  # Title above RH plot
        country,
        title,
        title_addition,
        footer_upper_text,
        footer_lower_text,
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
        df0,
        area='Value',
        labels='Label',
        cmap=df0['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='white', lw=0.5),
        textprops=dict(
            c='white', place='top left', padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[0].axis('off')
    ax[0].set_title(
        subplot0_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    # Plot centre treemap.
    tr.treemap(
        ax[1],
        df1,
        area='Value',
        labels='Label',
        cmap=df1['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='white', lw=0.5),
        textprops=dict(
            c='white', place='top left', padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[1].axis('off')
    ax[1].set_title(
        subplot1_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    # Plot RH treemap.
    tr.treemap(
        ax[2],
        df2,
        area='Value',
        labels='Label',
        cmap=df2['Color'].to_list(),
        fill='Name',
        rectprops=dict(ec='darkslategray', lw=0.5),
        textprops=dict(
            c='white', place='top left', padx=2, pady=5, reflow=False, max_fontsize=60
        ),
    )
    ax[2].axis('off')
    ax[2].set_title(
        subplot2_title,
        fontsize=user_globals.Constant.SUBPLOT_TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
        loc='left',
    )

    fig.suptitle(
        country,
        x=0.125,
        y=0.95,
        horizontalalignment='left',
        fontsize=user_globals.Constant.SUPTITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.SUPTITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.895,
        title,
        horizontalalignment='left',
        fontsize=user_globals.Constant.TITLE_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.885,
        title_addition,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TITLE_ADDITION_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.15,
        footer_upper_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.TITLE_ADDITION_FONT_SIZE.value,
        fontweight=user_globals.Constant.TREEMAP_SUBPLOT_TITLE_FONT_WEIGHT.value,
    )
    fig.text(
        0.125,
        0.08,
        footer_lower_text,
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=user_globals.Constant.FOOTER_TEXT_FONT_SIZE.value,
        fontweight=user_globals.Constant.FOOTER_TEXT_FONT_WEIGHT.value,
    )
