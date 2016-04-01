# Source: https://gist.github.com/Blether/8605849
#
# quickly calculate BMI
# for use from Drafts

import sys
import webbrowser
import urllib

def bmi(w, h):
	bmiout = round(w/(h ** 2), 2)
	return bmiout

def bmiStr(w, h):
	bmiout = str(bmi(float(w),float(h)))
	return bmiout
	
def bmiReportString(a,b):
	out = 'wt ' + a + ' h ' + b + ' BMI '  + bmiStr(a, b) + '\n' + 'wt ' + b + ' h ' + a + ' BMI '  + bmiStr(b, a) + '\n\n'
	return out

a = sys.argv[1]
b = sys.argv[2:]

if float(a) > 5:
	a = str(float(a)/100)

l=[]
for bn in b: l.append(bmiReportString(a,bn))
restofreport = "".join(l)

report = a + ' ' + " ".join(b) + '\n' + restofreport


webbrowser.open("x-drafts4://x-callback-url/create?text=" + urllib.quote(report))
