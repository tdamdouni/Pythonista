# https://forum.omz-software.com/topic/3270/get-ui-webview-loaded-url

import ui
w, h = ui.get_screen_size()

v = ui.View()
wv = ui.WebView()
wv.width = w
wv.height = h
wv.load_url('https://www.google.com')
wv.evaluate_javascript('window.location.href')
v.add_subview(wv)
v.present()

