# NoteToOrgInbox
#
# Create a note to be appended to the MobileOrg.org file
# Expects the title and body as arguments

import random
import datetime
import webbrowser
import urllib

# Utility functions to build UUIDs
def hexstring(length):
	result = ''
	for i in xrange(length):
		result += hex(random.randrange(0,15))[-1]
	return result
	
def uuid():
	return hexstring(8) + '-'+hexstring(4) + '-' + hexstring(4) + '-' + hexstring(4) + '-' + hexstring(32)
	
# Builds the note
output = '* TODO ' + urllib.unquote(sys.argv[1]) + '\n'
today = datetime.datetime.now().strftime('%Y-%m-%d %a %H:%M')
output += '['+today+']\n'
output += '** '+ urllib.unquote(sys.argv[2])+'\n'
output += '** Note ID: '+uuid()

output = urllib.quote(output)

# Sends the note back to Drafts
webbrowser.open('drafts4://x-callback-url/create?text='+output+'&action=AppendToOrg')

