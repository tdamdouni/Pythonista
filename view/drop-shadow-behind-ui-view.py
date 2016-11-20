# coding: utf-8

# https://forum.omz-software.com/topic/1942/drop-shadow-behind-ui-view

import ui

with ui.ImageContext(100, 100) as ctx:
	ui.set_shadow('blue', 5, 5, 2)
	with ui.GState():
		ui.concat_ctm(ui.Transform.rotation(0.78))
		ui.draw_string('    Rotated text')
	ui.draw_string('Not rotated')
	ctx.get_image().show()
	
#==============================

class shadowview(ui.View):
	def draw(self):
		path = ui.Path.rect(0, 0, self.width-10,self.height-10)
		ui.set_color((0.9,0.9,0.9,1.0))
		ui.set_shadow("black",0,0,10)
		path.fill()
		
#==============================

class shadowview(ui.View):
	'''A class for a ui.View that has a shadow behind it.
	
	This is accomplished by:
	1. Draw the background
	2. Redraw with a shadow, but set clipping so only the edge of the shadow
	shows. This prevents the part of the shadow that's under the background
	from showing.
	
	'''
	def draw(self):
	
		'1'
		#Setup path of window shape
		path = ui.Path.rect(0, 0, self.width-10, self.height-10)
		
		#Draw background
		ui.set_color((0.95,0.95,0.95,0.5))
		path.fill()
		
		
		'2'
		#Setup mask by creating image
		from PIL import ImageDraw
		i = Image.new('RGBA',(520,290), (255,255,255,0))
		draw = ImageDraw.Draw(i)
		draw.rectangle((self.width-10, 0, self.width, self.height),fill=(0,0,0,255))
		draw.rectangle((0, self.height-10, self.width, self.height),fill=(0,0,0,255))
		
		#Convert to UI, apply the mask, and draw shadow!
		i = pil_to_ui(i)
		i.clip_to_mask()
		ui.set_color((1,1,1,1))
		ui.set_shadow("black",-2,-2,10)
		path.fill()
		
#==============================

# coding: utf-8
from objc_util import *
import ui

UIColor = ObjCClass('UIColor')

view = ui.View(frame=(0,0,500,500))
box  = ui.View(frame=(0,0,100,100))

view.background_color = 'white'
box.background_color = 'red'
box.center = view.center

view.add_subview(box)

box_pntr = ObjCInstance(box)
## Note: this allows for shadows to be drawn
box_pntr.layer().setMasksToBounds_(False)
box_pntr.layer().setCornerRadius_(6)
## Note: CGColor is needed in order for this to work
box_pntr.layer().setBorderColor_(UIColor.cyanColor().CGColor())
box_pntr.layer().setBorderWidth_(3)
box_pntr.layer().setShadowRadius_(10)
box_pntr.layer().setShadowOffset_(CGSize(0,0))
box_pntr.layer().setShadowOpacity_(1.0)

view.present('sheet')

#==============================

# coding: utf-8

import ui
from objc_util import *

def shadow_box(parent):
	# using chopped up code from @blmacbeth
	UIColor = ObjCClass('UIColor')
	
	f = ui.Rect(*parent.bounds).inset(10,10)
	box  = ui.View(frame=f)
	
	box.background_color = 'white'
	
	box_pntr = ObjCInstance(box)
	## Note: this allows for shadows to be drawn
	box_pntr.layer().setMasksToBounds_(False)
	box_pntr.layer().setCornerRadius_(6)
	## Note: CGColor is needed in order for this to work
	box_pntr.layer().setBorderColor_(UIColor.grayColor().CGColor())
	box_pntr.layer().setBorderWidth_(.5)
	box_pntr.layer().setShadowRadius_(10)
	box_pntr.layer().setShadowOffset_(CGSize(0,0))
	box_pntr.layer().setShadowOpacity_(1.0)
	
	return box
	
