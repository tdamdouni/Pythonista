# takes post from markdown, converts to html, fixes links to open in new window

import clipboard
import re
import markdown

s = clipboard.get()

md = markdown.Markdown()
myString = md.convert(s)
output = re.sub(r'(?<!<a target="_blank") href="(?!http://(www\.)?n8henrie\.com)', ' target="_blank" href="', myString)

print output
clipboard.set(output)
