import json, requests, sys  #, pprint

'''
https://github.com/taherh/twitter_application_auth/blob/master/get_bearer_token.py

Use get_bearer_token.py (works on Pythonista) to get your Twitter access_token.
> You will need to create a new application on https://dev.twitter.com
> Enter below the Twitter access_token you get from running get_bearer_token.py
'''

twitter_access_token = 'Replace this text with the access_token you get from running get_bearer_token.py'

tweet_fmt = 'On {created_at}, {user[name]} ({user[screen_name]}) wrote:\n> {text}'

def recent_tweets(screen_name, tweet_count = 3):
    headers = { 'Authorization' : 'Bearer ' + twitter_access_token }
    payload = { 'count'         : str(tweet_count),  # keep low to avoid taxing Twitter API
                'screen_name'   : screen_name }
    timelineURL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    response = requests.get(timelineURL, params=payload, headers=headers)
    tweets_as_json = response.json()
    if not isinstance(tweets_as_json, list):    # we should get a list of tweet_dicts
        print(response.url)
        return response.text                    # exit with an error message from API
    with open('tweets.json', 'w') as out_file:  # write the tweets to a file to allow
        json.dump(tweets_as_json, out_file)     # experimentation without calling API
    for tweet_dict in tweets_as_json:
        #pprint.pprint(tweet_dict)              # uncomment to see available fields
        print(tweet_fmt.format(**tweet_dict))

def main(argv):
    screen_name = argv[1] if len(argv) > 1 else 'pycoders'
    tweet_count = argv[2] if len(argv) > 2 else 3
    return recent_tweets(screen_name, tweet_count)

if __name__ == '__main__':
    print('-' * 40)
    sys.exit(main(sys.argv))
