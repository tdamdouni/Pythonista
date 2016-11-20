# coding: utf-8

# https://forum.omz-software.com/topic/2964/matplotlib-step-graphic-xaxis-generates-one-month-too-much

# https://www.dropbox.com/s/fj6l70kzbtwknt6/Fichier%2024-03-16%2013%2053%2018.jpeg?dl=0

import matplotlib.pyplot as plt

ax.step(x,y,'-',where='pre',label=yyyy_prec+' ['+str(ymax)+']',color=colors[color_index-1])
plt.legend(loc=9,fontsize=10)
months = mdates.MonthLocator(range(1,13), bymonthday=1, interval=1) # every month
ax.xaxis.set_major_locator(months)
monthsfmt = mdates.DateFormatter('%b')
ax.xaxis.set_major_formatter(monthsfmt)
ax.yaxis.tick_left()
ax.yaxis.tick_right()
ax.grid(True)

# Resolved
# ax.set_xticklabels((...)) and set last tick label as an empty string

