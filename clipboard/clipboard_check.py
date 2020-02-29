from __future__ import print_function
#Convert clipboard to uppercase/lowercase
import clipboard
text = clipboard.get()
if text == '':
	print('No text in clipboard')
else:
	uppercase = text.upper()
	if uppercase != text:
		new_clip = uppercase
	else:
		#already uppercase, convert to lowercase
		new_clip = text.lower()
	clipboard.set(new_clip)
	print(new_clip)

