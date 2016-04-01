# https://gist.github.com/omz/f3886441053d0ea79f39

import ui

# Mapping based on http://www.upsidedowntext.com/unicode
CHARMAP = {'!': '\xc2\xa1', '"': ',,',
           "'": ',', '&': '\xe2\x85\x8b', 
           ')': '(', '(': ')', ',': "'", 
           '.': '\xcb\x99', 
           '1': '\xc6\x96',
           '0': '0', '3': '\xc6\x90',
           '2': '\xe1\x84\x85', 
           '5': '\xcf\x9b', 
           '4': '\xe3\x84\xa3', 
           '7': '\xe3\x84\xa5', '6': '9', 
           '9': '6', '8': '8', '<': '>', 
           '?': '\xc2\xbf', '>': '<',
           'A': '\xe2\x88\x80', 
           'C': '\xc6\x86', 'B': 'B', 
           'E': '\xc6\x8e', 'D': 'D',
           'G': '\xd7\xa4', 
           'F': '\xe2\x84\xb2', 
           'I': 'I', 'H': 'H', 'K': 'K', 
           'J': '\xc5\xbf', 'M': 'W', 
           'L': '\xcb\xa5', 'O': 'O', 
           'N': 'N', 'Q': 'Q', 
           'P': '\xd4\x80', 'S': 'S',
           'R': 'R', 'U': '\xe2\x88\xa9', 
           'T': '\xe2\x94\xb4', 'W': 'M', 
           'V': '\xce\x9b', 
           'Y': '\xe2\x85\x84', 
           'X': 'X', '[': ']', 
           'Z': 'Z', ']': '[', 
           '_': '\xe2\x80\xbe', 
           'a': '\xc9\x90', '`': ',', 
           'c': '\xc9\x94', 'b': 'q', 
           'e': '\xc7\x9d', 'd': 'p', 
           'g': '\xc6\x83', 
           'f': '\xc9\x9f', 
           'i': '\xe1\xb4\x89', 
           'h': '\xc9\xa5', 
           'k': '\xca\x9e', 
           'j': '\xc9\xbe', 
           'm': '\xc9\xaf', 
           'l': 'l', 'o': 'o', 'n': 'u', 
           'q': 'b', 'p': 'd', 's': 's', 
           'r': '\xc9\xb9', 'u': 'n', 
           't': '\xca\x87', 
           'w': '\xca\x8d',
           'v': '\xca\x8c', 
           'y': '\xca\x8e', 'x': 'x', 
           '{': '}', 'z': 'z', '}': '{',
           '-': '-'
}


class TextViewDelegate (object):
	def textview_should_change(self, tv, rng, repl):
		if repl == '':
			return True
		ud = ''.join(reversed([CHARMAP.get(x, x) for x in repl]))
		text_len = len(tv.text)
		tv.replace_range(rng, ud)
		tv.selected_range = rng[0], rng[0]
		return False

tv = ui.TextView()

def copy_action(sender):
	import clipboard
	import console
	clipboard.set(tv.text)
	console.hud_alert('Copied')

copy_button = ui.ButtonItem(title='Copy', action=copy_action)
tv.right_button_items = [copy_button]
tv.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
tv.autocorrection_type = False
tv.spellchecking_type = False

tv.font = ('HelveticaNeue', 36)
tv.delegate = TextViewDelegate()
tv.name = 'Upside-Down Text'
tv.present('sheet')