# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/2

import ui

class TestView(ui.View):
	def __init__(self, *args, **kwargs):
		pass
	def draw(self):
		print('in draw')
		
	def layout(self):
		print('in layout')
		
# --------------------

class TestView(ui.View):
	def __init__(self, *args, **kwargs):
		#self.__dict__.update(ui.TableViewCell().__class__.__dict__)
		pass
		
	@property
	def content_view(self):
		return ui.View()
		
	@property
	def image_view(self):
		return ui.ImageView()
		
	@property
	def text_label(self):
		return ui.Label()
		
	@property
	def accessory_type(self):
		pass
		
	@accessory_type.setter
	def accessory_type(self):
		pass
		
	def selectable(self):
		pass
		
	def selected_background_view(self):
		pass
		
	def selected_background_view(self):
		pass
		
	def draw(self):
		print('in draw')
		
	def layout(self):
		print('in layout')
		
# --------------------

# https://forum.omz-software.com/topic/3297/ui-tableviewcell-returning-a-custom-class-instead/11

import ui

class CustomUIRect(object):
	# my_color = None
	def as_rect(self, x=0, y=0, w=0, h=0):
		r = ui.Rect(x, y, w, h)
		return r
		
	def __init__(self, color):
		print('in init')
		self.my_color = color
		
if __name__ == '__main__':
	r = CustomUIRect('blue').as_rect()
	print(dir(r))
	print(r.my_color)
class TestView(ui.View):
	def __init__(self, *args, **kwargs):
		pass
	def draw(self):
		print('in draw')
		
	def layout(self):
		print('in layout')
# --------------------
import ui

class CustomUIRect(object):
	# my_color = None
	def as_rect(self, x=0, y=0, w=0, h=0):
		r = ui.Rect(x, y, w, h)
		return r
		
	def __init__(self, color):
		print('in init')
		self.my_color = color
		
if __name__ == '__main__':
	r = CustomUIRect('blue').as_rect()
	print(dir(r))
	print(r.my_color)
# --------------------
import ui
from objc_util import *

class MyTableViewDataSource (object):
	def __init__(self, data):
		self.data = data
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		wv = ui.WebView(frame=cell.content_view.bounds, flex='WH')
		wv.touch_enabled = False #necessary for tableview scrolling to work, unfortunate side effect is that you can't do any touch of content in the webview. Tried disabling scolling with objc but the result wasn't good either.
		wv.scales_page_to_fit = False
		wv.load_html(html)
		#webview needs to have an opaque background for selection colors to work... do in objc
		wv_obj = ObjCInstance(wv)
		wv_obj.webView().setBackgroundColor_(ObjCClass('UIColor').clearColor())
		wv_obj.webView().setOpaque_(False)
		cell.content_view.add_subview(wv)
		return cell
		
	def tableview_can_delete(self, tableview, section, row):
		return False
		
	def tableview_can_move(self, tableview, section, row):
		return False
		
	def tableview_did_select(self, tableview, section, row):
		t.name = self.data[row]['name']
		
if __name__ == '__main__':
	from faker import Faker
	fake = Faker()
	style = '<style>p {font: arial 10pt; color:#888888; margin:0px} a {color:#888888; text-decoration:none} h4 {margin:0px; background-color:#dd7575; color:white; border-radius:5px; padding: 0 5}</style>'
	contact_list = []
	for x in range(200):
		name, email, phone, address = fake.name(), fake.email(), fake.phone_number(), fake.address()
		html = style + '<h4 style="margin:0px">{}</h4><p>{}</p><p>{}</p><p>{}</p>'.format(name, email, phone, address)
		contact_list.append({'html':html, 'name':name})
	t=ui.TableView()
	t.frame=(0,0,400,480)
	t.data_source=MyTableViewDataSource(contact_list)
	t.delegate = t.data_source
	t.row_height = 100
	t.present('sheet')
# --------------------
from fake_format import fake_fmt
html = fake_fmt('<h4 style="margin:0px">{name}</h4><p>{email}</p>'
                '<p>{phone_number}</p><p>{address}</p>')
# --------------------

