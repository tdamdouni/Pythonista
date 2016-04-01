'''View for editing the walls and structure of mazes, as well as marking the start and end'''

import ui, io, time
from PIL import Image
from math import pi

def pil_to_ui(img):
	with io.BytesIO() as b:
		img.save(b, "PNG")
		return ui.Image.from_data(b.getvalue())

class MazeEditView(ui.View):
	'''Used for correcting the maze scan'''
	def __init__(self, image, finished_handler):
		self.img = image.convert('L')
		self.finished_handler = finished_handler
		self.load=self.img.load()
		self.buttonView=None
		self.angle = 0
		
	def invert(self,sender):
		'''Invert both the color of a button and the corresponding pixel in self.img'''
		x=int((sender.frame[0])/sender.frame[2])#sender.frame[2] is buttonsize
		y=int(sender.frame[1]/sender.frame[2])
		if sender.background_color==(1,1,1,1):
			sender.background_color=(0,0,0,1)
			self.load[x,y]=0

		elif sender.background_color==(0,0,0,1):
			sender.background_color=(1,1,1,1)
			self.load[x,y]=255

	def rotate(self,sender):
		self.angle += 1
		def anim():
			self.buttonView.transform=ui.Transform().rotation((pi/2*self.angle))
		ui.animate(anim,duration=0.5)
		
	def finish(self, *args):
		#uses *args to account for being activated by either button press or otherwise
		self.img = self.img.rotate(-90*self.angle)
		self.finished_handler(self.img)
		
	def makeButtons(self):
		buttonsize = int(self.height/16)
		self.startx=int((self.width/2-self.height/2))
	
		rot=ui.Button(frame=(self.startx-2*buttonsize-10,10,2*buttonsize,2*buttonsize))
		rot.image=ui.Image.named('ionicons-ios7-refresh-empty-256')
		rot.action=self.rotate
		rot.tint_color=(0,0,0)

		self.add_subview(rot)
		
		self.buttonView = ui.View(frame=(self.startx, 0, buttonsize*16,buttonsize*16))
		for x in range(16):
			for y in range(16):
				frame=(x*buttonsize,y*buttonsize,buttonsize,buttonsize)
				b=ui.Button(frame=frame)
				b.background_color=self.load[x,y]
				b.action=self.invert
				self.buttonView.add_subview(b)
		self.add_subview(self.buttonView)
		
	def draw(self):
		if not self.buttonView:
			self.makeButtons()
			
	def will_close(self):
		if __name__ == '__main__':
			self.finish()
if __name__ == '__main__':
	import photos
	def show(image):
		image.show()
	MazeEditView(image=photos.pick_image(),finished_handler=show).present(hide_title_bar=1)