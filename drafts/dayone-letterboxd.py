# -*- coding: utf-8 -*-
from __future__ import print_function
import feedparser, webbrowser, urllib, console, sys
selected = "no"
notes = ""
try:
	notes = sys.argv[2]
except:
	pass
console.clear()
feedURL="http://letterboxd.com/YOURUSERNAME/rss" # Insert your letterboxd username
# Cycle through RSS items
for post in feedparser.parse(feedURL).entries:
	print(post.title)
	# Continue with selected item
	if "preselect" in sys.argv:
		selected = "yes"
	elif not raw_input("-- Press enter to import"):
		console.clear()
		notes = raw_input("Any comments?")
		selected = "yes"
	if selected == "yes":
		dayone_fmt="Movie log\n\n|Movie||\n|:---|:---|\n|Title|[" + post.title.split(", ")[0].replace("|","–") + "](" + post.link + ")|\n|Year|" + post.title.split(", ")[1].lstrip(", ").split(" ")[0] + "\n|Rating|" + (post.title)[-5:].strip(" -1234567890") + "|\n|Notes|" + notes.replace("|","–") + "|\n<" + post.description.split("</p>")[0].lstrip("<p>") + post.description.split("</p>")[1].replace("</p>", "").replace("<p>", "") + "\n#watched"
		
		dayone_entry=urllib.quote(dayone_fmt.encode("utf-8"))
		webbrowser.open('dayone://post?entry=' + dayone_entry)
		sys.exit()
sys.exit()
