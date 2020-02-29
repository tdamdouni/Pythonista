# coding: utf-8

# https://gist.github.com/The-Penultimate-Defenestrator/c99849e7ed17e5a2f215

from __future__ import print_function
import ui, os, console

class DropDown(ui.View):
	def __init__(self,p,level,parent=None, frame=None,width=None,x=None, y=None):
		self.path = p
		self.subDirs=[os.path.join(p,o) for o in os.listdir(p) if os.path.isdir(os.path.join(p,o))]
		self.open = False
		self.level=level
		
		self.arrowClosed = ui.Image.named('iob:ios7_arrow_right_32')
		self.arrowOpened = ui.Image.named('iob:ios7_arrow_down_32')
		
		self.folderIcon  = ui.Image.named('iob:ios7_folder_outline_32')
		self.selectIcon  = ui.Image.named('iob:ios7_checkmark_empty_256')
		
		self.children = []
		
		self.ydent = 0
		
		self.above = []
		self.below = []
		
		self.selected = 0
		
	def draw(self):
	
		self.height = 40
		self.y = 40*len(self.superview.subviews[:self.superview.subviews.index(self)])+self.ydent*40
		self.x = 0
		self.width = self.superview.width
		indent=32*self.level
		
		for s in self.subviews:
			self.remove_subview(s)
			
		self.arrow=ui.ImageView(frame=(indent,4,32,32))
		self.arrow.image = self.arrowOpened if self.open else self.arrowClosed
		self.add_subview(self.arrow)
		
		self.folder=ui.ImageView(frame=(indent+32,4,32,32))
		self.folder.image = self.folderIcon
		self.add_subview(self.folder)
		
		self.text=ui.Label(frame=(indent+75,4,300,32))
		self.text.text = str(os.path.abspath(self.path)).split('/')[-1]
		self.text.font=('AvenirNext-Light',20)
		self.add_subview(self.text)
		
		maxscroll = max(x.y+40 for x in self.superview.subviews)
		self.superview.content_size = (0, maxscroll)
		
	def should_open(self):
		self.above = [x for x in self.superview.subviews if x.y < self.y]
		self.below = [x for x in self.superview.subviews if x.y > self.y]
		
		self.arrow.image = self.arrowOpened
		self.open = not self.open
		
		for sd in self.subDirs:
			self.children.append(DropDown(sd, self.level+1))
			self.superview.add_subview(self.children[-1])
			self.children[-1].ydent -= len(self.below)
			
		for b in self.below:
			b.ydent += len(self.children)
			b.draw()
			
	def should_collapse(self):
		self.above = [x for x in self.superview.subviews if x.y < self.y]
		self.below = [x for x in self.superview.subviews if x.y > self.y]
		
		self.arrow.image = self.arrowClosed
		self.open = not self.open
		
		for sd in self.children:
			sd.should_collapse()
			self.superview.remove_subview(sd)
			if sd.selected:
				self.superview.superview.deselect()
				
		for b in set(self.below)-set(self.children):
			b.ydent -= len(self.children)
			try:
				b.draw()
			except AttributeError as e:
				print(b)
				raise e
				
		self.children = []
		
	def select(self):
		self.superview.superview.select(self)
		
	def touch_began(self, touch):
		if not self.selected:
			self.background_color = .88, .88, .88
		self.selectCanditate=False
		x, y = touch.location
		
		a=self.arrow
		arrowBounds = list(a.frame[:2]) + [a.x+a.width,a.y+a.height]
		if x > arrowBounds[0]-20 and x < arrowBounds[2]+20:
			if self.open:
				self.should_collapse()
			else:
				self.should_open()
		else:
			self.selectCanditate=True
		self.initialTouch = touch.location
		
	def touch_ended(self, touch):
		if not self.selected:
			self.background_color = 1.0, 1.0, 1.0
		x, y = touch.location
		px, py = self.initialTouch
		if self.selectCanditate and abs(x-px) < 5 and abs(y-py) < 5:
			self.select()
			
			
class SVDelegate:
	def scrollview_did_scroll(self, sv):
		for sub in sv.subviews:
			if not sub.selected:
				sub.background_color = 1.0, 1.0, 1.0
		yscroll=sv.content_offset[1]
		sv.superview.checkscroll.content_offset=(0,yscroll)
		
class FilePicker(ui.View):
	def __init__(self,path,finished_handler,frame=(0,0,500,500),background_color=(1.0, 1.0, 1.0)):
		self.background_color=background_color
		self.frame=frame
		self.scroll=ui.ScrollView(frame=(0,0,self.width,self.height))
		self.scroll.delegate = SVDelegate()
		self.scroll.add_subview(DropDown(path,0))
		self.add_subview(self.scroll)
		
		self.selectedIndex = None
		self.finished_handler = finished_handler
		
		self.selectIcon  = ui.Image.named('iob:ios7_checkmark_empty_256')
		
		self.checkscroll = ui.ScrollView(frame=(0,0,self.width,self.height))
		self.checkscroll.touch_enabled=0
		self.add_subview(self.checkscroll)
		
		self.check = ui.ImageView(frame=(self.width-32,0,32,32))
		self.check.image=self.selectIcon
		self.check.hidden=1
		self.checkscroll.add_subview(self.check)
		
	def deselect(self):
		self.selectedIndex = None
		for sv in self.scroll.subviews:
			sv.selected=False
		self.check.hidden=1
		
	def select(self, folderView):
		self.selectedIndex = self.scroll.subviews.index(folderView)
		for sv in self.scroll.subviews:
			sv.selected=False
			sv.background_color = self.background_color
		folderView.selected = True
		self.check.hidden=0
		self.check.y=folderView.y+4
		
	def finish(self, sender):
		if self.selectedIndex != None:
			self.finished_handler(self.scroll.subviews[self.selectedIndex].path)
			self.close()
		else:
			console.hud_alert('Please select a directory','error')
			
	def will_close(self):
		if self.selectedIndex != None:
			self.finished_handler(self.scroll.subviews[self.selectedIndex].path)
			self.close()
		else:
			def reopen():
				if self.superview:
					self.superview.present('sheet')
				else:
					self.present('sheet')
					
					
			console.hud_alert('Please select a directory','error')
			
			ui.delay(reopen, 1)
			
def getFileName(dir,title=''):
	global selected
	selected = None
	
	def f_handle(result):
		global selected
		selected = result
	fp=FilePicker(dir,f_handle,frame=(0,0,500,500))
	fp.name = title
	fp.right_button_items=[ui.ButtonItem(title='Done', action=fp.finish)]
	fp.present('sheet')
	fp.wait_modal()
	return selected
	
if __name__ == '__main__':
	print(getFileName('/private/var/mobile/Containers/Shared/AppGroup/6FFE2397-8613-46A4-8F57-569169AA8746/Documents'))

