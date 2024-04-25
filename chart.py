#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite


# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np
import mpl_extra.treemap as tr #https://github.com/chenyulue/matplotlib-extra
import matplotlib.ticker


# Import user modules.
import user_globals


###############################################################################
#
# Function: line_plot()
#
# Description:
# Plots a single series.
#
# Input(s): Single x-y series, country name, color, and chart text.
# Output(s): Single x-y chart.
#
###############################################################################
def line_plot(x, y, country_name, color, title, ylabel, footer_text):
    # Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in x:
        if year % 10 == 0: # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(x)

    # Create figure and axes.
    fig, ax = plt.subplots(1, 1,
                figsize = (user_globals.Constant.FIG_SIZE.value,
                           user_globals.Constant.FIG_SIZE.value))
    ax.plot(x, y, color, linewidth = \
                  user_globals.Constant.LINE_WIDTH_PLOT_1x1.value,
                  marker = ".", markersize = 7, markerfacecolor = "white",
                  markeredgecolor = "black", markeredgewidth = 0.3)

    # Add comma as thousand seperator.
    ax.yaxis.set_major_formatter( \
             matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
    ax.set_ylim(top = scale(max(y)))
    ax.set_ylim(bottom = 0)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_ticks)
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_xlabel("Year")

    # Set aspect ratio 1:1.
    ax.set_box_aspect(1)

    # Figure title.
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.97,
        horizontalalignment = "left",
        fontsize = "xx-large",
        fontweight = "heavy")
    # Text beneath figure title.
    fig.text(
        0.125,
        0.925,
        title,
        fontweight = "demibold",
        horizontalalignment = "left",
        fontsize = "large")
    # Text in footer.
    fig.text(
        0.125,
        0.01,
        footer_text,
        fontweight = "regular",
        horizontalalignment = "left",
        fontsize = "small")


