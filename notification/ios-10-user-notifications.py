# https://forum.omz-software.com/topic/3467/ios-10-user-notifications-not-working

from objc_util import *
import random

load_framework('UserNotifications')

nc = ObjCClass('UNUserNotificationCenter').currentNotificationCenter()
nc.requestAuthorizationWithOptions_completionHandler_(4L, None)

err = None
d = NSDictionary.dictionary() #empty dict

# imgurl = nsurl('file:///private/var/mobile/Containers/Shared/AppGroup/09FE1A2B-E1E5-4112-B78F-665929FD7600/Pythonista3/Documents/Objective-C/swift.png') #gets deleted somehow...
imgurl = nsurl('file:///var/containers/Bundle/Application/586AFA89-329A-4E66-9221-2D9EA78A4F46/Pythonista3.app/AppIcon60x60@3x.png')  # Must be a local file

action = ObjCClass("UNNotificationAction").alloc()._initWithIdentifier_title_options_('firstButton', 'First', d)
action.isAuthenticationRequired = True
#action.isDestructive = True  # Red Text

textaction=ObjCClass("UNTextInputNotificationAction").alloc()._initWithIdentifier_title_options_textInputButtonTitle_textInputPlaceholder_('textInput','Title',d,'InputButtonTitle','Placeholder')

category = ObjCClass("UNNotificationCategory").alloc()._initWithIdentifier_actions_minimalActions_intentIdentifiers_options_('pythonista', [action,textaction], [action,textaction], d, d)

nc.setNotificationCategories_([category])

attachment1 = ObjCClass("UNNotificationAttachment").attachmentWithIdentifier_URL_options_error_('pythonistaimg', imgurl, d, err)

content = ObjCClass("UNMutableNotificationContent").new()
content.setCategoryIdentifier_('pythonista')
content.title = 'Hello, iOS 10'
content.subtitle = 'Introduction to Notifications'
content.shouldAddToNotificationsList = True
content.badge = random.randint(1, 100)
content.body = "Let's talk about notifications!"
content.shouldAlwaysAlertWhileAppIsForeground = True
#content.attachments = [attachment1] #Commemted for debug purposes

trigger = ObjCClass("UNTimeIntervalNotificationTrigger").alloc()._initWithTimeInterval_repeats_(1, False)
request = ObjCClass("UNNotificationRequest").alloc()._initWithIdentifier_content_trigger_('pythonistaNotification', content, trigger)

nc.addNotificationRequest_(request)
# --------------------

