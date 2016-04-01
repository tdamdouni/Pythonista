# This Pythonista script gets your current IP address, using ifconfig.me, and puts that
# into the clipboard.
#
# It will also, depending on the argument passed to it, launch any of the actions defined.
#
# (c) 2014 Dexter Ang. MIT License.
#

import clipboard
import sys
import urllib
import webbrowser

my_ip = urllib.urlopen("http://ifconfig.me/ip")
my_ip_string = my_ip.read()

clipboard.set(my_ip_string)

argument = sys.argv

if len(argument) == 2:
  if argument[1] == "1":
    # Drafts
    webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(my_ip_string))
  elif argument[1] == "2":
    # iMessage
    webbrowser.open("launch://messaging?body=" + urllib.quote(my_ip_string))
  elif argument[1] == "3":
    # Email
    webbrowser.open("launch://email?subject=" + urllib.quote("My IP address") + "&body=" + urllib.quote(my_ip_string))
  elif argument[1] == "4":
    # Gmail
    webbrowser.open("googlegmail:///co?subject=" + urllib.quote("My IP address") + "&body=" + urllib.quote(my_ip_string))
  else: 
    webbrowser.open("drafts4:")