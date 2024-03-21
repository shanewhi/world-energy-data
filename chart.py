#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:56:55 2024

@author: shanewhite
"""


# Import Python modules.
import matplotlib.pyplot as plt
import numpy as np


# Import user modules.
import user_globals


# Class method creates bar chart.
def column(data, column_color, title, ylabel):
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(user_globals.Constant.FIG_SIZE.value,\
                              user_globals.Constant.FIG_SIZE.value))
    ax = fig.add_subplot()
    if column_color == user_globals.Color.COAL.value:
        edge_color = 'silver'
    else:
        edge_color = 'black'
    ax.bar(
        data['Year'],
        data['Value'],
        width=1,
        color = column_color,
        edgecolor = edge_color,
        linewidth=0.5)
    ax.set_autoscaley_on(True)
    # On x-axis, display every second year, and display final year
    # irrespective of whether the start year is odd or even.
    ax.tick_params('x', labelrotation = 90)
    if (float(min(data['Year']) % 2) != 0.0):
        ax.set_xticks(np.arange(
            min(data['Year'] + 1),
            max(data['Year'] + 1),
            2))
    else:
        ax.set_xticks(np.arange(
            min(data['Year']),
            max(data['Year'] + 2),
            2))
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)
    #plt.savefig(title, dpi=300)


# Class method creates line chart.
def line(data, line_color, title, ylabel):
      plt.style.use('seaborn-v0_8')
      fig = plt.figure(figsize=(user_globals.Constant.FIG_SIZE.value,\
                              user_globals.Constant.FIG_SIZE.value))
      ax = fig.add_subplot()
      ax.set_ylim(0, 60)
      filled_marker_style = dict(marker='o',
                                 markersize=3.5,
                                 color=line_color,
                                 markerfacecolor='white',
                                 markeredgewidth = 0.5,
                                 markeredgecolor='grey',
                                 linewidth = 6)
      ax.plot(
          data['Year'],
          data['Value'],
          **filled_marker_style)
      # On x-axis, display every second year, and display final year
      # irrespective of whether the start year is odd or even.
      ax.tick_params('x', labelrotation = 90)
      if (float(min(data['Year']) % 2) != 0.0):
          ax.set_xticks(np.arange(
              min(data['Year'] + 1),
              max(data['Year'] + 1),
              2))
      else:
          ax.set_xticks(np.arange(
              min(data['Year']),
              max(data['Year'] + 2),
              2))
      ax.set_title(title)
      ax.set_xlabel('Year')
      ax.set_ylabel(ylabel)
      #plt.savefig(title, dpi=300)
