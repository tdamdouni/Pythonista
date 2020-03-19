# coding: utf-8

# https://github.com/humberry/ui-tutorial/blob/master/MiniPhotoView.py

# https://forum.omz-software.com/topic/2695/need-help-with-a-photo-gallery/4

import ui, photos, console

class MyPictureView(ui.View):
	def __init__(self, width, height):
		self.frame = (0,0,width,height)
		self.iwidth = 200.0
		self.iheight = 150.0
		framesize = 5
		iw = self.iwidth - 2 * framesize
		ih = self.iheight - 2 * framesize
		ratio = ih / iw
		self.img = []
		self.imgcount = photos.get_count()
		if self.imgcount < 100:
			console.hud_alert('Please wait while {} photos are loading...'.format(self.imgcount))
		else:
			console.hud_alert('Please wait while 100 photos are loading...')
			self.imgcount = 100
		for i in range(self.imgcount):
			img = ui.Image.from_data(photos.get_image(i,raw_data=True))
			w, h = img.size
			rat = h / w
			x_ratio = 1.0
			y_ratio = 1.0
			x = framesize
			y = framesize
			if rat > ratio:    #portrait
				x = ((iw - ih * rat) / 2) + framesize
				x_ratio = ih * rat / iw
			else:            #landscape
				y = ((ih - iw * rat) / 2) + framesize
				y_ratio = iw * rat / ih
			with ui.ImageContext(self.iwidth, self.iheight) as ctx:
				img.draw(x,y,iw * x_ratio,ih * y_ratio)
				self.img.append(ctx.get_image())
				
	def draw(self):
		i = 0
		if self.imgcount < 100:
			endrow = self.imgcount / 10 + 1
		else:
			endrow = 10
		for row in range(endrow):
			for column in range(10):
				if i == self.imgcount:
					break
				x = column * self.iwidth
				y = row * self.iheight
				self.img[i].draw(x,y,self.iwidth,self.iheight)
				i += 1
				
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

