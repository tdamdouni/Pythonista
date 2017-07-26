# coding: utf-8

# https://github.com/balachandrana/animating_gif_in_pythonista_scene/blob/master/GifSpriteNodeHorse.py

# http://stackoverflow.com/questions/10269099/pil-convert-gif-frames-to-jpg
# https://forum.omz-software.com/topic/3256/support-for-animated-gifs-in-scene-module
# https://forum.omz-software.com/topic/3809/display-gif

import io
import itertools
import os
import requests
import scene
import ui
from PIL import Image as PIL_Image

url = 'http://bestanimations.com/Animals/Mammals/Horses/horse-walking-animated-gif1.gif'
# url = 'http://fc00.deviantart.net/fs71/f/2012/189/a/a/dressage_horse_animation_by_lauwiie1993-d56it04.gif'  # there is a pallet problem with one frame of this one!
filename = url.split('/')[-1]

if not os.path.exists(filename):  # get horse image if it is not found locally
    with open(filename, 'wb') as out_file:
        out_file.write(requests.get(url).content)


def get_texture_and_duration(pil_image):
        duration = 4.0 / 60  # hardcoded!!
        new_im = PIL_Image.new("RGBA", pil_image.size)
        new_im.paste(pil_image)
        with io.BytesIO() as mem_file:
            new_im.save(mem_file, format='PNG')
            return (scene.Texture(ui.Image.from_data(mem_file.getvalue())),
                    duration)


def get_textures(gif_file):
    with PIL_Image.open(gif_file) as pil_image:
        # print(pil_image.info)
        preloaded_textures = []
        try:
            while True:
                preloaded_textures.append(get_texture_and_duration(pil_image))
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            print('{} textures loaded.'.format(len(preloaded_textures)))
            return itertools.cycle(preloaded_textures)


class GifSpriteNode(scene.SpriteNode):
    def __init__(self, gif_file, *args, **kwargs):
        self.preloaded_textures = get_textures(gif_file)
        texture, self.current_duration = next(self.preloaded_textures)
        super(GifSpriteNode, self).__init__(texture, *args, **kwargs)

    def update(self, dt):
        self.current_duration -= dt
        if self.current_duration > 0:
            return
        self.texture, self.current_duration = next(self.preloaded_textures)


if __name__ == '__main__':
    class MyScene (scene.Scene):
        def setup(self):
            self.background_color = 'white'
            self.toggle_state = False
            snake = scene.Texture(ui.Image.named('Snake'))
            self.sprite0 = scene.SpriteNode(snake, position=self.size / 2,
                                            parent=self)
            # self.sprite1 = GifSpriteNode('tunnelswirl.gif',
            #                             position=self.size / 2)
            self.sprite1 = GifSpriteNode(filename, position=self.size / 2)

        def update(self):
            if self.toggle_state:
                self.sprite1.update(self.dt)

        def touch_began(self, touch):
            self.toggle_state = not self.toggle_state
            if self.toggle_state:
                self.sprite0.remove_from_parent()
                self.add_child(self.sprite1)
            else:
                self.sprite1.remove_from_parent()
                self.add_child(self.sprite0)

    scene.run(MyScene(), show_fps=True)
