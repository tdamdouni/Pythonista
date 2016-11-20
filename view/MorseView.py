#!/usr/bin/env python

# Source code: https://github.com/cclauss/Pythonista_ui
# See: http://omz-forums.appspot.com/pythonista/post/4959204154540032
# See: http://en.wikipedia.org/wiki/Morse_code

import morse_code, toggle_flashlight, time, ui

dot_secs  = 0.2  # time a dot is lit up, also dark time between each dot or dash
dash_secs = dot_secs * 3  # time a dash is lit up, also dark time between each letter
word_secs = dot_secs * 7  # dark time between words

morse_dict = {
    '.' : (True,  dot_secs),
    '-' : (True,  dash_secs),
    ' ' : (False, dash_secs-dot_secs),
    ',' : (False, word_secs-dot_secs) }
valid_chars = ''.join(morse_dict.iterkeys())

@ui.in_background
def flash_message(msg='--- ... ---'):
	msg = msg.strip().replace('  ', ',')  # mark word boundries with ,
	assert msg, 'No message entered!!'
	assert not msg.strip(valid_chars), 'illegal morse code: ' + msg.strip(valid_chars)
	for c in msg:
		light_on, duration = morse_dict[c]
		if light_on: toggle_flashlight.toggle_flashlight()  # light on
		time.sleep(duration)
		if light_on: toggle_flashlight.toggle_flashlight()  # light off
		time.sleep(dot_secs)
		
class MorseView(ui.View):
	def __init__(self):
		self.width, _ = ui.get_screen_size()
		self.add_subview(self.make_button())
		self.add_subview(self.make_textview())
		self.present('sheet')
		
	def morse_action(self, sender):
		msg = morse_code.morse(self['textfield'].text)
		assert msg, 'No message!!'
		self['textfield'].text = msg
		flash_message(msg)
		
	def make_button(self):
		button = ui.Button(name='button', title='Send message')
		button.action = self.morse_action
		button.width  = self.width
		return button
		
	def make_textview(self):
		tf = ui.TextField(name='textfield', frame=self.bounds)
		offset = self['button'].height
		tf.y      += offset
		tf.height -= offset
		tf.border_color = (0, 0, 1)
		tf.border_width = 2
		tf.alignment = ui.ALIGN_CENTER
		tf.text = 'This is a test!'
		return tf
		
def main(args):
	view = MorseView()
	
if __name__ == "__main__":
	import sys  # put quotes around morse code on commandline or words will run together
	main(sys.argv[1:])  # strip off the script name

