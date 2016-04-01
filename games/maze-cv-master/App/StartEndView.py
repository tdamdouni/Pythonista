'''View for marking the start and end of a maze'''
import ui
from PIL import Image

class target(ui.View):
	pass
	
class dragDrop(ui.View):
	def snap(self):
		'''snap to nearest target in same dragContainer'''
		targets = self.superview.targets
		#find closest target
		centers = [t.center for t in targets]
		distances = [ abs(c[0]-self.center[0])+abs(c[1]-self.center[1]) for c in centers]
		
		self.center = centers[distances.index(min(distances))]
	def touch_moved(self, touch):
		cx, cy = touch.location
		ox, oy = touch.prev_location
		tx, ty = ox-cx, oy-cy
		self.x -= tx
		self.y -= ty
	def touch_ended(self,touch):
		self.snap()
		
class dragContainer(ui.View):
	def __init__(self, dragDrops, targets):
		for t in targets:
			self.add_subview(t)
		for d in dragDrops:
			self.add_subview(d)
		self.dragDrops = dragDrops
		self.targets = targets


class StartEndView(ui.View):
	def __init__(self, image, finished_handler):
		self.img = image.convert('RGB')
		self.load = self.img.load()
		self.finished_handler = finished_handler
		self.container = None
		
	def make(self):
		buttonsize = int(self.height/16)
		self.startx=int((self.width/2-self.height/2))
		
		self.start=dragDrop(frame=(self.startx-buttonsize,0,buttonsize,buttonsize),background_color=(0,1,0))
		self.end=dragDrop(frame=(self.startx-buttonsize,buttonsize,buttonsize,buttonsize), background_color=(1,0,0))
		
		drags = self.start, self.end 
		
		targets = []
		for x in range(16):
			for y in range(16):
				frame=(self.startx+x*buttonsize,y*buttonsize,buttonsize,buttonsize)
				if self.load[x,y] == (255,255,255):
					bg=(1,1,1)
				else:
					bg=(0,0,0)
				targets.append(target(frame=frame, background_color=bg))
				
		self.container = dragContainer(drags, targets)
		self.container.background_color=(1,1,1)
		self.container.frame = self.frame
		self.add_subview(self.container)
	
	def draw(self):
		if self.container is None:
			self.make()
	
	def finish(self, *args):
		sframe = self.start.frame
		eframe = self.end.frame
		start = (sframe[0]-self.startx)/sframe[2], sframe[1]/sframe[3]
		end = (eframe[0]-self.startx)/eframe[2], eframe[1]/eframe[3]
		start = tuple(int(c) for c in start)
		end = tuple(int(c) for c in end)
		self.finished_handler(start, end)
		
if __name__ == '__main__':
	import photos
	s = StartEndView(photos.pick_image())
	s.present(hide_title_bar=1)