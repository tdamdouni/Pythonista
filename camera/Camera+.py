# coding: utf-8

# http://ryancollins.org/2013/08/07/pythonista-programming-on-your-iphone-and-ipad/

# We're going to need work with dates, access to the clipboard,
# and to launch an app (you use the webbrowser to do that).
import datetime
import clipboard
import webbrowser

# Figure out the day of the year
day_of_year = datetime.datetime.now().timetuple().tm_yday

# Create out tag line
clip = " #365 (" + str(day_of_year) + "/365)"

# Put it in the clipboard
clipboard.set(clip)

# Open Camera+
webbrowser.open('cameraplus://')
