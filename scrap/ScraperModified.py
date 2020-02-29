# coding: utf-8

# https://forum.omz-software.com/topic/2380/returning-execution-to-main-thread-with-ui-webview

# A thread synchronization, such as threading.Event, threading.Semaphore, works nicely here. wait_modal requires you to present then close the view.

from __future__ import print_function
import ui
import threading
class Scraper (object):
    def __init__(self, callback, url, js = 'document.documentElement.outerHTML'):
        self.wv = ui.WebView()
        self.wv.delegate = self
        self.wv.load_url(url)
        self.callback = callback
        self.js = js
        self.ready_event=threading.Event()
        
    def webview_did_finish_load(self, webview):
        self.callback(webview.eval_js(self.js))
        self.ready_event.set()

# Example:
def parse_response(response):
    print('Webview finished loading - ' + response)

def main():
    s = Scraper(parse_response, 'https://www.google.com', 'document.title;')
    # Wait until scraper finished loading
    s.ready_event.wait()
    print('Main thread finished executing')
if __name__ == '__main__':
    main()