# https://forum.omz-software.com/topic/2582/get-web-source-code/11

import ui, appex
class wvdelegate(object):
	def webview_did_finish_load(self, webview):
		html = webview.eval_js('document.documentElement.innerHTML')
		webview.load_html('<xmp>' + html + r'<\xmp>')
		webview.delegate = None
wv = ui.WebView()
wv.load_url(appex.get_url())
wv.delegate = wvdelegate()
wv.present()

# You could also do like this to copy the HTML


import ui, appex, clipboard
class wvdelegate(object):
	def webview_did_finish_load(self, webview):
		self.html = webview.eval_js('document.documentElement.innerHTML')
		webview.load_html('<xmp>' + self.html + r'<\xmp>')
		webview.delegate.webview_did_finish_load = None
		wv.right_button_items = [ui.ButtonItem(image=ui.Image('iob:clipboard_32'), action=lambda x: clipboard.set(wv.delegate.html))]
wv = ui.WebView()
wv.load_url(appex.get_url())
wv.delegate = wvdelegate()
wv.present()

