from __future__ import print_function
import console
import sys
import webbrowser
import datetime
import urllib

console.clear()

#The Drafts action passes two variables to Pythonista - [[title]] 
#Use sys.argv[x] to call these variables. Remember, the script *name* takes sys.argv[0].

print("Formatting the article.\n")
	
articleTitle = sys.argv[1]
articleBody = sys.argv[2]

#Current date and time :
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M")
#URL Encode the date & time
UAnow = urllib.quote(now, safe='')

#Convert the title to lowercase and replaces any spaces with dashes. Use that as the slug.
articleSlug = articleTitle.lower().replace(" ","-")

#URL encode the title and body
UEArticleTitle = urllib.quote(articleTitle, safe='')
UEArticleBody = urllib.quote(articleBody, safe='')

#The crazy looking URL below will format the Pelican metadata like so:

#Title: UEArticleTitle
#Date: now
#Tags: 
#Category: 
#Slug: articleSlug
#Author: Rob
#Summary: 
#Status: draft

#UEArticleBody

#This creates a Notesy note with the name specified (it will append to an existing note if applicable) and sets the text.
#toNotesy = notesy://x-callback-url/append?name=whatever&text=[[draft]]

toNotesy = 'notesy://x-callback-url/append?name=' + UEArticleTitle + '&text=Title%3A%20' + UEArticleTitle + '%0ADate%3A%20' + UAnow + '%0ATags%3A%20%0ACategory%3A%20%0ASlug%3A%20' + articleSlug + '%0AAuthor%3A%20Rob%0ASummary%3A%20%0AStatus%3A%20draft%0A%0A' + UEArticleBody

#print toNotesy

webbrowser.open(toNotesy)
