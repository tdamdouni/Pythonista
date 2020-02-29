# coding: utf-8

# https://forum.omz-software.com/topic/2380/returning-execution-to-main-thread-with-ui-webview/4

from __future__ import print_function
import ui
import threading

class Scraper (object):
    def __init__(self, url, js = 'document.documentElement.outerHTML'):
        self.wv = ui.WebView()
        self.wv.delegate = self
        self.wv.load_url(url)
        self.js = js
        self.response = ''
        self.ready_event = threading.Event()
        self.ready_event.wait()
    
    def webview_did_finish_load(self, webview):
        self.response = webview.eval_js(self.js)
        self.ready_event.set()

def main():
    r = Scraper('https://www.google.com', 'document.title;').response
    print('Response: ' + r)

if __name__ == '__main__':
    main()