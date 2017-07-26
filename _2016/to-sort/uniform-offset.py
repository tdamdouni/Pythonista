# coding: utf-8

# https://forum.omz-software.com/topic/3422/what-the-heck-is-the-u_offset-uniform-in-shaders/2

import scene, ui

shader_text = '''
precision highp float;
varying vec2 v_tex_coord;
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
uniform vec2 u_offset;
uniform float u_scale;

void main(void) {
    vec4 color = vec4(0.0, 0.0, 0.0, 1.0);
    vec2 center = vec2(.5, .5);
    // set center based on touch position
    center -= ( u_offset/u_sprite_size);
    // set center based on time
    center -= 0.2*vec2(sin(u_time), cos(u_time));
    vec4 pixel_color = texture2D(u_texture, v_tex_coord);
    float radius = length(v_tex_coord - center);
    if (radius < .2) {
        color = pixel_color;
    };
    //Covert to gray image
    color = vec4(vec3(color.r+color.g+color.b/3.0), 1.0);
    gl_FragColor = color;
}
'''

class MyScene (scene.Scene):
	def setup(self):
		tile_texture = scene.Texture(ui.Image.named('Snake'))
		self.sprite = scene.SpriteNode(
		tile_texture,
		size=(500, 500),
		parent=self)
		self.sprite.shader = scene.Shader(shader_text)
		self.sprite.position = self.size/2
		self.state = 0.0
		
	def touch_began(self, touch):
		self.set_touch_position(touch)
		
	def touch_moved(self, touch):
		self.set_touch_position(touch)
		
	def set_touch_position(self, touch):
		dx, dy = self.sprite.position - touch.location
		self.sprite.shader.set_uniform('u_offset', (dx, dy))
		
		
scene.run(MyScene(), show_fps=True)

