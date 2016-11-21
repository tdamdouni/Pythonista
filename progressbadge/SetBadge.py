# coding: utf-8

# https://gist.github.com/filippocld/a60d8ba734751d91c518

from objc_util import *
from console import input_alert,hud_alert

badgesting = input_alert('App Badge','Not more than 5 charaters')
UIApplication.sharedApplication().setApplicationBadgeString_(badgesting[:5])
hud_alert('Badge Set!')
