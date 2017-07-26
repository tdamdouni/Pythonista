# https://forum.omz-software.com/topic/4086/using-webview-for-textfield/2

# @omz

import ui

def textfield_action(sender):
	web_view = sender.superview['webview']
	url = sender.text
	if not (url.startswith('http://') or url.startswith('https://')):
		url = 'http://' + url
	#web_view.load_url(url)
	web_view.load_url('https://www.google.com/search?q=' + sender.text)
	
	# If your search term contains spaces, or other characters that aren't allowed in a URL, you'll need to quote them, e.g. foo bar => foo%20bar. @omz

	import urllib.parse
	search_term = urllib.parse.quote(sender.text, '')
	webview.load_url('https://www.google.com/search?q=' + search_term)
	
main_view = ui.View(
    frame=(0, 0, 400, 400), bg_color='white', name='WebView Demo'
)
text_field = ui.TextField(
    frame=(0, 0, 400, 40),
    flex='W',
    keyboard_type=ui.KEYBOARD_URL,
    autocorrection_type=False,
    autocapitalization_type=ui.AUTOCAPITALIZE_NONE,
    action=textfield_action,
    placeholder='Enter URL'
)
main_view.add_subview(text_field)
web_view = ui.WebView(name='webview', frame=(0, 40, 400, 360), flex='WH')
main_view.add_subview(web_view)

web_view.background_color = 'purple'
web_view.load_html('<body style="background-color: purple;"/>')

main_view.present()

