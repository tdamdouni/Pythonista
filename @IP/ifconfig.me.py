# This Pythonista script gets your current IP address, using ifconfig.me, and puts that into the clipboard.
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

webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(my_ip_string))