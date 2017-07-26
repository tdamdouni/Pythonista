# coding: utf-8

# https://github.com/tdamdouni/Pythonista/blob/master/scrap/Selection.py

# in conjuction with Workflow "MD Selection"

import sys
import html2text
import clipboard
import webbrowser

webpage = clipboard.get()

text = sys.argv[1]

h = html2text.HTML2Text()
h.body_width = 0

converted = h.handle(text)

clipboard.set('> ' + converted)

webbrowser.open('safari-' + webpage)
