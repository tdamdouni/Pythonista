# coding: utf-8

from __future__ import print_function
import ui, os, sys

class MyImageView(ui.View):
    def __init__(self):
        self.root = os.path.expanduser('~')
        self.rootlen = len(self.root)
        self.path = os.getcwd()
        self.root = self.path[self.rootlen:]
        self.color = 'white'
        self.x_off = 0
        self.y_off = 0
        self.scr_height = None 
        self.scr_width = None 
        self.scr_cor = 2.0
        self.ratio = 1.0
        self.files = []
        self.index = 0
        for entry in sorted(os.listdir(self.path)):
            if os.path.isfile(self.path + '/' + entry):
                if entry.find('.jpg') >= 0:
                    self.files.append(entry)
        self.nr_files = len(self.files)
        print('files = ' + str(self.nr_files))
        if self.nr_files > 0:
            self.img = ui.Image.named(self.files[self.index])
            self.img_width, self.img_height = self.img.size
            self.name = self.root + '/' + self.files[self.index]
        else:
            print('Sorry, no images in this directory.')
            sys.exit()

    def draw(self):
        self.scr_height = self.height
        self.scr_width = self.width
        path = ui.Path.rect(0, 0, self.scr_width, self.scr_height)
        ui.set_color(self.color)
        path.fill()
        self.x_off = (self.scr_width - (self.img_width*self.ratio/self.scr_cor)) / 2
        self.y_off = (self.scr_height - (self.img_height*self.ratio/self.scr_cor)) / 2
        self.img.draw(self.x_off,self.y_off,self.img_width*self.ratio/self.scr_cor,self.img_height*self.ratio/self.scr_cor)

    def touch_began(self, touch):
        if (self.index + 1) < self.nr_files:
            self.index += 1
        else:
            self.index = 0
        self.img = ui.Image.named(self.files[self.index])
        self.img_width, self.img_height = self.img.size
        self.name = self.root + '/' + self.files[self.index]
        self.layout()
        self.set_needs_display()

    def layout(self):
        scr_height_real = self.height * self.scr_cor
        scr_width_real = self.width * self.scr_cor
        y_ratio = scr_height_real / self.img_height
        x_ratio = scr_width_real / self.img_width
        # 1.0 = okay, <1.0 = Image to small, >1.0 = Image to big
        if x_ratio == 1.0 and y_ratio == 1.0:
            self.ratio = 1.0 #perfect size
        elif x_ratio == 1.0 and y_ratio > 1.0:
            self.ratio = 1.0 #perfect width
        elif x_ratio > 1.0 and y_ratio == 1.0:
            self.ratio = 1.0 #perfect height
        elif x_ratio > 1.0 and y_ratio > 1.0:
            self.ratio = 1.0 #show image in original size
        elif x_ratio >= 1.0 and y_ratio < 1.0:
            self.ratio = y_ratio #shrink height
        elif x_ratio < 1.0 and y_ratio >= 1.0:
            self.ratio = x_ratio #shrink width
        elif x_ratio < 1.0 and y_ratio < 1.0:
            if x_ratio < y_ratio: #which side?
                self.ratio = x_ratio
            else:
                self.ratio = y_ratio
        else:
            print('This should never happen. :(')

view = MyImageView()
view.present('fullscreen')