###############################################################################
#
# Function: column_subplot()
#
# Description:
# 1x3 column subplots.
#
# Input(s): Primary Energy dataframe to create x-ticks, 3 dataframes to plot,
# and associated colors and chart text.
# Output(s): Single figure 1x3 column subplots.
#
###############################################################################
def column_subplot(
        df1,
        df2,
        df3,
        color1,
        color2,
        color3,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabel1,
        ylabel2,
        ylabel3,
        footer_text):

    # Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in df1.index:
        if year % 10 == 0: # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(df1.index)

    # Create figure and axes
    fig, ax = plt.subplots(1, 3,
                figsize = (user_globals.Constant.FIG_HSIZE_SUBPLOT_1X3.value,
                           user_globals.Constant.FIG_VSIZE_SUBPLOT_1X3.value))

    # Set space between subplots
    plt.subplots_adjust(wspace = 0.25, hspace = 0.4)

    # Figure title.
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.97,
        horizontalalignment = "left",
        fontsize = "xx-large",
        fontweight = "heavy")
    # Text beneath figure title.
    fig.text(
        0.125,
        0.9,
        title,
        fontweight = "demibold",
        horizontalalignment = "left",
        fontsize = "large")
    # Text in footer.
    fig.text(
        0.125,
        0.01,
        footer_text,
        fontweight = "regular",
        horizontalalignment = "left",
        fontsize = "small")

    # Grey edges for black columns.
    if color1 == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"

    ax[0].autoscale(axis = "y")
    ax[0].set_title(subplot1_title, weight = "demibold")
    ax[0].set_ylabel(ylabel1)
    ax[0].yaxis.grid(True)
    ax[0].set_xlim(min(df1.index) - 1, max(df1.index) + 1)
    ax[0].set_xticks(x_ticks)
    ax[0].set_xlabel("Year")
    ax[0].set_box_aspect(1)

    # If nil data remove y-axis detail, else plot bar chart.
    if max(df1) == 0:
        ax[0].set(yticklabels = [])
        ax[0].tick_params(left = False)
        # Place 0 line at bottom.
        ax[0].set_ylim(0, 1)
        ax[0].plot(df1.index, df1, color1, linewidth =
                      user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[0].bar(df1.index, df1, width = 1, color = color1,
                  edgecolor = edge_color, linewidth = 0.2)

    # Place grid behind columns.
    ax[0].set_axisbelow(True)

    # Repeat above for second and third subplots.
    ax[1].autoscale(axis = "y")
    ax[1].set_title(subplot2_title, weight = "demibold")
    ax[1].set_ylabel(ylabel2)
    ax[1].yaxis.grid(True)
    ax[1].set_xlim(min(df2.index) - 1, max(df2.index) + 1)
    ax[1].set_xticks(x_ticks)
    ax[1].set_xlabel("Year")
    ax[1].set_box_aspect(1)
    if  max(df2) == 0:
        ax[1].set(yticklabels = [])
        ax[1].tick_params(left = False)
        ax[1].set_ylim(0, 1)
        ax[1].plot(df2.index, df2, color2, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[1].bar(df2.index, df2, width = 1, color = color2,
                  edgecolor = edge_color, linewidth = 0.2)
    ax[1].set_axisbelow(True)

    ax[2].autoscale(axis = "y")
    ax[2].set_title(subplot3_title, weight = "demibold")
    ax[2].set_ylabel(ylabel3)
    ax[2].yaxis.grid(True)
    ax[2].set_xlim(min(df3.index) - 1, max(df3.index) + 1)
    ax[2].set_xticks(x_ticks)
    ax[2].set_xlabel("Year")
    ax[2].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if max(df3) == 0:
        ax[2].set(yticklabels = [])
        ax[2].tick_params(left = False)
        ax[2].set_ylim(0, 1)
        ax[2].plot(df3.index, df3, color3, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[2].bar(df3.index, df3, width = 1, color = color3,
                  edgecolor = edge_color, linewidth = 0.2)
    ax[2].set_axisbelow(True)


###############################################################################
#
# Function: column_subplot_equiv_units()
#
# Description:
# 1x3 column subplots.
#
# Input(s): Primary Energy dataframe to create x-ticks, 3 dataframes to plot,
# and associated colors and chart text.
# Output(s): Single figure 1x3 column subplots with equivalent y-axis scales.
#
###############################################################################
def column_subplot_equiv_units(
        df1,
        df2,
        df3,
        color1,
        color2,
        color3,
        country_name,
        title,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabels,
        footer_text):

    # Set range of y axes for all subplots based on largest.
    if country_name == 'WORLD':
        maxdf1 = np.nanmax(df1 * user_globals.Constant.PJ_TO_EJ.value)
        maxdf2 = np.nanmax(df2 * user_globals.Constant.PJ_TO_EJ.value)
        maxdf3 = np.nanmax(df3 * user_globals.Constant.PJ_TO_EJ.value)
    else:
        maxdf1 = np.nanmax(df1)
        maxdf2 = np.nanmax(df2)
        maxdf3 = np.nanmax(df3)

    y_top  = scale(max(maxdf1, maxdf2, maxdf3))

    # Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in df1.index:
        if year % 10 == 0: # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(df1.index)

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
        y = 0.97,
        horizontalalignment = "left",
        fontsize = "xx-large",
        fontweight = "heavy")
    # Text beneath figure title.
    fig.text(
        0.125,
        0.9,
        title,
        fontweight = "demibold",
        horizontalalignment = "left",
        fontsize = "large")
    # Text in footer.
    fig.text(
        0.125,
        0.01,
        footer_text,
        fontweight = "regular",
        horizontalalignment = "left",
        fontsize = "small")

    # Grey edges for black columns.
    if color1 == "black":
        edge_color = "dimgrey"
    else:
        edge_color = "black"

    ax[0].set_ylim(0, y_top)
    ax[0].set_title(subplot1_title, weight = "demibold")
    ax[0].set_ylabel(ylabels)
    ax[0].yaxis.grid(True)
    ax[0].set_xlim(min(df1.index) - 1, max(df1.index) + 1)
    ax[0].set_xticks(x_ticks)
    ax[0].set_xlabel("Year")
    ax[0].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if max(df1) == 0:
        ax[0].set(yticklabels = [])
        ax[0].tick_params(left = False)
        ax[0].set_ylim(0, 1)
        ax[0].plot(df1.index, df1, color1, linewidth =
                      user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        if country_name == "WORLD":
            ax[0].bar(df1.index, df1 * \
                      user_globals.Constant.PJ_TO_EJ.value, width = 1,
                      color = color1, edgecolor = edge_color, linewidth = 0.2)
        else:
            ax[0].bar(df1.index, df1, width = 1, color = color1,
                  edgecolor = edge_color, linewidth = 0.2)
    # Place grid behind columns.
    ax[0].set_axisbelow(True)

    # Repeat above for second and third suboplots.
    ax[1].set_ylim(0, y_top)
    ax[1].set_title(subplot2_title, weight = "demibold")
    ax[1].yaxis.grid(True)
    ax[1].set_xlim(min(df2.index) - 1, max(df2.index) + 1)
    ax[1].set_xticks(x_ticks)
    ax[1].set_xlabel("Year")
    ax[1].set_box_aspect(1)
    if  max(df2) == 0:
        ax[1].set(yticklabels = [])
        ax[1].tick_params(left = False)
        ax[1].set_ylim(0, 1) #force 0 line to appear at bottom
        ax[1].plot(df2.index, df2, color2, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        if country_name == "WORLD":
            ax[1].bar(df2.index, df2 * \
                      user_globals.Constant.PJ_TO_EJ.value, width = 1,
                      color = color2, edgecolor = edge_color, linewidth = 0.2)
        else:
            ax[1].bar(df2.index, df2, width = 1, color = color2,
                  edgecolor = edge_color, linewidth = 0.2)
    ax[1].set_axisbelow(True)

    ax[2].set_ylim(0, y_top)
    ax[2].set_title(subplot3_title, weight = "demibold")
    ax[2].yaxis.grid(True)
    ax[2].set_xlim(min(df3.index) - 1, max(df3.index) + 1)
    ax[2].set_xticks(x_ticks)
    ax[2].set_xlabel("Year")
    ax[2].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if max(df3) == 0:
        ax[2].set(yticklabels = [])
        ax[2].tick_params(left = False)
        ax[2].set_ylim(0, 1)
        ax[2].plot(df3.index, df3, color3, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        if country_name == "WORLD":
            ax[2].bar(df3.index, df3 * \
                      user_globals.Constant.PJ_TO_EJ.value, width = 1,
                      color = color3, edgecolor = edge_color, linewidth = 0.2)
        else:
            ax[2].bar(df3.index, df3, width = 1, color = color3,
                  edgecolor = edge_color, linewidth = 0.2)
    ax[2].set_axisbelow(True)


###############################################################################
#
# Function: line_subplot()
#
# Description:
# 2x3 line subplots.
#
# Input(s): Primary Energy dataframe to create x-ticks, 6 dataframes to plot,
# and associated colors and chart text.
# Output(s): Single figure 2x3 line subplots.
#
###############################################################################
def line_subplot(
        df1, df2, df3, df4, df5, df6, # Six dataframes to plot.
        color1, color2, color3, color4, color5, color6,
        country_name, title,
        subplot1_title, subplot2_title, subplot3_title,
        subplot4_title, subplot5_title, subplot6_title,
        ylabel, footer_text):
    plt.style.use(user_globals.Constant.CHART_STYLE.value)
    plt.rcParams["font.family"] = user_globals.Constant.CHART_FONT.value
    plt.rcParams["font.weight"] = "regular"

    # Create list x_ticks and fill with start year of each decade.
    x_ticks = []
    for year in df1.index:
        if year % 10 == 0:
            x_ticks.append(year)
    # Replace final with most recent year.
    x_ticks[len(x_ticks) - 1] = max(df1.index)

    # Set range of y axes for all subplots based on largest share of any fuel.
    maxdf1 = np.nanmax(df1)
    maxdf2 = np.nanmax(df2)
    maxdf3 = np.nanmax(df3)
    maxdf4 = np.nanmax(df4)
    maxdf5 = np.nanmax(df5)
    maxdf6 = np.nanmax(df6)
    y_top = scale(max(maxdf1, maxdf2, maxdf3, maxdf4, maxdf5, maxdf6))

    fig, ax = plt.subplots(2, 3, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.3)
    fig.suptitle(
        country_name,
        x = 0.125,
        y = 0.97,
        horizontalalignment = "left",
        fontsize = "xx-large",
        fontweight = "heavy")
    fig.text(
        0.125,
        0.935,
        title,
        fontweight = "demibold",
        horizontalalignment = "left",
        fontsize = "large")
    fig.text(
        0.125,
        0.03,
        footer_text,
        fontweight = "regular",
        horizontalalignment = "left",
        fontsize = "small")
    ax[0, 0].plot(df1.index, df1, color1, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 0].set_ylim(0, y_top)
    ax[0, 0].set_title(subplot1_title, weight = "demibold")
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xlim(min(df1.index), max(df1.index))
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 1].plot(df2.index, df2, color2, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 1].set_ylim(0, y_top)
    ax[0, 1].set_title(subplot2_title, weight = "demibold")
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xlim(min(df2.index), max(df2.index))
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].plot(df3.index, df3, color3, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 2].set_ylim(0, y_top)
    ax[0, 2].set_title(subplot3_title, weight = "demibold")
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xlim(min(df3.index), max(df3.index))
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[1, 0].plot(df4.index, df4, color4, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 0].set_ylim(0, y_top)
    ax[1, 0].set_title(subplot4_title, weight = "demibold")
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xlim(min(df4.index), max(df4.index))
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].plot(df5.index, df5, color5, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 1].set_ylim(0, y_top)
    ax[1, 1].set_title(subplot5_title, weight = "demibold")
    ax[1, 1].set_xlabel("Year")
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xlim(min(df5.index), max(df5.index))
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].plot(df6.index, df6, color6, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 2].set_ylim(0, y_top)
    ax[1, 2].set_title(subplot6_title, weight = "demibold")
    ax[1, 2].set_xlabel("Year")
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xlim(min(df6.index), max(df6.index))
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)


