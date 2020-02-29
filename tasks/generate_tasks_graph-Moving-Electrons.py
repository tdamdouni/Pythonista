# coding: utf-8

# https://gist.github.com/Moving-Electrons/eb55d919d5f56dc37c7a

from __future__ import print_function
import sys
import re
import datetime as dt
from collections import Counter
import pandas as pd
import seaborn as sns

'''
This script takes the following arguments and returns a graph showing the number of tasks due per day.

1. Taskpaper file
2. Output image file

It doesn't account for overdue tasks. The number of days to be presented in the graph can be defined
in the header of the script.
'''

# Contants definition
FILE = sys.argv[1] # .taskpaper file
OUTPUT = sys.argv[2]
NUMBER_OF_DAYS = 20

def Due_Dates_Dict(tasks):
	'''
	Takes the contents of a taskpaper file (passed as a list argument) and returns a Dictionary with
	Due Dates (keys) and number of times they repeat (values)
	'''
	
	today_date = dt.date.today()
	today_str = today_date.strftime("%Y-%m-%d")
	
	
	duePattern = '@due\((.*?)\)'
	donePattern = '@done\((.*?)\)'
	todayPattern = '.*(@today).*'
	DatesList = []
	
	for line in tasks:
	
		dueTag = re.search(duePattern, line)
		doneTag = re.search(donePattern, line)
		todayTag = re.search(todayPattern, line)
		
		
		if dueTag and not doneTag:
			DatesList.append(dueTag.group(1))
			
		if todayTag and not doneTag:
			DatesList.append(today_str)
			
			
	datesDict = Counter(DatesList)
	return datesDict
	
	
if __name__ == "__main__":

	with open(FILE, 'r') as infile:
		contents = infile.readlines()
		
	dates = Due_Dates_Dict(contents)
	print("Dates List Created")
	
	today_date = dt.date.today()
	today_str = today_date.strftime("%Y-%m-%d")
	
	later_date = dt.date.today() + dt.timedelta(days=NUMBER_OF_DAYS)
	later_str = later_date.strftime("%Y-%m-%d")
	print("Initial Date: "+today_str+"\nEnd Date: "+later_str)
	
	# Defining dataframe index as a Datetime object
	print('Dates Parsed:', dates.keys())
	
	df_index = pd.to_datetime(dates.keys(), format='%Y-%m-%d')
	
	main_df = pd.DataFrame(dates.values(), columns = ['tasks'], index = df_index).sort(ascending=True)
	
	# Getting rid of overdue items and just including upcoming tasks:
	reduced_df = main_df[(main_df.index >= today_str) & (main_df.index < later_str)]
	
	
	# Defining new index to include all days from today to the final date sample.
	# If we don't do this, dates with 0 tasks assigned will not show up
	# in the graph.
	allDates_index = pd.date_range(start=today_str, periods=NUMBER_OF_DAYS, freq='D')
	
	reduced_df_allDays = reduced_df.reindex(index=allDates_index, fill_value=0)
	
	# Transforming the dataframe index (DatetimeIndex object) to a regular pd.Series so "apply" can be used.
	# The Pandas "apply" method is used in this case to apply an "anonymous" function
	# (one we don't want to create a separate function for) to all the
	# components of the DataFrame/Series
	
	
	weekday_series = pd.Series(reduced_df_allDays.index, index = reduced_df_allDays.index).apply(lambda x: x.strftime('%a'))
	
	# Adding another column with string objects representing weekdays.
	reduced_df_allDays['weekday'] = weekday_series
	
	# Setting a pre-defined style from Seaborn
	sns.set_context('notebook')
	# Pandas plotting
	line_plot = reduced_df_allDays.plot(legend=False, title='Tasks Distribution - Next '+str(NUMBER_OF_DAYS)+' Days',
	y=['tasks'], kind='line')
	print("Generating Graph..")
	fig = line_plot.get_figure()
	fig.savefig(OUTPUT)
	print("Done.")

