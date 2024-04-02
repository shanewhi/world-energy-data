#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite

# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np
import mpl_extra.treemap as tr #https://github.com/chenyulue/matplotlib-extra


# Import user modules.
import user_globals


# 1x3 subplot column chart.
def column_subplot(
        primary_energy,
        df1,
        df2,
        df3,
        color1,
        color2,
        color3,
        title,
        title_addition,
        subplot1_title,
        subplot2_title,
        subplot3_title,
        ylabel1,
        ylabel2,
        ylabel3,
        footer_text):

    plt.style.use('bmh')
    plt.rcParams['font.family'] = user_globals.Constant.CHART_FONT.value
    # Font weight of axis values.
    plt.rcParams['font.weight'] = 'regular'

    #Create list x_ticks and fill with start of each decade.
    x_ticks = []
    for year in primary_energy.index:
        if year % 10 == 0: # Modulus.
            x_ticks.append(year)
    # Replace final value with most recent year.
    x_ticks[len(x_ticks) - 1] = max(primary_energy.index)

    # Create figure and axes
    fig, ax = plt.subplots(1, 3,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_1X3.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_1X3.value))

    # Set space between subplots
    plt.subplots_adjust(wspace = 0.25, hspace = 0.4)

    # Figure title.
    fig.suptitle(
        title,
        x = 0.1,
        y = 0.97,
        horizontalalignment = 'left',
        fontsize = 'xx-large',
        fontweight = 'heavy')
    # Text beneath figure title.
    fig.text(
        0.1,
        0.9,
        title_addition,
        fontweight = 'demibold',
        horizontalalignment = 'left',
        fontsize = 'large')
    # Text in footer.
    fig.text(
        0.1,
        0.01,
        footer_text,
        fontweight = 'regular',
        horizontalalignment = 'left',
        fontsize = 'small')

    if color1 == 'black':
        edge_color = 'dimgrey'
    else:
        edge_color = 'black'

    ax[0].autoscale(axis = 'y')
    ax[0].set_title(subplot1_title, weight = 'demibold')
    ax[0].set_ylabel(ylabel1)
    ax[0].yaxis.grid(True)
    ax[0].set_xlim(min(df1.index) - 2, max(df1.index) + 2)
    ax[0].set_xticks(x_ticks)
    ax[0].set_xlabel('Year')
    # Set aspect ratio 1:1.
    ax[0].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if max(df1['Value']) == 0:
        ax[0].set(yticklabels = [])
        ax[0].tick_params(left = False)
        ax[0].set_ylim(0, 1)
        ax[0].plot(df1.index, df1['Value'], color1, linewidth =
                      user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[0].bar(df1.index, df1['Value'], width = 1, color = color1,
                  edgecolor = edge_color, linewidth = 0.2)

    ax[1].autoscale(axis = 'y')
    ax[1].set_title(subplot2_title, weight = 'demibold')
    ax[1].set_ylabel(ylabel2)
    ax[1].yaxis.grid(True)
    ax[1].set_xlim(min(df2.index) - 2, max(df2.index) + 2)
    ax[1].set_xticks(x_ticks)
    ax[1].set_xlabel('Year')
    ax[1].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if  max(df2['Value']) == 0:
        ax[1].set(yticklabels = [])
        ax[1].tick_params(left = False)
        ax[1].set_ylim(0, 1) #force 0 line to appear at bottom
        ax[1].plot(df2.index, df2['Value'], color2, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[1].bar(df2.index, df2['Value'], width = 1, color = color2,
                  edgecolor = edge_color, linewidth = 0.2)

    ax[2].autoscale(axis = 'y')
    ax[2].set_title(subplot3_title, weight = 'demibold')
    ax[2].set_ylabel(ylabel3)
    ax[2].yaxis.grid(True)
    ax[2].set_xlim(min(df3.index) - 2, max(df3.index) + 2)
    ax[2].set_xticks(x_ticks)
    ax[2].set_xlabel('Year')
    ax[2].set_box_aspect(1)
    # If nil data remove y-axis detail, else plot bar chart.
    if max(df3['Value']) == 0:
        ax[2].set(yticklabels = [])
        ax[2].tick_params(left = False)
        ax[2].set_ylim(0, 1)
        ax[2].plot(df3.index, df3['Value'], color3, linewidth =
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[2].bar(df3.index, df3['Value'], width = 1, color = color3,
                  edgecolor = edge_color, linewidth = 0.2)


# 2x3 subplot line chart.
def line_subplot(
        primary_energy,
        df1, df2, df3, df4, df5, df6,
        color1, color2, color3, color4, color5, color6,
        title, title_addition,
        subplot1_title, subplot2_title, subplot3_title,
        subplot4_title, subplot5_title, subplot6_title,
        ylabel,
        footer_text):
    plt.style.use(user_globals.Constant.CHART_STYLE.value)
    plt.rcParams['font.family'] = user_globals.Constant.CHART_FONT.value
    plt.rcParams['font.weight'] = 'regular'

    # Create list x_ticks and fill with start of each decade.
    # Replace final with most recent year.
    x_ticks = []
    for year in primary_energy.index:
        if year % 10 == 0:
            x_ticks.append(year)
    x_ticks[len(x_ticks) - 1] = max(primary_energy.index)

    # Set range of y axes for all subplots based on largest share of any fuel.
    maxdf1 = np.nanmax(df1.Value)
    maxdf2 = np.nanmax(df2.Value)
    maxdf3 = np.nanmax(df3.Value)
    maxdf4 = np.nanmax(df4.Value)
    maxdf5 = np.nanmax(df5.Value)
    maxdf6 = np.nanmax(df6.Value)
    max_y = max(maxdf1, maxdf2, maxdf3, maxdf4, maxdf5, maxdf6)
    max_y = (int(max_y / 10) + 2) * 10

    fig, ax = plt.subplots(2, 3, sharex = False, sharey = False,
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.3)
    fig.suptitle(
        title,
        x = 0.1,
        y = 0.97,
        horizontalalignment = 'left',
        fontsize = 'xx-large',
        fontweight = 'heavy')
    fig.text(
        0.1,
        0.935,
        title_addition,
        fontweight = 'demibold',
        horizontalalignment = 'left',
        fontsize = 'large')
    fig.text(
        0.1,
        0.015,
        footer_text,
        fontweight = 'regular',
        horizontalalignment = 'left',
        fontsize = 'small')
    ax[0, 0].plot(df1.index, df1['Value'], color1, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 0].set_ylim(0, max_y)
    ax[0, 0].set_title(subplot1_title, weight = 'demibold')
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xlim(min(df1.index), max(df1.index))
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 1].plot(df2.index, df2['Value'], color2, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 1].set_ylim(0, max_y)
    ax[0, 1].set_title(subplot2_title, weight = 'demibold')
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xlim(min(df2.index), max(df2.index))
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].plot(df3.index, df3['Value'], color3, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 2].set_ylim(0, max_y)
    ax[0, 2].set_title(subplot3_title, weight = 'demibold')
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xlim(min(df3.index), max(df3.index))
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[1, 0].plot(df4.index, df4['Value'], color4, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 0].set_ylim(0, max_y)
    ax[1, 0].set_title(subplot4_title, weight = 'demibold')
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel('Year')
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xlim(min(df4.index), max(df4.index))
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].plot(df5.index, df5['Value'], color5, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 1].set_ylim(0, max_y)
    ax[1, 1].set_title(subplot5_title, weight = 'demibold')
    ax[1, 1].set_xlabel('Year')
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xlim(min(df5.index), max(df5.index))
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].plot(df6.index, df6['Value'], color6, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 2].set_ylim(0, max_y)
    ax[1, 2].set_title(subplot6_title, weight = 'demibold')
    ax[1, 2].set_xlabel('Year')
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xlim(min(df5.index), max(df5.index))
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)


