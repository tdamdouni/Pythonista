_https://forum.omz-software.com/topic/4472/show-preview_

There is no built-in “Show Preview” action, and there isn’t really a Python interface for this either. The good news is that Editorial can call native Objective-C code, using the objc_util module, so this hack should work (via a “Run Python Script” action):

from objc_util import UIApplication, on_main_thread

@on_main_thread
def main():
    app=UIApplication.sharedApplication()
    vc=app.keyWindow().rootViewController()
    vc.showAccessoryWithAnimationDuration_(0.3)
    avc = vc.accessoryViewController()
    avc.showPreview()

main()

Caveat: This might break at some point, when I change the internals. It should be possible to adapt it though.
