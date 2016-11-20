# coding: utf-8

# https://forum.omz-software.com/topic/2970/objc_util-uitextview-and-attributed-text

@on_main_thread
def test_001():
	red = UIColor.redColor()
	font = ObjCClass('UIFont').systemFontOfSize_(30.)
	mystring = ObjCClass('NSMutableAttributedString').alloc()
	teststring = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt facilisis dapibus.'
	mystring.initWithString_(teststring)
	#d_red = NSDictionary.alloc().initWithObjectsAndKeys_([red, 'NSForegroundColorAttributeName', None]) # crash
	d_red = NSDictionary.alloc().initWithObjects_forKeys_((red,), ('NSForegroundColorAttributeName',))
	mystring.setAttributes_range_(d_red, NSRange(10, 15))
	tv = ui.TextView()
	tvc = ObjCInstance(tv)
	
	#tvc.setAttributedText_(mystring)
	# the following line works just fine (why?)
	tvc.attributedText = mystring
	tvc.setFont_(font) # ok
	tv.present()
	
# The main problem here is that the constant NSForegroundColorAttributeName actually corresponds to the string 'NSColor'. Unfortunately, it's not really possible to figure this out without Xcode because those are compile-time constants, and they don't exist at runtime (there is no code you could write in Pythonista to translate from NSForegroundColorAttributeName to 'NSColor').

# It's possible to use custom attribute names for NSAttributedString (for metadata , custom rendering etc.), so attributes that the text view doesn't understand are simply ignored.

# As a general tip, objc_util bridges Python dicts to NSDictionary pretty seamlessly, so instead of the rather complicated NSDictionary.alloc().initWithObjects_forKeys_((red,), ('NSColor',)), you can simply use {'NSColor': red}.

