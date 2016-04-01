# https://github.com/cclauss/Ten-lines-or-less/blob/master/pythonista_docs.py
# coding: utf-8

import sys, ui

if __name__ == '__main__':
    docs_path = 'file://{}/../Documentation/index.html'.format(sys.executable)
    # webbrowser.open(docs_path)
    web_view = ui.WebView(name='Pythonista Documentation')
    web_view.load_url(docs_path)
    web_view.present()  # present Pythonista docs in a ui.WebView