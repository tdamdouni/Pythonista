# LinkToOrgInbox
#
# Create a note to be appended to the MobileOrg.org file
# Expects a URL on the clipboard

import random
import clipboard
import datetime
import webbrowser
import urllib
import urllib2
import re

# Utility functions to build the UUID
def hexstring(length):
  result = ''
  for i in xrange(length):
    result += hex(random.randrange(0,15))[-1]
  return result

def uuid():
  return hexstring(8) + '-' + hexstring(4) + '-' + hexstring(4) + '-' + hexstring(4) + '-' + hexstring(32)
		
# Gets title of the page
page = urllib2.urlopen(clipboard.get())
content = page.read()

title = re.search('<title>.*</title>',content).group(0)[7:-8]

# Builds the note
output = '* TODO Check [['+clipboard.get()+']['+title+']]\n'
today = datetime.datetime.now().strftime('%Y-%m-%d %a %H:%M')
output += '['+today+']\n'
output += '** Note ID: '+uuid()

output = urllib.quote(output)

# Sends the note back to Drafts and invokes the Dropbox action
webbrowser.open('drafts://x-callback-url/create?text='+output+'&action=AppendToOrg')
