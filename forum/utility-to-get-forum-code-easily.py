# https://forum.omz-software.com/topic/3599/utility-to-get-forum-code-easily

'''Snippet to copy forum code easily
1/ copy the message adress in safari by pressing the underlined text '2 days ago' in the message title:
     xxxxx posted 2 days ago reply quote  0
2/ run this script
3/ if there was some formated code in the message, you get it in the cipboard
'''
import requests, re, clipboard, console, os, bs4
# this for the tests
#clipboard.set('https://forum.omz-software.com/topic/3594/displaying-valid-color-names-in-two-tables/1')
try:
	src = clipboard.get()
	# post number to get the good one
	_,name = os.path.split(src)
	name = str(int(name)-1)
	# get html and interpret it
	r = requests.get(src)
	soup = bs4.BeautifulSoup(r.text)
	#get each post
	ls = soup.find_all('li',component="post")
	for li in ls:
		#find the good post
		a = li.find('a',component="post/anchor")
		if a['name']==name:
			# and strip its code
			code = li.find('code').getText()
	# communicate result
	if code:
		code = '# '+src + '\n\n' + code
		clipboard.set(code)
		console.hud_alert('Code in clipboard!','success',1)
	else:
		console.hud_alert('no code found!','error',1)
except:
	console.hud_alert('clipboard does not contain a valid url!','error',1)
	
# --------------------

