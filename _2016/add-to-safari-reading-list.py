# coding: utf-8

# https://forum.omz-software.com/topic/3857/webbrowser-add_to_reading_list-is-no-longer-working-when-including-non-english-characters-url-after-updating-ios-from-8-to-10

import webbrowser

a = 'http://example.com/a'
b = 'http://example.com/あ'
c = 'http://example.com/%e3%81%82'

for n in [a, b, c]:
	webbrowser.add_to_reading_list(n)

