#Made for Pythonista
#Reads the titles of reddit posts, fun little pythonista demo of BS4 and the speech module
#If anyone has any tips on how to ensure proper text encoding please leave a comment!
#
#
#
import httplib
import speech
import console
from bs4 import BeautifulSoup

def stop():
	speech.stop()
	
conn = httplib.HTTPConnection("www.reddit.com")
conn.request("GET", "/r/worldnews/.rss")
r1 = conn.getresponse()
data1 = r1.read()
soup=BeautifulSoup(unicode(data1))

console.clear()
entries=soup.find_all("title")
for titles in entries:
	print("#"+str(entries.index(titles))+": "+titles.decode_contents()+"\n")
	entries[entries.index(titles)]="Item #"+str(entries.index(titles))+", "+titles.decode_contents()
speech.say(". ".join(entries[1:]),'en-EN',0.2)


conn.close()