###############################################################################
#
# Function: treemap()
#
# Description:
# 1x2 treemap subplots.
#
# Input(s): Two dataframe to plot and associated colors and chart text.
# Output(s): Pair of treemaps in a single figure.
#
###############################################################################
def treemap(
        df1, # Dataframe 1
        df2, # Dataframe 2
        subplot1_title, # Title above LH plot
        subplot2_title, # Title above RH plot
        country_name,
        title,
        footer_text):

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
                         max_fontsize = 80))
    ax[0].legend(
        df1["Name"],
        loc = "upper left", bbox_to_anchor=(0, 0),
        frameon = False,
        handlelength = 2,
        ncol = 3,
        fontsize = "large")
    ax[0].axis("off")
    ax[0].set_title(subplot1_title, fontsize = "large",
                    fontweight = "demibold")

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
                   max_fontsize = 50))
    ax[1].legend(
        df2["Name"],
        loc = "upper left", bbox_to_anchor = (0, 0),
        frameon = False,
        handlelength = 2,
        ncol = 3,
        fontsize = "large")
    ax[1].axis("off")
    ax[1].set_title(subplot2_title, fontsize = "large",
                    fontweight = "demibold")
    fig.suptitle(country_name, x = 0.125, y = 0.97,
                 horizontalalignment = "left",
                 fontsize = "xx-large", fontweight = "heavy")
    fig.text(0.125, 0.92, title, fontweight = "demibold",
             horizontalalignment = "left", fontsize = "large")
    fig.text(0.125, 0.02, footer_text, fontweight = "regular",
             horizontalalignment = "left", fontsize = "small")


