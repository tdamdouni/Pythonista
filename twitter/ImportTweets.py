from __future__ import print_function
# http://pastebin.com/aubPNCp7#
# coding: utf-8
import twitter
import json

acc = 'tdamdouni'
acc = twitter.get_account(acc)

jsonToDict = json.JSONDecoder()

def getTweetsFrom(user,count='5',maxID=None):
	url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?'
	params = [	'screen_name=',
				'count=',
				'trim_user=true',
				'exclude_replies=false',]
	
	if maxID is not None:
		params.append('max_id='+maxID)		
	params[0] += user
	params[1] += str(count)
	
	combined = url
	for p in params:
		combined = combined + p + '&'
	combined = combined[:-1]	#removes last &
	#print combined
	
	result = twitter.request(acc,combined)

	result = jsonToDict.decode(result[1])
	#print result
	return result



def getAllTweetsFrom(user):
	url = 'https://api.twitter.com/1.1/users/lookup.json?screen_name=' + user
	userObj = twitter.request(acc,url)
	userObj = jsonToDict.decode(userObj[1])[0]
	tweetAmount = userObj['statuses_count']
	print('Potential number of tweets: ',tweetAmount)
	savedTweets = []
	lastID = getTweetsFrom(user,1)[0]['id_str']
	oldLastID = ''
	
	while oldLastID != lastID:
		oldLastID = lastID
		t = getTweetsFrom(user,'200',lastID)
		lastID = t[-1]['id_str']
		for tweet in range(len(t)):
			t[tweet] = t[tweet]['text']
		savedTweets.extend(t)
		print('Retrieved ' + str(len(savedTweets)) + ' Tweets')
		
	chars = 0
	for tweet in savedTweets:
		chars += len(tweet)
	print('All tweets from',user, '(', len(savedTweets),') together contain', chars, 'characters.')

getAllTweetsFrom('tdamdouni')