# https://forum.omz-software.com/topic/3443/share-playing-with-tableview/5

import ui, console, random, objc_util

myData1 = [ui.View, ui.Button, ui.ButtonItem, ui.ImageView, ui.Label, ui.NavigationView, ui.ScrollView, ui.SegmentedControl,
           ui.Slider, ui.Switch, ui.TableView, ui.TextField, ui.TextView,ui.WebView, ui.DatePicker, ui.ActivityIndicator,
           ui.TableViewCell, ui.ListDataSource, console, objc_util]

class MyTableDataSource(ui.ListDataSource):
	def __init__(self, data):
		super().__init__(data)
		self.data = data
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		return self.cell(row)
		
	def cell(self, row):
		selected_cell = ui.View()
		selected_cell.bg_color = "magenta"
		for x in self.data:
			cell = ui.TableViewCell()
			cell.bg_color = CELL_COLOR
			cell.selected_background_view = selected_cell
			cell.text_label.text = str(self.data[row])
			return cell
			
	def tableview_can_delete(self, tableview, section, row):
		#with paging_enabled, deleting (and/or selecting and viewing) the last row becomes a problem.
		#Hack_fix: only allow deleting while editing is enabled (and while editing is enabled, paging is disabled)
		#allowing selection/deletion/viewing of the last row(s)
		if not tableview.editing:
			return False
		return True
		
	def tableview_delete(self,tableview, section,row):
		self.data.remove(self.data[row])
		tableview.reload()
		return
		
	def tableview_can_move(self,tableview, section,row):
		return True
		
	def tableview_move_row(self,tableview, from_section, from_row, to_section, to_row):
		x = self.data[from_row]
		self.data.remove(self.data[from_row])
		self.data.insert(to_row, x)
		tableview.reload()
		
class MyTableViewDelegate (object):
	def tableview_did_select(self, tableview, row):
		if tv.name == 'attr_tv':
			def attrs(row):
				a = myData1[row]
				return((a,dir(a),len(dir(a))))
			a,d,l = attrs(row)
			s = str(a)
			s += '\n\n'.join(x for x in d) + '\n\n'
			s += '(' +''.join(str(l)) + ' attrs)'
			av.text = s
			
	def tableview_did_deselect(self, tableview, row):
		pass
		
	def tableview_title_for_delete_button(self, tableview, row):
		return 'Remove from List'
		
class MyView(ui.View):
	def __init__(self, ** kwargs):
		super().__init__(**kwargs)
		self.h = ui.View(frame = (0, 0, self.width, self.height))
		self.h.flex = 'lrwh'
		self.h.x,self.h.y = 0,0
		self.add_subview(self.h)
		
class ButtonHandler(object):
	def edit_button_tapped(self, sender):
		def Animation():
		#tv.alpha = .8 if tv.alpha == 1.0 else 1.0
			tv.paging_enabled = False if tv.paging_enabled == True else True
			rb.tint_color = LBC2 if rb.tint_color == LBC else LBC
			rb.title = 'Done' if rb.title == 'Edit' else 'Edit'
			#eb.alpha = .9 if eb.alpha == 1.0 else 1.0
			#eb.bg_color = '#90ee90' if eb.bg_color == GRAY else GRAY
			#eb.tint_color = LBC2 if eb.tint_color == LBC else LBC
			#eb.title = 'Done' if eb.title == 'Edit' else 'Edit'
			tv.editing = not tv.editing
		tvAnim = ui.animate(Animation, duration=0.5)
		
	def add_button_tapped(self, sender):
		@ui.in_background
		def add_item():
			input = console.input_alert('Add Item','Enter text for Item','My New Item','Submit')
			myData1.append(input)
			tv.reload()
		def Animation():
			lb.title = 'Add Item'
		tvAnim = ui.animate(Animation, duration=0.5)
		add_item()
		
CELL_COLOR = (.47, 1.0, .51, 1.)
WHITE = (1.0, 1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0, 1.0)
GRAY = (0.7, 0.7, 0.7, 1.0)
LBC = (1.0, .52, .0, 1.0)
LBC2 = (.39, 1.0, .27, 1.0)

handler = ButtonHandler()
w = ui.get_screen_size()[0]
h = ui.get_screen_size()[1]
f = (0, 0, w, h)

mv = MyView(frame=f, bg_color=WHITE, name='Attr Table')

#eb = ui.Button()
#eb.title = "Edit"
#eb.tint_color = LBC
#eb.flex='blr'
#eb.enabled = True
#eb.frame = (180, 300, 52, 32)
#eb.border_width = 1
#eb.border_color = (.0, .0, .0, 1.0)
#eb.corner_radius = 5
#eb.bg_color = GRAY
#eb.action = handler.button_tapped
#mv.h.add_subview(eb)


rb = ui.ButtonItem()
rb.tint_color = LBC
rb.title = "Edit"
rb.enabled = True
rb.action = handler.edit_button_tapped

lb = ui.ButtonItem()
lb.tint_color = LBC
lb.title = 'Add Item'
lb.enabled = True
lb.action = handler.add_button_tapped

tv = ui.TableView()
tv.name = 'attr_tv'
tv.data_source = MyTableDataSource(myData1)

#tv.content_size = ( , )
#tv.autoresizing =
#tv.center = (a,b,c,d
#tv.content_inset = (a,b,c,d)
#tv.content_mode =
#tv.content_offset = (a,b)
#tv.content_size = (a,b)
#tv.decelerating =  #not writable
#tv.directional_lock_enabled =
#tv.indicator_style =

tv.flex="lrwb"
tv.frame=(0,0,mv.h.bounds[2],mv.h.bounds[3]*.4)
tv.row_height = tv.frame[3]/6
tv.corner_radius = 5
tv.border_width = 1
tv.border_color = 'magenta'
tv.bg_color = (.98, 1.0, .43,1.0)
tv.bounces = True

tv.paging_enabled = True
tv.shows_vertical_scroll_indicator = False
tv.reload_disabled = False
tv.editing = False
tv.allows_selection = True
tv.allows_selection_during_editing = True
tv.allows_multiple_selection = False
tv.allows_multiple_selection_during_editing = False
tv.delegate = MyTableViewDelegate

sv = ui.ScrollView()
sv.name = 'scrollview'
sv.flex = 'lrwhb'
sv.frame = (0,300,w,h)
sv.corner_radius = 5
sv.border_width = 1
sv.border_color = 'purple'
sv.bg_color = '#ff44a6'
sv.shows_horizontal_scroll_indicator = False
sv.shows_vertical_scroll_indicator = False
mv.add_subview(sv)

av = ui.TextView()
av.name = 'textview'
av.flex = 'lrwtbh'
av.frame = (0,0,w,440)
av.corner_radius = 5
av.border_width = 1
av.border_color = '#ff0000'
av.bg_color = '#b3fff5'
av.shows_horizontal_scroll_indicator = False
av.shows_vertical_scroll_indicator = True
av.text = 'Select an Attr'
av.font = 'Arial Rounded MT Bold', 20
sv.add_subview(av)

mv.left_button_items = [lb]
mv.right_button_items= [rb]

mv.h.add_subview(tv)
mv.present('fullscreen')
# --------------------