###############################################################################
#
# Function: column_grouped()
#
# Description:
# Single figure plot of grouped columns. Plotted values are input as a variable
# number of dataframes and matching colors.
#
# Input(s): Country name, associated chart text, variable number of chart
# colors and dataframes to plot
# Output(s): Single figure 1x3 column subplot with equivalent y-axis scales.
#
###############################################################################
def column_grouped(
        country_name,
        title,
        y_label,
        footer_text,
        start_yr,
        *colors,
        **series):
    plt.style.use(user_globals.Constant.CHART_STYLE.value)
    plt.rcParams["font.family"] = user_globals.Constant.CHART_FONT.value
    # Font weight of axis values.
    plt.rcParams["font.weight"] = "regular"

    # Create figure and axes.
    fig, ax = plt.subplots(1, 1, figsize =
                          (user_globals.Constant.FIG_HSIZE_COLUMN_PLOT.value,
                           user_globals.Constant.FIG_VSIZE_COLUMN_PLOT.value))
    label_pad = 2
    df_qty = (len(series))
    column_width = 1 / df_qty
    multiplier = 0
    offset = column_width * multiplier
    plot_names = []

    # Cycle through and plot input dataframes.
    for key, value in series.items():
        series = value
        offset = column_width * multiplier
        if country_name == "WORLD":
             p = ax.bar(series.truncate(before = start_yr).index.astype \
                    ("float") + offset, series.truncate(before = \
                    start_yr) * user_globals.Constant.PJ_TO_EJ.value,
                    width = column_width, color = colors[multiplier],
                    edgecolor = "black", linewidth = 0.2)
        else:
            p = ax.bar(series.truncate(before = start_yr).index.astype \
                   ("float") + offset, series.truncate(before = \
                   start_yr), width = column_width,
                   color = colors[multiplier], edgecolor = "black",
                   linewidth = 0.2)
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
    ax.set_xlim(start_yr, end_yr+1-column_width/2)
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
        y = 0.95,
        horizontalalignment = "left",
        fontsize = "xx-large",
        fontweight = "heavy")
    # Text beneath figure title.
    fig.text(
        0.065,
        0.9,
        title,
        fontweight = "demibold",
        horizontalalignment = "left",
        fontsize = "large")
    # Text in footer.
    fig.text(
        0.065,
        0.03,
        footer_text,
        fontweight = "regular",
        horizontalalignment = "left",
        fontsize = "small")
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
        fontsize = "large")
    # Show x axis line.
    plt.axhline(0, color="black", lw = 0.4)


###############################################################################
#
# Function: scale()
#
# Description:
# Determines suitable y-axis scale based on input value. This function acts as
# an alternative to Matplotlib"s autoscale() that can sometimes be inadequate.
#
# Input(s): Single float value.
# Output(s): Scaled single float value.
#
###############################################################################
def scale(val):
    if val < 10:
        rounded = round(val, 0)
        if rounded < val:
            return rounded + 0.25
        else:
            return(rounded)
    elif val < 100:
        val /= 10
        rounded = round(val, 0)
        if rounded < val:
            return((rounded + 1) * 10)
        else:
            return(rounded) * 10
    elif val < 1000:
        val /= 100
        rounded = round(val, 0)
        if rounded < val:
            return((rounded + 0.5) * 100)
        else:
            return(rounded) * 100
    elif val < 10000:
        val /= 1000
        rounded = round(val, 0)
        if rounded < val:
            return((rounded + 0.5) * 1000)
        else:
            return(rounded) * 1000
    else:
        val /= 10000
        rounded = round(val, 0)
        if rounded < val:
            return((rounded + 0.5) * 10000)
        else:
            return(rounded) * 10000

