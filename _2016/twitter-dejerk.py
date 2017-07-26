# https://gist.github.com/paultopia/236bfe61782cd7e5ad7f0a4f00edd202

# https://forum.omz-software.com/topic/3943/twitter-jerk-remover-lazyscript

# written for pythonista ios app, takes advantage of its library and access to ios twitter login.  generates a list of followers who don't follow you back and lets you look at each individually to decide whethee to dispose of them or not.  Only works for followers < 5000 amd following < 5000, else rate limits and cursors get imvolved and are icky.  could use a real UI.

import twitter, json, webbrowser, random
account = twitter.get_all_accounts()[0]
followers = frozenset(json.loads(twitter.request(account, "https://api.twitter.com/1.1/followers/ids.json", "GET")[1].decode("utf-8"))["ids"])
ifollow =  frozenset(json.loads(twitter.request(account, "https://api.twitter.com/1.1/friends/ids.json", "GET")[1].decode("utf-8"))["ids"])
not_following_back = list(ifollow.difference(followers))
def make_url(id):
    return 'https://twitter.com/intent/user?user_id=' + str(id)
turls = [make_url(id) for id in not_following_back]
random.shuffle(turls) # so you don't get the same ones you kept before over and over on repeated runs

# lazy ui: just opens a browser tab (may need to log in the first time) with each person who doesn't follow you back, hitting enter opens new one.
state = ''
while state is not 'd':
    url = turls.pop()
    webbrowser.open(url)
    state = input('enter d if done, anything else to continue')

