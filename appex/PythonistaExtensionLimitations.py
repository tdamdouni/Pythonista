# coding: utf-8

# https://forum.omz-software.com/topic/1988/launching-pythonista-from-1-6b-app-extension

# I'm trying to write a script for the 1.6 app extension that will:

# Take some text passed in from the share sheet
# Format the text in a specific way
# Place the formatted text on the pasteboard
# Launch Pythonista and run another script that will take the text on the pasteboard and do something with it.

# Is it possible to launch a pythonista:// URL from the app extension? If not, is it possible to do something with objc_util?

# Worst case, I can make it a two-step process but it would be great to have it in one place.

import appex
import clipboard
import webbrowser 

initial_text = appex.get_text()

# text processing stuff

clipboard.set(processed_text)
webbrowser.open('pythonista://NewFromClipboard.py')

# @omz
# As far as I'm aware, this is unfortunately impossible. The API that is supposed to open URLs from app extensions is [explicitly documented](https://developer.apple.com/library/ios/documentation/Foundation/Reference/NSExtensionContext_Class/#//apple_ref/occ/instm/NSExtensionContext/openURL:completionHandler:) as only being available for Today widgets, the regular one (via UIApplication) doesn't do anything either in an extension.

# In earlier versions of iOS 8, there was a workaround for this (essentially abusing a web view), but this has apparently been patched in 8.4.