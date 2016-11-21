# coding: utf-8

# https://www.macstories.net/reviews/pythonista-2-0-brings-action-extension-ipad-pro-support-code-editor-improvements-and-more/

import sys
import html2text
import clipboard
import webbrowser
import appex
import console

h = html2text.HTML2Text()
h.body_width = 0


if appex.is_running_extension() is True:
	text = appex.get_text()
	converted = h.handle(text)
	clipboard.set(converted)
	console.hud_alert('HTML Converted to Markdown', 'success')
else:
	webpage = clipboard.get()
	text = sys.argv[1]
	converted = h.handle(text)
	clipboard.set('> ' + converted)
	webbrowser.open('safari-' + webpage)

