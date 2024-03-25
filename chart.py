#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Created on Wed Mar 20 13:56:55 2024
#@author: shanewhite

#import Python modules
import matplotlib.pyplot as plt
import numpy as np

#import user modules
import user_globals

#three subplot column chart, 1 row, 3 columns
def column_subplot(primary_energy, df0, df1, df2, color0, color1, color2, \
                   title, sub_title0, sub_title1, sub_title2, ylabel0, \
                   ylabel1, ylabel2):
    #plt.style.use('default')
    #plt.style.use('bmh')
    plt.style.use('seaborn-darkgrid')
    plt.rcParams['font.family'] = user_globals.Constant.FONT.value
    #font weight of axis values
    plt.rcParams['font.weight'] = 'regular'
    #create list x_ticks and fill with start of each decade
    x_ticks = []
    for year in primary_energy.index:
        if year % 10 == 0: #modulus
            x_ticks.append(year)
    #replace final value with most recent year
    x_ticks[len(x_ticks) - 1] = max(primary_energy.index)
    #create figure and axes
    fig, ax = plt.subplots(1, 3, \
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_1X3.value, \
                user_globals.Constant.FIG_VSIZE_SUBPLOT_1X3.value))
    #set space between subplots
    plt.subplots_adjust(wspace = 0.2, hspace = 0.3)
    #main title
    fig.suptitle(title, x = 0.1, y = 0.97, horizontalalignment = 'left', \
                 fontsize = 'xx-large', fontweight = 'heavy')
    fig.text(0.1, 0.9, 'Fossil Fuel Production', \
             fontweight = 'demibold', horizontalalignment = 'left', \
             fontsize = 'large')
    fig.text(0.1, 0.01, 'Any gap at beginning of a chart is due to data' + \
             ' not present in dataset.\n',
             fontweight = 'light', horizontalalignment = 'left', \
             fontsize = 'small')
    if color0 == 'black':
        edge_color = 'silver'
    else:
        edge_color = 'black'
    ylim = autoscale_column(df0) #matplotlib autoscale is inadequate here
    ax[0].set_ylim(0, ylim)
    ax[0].set_title(sub_title0, weight = 'demibold')
    ax[0].set_ylabel(ylabel0)
    ax[0].yaxis.grid(True)
    ax[0].set_xlim(min(df0.index), max(df0.index))
    ax[0].set_xticks(x_ticks)
    ax[0].set_xlabel('Year')
    #set aspect ratio 1:1
    ax[0].set_box_aspect(1)
    #if nil data remove y-axis detail, else plot bar chart
    if max(df0.Value) == 0:
        ax[0].set(yticklabels = [])
        ax[0].tick_params(left = False)
        ax[0].set_ylim(0, 1)
        ax[0].plot(df0.index, df0.Value, color0, linewidth = \
                      user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[0].bar(df0.index, df0.Value,width = 1, color = color0, \
                  edgecolor = edge_color, linewidth = 0.2)
    if color1 == 'black':
        edge_color = 'silver'
    else:
        edge_color = 'black'
    ylim = autoscale_column(df1)
    ax[1].set_ylim(0, ylim)
    ax[1].set_title(sub_title1, weight = 'demibold')
    ax[1].set_ylabel(ylabel1)
    ax[1].yaxis.grid(True)
    ax[1].set_xlim(min(df1.index), max(df1.index))
    ax[1].set_xticks(x_ticks)
    ax[1].set_xlabel('Year')
    #set aspect ratio 1:1
    ax[1].set_box_aspect(1)
    #if nil data remove y-axis detail, else plot bar chart
    if  max(df1.Value) == 0:
        ax[1].set(yticklabels = [])
        ax[1].tick_params(left = False)
        ax[1].set_ylim(0, 1) #force 0 line to appear at bottom
        ax[1].plot(df1.index, df1.Value, color1, linewidth = \
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[1].bar(df1.index, df1.Value, width = 1, color = color1, \
                  edgecolor = edge_color, linewidth = 0.2)
    if color2 == 'black':
        edge_color = 'silver'
    else:
        edge_color = 'black'
    ylim = autoscale_column(df2)
    ax[2].set_ylim(0, ylim)
    ax[2].set_title(sub_title2, weight = 'demibold')
    ax[2].set_ylabel(ylabel2)
    ax[2].yaxis.grid(True)
    ax[2].set_xlim(min(df2.index), max(df2.index))
    ax[2].set_xticks(x_ticks)
    ax[2].set_xlabel('Year')
    #set aspect ratio 1:1
    ax[2].set_box_aspect(1)
    #if nil data remove y-axis detail, else plot bar chart
    if max(df2.Value) == 0:
        ax[2].set(yticklabels = [])
        ax[2].tick_params(left = False)
        ax[2].set_ylim(0, 1)
        ax[2].plot(df2.index, df2.Value, color2, linewidth = \
                   user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    else:
        ax[2].bar(df2.index, df2.Value,width = 1, color = color2, \
                  edgecolor = edge_color, linewidth = 0.2)

def autoscale_column(df):
    max_y = max(df.Value)
    if max_y < 10:
        ylim = int(max_y) + 1
    else:
        ylim = (int(max_y / 10) + 1) * 10
    return ylim

#six subplot line chart, 2 rows, 3 columns
def line_subplot(primary_energy, df1, df2, df3, df4, df5, df6, color1, \
                 color2, color3, color4, color5, color6, title, sub_title1, \
                 sub_title2, sub_title3, sub_title4, sub_title5, sub_title6, \
                 ylabel):
    #plt.style.use('default')
    plt.style.use('seaborn-darkgrid')
    plt.rcParams['font.family'] = user_globals.Constant.FONT.value
    plt.rcParams['font.weight'] = 'regular'
    #plt.style.use('bmh')
    #x-axis:
    #create list x_ticks and fill with start of each decade
    #replace final with most recent year
    x_ticks = []
    for year in primary_energy.index:
        if year % 10 == 0:
            x_ticks.append(year)
    x_ticks[len(x_ticks) - 1] = max(primary_energy.index)
    #y-axis:
    #scale max to be 10% greater than the next decade above the highest fuel
    #share
    maxdf1 = np.nanmax(df1.Value)
    maxdf2 = np.nanmax(df2.Value)
    maxdf3 = np.nanmax(df3.Value)
    maxdf4 = np.nanmax(df4.Value)
    maxdf5 = np.nanmax(df5.Value)
    maxdf6 = np.nanmax(df6.Value)
    max_y = max(maxdf1, maxdf2, maxdf3, maxdf4, maxdf5, maxdf6)
    max_y = (int(max_y / 10) + 2) * 10
    fig, ax = plt.subplots(2, 3, sharex = False, sharey = False, \
                figsize=(user_globals.Constant.FIG_HSIZE_SUBPLOT_2X3.value,\
                user_globals.Constant.FIG_VSIZE_SUBPLOT_2X3.value))
    plt.subplots_adjust(wspace = 0.2, hspace = 0.3)
    fig.suptitle(title, x = 0.1, y = 0.97, horizontalalignment = 'left', \
                 fontsize = 'xx-large', \
                 fontweight = 'heavy')
    fig.text(0.1, 0.935, 'Share of Fuels in Energy System', \
             fontweight = 'demibold', horizontalalignment = 'left', \
             fontsize = 'large')
    fig.text(0.1, 0.045, 'Shares of geothermal, biofuels and \'other\' are ' +\
             'small and omitted for clarity',\
         fontweight = 'light', horizontalalignment = 'left', \
         fontsize = 'small')
    fig.text(0.1, 0.03, 'Gaps may be present in line segments due to data' +\
                        ' not present in dataset.',
         fontweight = 'light', horizontalalignment = 'left', \
         fontsize = 'small')
    fig.text(0.1, 0.015, 'Share for a given year is calculated using only' +\
                         ' data for fuels reported in that year.', \
         fontweight = 'light', horizontalalignment = 'left', \
         fontsize = 'small')
    ax[0, 0].plot(df1.index, df1.Value, color1, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 0].set_ylim(0, max_y)
    ax[0, 0].set_title(sub_title1, weight = 'demibold')
    ax[0, 0].set_ylabel(ylabel)
    ax[0, 0].yaxis.grid(True)
    ax[0, 0].set_xlim(min(df1.index), max(df1.index))
    ax[0, 0].set_xticks(x_ticks)
    ax[0, 0].set_box_aspect(1)
    ax[0, 1].plot(df2.index, df2.Value, color2, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 1].set_ylim(0, max_y)
    ax[0, 1].set_title(sub_title2, weight = 'demibold')
    ax[0, 1].yaxis.grid(True)
    ax[0, 1].set_xlim(min(df2.index), max(df2.index))
    ax[0, 1].set_xticks(x_ticks)
    ax[0, 1].set_box_aspect(1)
    ax[0, 2].plot(df3.index, df3.Value, color3, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[0, 2].set_ylim(0, max_y)
    ax[0, 2].set_title(sub_title3, weight = 'demibold')
    ax[0, 2].yaxis.grid(True)
    ax[0, 2].set_xlim(min(df3.index), max(df3.index))
    ax[0, 2].set_xticks(x_ticks)
    ax[0, 2].set_box_aspect(1)
    ax[1, 0].plot(df4.index, df4.Value, color4, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 0].set_ylim(0, max_y)
    ax[1, 0].set_title(sub_title4, weight = 'demibold')
    ax[1, 0].set_ylabel(ylabel)
    ax[1, 0].set_xlabel('Year')
    ax[1, 0].yaxis.grid(True)
    ax[1, 0].set_xlim(min(df4.index), max(df4.index))
    ax[1, 0].set_xticks(x_ticks)
    ax[1, 0].set_box_aspect(1)
    ax[1, 1].plot(df5.index, df5.Value, color5, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 1].set_ylim(0, max_y)
    ax[1, 1].set_title(sub_title5, weight = 'demibold')
    ax[1, 1].set_xlabel('Year')
    ax[1, 1].yaxis.grid(True)
    ax[1, 1].set_xlim(min(df5.index), max(df5.index))
    ax[1, 1].set_xticks(x_ticks)
    ax[1, 1].set_box_aspect(1)
    ax[1, 2].plot(df6.index, df6.Value, color6, linewidth = \
                  user_globals.Constant.LINE_WIDTH_SUBPOLT.value)
    ax[1, 2].set_ylim(0, max_y)
    ax[1, 2].set_title(sub_title6, weight = 'demibold')
    ax[1, 2].set_xlabel('Year')
    ax[1, 2].yaxis.grid(True)
    ax[1, 2].set_xlim(min(df5.index), max(df5.index))
    ax[1, 2].set_xticks(x_ticks)
    ax[1, 2].set_box_aspect(1)

#line chart
#redundant as of March 25, 2024
def line(data, line_color, title, ylabel):
      plt.style.use('default')
      plt.rcParams['font.family'] = user_globals.Constant.FONT.value
      fig = plt.figure(figsize=(user_globals.Constant.FIG_SIZE.value,\
                                user_globals.Constant.FIG_SIZE.value))
      ax = fig.add_subplot()
      ax.set_ylim(0, 60)
      filled_marker_style = dict(marker = 'o',
                                 markersize = \
                                 user_globals.Constant.LINE_MARKER_SIZE.value,
                                 color = line_color,
                                 markerfacecolor = 'white',
                                 linewidth = 6)
                                 #markeredgewidth = 0.8
                                 #markeredgecolor='grey'
      ax.plot(
              data.index,
              data['Value'],
              **filled_marker_style)
      #on x-axis, display every second year, and display final year
      #irrespective of whether the start year is odd or even
      ax.tick_params('x', labelrotation = 90)
      if min(data.index) % 2 != 0:
          ax.set_xticks(np.arange(
              min(data.index + 1),
              max(data.index + 1),
              2))
      else:
          ax.set_xticks(np.arange(
              min(data.index),
              max(data.index + 2),
              2))
      ax.set_title(title)
      ax.set_xlabel('Year')
      ax.set_ylabel(ylabel)
      ax.grid('True', axis = 'y')
      #plt.savefig(title, dpi=300)

#column chart
#redundant as of March 25, 2024
def column(data, column_color, title, ylabel):
    #plt.style.use('default')
    plt.style.use('seaborn-darkgrid')
    plt.rcParams['font.family'] = user_globals.Constant.FONT.value
    plt.rcParams['font.weight'] = 'regular'
    fig = plt.figure(figsize=(user_globals.Constant.FIG_SIZE.value,\
                              user_globals.Constant.FIG_SIZE.value))
    ax = fig.add_subplot()
    if column_color == user_globals.Color.COAL.value:
        edge_color = 'silver'
    else:
        edge_color = 'black'
    ax.bar(
        data.index,
        data.Value,
        width = 1,
        color = column_color,
        edgecolor = edge_color,
        linewidth = 0.5)
    ax.set_autoscaley_on(True)
    # On x-axis, display every second year, and display final year
    # irrespective of whether the start year is odd or even.
    ax.tick_params('x', labelrotation = 90)
    if min(data.index) % 2 != 0:
        ax.set_xticks(np.arange(
            min(data.index + 1),
            max(data.index + 1),
            2))
    else:
        ax.set_xticks(np.arange(
            min(data.index),
            max(data.index + 2),
            2))
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    #plt.savefig(title, dpi=300)
