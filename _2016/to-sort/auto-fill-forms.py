# https://forum.omz-software.com/topic/3489/auto-fill/4

import ui,time
w=ui.WebView()
w.frame=(0,0,570,570)
w.load_url('https://google.com')
w.present()

# make sure the page has finished loading
time.sleep(1)
while not w.eval_js('document.readyState') == 'complete':
	time.sleep(1.)
	
# using bs4 and requests to poke around, i know the textfield has a name of q
# i can set the value using javascript
w.eval_js('document.getElementsByName("q")[0].value="using javascript to fill in forms";')

# i happen to know the name of the form is "f", i will submit the form
time.sleep(1)
w.eval_js('document.getElementsByName("f")[0].submit()')

