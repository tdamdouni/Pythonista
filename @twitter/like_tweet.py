# coding: utf-8

# https://gist.github.com/crocbuzz/37167e5eb02867eee868

import twitter
import json
import re
import clipboard

account = twitter.get_account('acrockr')

# Do not touch the code below

api = 'https://api.twitter.com/1.1/favorites/create.json'
regex = '^(http?s://?w?w?w?.twitter\.com/)([a-zA-Z0-9_]{1,15})(/status/)([0-9]{1,20})$'

def like_tweet(x):
	pattern_match = re.findall(regex, x)
	tup = pattern_match[0]
	user = tup[1]
	id = tup[3]
	params = {'id':id}
	status = twitter.request(account, api, 'POST', params)
		
def fetch_link_from_clipboard():
	text = clipboard.get()
	if re.match(regex, text):
		print('Tweet link found in clipboard...')
		like_tweet(text)
	else:
		print('Clipboard does not contain a link to a tweet.')

fetch_link_from_clipboard()
	
	