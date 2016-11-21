# https://gist.github.com/Petitsurume/f871af650fd7ca6aabf8a8908809fca0

import objc_util
SFSafariViewController = objc_util.ObjCClass('SFSafariViewController')
safari = SFSafariViewController.alloc().initWithURL_(objc_util.nsurl('http://www.google.com'))
root_vc = objc_util.ObjCClass('UIApplication').sharedApplication().keyWindow().rootViewController()
while root_vc.presentedViewController():
	root_vc = root_vc.presentedViewController()
root_vc.presentViewController_animated_completion_(safari,False,None)