class AbstractDataSource(object):
	def __init__(self, tbl, items, **kwargs):
		# assign positional args
		tbl.data_source = self
		tbl.data_source.items = items
		
		self.sections = None
		self.can_move = False
		self.can_delete = False
		self.can_edit = False
		self.make_cell_func = None
		
		self.cell_type = ''
		
		self.sec_title = None
		
		for k,v in kwargs.iteritems():
			if hasattr(self, k):
				setattr(self, k, v)
				
	def tableview_number_of_rows(self, tv, sec):
		# Return the number of rows in the section
		return len(tbl.data_source.items)
		
	def tableview_cell_for_row(self, tv, sec, row):
		# Create and return a cell for the given section/row
		if self.make_cell_func:
			return self.make_cell_func(tv, sec, row)
			
		cell = ui.TableViewCell(self.cell_type)
		cell.text_label.text = 'Foo Bar'
		return cell
		
	def tableview_title_for_header(self, tv, sec):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		if self.sec_title:
			return self.sec_title
		elif not self.sections:
			return None
		else:
			return 'Some Section'
			
	def tableview_can_delete(self, tv, sec, row):
		# Return True if the user should be able to delete the given row.
		return True
		
	def tableview_can_move(self, tv, sec, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return True
		
	def tableview_delete(self, tv, sec, row):
		# Called when the user confirms deletion of the given row.
		pass
		
	def tableview_move_row(self, tv, from_sec, from_row, to_sec, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass
		
		
class MyListDataSource(AbstractDataSource):
	def __init__(self, tbl, items, **kwargs):
		AbstractDataSource.__init__(self, tbl,  items , **kwargs)
		# we do this instead of overriding, to get extended functionality..
		self.make_cell_func = self.make_cell
		
	def make_cell(self, tv, sec, row):
		cell = ui.TableViewCell(self.cell_type)
		cell.text_label.text = 'make_cell - row' + str(row)
		return cell
		
if __name__ == '__main__':
	f = (0,0,500, 500)
	v = ui.View(frame = f, bg_color = 'white')
	tbl = ui.TableView()
	box = shadow_box(v)
	v.add_subview(box)
	ds = MyListDataSource(tbl, range(20), sec_title = 'ian 👿')
	box.add_subview(tbl)
	v.present('sheet')
	r = ui.Rect(*tbl.superview.bounds).inset(10,10)
	tbl.frame = r```
#==============================

# coding: utf-8
from objc_util import *
import ui

UIColor = ObjCClass('UIColor')

def Color(red=0, green=0, blue=0, alpha=1):
	return UIColor.colorWithRed_green_blue_alpha_(red, green, blue, alpha)
	
class ShadowView (ui.View):
	def __init__(self, *args, **kwargs):
		super(ShadowView, self).__init__()
		self.pntr = ObjCInstance(self)
		self.pntr.layer().setMasksToBounds_(False) ## Go ahead and do this.
		
	@property
	def corner_radius(self):
		return self.pntr.layer().cornerRadius()
		
	@corner_radius.setter
	def corner_radius(self, val):
		self.pntr.layer().setCornerRadius_(val)
		
	@property
	def border_color(self):
		return self.pntr.layer().borderColor()
		
	@border_color.setter
	def border_color(self, color):
		self.pntr.layer().setBorderColor_(Color(*color).CGColor())
		
	@property
	def border_width(self):
		return self.pntr.layer().borderWidth()
		
	@border_width.setter
	def border_width(self, val):
		self.pntr.layer().setBorderWidth_(val)
		
	@property
	def opacity(self):
		return self.pntr.layer().opacity()
		
	@opacity.setter
	def opacity(self, val):
		self.pntr.layer().setOpacity_(value)
		
	@property
	def hidden(swlf):
		return self.pntr.layer().hidden()
		
	@hidden.setter
	def hidden(self, val):
		self.pntr.layer().setHidden_(val)
		
	@property
	def masks_to_bounds(self):
		return self.pntr.layer().masksToBounds()
		
	@masks_to_bounds.setter
	def masks_to_bounds(self, val):
		self.pntr.layer().setMasksToBounds_(val)
		
	@property
	def mask(self):
		return self.pntr.layer().mask()
		
	@mask.setter
	def mask(self, new_mask):
		self.pntr.layer().setMask_(new_mask)
		
	@property
	def double_sided(self):
		return self.pntr.layer().doubleSided()
		
	@double_sided.setter
	def double_sided(self, val):
		self.pntr.layer().setDoubleSided_(val)
		
	@property
	def shadow_opacity(self):
		return self.pntr.layer().shadowOpacity()
		
	@shadow_opacity.setter
	def shadow_opacity(self, val):
		self.pntr.layer().setShadowOpacity_(val)
		
	@property
	def shadow_radius(self):
		return self.pntr.layer().shadowRadius()
		
	@shadow_radius.setter
	def shadow_radius(self, val):
		self.pntr.layer().setShadowRadius_(val)
		
	@property
	def shadow_offset(self):
		return self.pntr.layer().shadowOffset()
		
	@shadow_offset.setter
	def shadow_offset(self, offset):
		## offset should be a tuple, but I'll take a CGSize
		if isinstance(offset, CGSize):
			self.pntr.layer().setShadowOffset_(offset)
		elif isinstance(offset, tuple):
			self.pntr.layer().setShadowOffset_(CGSize(*offset))
		else:
			raise TypeError("Cannot use type %s. Use CGSize or tuple" % type(offset))
			
	@property
	def shadow_color(self):
		return self.pntr.layer().shadowColor()
		
	@shadow_color.setter
	def shadow_color(self, color):
		if isinstance(color, UIColor.CGColor()):
			self.pntr.layer().setShadowColor_(color)
		elif isinstance(color, tuple) and len(color) == 4:
			self.pntr.layer().setShadowColor_(Color(*color).CGColor())
		else:
			raise ValueError('Cannot use type %s. Use UIColor or tuple' % type(color))
			
		@property
		def shadow_path(self):
			return self.pntr.layer().shadowPath()
			
		@shadow_path.setter
		def shadow_path(self, path):
			self.pntr.layer().setShadowPath_(path)
			
		@property
		def style(self):
			return self.pntr.layer().style()
			
		@style.setter
		def style(self, style):
			self.pntr.layer().setStyle_(style)
			
if __name__ == '__main__':
	view = ui.View(frame=(0,0,500,500))
	box  = ShadowView(frame=(0,0,100,100))
	
	view.background_color = 'white'
	box.background_color = 'red'
	box.center = view.center
	
	view.add_subview(box)
	
	box.masks_to_bounds = False
	box.corner_radius = 6.
	box.border_color = (0,1,0)
	box.border_width = 6
	box.shadow_radius = 10
	box.shadow_offset = (0,0)
	box.shadow_opacity = 1
	
	view.present('sheet')
	
#==============================

super(ShadowView, self).__init__(*args, **kwargs)

