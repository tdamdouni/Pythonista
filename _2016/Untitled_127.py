# https://gist.github.com/jsbain/144fba5549ece5df62550dd456272bf1

# https://forum.omz-software.com/topic/3926/transparent-scene-background-using-objc_utils/6

from objc_util import *
import ui
from scene import *


from scene import *

ripple_shader = '''
precision highp float;
varying vec2 v_tex_coord;
// These uniforms are set automatically:
uniform sampler2D u_texture;
uniform float u_time;
uniform vec2 u_sprite_size;
// This uniform is set in response to touch events:
uniform vec2 u_offset;

void main(void) {
    vec2 p = -1.0 + 2.0 * v_tex_coord + (u_offset / u_sprite_size * 2.0);
    float len = length(p);
    vec2 uv = v_tex_coord + (p/len) * 1.5 * cos(len*50.0 - u_time*10.0) * 0.03;
    gl_FragColor = texture2D(u_texture,uv);
}
'''

class MyScene (Scene):
    def setup(self):
            self.sprite = SpriteNode('test:Pythonista', parent=self)
            self.sprite.shader = Shader(ripple_shader)
            self.sprite.scale=0.25
            self.did_change_size()

    def did_change_size(self):
            # Center the image:
            self.sprite.position = self.size/2

    def touch_began(self, touch):
            self.set_ripple_center(touch)

    def touch_moved(self, touch):
            self.set_ripple_center(touch)

    def set_ripple_center(self, touch):
            # Center the ripple effect on the touch location by setting the `u_offset` shader uniform:
            dx, dy = self.sprite.position - touch.location
            self.sprite.shader.set_uniform('u_offset', (dx, dy))


sv=SceneView()
s=MyScene()
v=ui.View()
w=ui.WebView(frame=(0,0,300,300))
v.add_subview(w)
w.load_url('http://youtube.com')
sv.scene=s
v.bg_color='red'
v.add_subview(sv)
v.present('panel')

S=ObjCInstance(sv)
m=ui.View(frame=(120,120,80,80))
m.bg_color=(1,1,1,1)
S.layer().mask=ObjCInstance(m).layer()
