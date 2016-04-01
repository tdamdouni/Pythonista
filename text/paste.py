# https://gist.github.com/GuyCarver/4143021
# paste clipboard to buffer.
import clipboard
import editor

cliptext = clipboard.get()
if cliptext != '':
	text = editor.get_text()
	selection = editor.get_selection()
	selected_text = text[selection[0]:selection[1]]
	replacement = cliptext + selected_text
	
	editor.replace_text(selection[0], selection[1], replacement)
#	editor.set_selection(selection[0], selection[0] + len(replacement) - 1)

# Cclauss Comment

# Paste the current clipboard text into the editor replacing the current selection.
#import clipboard, editor
#cliptext = clipboard.get()
#if cliptext:
#    selection = editor.get_selection()
#    editor.replace_text(selection[0], selection[1], cliptext)
