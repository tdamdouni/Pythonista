# -*- coding: utf-8 -*-
from  __future__ import print_function
import collections
import photos
import scene
import sys
import Image
import ImageFont
import ImageDraw
import clipboard

fonttypes = ('Helvetica', 'Helvetica Bold', 'Arial', 'Avenir Book',
             'Times New Roman', 'Baskerville', 'Courier',
             'Chalkduster', 'American Typewriter', 'Verdana')

colors_dict = collections.OrderedDict([
              ('black', (0,0,0)), ('white',   (1,1,1)), ('grey',   (0.7,0.7,0.7)),
              ('red',   (1,0,0)), ('green',   (0,1,0)), ('blue',   (0,0,1)),
              ('cyan',  (0,1,1)), ('magenta', (1,0,1)), ('yellow', (1,1,0))])

def color(color_name):
    return colors_dict[color_name.lower()]

def color_by_number(color_number):
    return colors_dict[colors_dict.keys()[color_number % len(colors_dict)]]

def pic_save(image, width, height, text, font, fontsize, color, x, y, scale):
    background = Image.new('RGBA', (width,height), 'white')
    background.paste(image, (0, 0))
    draw = ImageDraw.Draw(background)
    fontsize *= scale
    y = height - y
    f = ImageFont.truetype(font, int(fontsize))
    textsize = draw.textsize(text, font=f)
    x -= textsize[0]/2
    y -= ((textsize[1]/1.15)/2) # remove offset / add div factor 1.15 (difference between pixel size and font size)
    draw.text((x, y), text, font=f, fill=color)
    clipboard.set_image(background, format='jpeg', jpeg_quality=0.98)
    photos.save_image(clipboard.get_image())

class TextButton(scene.Layer):
    def __init__(self, inScene, inLoc, inText, inFgColor, inBgColor):
        (theImage, theSize) = scene.render_text(inText, font_size=48)
        super(self.__class__, self).__init__(scene.Rect(inLoc[0], inLoc[1], *theSize))
        inScene.add_layer(self)
        self.parent = inScene
        self.text   = inText.strip()
        self.image  = theImage
        self.stroke = inFgColor  # border color
        self.stroke_weight = 2   # border width
        self.background = inBgColor

    def touch_began(self, touch):
        self.parent.button_pressed(self.text)

class PhotoText(scene.Scene):
    def __init__(self):
        self.text = raw_input('Text to insert in the picture [Hello]: ') or 'Hello'
        self.position = None
        self.fontnr = 0       # Helvetica
        self.colornr = 3      # red
        self.fontsize = 48.0  # 48 point
        self.img2 = photos.pick_image()
        self.img = self.img2.convert('RGBA') #fix for current scene.load_pil_image()
        self.picsize = scene.Size(*self.img.size)
        self.btn_height = 0
        if self.img:
            scene.run(self, frame_interval=3)   # save battery with less frame rates -> 3 = 20fps
        else:
            print('Good bye!')

    def increase_font_size(self):
        if 2 <= self.fontsize < 16:
            self.fontsize += 1.0
        elif self.fontsize >= 16:
            self.fontsize += 16.0

    def decrease_font_size(self):
        if 3 < self.fontsize <= 16:
            self.fontsize -= 1.0
        elif self.fontsize > 16:
            self.fontsize -= 16.0

    def next_font(self):
        self.fontnr += 1

    def next_color(self):
        self.colornr += 1

    def save_image(self):
        color = tuple([int(i * 255) for i in self.current_color()])  # covert scene color to PIL color
        pic_save(self.img, self.picsize[0], self.picsize[1], self.text, self.current_font(), self.fontsize, color, self.position[0]*self.picscale, self.position[1]*self.picscale, self.picscale)   # no ...position[1]-self.btn_height)
        sys.exit()

    def cancel(self):
        sys.exit(1)

    def setup(self):
        self.button_dict = collections.OrderedDict([
                           ('+',      self.increase_font_size),
                           ('—',      self.decrease_font_size),
                           ('Font',   self.next_font),
                           ('Color',  self.next_color),
                           ('Save',   self.save_image),
                           ('Cancel', self.cancel) ])

        fgColor = scene.Color(*color('black'))
        bgColor = scene.Color(*color('grey'))
        loc = [0, 0]
        for button_text in self.button_dict:
            if button_text == '+':
                button_text = '  +  '  # double spaces around '+'
            else:                      # single space around others
                button_text = ' ' + button_text + ' '
            theButton = TextButton(self, loc, button_text, fgColor, bgColor)
            self.btn_height = max(self.btn_height, theButton.frame.h)
            loc[0] += theButton.frame.w + 4  # 4 pixels between each button

        self.picratio = self.picsize.w / (self.picsize.h * 1.0)
        usable_space = self.bounds.h - self.btn_height
        x = usable_space * self.picratio
        if x <= self.bounds.w:
            y = usable_space
        else:
            x = self.bounds.w
            y = self.bounds.w / self.picratio
        self.position = scene.Size(x/2, y/2)    # no ...y/2+self.btn_height
        self.picscale = self.picsize[0] / (x * 1.0)
        self.layer = scene.Layer(scene.Rect(0, self.btn_height, x, y))
        self.layer.image = scene.load_pil_image(self.img)
        self.add_layer(self.layer)

    def button_pressed(self, button_text):
        #print('button_pressed({})'.format(button_text))
        self.button_dict[button_text]()  # call the associated function

    def current_color(self):
        return color_by_number(self.colornr)

    def current_font(self):
        return fonttypes[self.fontnr % len(fonttypes)]

    def touch_moved(self, touch):
        if ((0 < touch.location[0] < self.bounds.w)
        and (self.btn_height < touch.location[1] < self.bounds.h - 20)):
            self.position = touch.location
            self.position[1] -= self.btn_height

    def touch_ended(self, touch):
        self.touch_moved(touch)

    def draw(self):
        scene.background(*color('black'))
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        scene.tint(*self.current_color())  # draw the user's text
        scene.text(self.text, self.current_font(), self.fontsize,
                   self.position[0], self.position[1]+self.btn_height, 5)   # add ...position[1]+self.btn_height
        scene.fill(*color('white'))   # watch+battery -> white background
        scene.rect(0, self.bounds.h, self.bounds.w, 20)  # watch+battery

if photos.get_count():
    PhotoText()
else:
    print('Sorry no access or no pictures.')
