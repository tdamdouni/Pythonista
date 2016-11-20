# https://github.com/dgelessus/pythonista-scripts/blob/master/today_python_console.py

import appex
import code
import sys
import threading
import time
import ui

class NotifyOnCloseView(ui.View):
	def will_close(self):
		with self.condition:
			self.condition.notify_all()
			
class Keyboard(object):
	KEY_LAYOUTS = [
	[
	[*"^1234567890ß´", "BACKSPACE"],
	[*"qwertzuiopü+", "ENTER_TOP"],
	[*"asdfghjklöä#", "ENTER_BOTTOM"],
	["SHIFT", *"<yxcvbnm,.-"],
	["ALT", "SPACE", "ARROW_LEFT", "ARROW_RIGHT"],
	], [
	[*"°!\"§$%&/()=?`", "BACKSPACE"],
	[*"QWERTZUIOPÜ*", "ENTER_TOP"],
	[*"ASDFGHJKLÖÄ'", "ENTER_BOTTOM"],
	["SHIFT", *">YXCVBNM;:_"],
	["ALT", "SPACE", "ARROW_LEFT", "ARROW_RIGHT"],
	], [
	[*"„¡“¶¢[]|{}≠¿'", "BACKSPACE"],
	[*"«∑€®†Ω¨⁄øπ•±", "ENTER_TOP"],
	[*"å‚∂ƒ©ªº∆@œæ‘", "ENTER_BOTTOM"],
	["SHIFT", *"≤¥≈ç√∫~µ∞…–"],
	["ALT", "SPACE", "ARROW_LEFT", "ARROW_RIGHT"],
	], [
	[*"“¬”#£ﬁ^\\˜·¯˙˚", "BACKSPACE"],
	[*"»„‰¸˝ˇÁÛØ∏°", "ENTER_TOP"],
	[*"ÅÍ™ÏÌÓıˆﬂŒÆ’", "ENTER_BOTTOM"],
	["SHIFT", *"≥‡ÙÇ◊‹›˘˛÷—"],
	["ALT", "SPACE", "ARROW_LEFT", "ARROW_RIGHT"],
	],
	]
	
	KEY_SYMBOLS = {
	"ALT": "\N{option key}",
	"ARROW_LEFT": "\N{leftwards arrow}",
	"ARROW_RIGHT": "\N{rightwards arrow}",
	"BACKSPACE": "\N{erase to the left}",
	"ENTER_BOTTOM": "\N{return symbol}",
	"ENTER_TOP": "|",
	"SHIFT": "\N{upwards white arrow}",
	"SPACE": "\N{open box}",
	}
	
	MOD_SHIFT = 1 << 0
	MOD_ALT = 1 << 1
	
	def __init__(self):
		self.text = []
		self.pos = 0
		self.modifiers = 0b00
		
		##self.root = ui.load_view("keyboard")
		self.root = NotifyOnCloseView()
		self.root.width = 480
		self.root.height = 480
		self.root.bg_color = (0.0, 0.0, 0.0, 0.0)
		
		self.root.add_subview(ui.Label(name="textbox"))
		self.root["textbox"].flex = "TW"
		self.root["textbox"].x = 0
		self.root["textbox"].y = 274
		self.root["textbox"].width = self.root.width
		self.root["textbox"].height = 32
		self.root["textbox"].text = "|"
		self.root["textbox"].font = ("Menlo", 18)
		self.root["textbox"].text_color = (1.0, 1.0, 1.0, 1.0)
		
		self.root.add_subview(ui.View(name="keys"))
		self.root["keys"].flex = "TW"
		self.root["keys"].x = 0
		self.root["keys"].y = 314
		self.root["keys"].width = self.root.width
		self.root["keys"].height = 160
		
		self.reading = self.root.condition = threading.Condition()
		
		self.cached_layouts = []
		
		for layout in type(self).KEY_LAYOUTS:
			container = ui.View()
			self.cached_layouts.append(container)
			container.flex = "WH"
			container.x = 0
			container.y = 0
			container.width = self.root["keys"].width
			container.height = self.root["keys"].height
			
			row_height = container.height / len(layout)
			
			for i, chars in enumerate(layout):
				row = ui.View()
				container.add_subview(row)
				row.x = 0
				row.y = i * row_height
				row.width = row.superview.width
				row.height = row_height
				row.flex = "TBLRWH"
				
				key_width = row.width / len(chars)
				
				for j, char in enumerate(chars):
					key = ui.Button()
					row.add_subview(key)
					key.x = j * key_width
					key.y = 0
					key.width = key_width
					key.height = key.superview.height
					key.flex = "TBLRWH"
					key.font = ("Menlo", 18)
					key.key = char
					key.title = type(self).KEY_SYMBOLS.get(char, char)
					key.tint_color = (1.0, 1.0, 1.0, 1.0)
					key.bg_color = (0.0, 0.0, 0.0, 0.25)
					key.border_color = (0.0, 0.0, 0.0, 1.0)
					key.border_width = 2.0
					key.corner_radius = 5.0
					key.action = self.key_pressed
					
		self.update_layout()
		
	def update_layout(self):
		keys = self.root["keys"]
		
		for sv in keys.subviews:
			keys.remove_subview(sv)
			
		v = self.cached_layouts[self.modifiers]
		keys.add_subview(v)
		v.x = 0
		v.y = 0
		v.width = keys.width
		v.height = keys.height
		
	def update_text(self):
		self.root["textbox"].text = "".join([*self.text[:self.pos], "|", *self.text[self.pos:]])
		
	def key_pressed(self, sender):
		key = sender.key
		
		if key == "ALT":
			self.modifiers ^= type(self).MOD_ALT
			self.update_layout()
		elif key == "ARROW_LEFT":
			if self.pos > 0:
				self.pos -= 1
		elif key == "ARROW_RIGHT":
			if self.pos < len(self.text):
				self.pos += 1
		elif key == "BACKSPACE":
			if self.pos > 0:
				del self.text[self.pos-1]
				self.pos -= 1
		elif key in {"ENTER_BOTTOM", "ENTER_TOP"}:
			self.text.append("\n")
			with self.reading:
				self.reading.notify()
		elif key == "SHIFT":
			self.modifiers ^= type(self).MOD_SHIFT
			self.update_layout()
		elif key == "SPACE":
			self.text.insert(self.pos, " ")
			self.pos += 1
		else:
			self.text.insert(self.pos, key)
			self.pos += 1
			
		self.update_text()
		
	def read(self, size=-1):
		with self.reading:
			self.reading.wait()
			ret = "".join(self.text)
			
		self.text.clear()
		self.pos = 0
		self.update_text()
		
		print(ret, end="")
		return ret
		
def main():
	kb = Keyboard()
	
	if appex.is_widget():
		appex.set_widget_view(kb.root)
	else:
		kb.root.present("sheet")
		
	def read(self, size=-1):
		return kb.read(size)
		
	def readline(self):
		return kb.read()
		
	sys.stdin.__class__.read = read
	sys.stdin.__class__.readline = readline
	
	code.interact()
	
if __name__ == "__main__":
	main()

