# coding: utf-8
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

webbrowser.open('drafts4://new?text=' + s)

