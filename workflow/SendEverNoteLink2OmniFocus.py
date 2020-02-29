from __future__ import print_function
import clipboard
import re
import webbrowser
import console

console.clear()

#enURL = "https://www.evernote.com/shard/s17/nl/1950193/1045b8fc-e5a6-4b85-85c7-39ee41c0d9c7/"
ofURL = "omnifocus:///add?note="

def get_shardID(URLToParse):
	start = re.search(r'shard/', URLToParse)
	finish = re.search(r'/', URLToParse[start.span()[1]:])
	shardID_span = (start.span()[1], start.span()[1]+finish.span()[1]-1)
	shardID = URLToParse[shardID_span[0]:shardID_span[1]]
	return shardID

def get_userID(URLToParse):
	start = re.search(r'(shard/([^/]+/){2})', URLToParse)
	finish = re.search(r'/', URLToParse[start.span()[1]:])
	userID_span = (start.span()[1], start.span()[1]+finish.span()[1]-1)
	userID = URLToParse[userID_span[0]:userID_span[1]]
	return userID

def get_noteID(URLToParse):
	start = re.search(r'(shard/([^/]+/){3})', URLToParse)
	finish = re.search(r'/', URLToParse[start.span()[1]:])
	noteID_span = (start.span()[1], start.span()[1]+finish.span()[1]-1)
	noteID = URLToParse[noteID_span[0]:noteID_span[1]]
	return noteID

webURL = clipboard.get()
#webURL = enURL

if webURL != "":
	shardID = get_shardID(webURL)
	print('shardID = ', shardID)
	userID = get_userID(webURL)
	print('userID = ', userID)
	noteID = get_noteID(webURL)
	print('noteID = ', noteID)
	appifiedURL = "evernote:///view/" + userID + "/" + shardID + "/" + noteID + "/" + noteID + "/"
	print(appifiedURL)
	clipboard.set(appifiedURL)
	print("Evernote URL copied to clipboard.")
	print('Copying link to new OmniFocus action...')
	webbrowser.open(ofURL+appifiedURL)