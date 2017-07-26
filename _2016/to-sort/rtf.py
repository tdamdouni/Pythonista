# coding: utf-8

# https://gist.github.com/jsbain/b2436247405bb2ee81c1a52f5f2f3e83

# https://forum.omz-software.com/topic/3061/text-styling-in-ui-textview/4

from objc_util import *
import ui
import os

def save_text(tv,filename):
	'''save the attributed text from tv to an rtf file (provide full path)'''
	attribtxt=ObjCInstance(tv).attributedText()
	data=attribtxt.RTFFromRange_documentAttributes_(NSRange(0,attribtxt.length()),	None)

	data.writeToFile_atomically_(filename,True)
@on_main_thread
def load_text(tv,filename):
	'''load an rtf file, and load into the attributed text f the textview. (provide full path)

'''
	loaded_data=NSData.dataWithContentsOfFile_(filename)
	nas=ObjCClass('NSAttributedString')
	newtext=nas.alloc().initWithRTF_documentAttributes_(loaded_data,None)
	ObjCInstance(tv).attributedText=newtext

if __name__=='__main__':
	
	tv=ui.TextView()
	tv.text='hello'
	tv.font=('Snell Roundhand',46)
	filename=os.path.abspath('myfile.rtf')
	
	save_text(tv,filename)
	
	tv2=ui.TextView()
	load_text(tv2,filename)
	tv2.present('sheet')
