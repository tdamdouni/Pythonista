# https://forum.omz-software.com/topic/3273/share-code-ui-tableview-as-a-banner-or-something-like-that

import ui, console

'''
        A long winded example of using a ui.TableView as a banner
        rather than use generic loops, kept it open for trial and error

        there are easier ways to do this. but in some cases in can see this
        also a convient way.

        you can also manually scroll the list of course, also could be
        another type of controller for the content part of the view
'''

class MyTable(ui.ListDataSource):
	def __init__(self, items):
		super().__init__(items)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		if row is 0:
			return self.cell0(tableview, section, row)
		elif row is 1:
			return self.cell1(tableview, section, row)
		elif row is 2:
			return self.cell2(tableview, section, row)
		elif row is 3:
			return self.cell3(tableview, section, row)
		elif row is 4:
			return self.cell4(tableview, section, row)
			
			
	def cell0(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.bg_color = 'orange'
		cell.text_label.text = 'TableViewCell()'
		return cell
		
	def cell1(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.bg_color = 'purple'
		cell.text_label.text = 'TableViewCell(subtitle)'
		cell.detail_text_label.text = 'the subtitle line'
		return cell
		
	def cell2(self, tableview, section, row):
		cell = ui.TableViewCell('value1')
		cell.bg_color = 'green'
		cell.text_label.text = 'TableViewCell(value1)'
		cell.detail_text_label.text = 'the subtitle line'
		return cell
		
	def cell3(self, tableview, section, row):
		cell = ui.TableViewCell('value2')
		cell.bg_color = 'deeppink'
		cell.text_label.font = ('Avenir Next Condensed', 22)
		cell.text_label.text = 'TableViewCell(value2)'
		cell.detail_text_label.text = 'the subtitle line'
		return cell
		
	def cell4(self, tableview, section, row):
		# draw 4 lines of text, each in a new ui.Label
		# also a button in the center of the view
		
		# the action for the button in the center of the cell
		def btn_action(sender):
			console.alert('yes, the button was clicked')
			
		cell = ui.TableViewCell()
		cell.bg_color = 'navy'
		cell.height = tableview.row_height
		cell.width = tableview.width
		
		# create the ui.Labels and assign the attrs
		y = 10
		for i in range(1, 5):
			lb = ui.Label()
			lb.font =('Futura', 28)
			lb.text = 'Line ' + str(i)
			lb.text_color = 'white'
			lb.size_to_fit()
			lb.x = 10
			lb.y = y
			y += lb.bounds.max_y + 10
			cell.content_view.add_subview(lb)
			
		btn = ui.Button(frame = (0, 0, 128, 128))
		btn.font = ('Arial Rounded MT Bold', 28)
		btn.corner_radius = btn.width / 2
		btn.title ='Yeah'
		btn.bg_color = 'teal'
		btn.tint_color = 'white'
		btn.center = cell.center
		btn.action = btn_action
		cell.content_view.add_subview(btn)
		
		return cell
		
	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False
		
		
class MyClass(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.header = None
		self.tv = None
		
		self.make_view()
		
	def make_view(self):
		h = ui.View(frame = (0, 0, self.width, self.height * .25))
		h.flex = 'wh'
		self.add_subview(h)
		
		tv = ui.TableView(name = 'tv', frame = h.bounds)
		tv.row_height = h.height
		tv.data_source = MyTable(range(5))
		tv.paging_enabled = True                    # important
		tv.shows_vertical_scroll_indicator = False  # important
		tv.allows_selection = False                 # important
		self.tv = tv
		h.add_subview(tv)
		
if __name__ == '__main__':
	import time
	w = ui.get_screen_size()[0] - 100
	h = ui.get_screen_size()[1] - 100
	f = (0, 0, w, h)
	mc = MyClass(frame = f, bg_color = 'white', name = 'Header??')
	mc.present('sheet')
	
	# just show each row in the table with a delay
	rh = mc.tv.row_height
	for i in range(0, 5):
		# can access the ui.ScrollView from the ui.TableView as its
		# ui.Ta
		mc.tv.content_offset = (0, i * rh)
		time.sleep(1)
		
# --------------------