# 1x2 treemap with 1.1:1 aspect ratio.
# Plots contents of two dataframes.
def treemap(df1, df2, subplot1_title, subplot2_title, suptitle,
            suptitle_addition, footer_text):

    plt.rcParams['font.family'] = user_globals.Constant.CHART_FONT.value
    plt.rcParams['font.weight'] = 'regular'
    fig, ax = plt.subplots(1, 2, figsize = (
                           user_globals.Constant.FIG_HSIZE_TREE_1X2.value,
                           user_globals.Constant.FIG_VSIZE_TREE_1X2.value),
                           subplot_kw=dict(aspect=1.1))

    tr.treemap(
        ax[0],
        df1,
        area = 'Value',
        labels ='Label',
        cmap = df1['Color'].to_list(),
        fill = 'Name',
        rectprops = dict(ec = '#eeeeee', lw = 1),
        textprops = dict(c = 'white',
                         place = 'top left',
                         reflow = True,
                         max_fontsize = 80))
    ax[0].legend(
        df1['Name'],
        bbox_to_anchor = (1,0),
        frameon = False,
        handlelength = 2,
        ncol = 2,
        fontsize = 'large')
    ax[0].axis('off')
    ax[0].set_title(subplot1_title, fontsize = 'large',
                    fontweight = 'demibold')

    tr.treemap(ax[1],
               df2,
               area = 'Value',
               labels ='Label',
               cmap = df2['Color'].to_list(),
               fill = 'Name',
               rectprops = dict(ec = '#eeeeee', lw = 1),
               textprops = dict(
                   c = 'white',
                   place = 'top left',
                   reflow = True,
                   max_fontsize = 50))
    ax[1].legend(
        df2['Name'],
        bbox_to_anchor = (1,0),
        frameon = False,
        handlelength = 2,
        ncol = 3,
        fontsize = 'large')
    ax[1].axis('off')
    ax[1].set_title(subplot2_title, fontsize = 'large',
                    fontweight = 'demibold')

    fig.suptitle(suptitle, x = 0.1, y = 0.97, horizontalalignment = 'left',
                 fontsize = 'xx-large', fontweight = 'heavy')
    fig.text(0.1, 0.92, suptitle_addition, fontweight = 'demibold',
             horizontalalignment = 'left', fontsize = 'large')
    fig.text(0.1, 0.02, footer_text, fontweight = 'regular',
             horizontalalignment = 'left', fontsize = 'small')
