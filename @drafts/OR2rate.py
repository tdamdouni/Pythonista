# Source: https://gist.github.com/Blether/f6ee2db4b4cfc04a23f2
#
# quickly calculate rate from baseline and OR
# for use from Drafts

import sys
import webbrowser
import urllib

def applyOR(baserate, oddsratio):
	baseodds = baserate/(1-baserate)
	newodds = baseodds*oddsratio
	newrate = newodds/(1+newodds)
	return str(round(newrate,2))
	
def ORoutputstring(a,b):
	 out = 'baseline rate ' + a + ', OR ' + b + ': \trate '  + applyOR(float(a), float(b)) + '\n'
	 return out

a = sys.argv[1]
b = sys.argv[2:]

l=[]
for bn in b: l.append(ORoutputstring(a,bn))
restofreport = "".join(l)

report = a + ' ' + " ".join(b) + '\n' + restofreport
 
webbrowser.open("x-drafts4://x-callback-url/create?text=" + urllib.quote(report))

