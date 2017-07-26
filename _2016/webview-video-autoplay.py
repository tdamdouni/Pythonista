# https://forum.omz-software.com/topic/3910/autoplay-mp4-video-in-webview/7

import ui
import os,time

# [~/Documents]$ wget http://techslides.com/demos/sample-videos/small.mp4
absfilepath=os.path.abspath('small.mp4')


TEMPLATE='''
<video id="myvideo" autoplay preload="auto">
    <source src="file://{{FPATH}}" type="video/mp4">
</video>
'''
v = ui.View()
webview = ui.WebView()
v.add_subview(webview)

html = TEMPLATE.replace('{{FPATH}}', absfilepath)
webview.load_html(html)

#button = ui.Button(title="Start Game")
#button.action = button_tapped
#v.add_subview(button)

v.frame = (0,0,500,500)
webview.frame = (0,0,500,500)
v.present()

#after view is presented, check that html is loaded, then play
# might be better to check document.readyState, but sometimes this can be complete before you start
id=webview.eval_js('document.getElementById("myvideo").id')
while not id =='myvideo':
	print('sleeping')
	time.sleep(1)
	id=webview.eval_js('document.getElementById("myvideo").id')
webview.eval_js('document.getElementById("myvideo").play();')

