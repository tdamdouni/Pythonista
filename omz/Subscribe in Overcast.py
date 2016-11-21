# coding: utf-8

# @omz twitter

import urllib
import appex
from objc_util import UIApplication, nsurl
import time

page_url = appex.get_url()
if page_url:
	overcast_url = 'overcast://x-callback-url/add?url=%s' %(urllib.quote(page_url, ''),)
	app = UIApplication.sharedApplication()
	app.openURL_(nsurl(overcast_url))
	time.sleep(0.5)
	appex.finish()