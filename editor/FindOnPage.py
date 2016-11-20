# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2595/suggestion-find-in-the-built-in-docs/5

# Adds a "Find on page" button to the documentation browser.
# NOTE: Only intended for iPad, probably doesn't work correctly on iPhone.

from objc_util import *
import console
UIBarButtonItem = ObjCClass('UIBarButtonItem')

js_tpl = '''
// http://james.padolsey.com/snippets/highlighting-text-with-javascript/
function highlight(container, what) {
    var content = container.innerHTML,
        pattern = new RegExp('(>[^<.]*)(' + what + ')([^<.]*)','gi'),
        replaceWith = '$1<span style="background-color:yellow" class="search-highlight">$2</span>$3',
        highlighted = content.replace(pattern,replaceWith);
    return (container.innerHTML = highlighted) !== content;
}
// http://stackoverflow.com/a/11986374
function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [curtop];
    }
}
highlight(document.body, '{TERM}');
window.scroll(0, findPos(document.getElementsByClassName("search-highlight")[0]));
'''

def get_accessory_tab_vc():
	root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()
	tab_vc = root_vc.accessoryViewController()
	return tab_vc
	
def get_docs_vc():
	tab_vc = get_accessory_tab_vc()
	if not tab_vc.documentationViewController():
		tab_vc.showDocumentation()
	return tab_vc.documentationViewController()
	
def searchAction(_self, _cmd):
	term = console.input_alert('Search on page')
	doc_vc = get_docs_vc()
	webview = doc_vc.webView()
	search_js = js_tpl.replace('{TERM}', term)
	webview.stringByEvaluatingJavaScriptFromString_(search_js)
	
DocSearchHandler = create_objc_class('DocSearchHandler', methods=[searchAction])

@on_main_thread
def add_search_button():
	doc_vc = get_docs_vc()
	buttons = doc_vc.navigationItem().rightBarButtonItems().mutableCopy().autorelease()
	if len(buttons) > 1:
		return
	search_img = UIImage.imageNamed_('Search')
	handler = DocSearchHandler.new()
	search_button = (UIBarButtonItem.alloc()
	.initWithImage_style_target_action_(search_img, 0, handler, 'searchAction'))
	buttons.addObject_(search_button)
	doc_vc.navigationItem().rightBarButtonItems = buttons
	tab_vc = get_accessory_tab_vc()
	tab_vc.reloadBarButtonItemsForSelectedTab()
	
add_search_button()

