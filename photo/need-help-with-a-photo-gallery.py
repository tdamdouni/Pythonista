# coding: utf-8

# https://forum.omz-software.com/topic/2695/need-help-with-a-photo-gallery/4

import ui, photos

class MyPictureView(ui.View):
	def __init__(self, width, height):
		self.frame = (0,0,width,height)
		self.iwidth = 300
		self.iheight = 200
		framesize = 10
		self.img = ui.Image.from_data(photos.pick_image(raw_data=True))
		#w, h = self.img.size
		#print 'img size: ' + str(w) + ' x ' + str(h)
		with ui.ImageContext(self.iwidth, self.iheight) as ctx:
			self.img.draw(framesize,framesize,self.iwidth-2*framesize,self.iheight-2*framesize)
			self.img = ctx.get_image()
			
	def draw(self):
		x = 0
		y = 0
		self.img.draw(x,y,self.iwidth,self.iheight)
		
		x = self.iwidth
		self.img.draw(x,y,self.iwidth,self.iheight)
		
		x = 2 * self.iwidth
		self.img.draw(x,y,self.iwidth,self.iheight)
		
		x = 0
		y = self.iheight
		self.img.draw(x,y,self.iwidth,self.iheight)
		
		y = 2 * self.iheight
		self.img.draw(x,y,self.iwidth,self.iheight)
		
		y = 3 * self.iheight
		self.img.draw(x,y,self.iwidth,self.iheight)
		
	def layout(self):
		pass
		
	def touch_began(self, touch):
		pass
		
class MiniPhotoView(ui.View):
	def __init__(self):
		self.view = ui.View(background_color='lightyellow')
		self.view.name = 'MiniPhotoView'
		scrollview1 = ui.ScrollView()
		scrollview1.name = 'scrollview1'
		scrollview1.flex = 'WH'
		scrollview1.content_size = (2000,2000)
		self.view.add_subview(scrollview1)
		self.view.present('full_screen')
		self.sv1 = self.view['scrollview1']
		width, height = self.sv1.content_size
		self.sv1.add_subview(MyPictureView(width,height))
		
if photos.get_count():
	MiniPhotoView()
else:
	print('Sorry no access or no pictures.')

