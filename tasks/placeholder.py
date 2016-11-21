# coding: utf-8

# https://discourse.omnigroup.com/t/ios-templating-and-pythonista/24217/4

import appex
import clipboard
import dialogs
import re
import urllib
import webbrowser

def fill_placeholders(action_in):
# Find placeholders
	known_placeholders = set()
	placeholders = []
	fields = []
for placeholder_match in re.finditer(u"«(.+?)»", action_in):
	placeholder = placeholder_match.group(1)
if placeholder not in known_placeholders:
	known_placeholders.add(placeholder)
placeholders.append(placeholder)
fields.append({'type': 'text', 'title': placeholder, 'key': placeholder})

