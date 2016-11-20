# coding: utf-8

# https://gist.github.com/steventroughtonsmith/51edd66425998e5fca37

from Foundation import *
from QuartzCore import *
from UIKit import *

import console

WKWebView = ObjCClass('WKWebView')

@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().windows()[0].rootViewController()
	tabVC = rootVC.detailViewController()
	
	methods = [openURL, search]
	protocols = ['OMTabContent']
	CustomViewController = create_objc_class('CustomViewController', UIViewController, methods=methods, protocols=protocols)
	
	vc = CustomViewController.new()
	vc.title = 'Web'
	
	urlBarItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Textures/ionicons-link-24'),0,vc,sel('openURL'))
	searchBarItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('Textures/ionicons-search-24'),0,vc,sel('search'))
	
	vc.navigationItem().rightBarButtonItems = [urlBarItem, searchBarItem]
	
	webView = WKWebView.new()
	webView.loadRequest_(NSURLRequest.requestWithURL_(NSURL.URLWithString_('http://www.google.com')))
	vc.view = webView
	
	tabVC.addTabWithViewController_(vc)
	
def openURL(_self, _cmd):
	address = console.input_alert('Open URL')
	if len(address) > 0:
		ObjCInstance(_self).view().loadRequest_(NSURLRequest.requestWithURL_(NSURL.URLWithString_(address)))
		
def search(_self, _cmd):
	term = console.input_alert('Search')
	if len(term) > 0:
		ObjCInstance(_self).view().loadRequest_(NSURLRequest.requestWithURL_(NSURL.URLWithString_('http://google.com/search?q='+term)))
		
if __name__ == '__main__':
	main()

