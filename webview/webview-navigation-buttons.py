# https://forum.omz-software.com/topic/3315/webview-navigation-buttons

import ui

class MyWebView(ui.View):
	def __init__(self, url):
		self.width, self.height = ui.get_window_size()
		self.wv = ui.WebView(frame=self.bounds)
		self.wv.load_url(url)
		self.add_subview(self.wv)
		bi_back = ui.ButtonItem(image=ui.Image.named('iob:ios7_arrow_back_32'))
		bi_forward = ui.ButtonItem(image=ui.Image.named('iob:ios7_arrow_forward_32'))
		bi_back.action = self.go_back
		bi_forward.action = self.go_forward
		self.right_button_items = [bi_forward, bi_back]
		self.present()
		
	def go_back(self, bi):
		self.wv.go_back()
		
	def go_forward(self, bi):
		self.wv.go_forward()
		
		
wv = MyWebView('https://forum.omz-software.com')

