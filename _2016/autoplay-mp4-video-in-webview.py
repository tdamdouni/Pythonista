# https://forum.omz-software.com/topic/3910/autoplay-mp4-video-in-webview/2

webview = ui.WebView()
html = TEMPLATE.replace('{{FPATH}}', absfilepath)
webview.load_html(html)
webview.present()
# --------------------
<video autoplay>
	<source src="{{FPATH}}" type="video/mp4">
</video>
# --------------------
cover_image = ui.WebView()
cover_image.load_url(os.path.abspath(local_file))
# --------------------
cover_image.touch_enabled = False
# --------------------

