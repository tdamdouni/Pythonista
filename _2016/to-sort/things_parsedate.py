# Date parsing for Things
# by Cormac Relf - cormacrelf.com - @cormacrelf

# depends on parsedatetime
# use the .py files extracted from v0.8.7 from here: https://gist.github.com/4583376
# alternatively:
#       download pipista; https://gist.github.com/4116558
#       in the plain Pythonista console, type `import pipista`, then `pipista.pypi_download("parsedatetime")`
#       download shellista; https://gist.github.com/4139094
#       running shellista, enter the following commands, which have been shortened for your convenience:
#       gunzip parse*.tar.gz
#       untar parse*.tar
#       cd parse*7
#       cd parse*7
#       cd parsedatetime
#       mv parse*.py ~

# usage: Create a Launch Center Pro shortcut like this:
# pythonista://things_parsedate?action=run&argv=[prompt]&argv=[prompt]
# The first prompt is for the title, the second is for the date to be parsed.

# Note: date parsing means you can type things like "next thursday" or "in 7 days" into the prompt,
# and Things will be sent a matching due date. The default is tomorrow; if you enter something like
# "in three Jupiter-years" instead of a sane date, you'll have to do your task by tomorrow instead.
# You can certainly change this logic - for example, default to no due date. Tomorrow is just my
# personal preference.

import webbrowser
import urllib
import datetime
import parsedatetime as pdt

# title is going straight back into the URL
title = urllib.quote(sys.argv[1])
input_date = sys.argv[2]
due_date = None
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# iOS users prone to accidental spacebar presses
if input_date == "" or input_date == " ":
	# tomorrow by default
	due_date = tomorrow
else:
	cal = pdt.Calendar()
	result = cal.parse(input_date)
	if result[1] == 0:
		# this is a parse error, default to tomorrow
		due_date = tomorrow
	else:
		tm = result[0]
		# turn time struct into date
		due_date = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday)
		
url = "things:add?title=" + title

# encode due date as Things-readable YYYY-M(M)-D(D)
url += "&dueDate=" + str(due_date.year) + "-" + str(due_date.month) + "-" + str(due_date.day)

webbrowser.open(url)

