'''A simple analog clock, drawn with the ui module (without using any images), and animated using an sk.Scene.'''

import sk
import ui
from time import time, localtime
from math import pi, sin, cos, floor

class Clock (sk.Scene):
	def __init__(self):
		screen_w, screen_h = ui.get_screen_size()
		ipad = min(screen_w, screen_h) >= 768
		diameter = floor(min(screen_w, screen_h) * 0.9)
		border = 20.0 if ipad else 12.0
		font_size = 70.0 if ipad else 32.0
		face_img = self.draw_face(diameter, border, font_size)		
		self.face_sprite = sk.SpriteNode(sk.Texture(face_img))
		self.face_sprite.position = self.size[0]/2, self.size[1]/2
		self.add_child(self.face_sprite)
		hand_length = diameter/2 - font_size
		hand_width = 15 if ipad else 12
		second_hand_img = self.draw_hand(hand_width/1.5, hand_length, 'red')
		minute_hand_img = self.draw_hand(hand_width, hand_length, 'black')
		hour_hand_img = self.draw_hand(hand_width, hand_length*0.7, 'black')
		self.second_hand_sprite = sk.SpriteNode(sk.Texture(second_hand_img))
		self.second_hand_sprite.anchor_point = (0.5, 0.0)
		self.minute_hand_sprite = sk.SpriteNode(sk.Texture(minute_hand_img))
		self.minute_hand_sprite.anchor_point = (0.5, 0.0)
		self.hour_hand_sprite = sk.SpriteNode(sk.Texture(hour_hand_img))
		self.hour_hand_sprite.anchor_point = (0.5, 0.0)
		self.face_sprite.add_child(self.hour_hand_sprite)
		self.face_sprite.add_child(self.minute_hand_sprite)
		self.face_sprite.add_child(self.second_hand_sprite)
		self.center_sprite = sk.SpriteNode(sk.Texture(self.draw_center(hand_width*1.5, 'black')))
		self.face_sprite.add_child(self.center_sprite)
	
	def draw_face(self, diameter, border, font_size):
		with ui.ImageContext(diameter, diameter) as ctx:
			ui.set_color('white')
			circle = ui.Path.oval(border/2, border/2, diameter-border, diameter-border)
			circle.line_width = border-1
			circle.fill()
			ui.set_color('silver')
			with ui.GState():
				ui.set_shadow((0, 0, 0, 0.35), 0, 1, 5.0)
				circle.stroke()
			angle = (-pi/2) + (pi*2)/12.0
			for i in xrange(1, 13):
				number = str(i)
				x = diameter/2 + cos(angle) * (diameter/2 - font_size*1.2)
				y = diameter/2 + sin(angle) * (diameter/2 - font_size*1.2)
				font = ('HelveticaNeue-UltraLight', font_size)
				w, h = ui.measure_string(number, font=font)
				rect = (x-50, y-h/2, 100, h)
				ui.draw_string(number, rect=rect, font=font, alignment=ui.ALIGN_CENTER)
				angle += (pi*2.0)/12.0			
			return ctx.get_image()
	
	def draw_hand(self, width, length, color):
		with ui.ImageContext(width, length) as ctx:
			# Leave a few pixels transparent 
			round_rect = ui.Path.rounded_rect(2, 2, width-4, length-2, (width-4)*0.5)
			ui.set_color(color)
			round_rect.fill()
			return ctx.get_image()
	
	def draw_center(self, diameter, color):
		with ui.ImageContext(diameter, diameter) as ctx:
			ui.set_color(color)
			ui.Path.oval(0, 0, diameter, diameter).fill()
			return ctx.get_image()
	
	def did_change_size(self, old_size):
		self.face_sprite.position = self.size[0]/2, self.size[1]/2
	
	def update(self):
		t = localtime()
		second = t.tm_sec + time() % 1.0 
		minute = t.tm_min + (second/60.0)
		hour = t.tm_hour % 12 + (minute/60.0)
		self.second_hand_sprite.z_rotation = (second/60.0) * (-pi * 2)
		self.minute_hand_sprite.z_rotation = (minute/60.0) * (-pi * 2)
		self.hour_hand_sprite.z_rotation = (hour/12.0) * (-pi * 2)
	
def main():
	clock = Clock()
	scene_view = sk.View()
	scene_view.frame_interval = 2 #30 fps
	scene_view.run_scene(clock)
	scene_view.present()

if __name__ == '__main__':
	main()