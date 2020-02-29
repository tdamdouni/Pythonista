# coding: utf-8

from __future__ import print_function
import ui
from objc_util import *
import dialogs
import keychain

NSMutableAttributedString=ObjCClass('NSMutableAttributedString')
UIColor=ObjCClass('UIColor')
NSFontAttributeName=ns('NSFont')
NSForegroundColorAttributeName=ns('NSColor')
UIFont=ObjCClass('UIFont')

SELECTING = False
TYPING_WITH = "normal"

class tvDelegate (object):
	def textview_did_change(self,textview):
		tv.attributedText = NSMutableAttributedString.scrcStringWithString_(tv.text)
		if TYPING_WITH == "bold":
			tv.attributedText.addAttributes_range_({NSFontAttributeName:UIFont.fontWithName_size_("Helvetica-Bold",15)},NSRange(-1,0))
			tvobj.setAttributedText_(tv.attributedText)
	def textview_did_change_selection(self,textview):
		global SELECTING
		if textview.selected_range[0] == textview.selected_range[1]:
			SELECTING = False
		else:
			SELECTING = True
	def textview_did_begin_editing(self,textview):
		v["button5"].frame = (654,638,108,41)
	def textview_did_end_editing(self,textview):
		v["button5"].frame = (654,913,108,41)

def setText(info,point=0):
	if info == "typed":
		tvobj.setTypingAttributes_(tv.attributedText)
		tv.attributedText.addAttributes_range_({NSFontAttributeName:UIFont.fontWithName_size_("Helvetica-Bold",15)},NSRange(tv.text[-1],1))
		print(tv.attributedText)
		tvobj.setAttributedText_(tv.attributedText)
	elif info == "selected":
		tvobj.setAttributedText_(tv.attributedText)
		print("=====\n"+str(tv.attributedText)+"\n=====")
def bold(sender):
	global TYPING_WITH
	dBold = {
	NSFontAttributeName:UIFont.fontWithName_size_("Helvetica-Bold",15)
	}
	dNormal = {
	NSFontAttributeName:UIFont.fontWithName_size_("Helvetica",15)
	}
	if SELECTING == True:
		#print "hi"
		tv.attributedText.addAttributes_range_(dBold,NSRange(tv.selected_range[0],tv.selected_range[1]-tv.selected_range[0]))
		
		print(tv.attributedText)
		
		setText("selected",(tv.selected_range[0]))
	elif SELECTING == False:
		if TYPING_WITH == "normal":
			TYPING_WITH = "bold"
			v["scrollview1"]["buttonB"].background_color = "white"
			v["scrollview1"]["buttonB"].tint_color = '#3c7dff'
			tvobj.setTypingAttributes_(dBold)
		elif TYPING_WITH == "bold":
			TYPING_WITH = "normal"
			v["scrollview1"]["buttonB"].background_color = None
			v["scrollview1"]["buttonB"].tint_color = "white"
			tvobj.setTypingAttributes_(dNormal)
		#setText("typed")
def italic(sender):
	pass
def underline(sender):
	pass
def font(sender):
	pass
def save(sender):
	pass
	
v = ui.load_view()
v.present()
tv = v["textview1"]
tv.attributedText = NSMutableAttributedString.scrcStringWithString_(tv.text)
tvobj = ObjCInstance(tv)
tv.delegate = tvDelegate()
tv.auto_content_inset = True

