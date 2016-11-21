# https://github.com/danrcook/Post-to-Pythonista-Forum

# Copy the code into a .py file in Pythonista. Add your OMZ forum username and password to the top variables.
# You can use this as an action extension in Pythonista App. This requires code to be open. When you run it, it will take copy the code you are working on into the post and append/prepend HTML tags to indicate the code. A title is required and please select the right category.

import urllib
import ui
import editor
import markdown
import requests

omz_forum_username = ''
omz_forum_password = ''

def submit_post(sender):
	global omz_forum_password, omz_forum_username
	login_info = {'username': omz_forum_username, 'password': omz_forum_password,}
	login_data = urllib.urlencode(login_info)
	
	if not title_field.text:
		alert_text.text = 'You need a Title!'
		alert.present('popover')
		return None
		
	sc_option = ('General', 'Share Code', 'Questions')[sc.selected_index]
	
	post_info = {'title' : str(title_field.text), 'category' : sc_option, 'text' : post_edit_box.text, 'forum' : 'pythonista'}
	post_data = urllib.urlencode(post_info)
	clen = '\'%s\'' % len(post_edit_box.text)
	
	with requests.session() as c:
		login = c.post('https://omz-forums.appspot.com/login?%s' % login_data)
		post_headers = {'content-length': clen, 'content-type': 'text/html; charset=UTF-8'}
		post_url = 'http://omz-forums.appspot.com/pythonista/new?%s' % post_data
		if login.cookies:
			c.post(post_url, headers=post_headers)
			alert_text.text = 'Submitted'
			alert.present('popover')
			view.close()
		elif not login.cookies:
			alert_text.text = 'Login Unsuccessful'
			alert.present('popover')
			
def cancel_alert(sender):
	alert.close()
	
def submit_test(sender):
	testtext = post_edit_box.text
	post_edit_box.text = 'testing' + testtext
	
def insert_code():
	return 'Write Something!\n\n<pre><code>\n\n%s\n</code></pre>' % editor.get_text()
	
def markdown_prev(sender):
	mkd_w.load_html(markdown.markdown(post_edit_box.text))
	mkd.present('fullscreen')
	
#UI Code
view = ui.View()
view.background_color = 'white'
markdown_prev = ui.ButtonItem(title='Markdown Preview', action=markdown_prev, enabled=True)
view.right_button_items = [markdown_prev]

#Title Field
title_field = ui.TextField()
title_field.frame = 5,8,600,30
title_field.corner_radius = 5
title_field.bordered = True
title_field.border_color = '#999999'
title_field.border_width = 1
title_field.placeholder = 'Title of Post (Required)'
view.add_subview(title_field)

#Post Type
sc = ui.SegmentedControl()
sc.segments = ['General','Share Code','Question']
sc.enabled = True
sc.selected_index = 0
sc.frame = 615,8,400,30
view.add_subview(sc)

#Label
post_label = ui.Label()
post_label.frame = 5,45,250,30
post_label.text = "Edit your post:"
view.add_subview(post_label)

#Post Draft Box
post_edit_box = ui.TextView()
post_edit_box.frame = 5,80,1014,620
post_edit_box.font = ('Arial',14)
post_edit_box.border_width = 1
post_edit_box.border_color = '#999999'
post_edit_box.corner_radius = 5
post_edit_box.text = insert_code()
view.add_subview(post_edit_box)

#Markdown Preview View
mkd = ui.View()
submit = ui.ButtonItem(title='Submit', action=submit_post, enabled=True)
mkd.right_button_items = [submit]
mkd_w = ui.WebView()
mkd_w.scales_page_to_fit = False
mkd_w.flex = 'WH'
mkd.add_subview(mkd_w)

#Alert Popup
alert = ui.View()
alert.name = 'Notice:'
alert.width, alert.height = 300,300
alert_text = ui.TextView()
alert_text.frame = 0,0,300,260
alert_button = ui.Button()
alert_button.title = 'Okay'
alert_button.frame = 0,260,300,40
alert_button.action = cancel_alert
alert.add_subview(alert_text)
alert.add_subview(alert_button)

view.present('fullscreen')

