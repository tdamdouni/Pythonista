# @viticci
# Same as ConvertMarkdown, but also pastes output into a new *Editorial* document using Editorial's URL scheme.
# You can change the URL for webbrowser.open at the end to any app you like
# The app has to support a URL scheme that lets you add output to a document
# Text is set to clipboard, then encoded to utf-8 to avoid Unicode errors
# In Byword's case, the output is passed along to a new text file after Markdown conversion to HTML

import webbrowser
import markdown
import clipboard
import urllib

input_file = clipboard.get()

s = input_file

md = markdown.Markdown()
html = md.convert(s)

clipboard.set(html)

s = clipboard.get()
s = urllib.quote(s.encode('utf-8'))

webbrowser.open('editorial://new?text=' + s)