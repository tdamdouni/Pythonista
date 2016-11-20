# https://github.com/cclauss/Ten-lines-or-less/blob/master/pythonista_docs.py
import os, ui

if __name__ == '__main__':
	app_path = os.path.abspath(os.path.join(os.__file__, '../..'))
	fmt = 'file://{}/Documentation/index.html'
	web_view = ui.WebView(name='Pythonista Documentation')
	web_view.load_url(fmt.format(app_path))
	web_view.present()  # present Pythonista docs in a ui.WebView

