# https://forum.omz-software.com/topic/3577/webview-not-allowing-me-to-scroll-to-the-bottom-right-corner

import ui
main = ui.ScrollView(frame=(0, 0, *ui.get_screen_size()))
main.content_size = (1920, 1080)
wv = ui.WebView(frame=(0, 0, *main.content_size))
wv.load_url('http://amdouni.com')
main.add_subview(wv)
main.present()

