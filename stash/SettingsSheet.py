# coding: utf-8

# https://forum.omz-software.com/topic/1082/settingssheet

'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Setting 1</key>
    <string>On</string>
    <key>Setting 2</key>
    <string>On</string>
    <key>Setting 3</key>
    <string>On</string>
</dict>
</plist>
'''

import ui, os, Settings

class SettingsSheet (ui.View, Settings.Settings):
	def __init__(self):
		Settings.Settings.__init__(self)
		self.__make_self()
		self.did_load()
		self.__make_l()
		self.__make_lds()
		self.__make_tv()
		self.layout()
		self.present('sheet')
		
	def did_load(self):
		self.settings_file = __file__
		
	def layout(self):
		self.__tv.width = self.width
		self.__tv.row_height = 50
		self.__tv.height = len(self.settings_dict) * self.__tv.row_height
		
	def __make_self(self):
		self.SettingsSheet_version = '4.0'
		self.SettingsSheet_source_code = 'Original by @tony.'
		self.SettingsSheet_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		self.name = 'Settings'
		self.background_color = 'white'
		self.cells = list()
		
	def __make_l(self):
		self.open_settings()
		self.__l = list()
		for sK in self.settings_dict:
			self.__l.append(self.get_setting(sK))
			self.__l.sort()
			
	def __make_lds(self):
		self.__lds = SettingsSheetDataSource(self.__l)
		self.__lds.delete_enabled = False
		
	def __make_tv(self):
		self.__tv = ui.TableView()
		self.__tv.allows_selection = False
		self.__tv.data_source = self.__lds
		self.__tv.delegate = self.__lds
		self.add_subview(self.__tv)
		
	def will_close(self):
		self.close_settings()
		
class SettingsSheetDataSource(ui.ListDataSource):
	def tableview_cell_for_row(self, tableview, section, row):
		self.__make_self()
		self.__make_tvc(row)
		self.__make_sw(row)
		self.tableview.superview.cells.append(self.__tvc)
		return self.__tvc
		
	def __make_self(self):
		self.SettingsSheetDataSource_version = '4.0'
		self.SettingsSheetDataSource_source_code = 'Original by @tony.'
		self.SettingsSheetDataSource_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
		
	def __make_tvc(self, row):
		self.__tvc = ui.TableViewCell()
		self.__tvc.text_label.text = self.items[row]['setting']
		
	def __make_sw(self, row):
		self.__sw = ui.Switch()
		self.__sw.name = self._items[row]['setting']
		self.__sw.value = True if self.items[row]['value'] == 'On' else False
		self.__sw.action = self.__swA
		self.__sw.y = 10
		self.__sw.x = self.tableview.width - 60
		self.__tvc.content_view.add_subview(self.__sw)
		
	def __swA(self, sender):
		self.tableview.superview.set_setting(sender.name, 'On' if sender.value else 'Off')
		
if __name__ == "__main__":
	ss = SettingsSheet()
	if False:
		ss.cells[0].text_label.text = 'Amended after load'
		ss.cells[0].content_view['Setting 1'].value = False
# --------------------

