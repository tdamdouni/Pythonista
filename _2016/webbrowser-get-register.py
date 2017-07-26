# https://forum.omz-software.com/topic/3546/webbrowser-get-and-register/4

from objc_util import *
app = UIApplication.sharedApplication()
app.openURL_(nsurl('googlechrome://apple.com'))
