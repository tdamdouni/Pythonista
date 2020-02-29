# coding: utf-8

# @omz

# https://forum.omz-software.com/topic/2941/any-idea-how-to-make-a-delagate-for-objc_utl-to-use/5

# https://developer.apple.com/library/mac/documentation/Networking/Conceptual/NSNetServiceProgGuide/Articles/BrowsingForServices.html

from __future__ import print_function
from objc_util import *
NSNetServiceBrowser = ObjCClass('NSNetServiceBrowser')

def netServiceBrowser_didFindService_moreComing_(_self, _cmd, _browser, _service, more):
    print('Service found:', ObjCInstance(_service))

BrowserDelegate = create_objc_class('BrowserDelegate',
    methods=[netServiceBrowser_didFindService_moreComing_],
    protocols=['NSNetServiceBrowserDelegate'])

def main():
    browser = NSNetServiceBrowser.alloc().init()
    delegate = BrowserDelegate.alloc().init()
    browser.setDelegate_(delegate)
    browser.searchForServicesOfType_inDomain_('_ssh._tcp.', '')

if __name__ == '__main__':
    main()
