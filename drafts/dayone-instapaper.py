from __future__ import print_function
# https://gist.github.com/lukf/8982684

import feedparser, webbrowser, urllib, console, sys, datetime
console.clear()
feedURL="URL" # RSS feed URL
outp="Reading list from today \n" # header
dayone_footer="#readlater" # Gets appended to the entry
today=datetime.date.today()
todayString=today.strftime("%a, %d %b %Y")
for post in feedparser.parse(feedURL).entries:
	postDate=post.published
	if todayString in postDate:
		# add to outp
		outp=outp+(postDate.lstrip(todayString))[:-3]+" "+"["+post.title+"]("+post.link+")\n"
		
dayone_entry=outp+dayone_footer
# User confirmation
print(dayone_entry)
if not raw_input("-- Press enter to import"):
	# encode final entry
	dayone_entry = urllib.quote(dayone_entry.encode("utf-8"))
	webbrowser.open('dayone://post?entry='+dayone_entry)
sys.exit()

###

import feedparser, webbrowser, urllib, console, sys, datetime
console.clear()
feedURL = 'URL' # RSS feed URL
todayString = datetime.date.today().strftime('%a, %d %b %Y')
outp = ''
fmt = '{} [{}]({})\n'
for post in feedparser.parse(feedURL).entries:
    postDate = post.published
    if todayString in postDate:
        outp += fmt.format(postDate.lstrip(todayString)[:-3], post.title, post.link)
if not outp:
    sys.exit('No output!!')
dayone_entry = 'Reading list from today\n{}\n#readlater'.format(outp)
# User confirmation
print(dayone_entry)
if not raw_input('-- Press enter to import'):
    # encode final entry
    dayone_entry = urllib.quote(dayone_entry.encode('utf-8'))
    webbrowser.open('dayone://post?entry=' + dayone_entry)
