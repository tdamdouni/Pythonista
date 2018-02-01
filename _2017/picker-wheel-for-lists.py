# coding: utf-8

# https://forum.omz-software.com/topic/4592/picker-wheel-for-lists-not-just-dates/2

from objc_util import ObjCInstance, c, ObjCClass, ns, create_objc_class, NSObject
from ctypes import c_void_p
import ui


# Data for both pickers
_data = [
    [str(x) for x in range(2000, 2040)],
    ['xxxx', 'yyyy', 'zzzz']
]

# ObjC classes
UIColor = ObjCClass('UIColor')
UIPickerView = ObjCClass('UIPickerView')
UIFont = ObjCClass('UIFont')
NSAttributedString = ObjCClass('NSAttributedString')


# Default attributes, no need to recreate them again and again
def _str_symbol(name):
	return ObjCInstance(c_void_p.in_dll(c, name))
	
	
_default_attributes = {
    _str_symbol('NSFontAttributeName'): UIFont.fontWithName_size_(ns('Courier'), 16),
    _str_symbol('NSForegroundColorAttributeName'): UIColor.redColor(),
    _str_symbol('NSBackgroundColorAttributeName'): UIColor.greenColor()
}


# Data source & delegate methods
def pickerView_attributedTitleForRow_forComponent_(self, cmd, picker_view, row, component):
	tag = ObjCInstance(picker_view).tag()
	return NSAttributedString.alloc().initWithString_attributes_(ns(_data[tag - 1][row]), ns(_default_attributes)).ptr
	
	
def pickerView_titleForRow_forComponent_(self, cmd, picker_view, row, component):
	tag = ObjCInstance(picker_view).tag()
	return ns(_data[tag - 1][row]).ptr
	
	
def pickerView_numberOfRowsInComponent_(self, cmd, picker_view, component):
	tag = ObjCInstance(picker_view).tag()
	return len(_data[tag - 1])
	
	
def numberOfComponentsInPickerView_(self, cmd, picker_view):
	return 1
	
	
def rowSize_forComponent_(self, cmd, picker_view, component):
	return 100
	
	
def pickerView_rowHeightForComponent_(self, cmd, picker_view, component):
	return 30
	
	
def pickerView_didSelectRow_inComponent_(self, cmd, picker_view, row, component):
	tag = ObjCInstance(picker_view).tag()
	print(f'Did select {_data[tag - 1][row]}')
	
	
methods = [
    numberOfComponentsInPickerView_, pickerView_numberOfRowsInComponent_,
    rowSize_forComponent_, pickerView_rowHeightForComponent_, pickerView_attributedTitleForRow_forComponent_,
    pickerView_didSelectRow_inComponent_
]

protocols = ['UIPickerViewDataSource', 'UIPickerViewDelegate']


UIPickerViewDataSourceAndDelegate = create_objc_class(
    'UIPickerViewDataSourceAndDelegate', NSObject, methods=methods, protocols=protocols
)


# UIPickerView wrapper which behaves like ui.View (in terms of init, layout, ...)
class UIPickerViewWrapper(ui.View):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._picker_view = UIPickerView.alloc().initWithFrame_(ObjCInstance(self).bounds()).autorelease()
		ObjCInstance(self).addSubview_(self._picker_view)
		
	def layout(self):
		self._picker_view.frame = ObjCInstance(self).bounds()
		
	@property
	def tag(self):
		return self._picker_view.tag()
		
	@tag.setter
	def tag(self, x):
		self._picker_view.setTag_(x)
		
	@property
	def delegate(self):
		return self._picker_view.delegate()
		
	@delegate.setter
	def delegate(self, x):
		self._picker_view.setDelegate_(x)
		
	@property
	def data_source(self):
		return self._picker_view.dataSource()
		
	@data_source.setter
	def data_source(self, x):
		self._picker_view.setDataSource_(x)
		
		
class MyView(ui.View):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.background_color = 'white'
		
		self.delegate_and_datasource = UIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
		
		pv1 = UIPickerViewWrapper(frame=[100, 100, 200, 100])
		pv1.delegate = self.delegate_and_datasource
		pv1.data_source = self.delegate_and_datasource
		pv1.tag = 1
		self.add_subview(pv1)
		
		pv2 = UIPickerViewWrapper(frame=[100, 400, 200, 100])
		pv2.delegate = self.delegate_and_datasource
		pv2.data_source = self.delegate_and_datasource
		pv2.tag = 2
		self.add_subview(pv2)
		
		
if __name__ == '__main__':
	v = MyView()
	v.present('full_screen')

