# coding: utf-8

# https://forum.omz-software.com/topic/2554/how-can-i-get-console-width

import ui
width, height = ui.get_screen_size()

#==============================

# coding: utf-8

import console, ui, math

fnt_name = 'Source Sans Pro'
fnt_size = 12

fnt = (fnt_name, fnt_size)
w = ui.get_screen_size()[0]
char_width = ui.measure_string('M', font = fnt)[0]
print char_width
num_chars = math.floor((w / char_width))
print num_chars
console.set_font(fnt_name, fnt_size)
print 'M' * int(num_chars)

#==============================

from objc_util import *
w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()

def filter_subviews(view,text=None, objcclasstext=None):
	matching_svs=[]
	sv=view.subviews()
	if sv is None:
		return matching_svs
	for v in sv:
		if objcclasstext and objcclasstext in v._get_objc_classname():
			matching_svs.append(v)
		if text and hasattr(v,'text'):
			if str(v.text()) and text in str(v.text()):
				matching_svs.append(v)
		matching_svs.extend(
		filter_subviews(v, text=text, objcclasstext=objcclasstext))
	return matching_svs
	
# don't find editor window, so concatenate string
print 'find'+'me'
# in this case, only one entry will be returned.  otherwise, may need to look at list to figure out which view is the one you are seeking.
console_view=filter_subviews(main_view,'find'+'me')[0]

#==============================

<OMTextView: <OMTextView: 0x16942e00; baseClass = UIScrollView; frame = (0 0; 320 460); text = 'findme
>>> console_view
'; clipsToBounds = YES; autoresize = W+H; gestureRecognizers = <NSArray: 0x16683d30>; layer = <CALayer: 0x166838a0>; contentOffset: {0, 0}; contentSize: {304, 71}>>

#==============================

consoleWidth = getConsoleWidth() # <= 50
print('DownloadFromWeb')
print('Give me an URL, and I will download it for you.')
print('='*consoleWidth)

#==============================

import ui
def getConsoleWidth(font=('Menlo',14)):
	screenWidth = ui.get_screen_size().width
	charWidth = ui.measure_string('.',font=font).width
	return int(screenWidth / charWidth-1.5)
	
#==============================

app=ObjCClass('UIApplication').sharedApplication()
d=app.delegate()
cv=d.consoleViewController()
font=d.consoleViewController().outputFont()
print font

#==============================

defaults = ObjCClass('NSUserDefaults').standardUserDefaults()
print str(defaults.stringForKey_('OutputFontName'))
print defaults.integerForKey_('OutputFontSize')

