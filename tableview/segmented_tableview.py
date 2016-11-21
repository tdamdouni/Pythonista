# coding: utf-8

# See: https://forum.omz-software.com/topic/2374/is-there-a-way-to-programmatically-highlight-a-ui-segmentedcontrol

import ui

class SegNav(ui.View):
	def __init__(self):
		self.present()
		self.name = 'SegNav'
		seg = ui.SegmentedControl()
		seg.action = self.seg_view_action
		seg.background_color = 'white'
		seg.flex = 'W'
		seg.height = 40
		seg.segments = 'even', 'odd'
		seg.selected_index = 0  # set the highlight
		seg.width = self.bounds.w
		self.add_subview(seg)
		
		x, y, w, h = self.bounds
		self.table_view = ui.TableView()
		self.table_view.data_source = ui.ListDataSource(xrange(0, 42, 2))
		self.table_view.flex = 'WH'
		self.table_view.frame = x, y + seg.height, w, h - seg.height
		self.add_subview(self.table_view)
		
	def seg_view_action(self, sender):
		# print(sender.segments[sender.selected_index])
		self.table_view.data_source.items = xrange(sender.selected_index, 42, 2)
		
SegNav()

