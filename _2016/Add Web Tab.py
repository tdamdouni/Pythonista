# coding: utf-8

# https://gist.github.com/omz/b39519b877c07dbc69f8

from objc_util import *
import console
import urllib
import dialogs

WKWebView = ObjCClass('WKWebView')
UIViewController = ObjCClass('UIViewController')
UIBarButtonItem = ObjCClass('UIBarButtonItem')
NSURLRequest = ObjCClass('NSURLRequest')
UITextField = ObjCClass('UITextField')
UISearchBar = ObjCClass('UISearchBar')
NSDataDetector = ObjCClass('NSDataDetector')

@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	methods = [share, goBack, goForward, searchBarSearchButtonClicked_]
	protocols = ['OMTabContent', 'UISearchBarDelegate']
	CustomViewController = create_objc_class('CustomViewController', UIViewController, methods=methods, protocols=protocols)
	vc = CustomViewController.new().autorelease()
	vc.title = 'Web'
	
	share_item = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Action'), 0, vc, sel('share'))
	back_item = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Back'), 0, vc, sel('goBack'))
	fw_item = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Forward'), 0, vc, sel('goForward'))
	
	vc.navigationItem().rightBarButtonItems = [share_item, fw_item, back_item]
	webView = WKWebView.new().autorelease()
	webView.loadRequest_(NSURLRequest.requestWithURL_(nsurl('http://www.google.com')))
	
	searchbar = UISearchBar.alloc().initWithFrame_(((0, 0), (200, 32)))
	searchbar.searchBarStyle = 2
	searchbar.placeholder = 'Search or enter address'
	searchbar.delegate = vc
	# There seems to be a bug in objc_util that makes the regular method name translation fail for setAutocapitalizationType: (could have to do with the property being defined in a protocol, not completely sure).
	ObjCInstanceMethod(searchbar, 'setAutocapitalizationType:')(0)
	
	vc.navigationItem().titleView = searchbar
	
	vc.view = webView
	tabVC.addTabWithViewController_(vc)
	
def share(_self, _cmd):
	view = ObjCInstance(_self).view()
	url = view.URL()
	if url:
		url_str = str(url.absoluteString())
		dialogs.share_url(url_str)

def goBack(_self, _cmd):
	view = ObjCInstance(_self).view()
	view.goBack()

def goForward(_self, _cmd):
	view = ObjCInstance(_self).view()
	view.goForward()

def searchBarSearchButtonClicked_(_self, _cmd, _sb):
	searchbar = ObjCInstance(_sb)
	term = str(searchbar.text())
	searchbar.resignFirstResponder()
	if term:
		det = NSDataDetector.dataDetectorWithTypes_error_(1<<5, None)
		res = det.firstMatchInString_options_range_(term, 0, (0, len(term)))
		view = ObjCInstance(_self).view()
		if res:
			view.loadRequest_(NSURLRequest.requestWithURL_(res.URL()))
			searchbar.text = res.URL().absoluteString()
		else:
			view.loadRequest_(NSURLRequest.requestWithURL_(nsurl('http://www.google.com/search?q=' + urllib.quote(term))))
	
if __name__ == '__main__':
	main()
