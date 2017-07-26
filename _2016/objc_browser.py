import ui
from objc_util import *
from objc_tools import bundles
import dialogs

def get_classes():
	classes = {}
	classes['No Class'] = []
	for i in ObjCClass.get_names():
		if bundles.bundleForClass(i):
			try:
				if classes[bundles.bundleForClass(i).bundleID]:
					classes[bundles.bundleForClass(i).bundleID] += [i]
				else:
					classes[bundles.bundleForClass(i).bundleID] = [i]
			except KeyError:
				classes[bundles.bundleForClass(i).bundleID] = [i]
		else:
			classes['No Class'] += [i]
			
			
	clist = []
	for k, v in classes.items():
		clist += [[k, v]]
	return clist

def get_frameworks():
	flist = []
	frameworks = {}
	frameworks['No Framework'] = {'bundle': None, 'items': []}
	for i in ObjCClass.get_names():
		if bundles.bundleForClass(i):
			try:
				if frameworks[bundles.bundleForClass(i).bundleID]:
					frameworks[bundles.bundleForClass(i).bundleID]['items'] += [i]
				else:
					frameworks[bundles.bundleForClass(i).bundleID] = {'bundle': bundles.bundleForClass(i), 'items': [i]}
			except KeyError:
				frameworks[bundles.bundleForClass(i).bundleID] = {'bundle': bundles.bundleForClass(i), 'items': [i]}
		else:
			frameworks['No Framework']['items'] += [i]
	flist = sorted(frameworks.keys())
	return {'flist': flist, 'frameworks': frameworks}
	
class FrameworkClassesDataSource(object):
	'''Pass the items from get_frameworks
	>>> d = get_frameworks()
	>>> h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])'''
	def __init__(self, fwork_items):
		self.items = fwork_items['items']
		self.name = fwork_items['bundle'].bundleID

	def tableview_did_select(self, tableview, section, row):
		clipboard.set(self.items[row])

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = self.items[row]
		return cell

	def tableview_title_for_header(self, tableview, section):
		return self.name

class FrameworkClassesDelegate (object):
	def tableview_did_select(self, tableview, section, row):
		obj = tableview.data_source.fworks['frameworks'][tableview.data_source.fworks['flist'][row]]
		tableview.superview['selected']['table'].data_source = FrameworkClassesDataSource(obj)
		tableview.superview['selected']['table'].reload()
		
		
class AllFrameworksDataSource(object):
	def __init__(self, fworks):
		self.fworks = fworks

	def tableview_did_select(self, tableview, section, row):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.fworks['flist'])

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		#print('section: ', section, ' row: ', row)
		cell.text_label.text = self.fworks['flist'][row].split('.')[-1]
		cell.accessory_type = 'disclosure_indicator'
		return cell

	def tableview_title_for_header(self, tableview, section):
		return 'Framework'
		
		
if __name__ == '__main__':
	v = ui.load_view()
	v.background_color = 'efeff4'
	s = AllFrameworksDataSource(get_frameworks())
	v['classes'].data_source = s
	v['classes'].reload()
	v['classes'].delegate = FrameworkClassesDelegate()
	#h = FrameworkClassesDataSource(d['frameworks']['com.apple.UIKit'])
	
	#v['selected'].data_source = h
	#v['selected'].reload()
	v.present('panel')

