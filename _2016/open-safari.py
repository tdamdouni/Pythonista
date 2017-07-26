# https://forum.omz-software.com/topic/3794/open-gif-or-image-in-safari/6

from objc_util import nsurl,UIApplication
from socket import gethostname
app = UIApplication.sharedApplication()
URL = 'http://%s.local:8080' % gethostname()
app.openURL_(nsurl(URL))
