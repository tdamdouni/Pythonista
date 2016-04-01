# https://gist.github.com/nicolasH/6102105
import sys
import console
import requests
from bs4 import BeautifulSoup
from datetime import datetime
#
# Check the status of the Apple Dev Center systems.
# Offline systems appear in orange
# Online systems appear in black
#
# Author: Nicolas HOIBIAN | @nico_h | www.niconomicon.net
# License: Creative Common By-NC-SA
#
# @viticci on twitter created a version that uses the Pythonista notification module for timely reminders:
# http://www.macstories.net/linked/check-dev-center-status-from-ios-with-pythonista/
#
# url fetching activity indicator courtesy of @fcrespo82 on twitter
#https://gist.github.com/fcrespo82/5b9b35bc8a0a62c7ec1a

console.clear()
console.set_font("Futura", 16)
console.set_color(0, 0, 0)
print "Fetching DevCenter status"
print datetime.now().strftime("%Y/%m/%d %H:%M:%S (local time)")
url="https://developer.apple.com/support/system-status/"
console.show_activity()
resp = requests.get(url)
console.hide_activity()

html_doc = resp.text
soup = BeautifulSoup(html_doc)

down = 0
up = 0
# Data Last Updated on apple server
for h2 in soup.find_all("h2"):
  print "Data Last", h2.text
print "_______________________"
for td in soup.find_all("td"):
 if td["class"][0] == "offline":
   console.set_color(1, 0.5, 0)
   down+=1
 else:
   console.set_color(0, 0, 0)
   up+=1
 print td.text

console.set_color(0, 0, 0)
print "_______________________"
console.set_color(1, 0.5, 0)
print "Offline:", down
console.set_color(0, 0, 0)
print "Online:", up