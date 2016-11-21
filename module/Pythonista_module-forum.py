
# coding: utf-8

# https://forum.omz-software.com/topic/2717/pythonista-module/42

from objc_util import *

class Pythonista(object):
	@on_main_thread
	def __init__(self):
		self.app = UIApplication.sharedApplication()
		self.rootVC = self.app.keyWindow().rootViewController()
		self.tabVC = self.rootVC.detailViewController()
		self.consoleVC = self.app.delegate().consoleViewController()
		self.userDefaults = ObjCClass('NSUserDefaults').standardUserDefaults()
		
	@on_main_thread
	def setBadgeString(self, s):
		self.app.setApplicationBadgeString_(s)
		
	@on_main_thread
	def setBadgeNumber(self, i):
		self.app.setApplicationIconBadgeNumber_(i)
		
	@on_main_thread
	def openURL(self, s):
		self.app._openURL_(nsurl(s))
		
	@on_main_thread
	def getConsoleFont(self):
		self.consoleVC.view()
		return self.consoleVC.outputFont()
		
	@on_main_thread
	def getDefaultFont(self):
		return [str(self.userDefaults.stringForKey_('OutputFontName')), self.userDefaults.integerForKey_('OutputFontSize')]
		
	@on_main_thread
	def addTab(self, s):
		newVC = create_objc_class('CustomViewController', ObjCClass('UIViewController'), methods=[], protocols=['OMTabContent',]).new().autorelease()
		newVC.title = s
		self.tabVC.addTabWithViewController_(newVC)
		
		
if __name__ == "__main__":
	p = Pythonista()
	#p.setBadgeString('test')
	#p.setBadgeNumber(1)
	#p.openURL('pythonita://')
	#print p.getConsoleFont()
	#print p.getDefaultFont()
	p.addTab('New')
	
# --------------------

from flask import Flask
app = Flask(__name__)

# --------------------

class WebTab(Tab):
	@on_main_thread
	def makeSelf(self):
		self.name = 'WebTab'
		biA = ButtonItem(self, image = 'Action', action ='wtShare')
		self.right_button_items.append(biA)
		biF = ButtonItem(self, image = 'Forward', action ='wtGoForward')
		self.right_button_items.append(biF)
		biB = ButtonItem(self, image = 'Back', action = 'wtGoBack')
		self.right_button_items.append(biB)
		sb = SearchBar(self)
		self.newVC.navigationItem().titleView = sb
		wv = WebView(self)
		wv.loadRequest_(NSURLRequest.requestWithURL_(nsurl('http://www.google.com')))
		self.newVC.view = wv
		
	@on_main_thread
	def customVC(self):
		return create_objc_class('CustomViewController', ObjCClass('UIViewController'), methods=[wtShare, wtGoBack, wtGoForward, searchBarSearchButtonClicked_], protocols=['OMTabContent', 'UISearchBarDelegate']).new().autorelease()
		
#--------------------

