# https://forum.omz-software.com/topic/4086/using-webview-for-textfield/13

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
	
	#url = www.google.se
def buttonTapped(sender3):
	n_view = ui.View()
	n_view.name = 'Option'
	n_view.background_color = 'white'
	#n_view.frame=(0, 0, 400, 400)
	#sender3.navigation_view.push_view(n_view) <-- This is where I get the "Attribute Error"
	nav_view.present()
	sender3.superview.navigation_view.push_view()
	
main_view = ui.View(
    frame=(0, 0, 400, 400), bg_color='white', name='Grizzly Browser'
)
text_field = ui.TextField(
        frame=(129, 0, 50, 40),
        flex='W',
        keyboard_type=ui.KEYBOARD_URL,
        autocorrection_type=False,
        autocapitalization_type=ui.AUTOCAPITALIZE_NONE,
        action=textfield_url,

        placeholder='URL:'
        #text_field
)
seach_field = ui.TextField(
            frame=(520, 0, 0, 40),
            flex='w',
            keyboard_type=ui.KEYBOARD_WEB_SEARCH,
            autocorrection_type=False,
            autocapitalization_type=ui.AUTOCAPITALIZE_NONE,
            action=searchfield_url,
            placeholder = 'Search:'
)


B1 = ui.Button(title = 'Home' ,frame = (4,5,20,20))
B1.action = homeButton
B1.tint_color = 'black'


B2 = ui.Button(title = 'Back' ,frame = (55,5,20,20))
B2.action = Back
B2.tint_color = 'black'





b3 = ui.Button(title = 'opt')
b3.action = buttonTapped
b3.frame = (80,0,50,50)
main_view.add_subview(b3)


main_view.add_subview(text_field)
web_view = ui.WebView(name='webview', frame=(0, 40, 400, 360), flex='WH')



nav_view = ui.NavigationView(main_view)
nav_view.frame=(0, 0, 400, 400)

#web_view.load_html('<body style="background-color: indigo;"/>')
main_view.add_subview(web_view)
main_view.add_subview(B1)
main_view.add_subview(B2)
main_view.add_subview(seach_field)
main_view.present()

web_view.load_url('http://www.feber.se') #StartPage

