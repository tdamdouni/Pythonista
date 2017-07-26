# coding: utf-8

# https://github.com/balachandrana/animating_gif_in_pythonista_scene/blob/master/record_pythonista__scene_as_gif.py

# https://forum.omz-software.com/topic/3275/recording-scene-programs-as-an-animated-gif-image

# https://forum.omz-software.com/topic/3809/display-gif

import scene
import ui
from PIL import Image as PILImage
from images2gif import writeGif
import io

state = 'stop_recording'
maximum_number_of_frames = 30
gif_duration = 1.0/60

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
    //color = vec4(vec3(color.r+color.g+color.b/3.0), 1.0);
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
        self.record_start = scene.LabelNode('Start_Recording', position=scene.Point(350,50), parent=self)
        self.record_stop = scene.LabelNode('Stop_Recording', position=scene.Point(650,50), parent=self)

    def update(self):
        if state != 'stop_recording':
            update_image_buffer()

    def touch_began(self, touch):
        global state
        if touch.location in self.record_start.frame:
            print('start recording')
            state = 'start_recording'
        elif touch.location in self.record_stop.frame:
            print('stop recording. beginning to write gif file')
            if state == 'start_recording':
                state = 'write_to_giffile'
            else:
                state = 'stop_recording'
        elif touch.location in self.sprite.frame:
            self.set_touch_position(touch)

    def touch_moved(self, touch):
        if touch.location in self.sprite.frame:
            self.set_touch_position(touch)

    def set_touch_position(self, touch):
        #pass
        dx, dy = self.sprite.position - touch.location
        self.sprite.shader.set_uniform('u_offset', (dx, dy))


sz = ui.get_screen_size()
fr=(0, 0, sz.w, sz.h)
v = ui.View(frame=fr)
frame = v.frame
scene_view = scene.SceneView()
scene_view.name = 'scene1'
scene_view.flex= 'WH'
scene_view.width = frame.w
scene_view.height = frame.h
#scene_view.frame_interval = 10
scene_view.shows_fps = True
scene_view.scene = MyScene()
v.add_subview(scene_view)

image_buffer = []
def update_image_buffer():
    global state, image_buffer
    if state == 'start_recording':
        if len(image_buffer) < maximum_number_of_frames:
            with ui.ImageContext(frame.w, frame.h, 1) as c:
                v['scene1'].draw_snapshot()
                im = c.get_image()
            image_buffer.append(PILImage.open(io.BytesIO(im.to_png())))
        else:
            state = 'write_to_giffile'
    elif state == 'write_to_giffile':
        print('stop recording. beginning to write gif file')
        state = 'stop_recording'
        write_to_giffile('recorded_scene.gif')

@ui.in_background
def write_to_giffile(giffile):
    global image_buffer
    writeGif(giffile,  image_buffer, gif_duration)
    print('writing gif over')

v.present('fullscreen') #, hide_title_bar=True)
