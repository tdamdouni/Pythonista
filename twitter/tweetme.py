import twitter, ui, dialogs, console

all_accounts = twitter.get_all_accounts()
if len(all_accounts) >= 1:
	account = all_accounts[0] # get main account
	
text = dialogs.text_dialog(title='Tweet a Tweet', autocapitalization=ui.AUTOCAPITALIZE_SENTENCES)
if len(text) < 140:
	twitter.post_tweet(account, text, parameters=None)
	console.hud_alert('Tweet Posted!', 'success', 1.5)
else:
	console.hud_alert('Exceeded Character Limit', 'error', 1.5)

