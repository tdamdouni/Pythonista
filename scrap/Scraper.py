# coding: utf-8

# @Multi-Threads

# https://forum.omz-software.com/topic/2380/returning-execution-to-main-thread-with-ui-webview

# I'm trying to implement a Web Scraper that uses ui.WebView to render a page and then return HTML from that page. The pages can be rendered with JavaScript so I can't use requests or mechanize like I normally would.

# The problem I have at the moment with my current implementation (below) is that I want the main thread to wait until the page has finished rendering and then return the HTML of that page back to the main thread. At the moment the main thread finishes executing before the page has finished loading.

from __future__ import print_function
import ui

class Scraper (object):
    def __init__(self, callback, url, js = 'document.documentElement.outerHTML'):
        self.wv = ui.WebView()
        self.wv.delegate = self
        self.wv.load_url(url)
        self.callback = callback
        self.js = js
    
    def webview_did_finish_load(self, webview):
        self.callback(webview.eval_js(self.js))

# Example:
def parse_response(response):
    print('Webview finished loading - ' + response)

def main():
    s = Scraper(parse_response, 'https://www.google.com', 'document.title;')
    # How can I wait for the Web View to finish loading here and return the HTML of the webpage before proceeding on the main thread?
    print('Main thread finished executing')
if __name__ == '__main__':
    main()

# http://omz-software.com/pythonista/docs/ios/ui.html#ui.View.wait_modal Will wait until the user closes the view or http://omz-software.com/pythonista/docs/ios/ui.html#ui.View.close is called on the view.