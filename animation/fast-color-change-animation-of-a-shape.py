# https://forum.omz-software.com/topic/3274/fast-color-change-animation-of-a-shape/2

from scene import *
from ui import Path
import math
import random
from colorsys import hsv_to_rgb

YELLOW = 1/6
BLUE = 2/3
S = 24

class Grid(Scene):
	def setup(self):
		width = int(self.bounds.width) // S
		height = int(self.bounds.height) // S
		self.cells = [Cell(i, j, parent=self) for i in range(width) for j in range(height)]
		
	def touch_moved(self, touch):
		for cell in self.cells:
			cell.touched += S/abs(cell.frame.center() - touch.location)**2
			cell.update()
			
class Cell(ShapeNode):
	def __init__(self, i, j, **vargs):
		self.touched = 0
		super().__init__(Path.rect(0, 0, S, S), 'white', position=(i*S, j*S), **vargs)
		
	def cell_color(self):
		scale = min(1, self.touched)
		hue = scale * YELLOW + (1-scale) * BLUE
		return hsv_to_rgb(hue, 1, 1)
		
	def update(self):
		self.fill_color = self.cell_color()
		
if __name__ == '__main__':
	run(Grid(), show_fps=True)
	
	
# --------------------

import scene, ui

shader_text = '''
precision highp float;
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform float u_scale;
uniform vec2 u_offset;

void main(void) {
    vec2 uv = mod(v_tex_coord, .125);
    vec2 invuv = uv*8.;
    vec2 pq = floor(v_tex_coord*8.0)/8.;
    //vec4 color = texture2D(u_texture, invuv);
    vec2 t = floor(u_offset*8.0/(u_sprite_size))/8.;
    float r = 0.;
    if ((pq.x == t.x) && (pq.y == t.y)) r = 1.0;
    vec4 color = vec4(pq.x, pq.y, r, 1.);
    gl_FragColor = color;
}
'''

class MyScene (scene.Scene):
	def setup(self):
		tile_texture = scene.Texture(ui.Image.named('Snake'))
		self.sprite = scene.SpriteNode(
		tile_texture,
		size=(600, 600),
		anchor_point=(0,0),
		parent=self)
		self.sprite.shader = scene.Shader(shader_text)
		self.sprite.position = (100, 100)
		
	def touch_began(self, touch):
		self.set_touch_position(touch)
		print (self.sprite.shader.get_uniform('u_offset'))
		
	def set_touch_position(self, touch):
		dx, dy = touch.location -self.sprite.position
		self.sprite.shader.set_uniform('u_offset', (dx, dy))
		
scene.run(MyScene(), show_fps=True)



# --------------------

