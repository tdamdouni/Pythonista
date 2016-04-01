# -*- coding: utf-8 -*-
import os
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon('plugin.video.funimation')
name = addon.getAddonInfo('id')
icon = addon.getAddonInfo('icon')
msg_success = addon.getLocalizedString(30602)
msg_fail = addon.getLocalizedString(30604)

# remove cookie
cookie_path = xbmc.translatePath(addon.getAddonInfo('profile'))
cookie_path = os.path.join(cookie_path, 'fun-cookie.txt')
if os.path.exists(cookie_path):
    os.remove(cookie_path)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (
        name, msg_success, 3000, icon))
else:
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (
        name, msg_success, 3000, icon))
