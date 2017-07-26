# https://forum.omz-software.com/topic/3715/tableview-cell-and-image-to-stick-the-right-of-a-cell

import ui

class DocsetManagementView (object):
	def __init__(self, docsets):
		self.data = docsets
		
	def tableview_did_select(self, tableview, section, row):
		pass
		
	def tableview_number_of_sections(self, tableview):
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		return len(self.data)
		
	def tableview_cell_for_row(self, tableview, section, row):
		status = self.data[row]['status']
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = self.data[row]['name']
		cell.detail_text_label.text = status
		iv = self.__getDetailImageViewForStatus(status, cell.height)
		iv.flex = 'L'
		cell.content_view.add_subview(iv)
		return cell
		
	def __getDetailImageForStatus(self, status):
		if status == 'online' or status == 'updateAvailable':
			return 'iob:ios7_cloud_download_outline_24'
		else:
			return 'iob:ios7_close_outline_24'
			
	def __getDetailImageViewForStatus(self, status, height):
		img = ui.Image.named(self.__getDetailImageForStatus(status))
		iv = ui.ImageView()
		iv.image = img
		size = img.size
		ratio = size.y / size.x
		iv.height = height * 0.9
		iv.width = iv.height * ratio
		return iv
		
def get_view(docsets):
	w,h = ui.get_screen_size()
	tv = ui.TableView()
	tv.flex = 'WH'
	data = DocsetManagementView(docsets)
	tv.delegate = data
	tv.data_source = data
	return tv
	
if __name__ == '__main__':
	view = get_view([{'name':'test','status':'online'},{'name':'test2','status':'downloaded'}])
	view.present()
# --------------------
# [...]
	def tableview_cell_for_row(self, tableview, section, row):
		status = self.data[row]['status']
		cell = ui.TableViewCell('subtitle')
		cell.text_label.text = self.data[row]['name']
		cell.detail_text_label.text = status
		iv = self.__getDetailImageViewForStatus(status, cell.height)
		iv.flex = 'L'
		# -----
		iv.x = cell.content_view.width - iv.width
		# ^^^^^
		cell.content_view.add_subview(iv)
		return cell
# [...]# --------------------

