# coding: utf-8

# https://gist.github.com/anonymous/8fe3a37d3d588a0c265ea23ae336d60a

from objc_util import *
import ui
import console

global wv

#========== methods and delegate protocols of new class:begin	
UIColor=ObjCClass('UIColor')
UIPickerView = ObjCClass('UIPickerView')
UIFont=ObjCClass('UIFont')

def pickerView_attributedTitleForRow_forComponent_(self,cmd,pickerview,row,component):
	UIfont = UIFont.fontWithName_size_(ns('Courier'),16)
	UIback = UIColor.color(red=0.3, green=0.3, blue=0.3, alpha=1.0)
	UIfore = UIColor.color(red=0.0, green=0.8, blue=0.8, alpha=1.0)

	NSMutableAttributedString = ObjCClass('NSMutableAttributedString')

	txt = wv.PickerView_data[ObjCInstance(pickerview).tag()][row]
		
	attributed_string = NSMutableAttributedString.alloc().initWithString_(ns(txt))
	range = NSRange(0, len(txt))
	attributed_string.addAttribute_value_range_(ObjCInstance(c_void_p.in_dll(c, 'NSFontAttributeName')),UIfont,range)
	attributed_string.addAttribute_value_range_(ObjCInstance(c_void_p.in_dll(c, 'NSForegroundColorAttributeName')),UIfore,range)
	attributed_string.addAttribute_value_range_(ObjCInstance(c_void_p.in_dll(c, 'NSBackgroundColorAttributeName')),UIback,range)

	return attributed_string.ptr

def pickerView_titleForRow_forComponent_(self,cmd,pickerview,row,component):
	# not necessary if pickerView_attributedTitleForRow_forComponent_ exists
	txt = wv.PickerView_data[ObjCInstance(pickerview).tag()][row]
	return ns(txt).ptr

def pickerView_numberOfRowsInComponent_(self,cmd,pickerview,component):
	n = len(wv.PickerView_data[ObjCInstance(pickerview).tag()])
	return n

def numberOfComponentsInPickerView_(self,cmd,pickerview):
	return 1			# number of spinning-wheels
	
def rowSize_forComponent_(self,cmd,pickerview,component):
	return 100
	
def pickerView_rowHeightForComponent_(self,cmd,pickerview,component):
	return 30.0
	
def pickerView_didSelectRow_inComponent_(self,cmd,pickerview,row,component):
	txt = wv.PickerView_data[ObjCInstance(pickerview).tag()][row]
	print(txt)
	
methods = [numberOfComponentsInPickerView_, pickerView_titleForRow_forComponent_, pickerView_numberOfRowsInComponent_, rowSize_forComponent_, pickerView_rowHeightForComponent_, pickerView_attributedTitleForRow_forComponent_, pickerView_didSelectRow_inComponent_] 

protocols = ['UIPickerViewDataSource','UIPickerViewDelegate']

MyUIPickerViewDataSourceAndDelegate = create_objc_class('MyUIPickerViewDataSourceAndDelegate', NSObject, methods=methods, protocols=protocols)
#========== methods and delegate protocols of new class:end

class MyUIPickerView:
	@on_main_thread
	def __init__(self,tag=0,frame=None):
		
		frame_objc = CGRect(CGPoint(frame[0],frame[1]), CGSize(frame[2], frame[3]))
				
		self.PickerView = UIPickerView.alloc().initWithFrame_(frame_objc)
		
		self.MyUIPickerViewDataSourceAndDelegate = MyUIPickerViewDataSourceAndDelegate.alloc().init().autorelease()
		self.PickerView.setDataSource_(self.MyUIPickerViewDataSourceAndDelegate)
		self.PickerView.setDelegate_(self.MyUIPickerViewDataSourceAndDelegate)
		
		self.PickerView.showsSelectionIndicator = True
		self.PickerView.setTag_(tag)						# to identify the Picker View
		self.PickerView.release()
		
class MyView(ui.View):
	@on_main_thread
	def __init__(self, *args, **kwargs):
		ui.View.__init__(self, *args, **kwargs)
		
		self.background_color = 'white'
		
		self.PickerView_data = {}
		
		self_objc = ObjCInstance(self)

		x = MyUIPickerView(tag=1,frame=[100,100,200,100])
		x.PickerView.backgroundColor = UIColor.color(red=1.0, green=1.0, blue=1.0, alpha=1.0)
		self_objc.addSubview_(x.PickerView)
		years = []
		for year in range(2000,2040):
			years.append(str(year))
		self.PickerView_data[1] = years

		y = MyUIPickerView(tag=2,frame=[100,400,200,100])
		y.PickerView.backgroundColor = UIColor.color(red=0.9, green=0.9, blue=0.9, alpha=1.0)
		self_objc.addSubview_(y.PickerView)
		self.PickerView_data[2] = ['xxxxxa','yyyyy','zzzzz']
		
if __name__ == '__main__':
	global wv
	console.clear()
	wv = MyView()
	wv.present('full_screen')

