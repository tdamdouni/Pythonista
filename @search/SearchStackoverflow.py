# Search StackOverflow for selected text

import editor
import webbrowser

text = editor.get_text()
s = editor.get_selection()
selection = text[s[0]:s[1]]
if len(selection) > 0:
	from urllib import quote
	q = quote(selection)
	search_url = 'http://stackoverflow.com/search?q=' + q
	webbrowser.open(search_url)
else:
	from console import alert
	i = alert('No Selection', 'Do you want to open the StackOverflow homepage?', 'StackOverflow')
	if i == 1:
		webbrowser.open('http://stackoverflow.com')
