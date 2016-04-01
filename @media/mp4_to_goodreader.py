import urllib2
import webbrowser
import re
import sys
import clipboard

mp4= re.compile('(http.+mp4). class')

URL = sys.argv[1]

title = re.compile('\/\d+\/([\w_]+).html')
clipboard.set(title.findall(URL)[0])

getText = urllib2.Request(URL)
openText = urllib2.urlopen(getText)
content = (openText.read().decode('utf-8'))

final = content.encode('utf-8')

p = mp4.findall(final)

mp4_file = re.compile('mp4File\=(.+)')
r = mp4_file.findall(p[0])
file = urllib2.unquote(r[0]).decode("utf8")

webbrowser.open('g' + file)
