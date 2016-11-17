# https://forum.omz-software.com/topic/3239/can-we-tweet-with-selected-photos

import twitter, ui, dialogs, console,photos

def tweet(account,text,param=None):
	if len(text) < 140:
		twitter.post_tweet(account, text, parameters=param)
		console.hud_alert('Tweet Posted', 'success', 1.5)
	else:
		console.hud_alert('Exceeded Character Limit', 'error', 1.5)
		
assets = photos.pick_asset(title='Pick Some Assets', multi=False)
params={
    'media_id_string':assets.local_id,
    'image_type':assets.media_type,
    'image':{
        'w':assets.pixel_width,
        'h':assets.pixel_height
    }
}

all_accounts = twitter.get_all_accounts()
if len(all_accounts) >= 1:
	account = all_accounts[0]
	text = dialogs.text_dialog(title='Input Tweet')
	if text:
		tweet(account,text+' #my_hash_tag',params)
	else:
		console.hud_alert('User Cancelled')
		
# --------------------

