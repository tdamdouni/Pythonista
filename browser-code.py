# https://forum.omz-software.com/topic/4123/possible-to-change-menubar-header-color-and-font-for-ui-view/4

import ui
import urllib.parse

def textfield_url(test):

	web_view = test.superview['webview'] # superview = in front of other
	url = test.text
	if not (url.startswith('http://') or url.startswith('https://')): # needed for urls starting with http or https
		url = 'http://' + url
		
	web_view.load_url(url)
	
def searchfield_url(test2):
	web_view = test2.superview['webview']
	url = test2.text
	search_term = urllib.parse.quote(test2.text, '')
	web_view.load_url('https://www.google.com/search?q=' + search_term)
	
def homeButton (sender): # Working!
	web_view.load_url('http://www.google.se')
	#url = 'www.google.se'
	
def Back(sender2): # Working!
	web_view.go_back()
	
def buttonTapped(sender3): # Working!
	def bHome(sender5):# Working!
		web_view.load_url('http://www.google.se')
		
	n_view = ui.View()
	n_view.name = 'Option'
	n_view.background_color = .47, .47, .47
	n_view.frame=(0,40,400,360)
	sender3.superview.navigation_view.push_view(n_view)
	b4 = ui.Button(title = 'Home', frame = (360,80,70,70))
	b4.tint_color = 'black'
	b4.action = bHome
	n_view.add_subview(b4)
	b5 = ui.Button(frame = (330,180,100,70))
	b5.title = 'bookmarks'
	b5.tint_color = 'black'
	n_view.add_subview(b5)
	
main_view = ui.View(
     name='Grizzly Browser'
)
main_view.background_color = 'white'

text_field = ui.TextField(
        frame=(129, 0, 50, 40),
        flex='W',
        keyboard_type=ui.KEYBOARD_URL,
        autocorrection_type=False,
        autocapitalization_type=ui.AUTOCAPITALIZE_NONE,
        action=textfield_url,

        placeholder='URL:'

)

text_field.f = .67, .07, .23
seach_field = ui.TextField(
            frame=(520, 0, 0, 40),
            flex='w',
            keyboard_type=ui.KEYBOARD_WEB_SEARCH,
            autocorrection_type=False,
            autocapitalization_type=ui.AUTOCAPITALIZE_NONE,
            action=searchfield_url,
            placeholder = 'Search:'
)

B1 = ui.Button(frame = (4,5,30,30))
B1.image = ui.Image.named('iob:home_256')
B1.action = homeButton
B1.tint_color = 'black'

B2 = ui.Button(frame = (50,5,30,30))
B2.image = ui.Image.named('iob:reply_256')
B2.action = Back
B2.tint_color = .21, .13, .15

b3 = ui.Button(frame = (100,10,20,20))
b3.action = buttonTapped
b3.image = ui.Image.named('iob:gear_a_256')
main_view.add_subview(b3)

main_view.add_subview(text_field)
web_view = ui.WebView(name='webview', frame=(0, 40, 400, 360), flex='WH')

main_view.add_subview(web_view)
main_view.add_subview(B1)
main_view.add_subview(B2)
main_view.add_subview(seach_field)

web_view.load_url('http://www.google.se') #StartPage
#main_view.present('fullscreen',title_bar_color='silver') # Crashes everytime
nav_view = ui.NavigationView(main_view)
nav_view.present()

