# coding: utf-8
#. objc from http://www.thinkandbuild.it/interactive-notifications-with-notification-actions/

# https://gist.github.com/jsbain/3c54779a97725d8bd5c1f520c93c95e3

# https://forum.omz-software.com/topic/3646/notifications-extra-options-other-than-action-url

from objc_util import *


UIUserNotificationSetting = ObjCClass('UIUserNotificationSettings')
UIMutableUserNotificationCategory = ObjCClass('UIMutableUserNotificationCategory')
UIMutableUserNotificationAction = ObjCClass('UIMutableUserNotificationAction')
UIUserNotificationSettings = ObjCClass('UIUserNotificationSettings')
UILocalNotification = ObjCClass('UILocalNotification')
BG=1
FG=0
UIUserNotificationActionContextDefault=0
UIUserNotificationActionContextMinimal=1

UIUserNotificationTypeNone    = 0,
UIUserNotificationTypeBadge   = 1 << 0
UIUserNotificationTypeSound   = 1 << 1
UIUserNotificationTypeAlert   = 1 << 2

# define Action
actionA = UIMutableUserNotificationAction.new()
actionA.identifier = "OPTION_A"
actionA.title = "OpenInApp"
actionA.activationMode = FG
actionA.authenticationRequired = True
actionA.destructive = False


#define Action
actionB = UIMutableUserNotificationAction.new()
actionB.identifier = 'OPTION_B'
actionB.title = "RunInBG"
actionB.activationMode = BG
actionB.authenticationRequired = True
actionB.destructive = False

#define another Action
actionC = UIMutableUserNotificationAction.new()
actionC.identifier = 'OPTION_C'
actionC.title = "C"
actionC.activationMode = FG
actionC.destructive = True

#// Category
myCategory = UIMutableUserNotificationCategory.new()
myCategory.identifier = 'MY_CATEGORY'

#// A. Set actions for the default context(alert)
myCategory.setActions_forContext_(
                        [actionA, actionB, actionC], UIUserNotificationActionContextDefault)


#// B. Set actions for the minimal context (banner)
myCategory.setActions_forContext_(
                        [actionA, actionB], UIUserNotificationActionContextMinimal)

#Registration *****************************************

types = UIUserNotificationTypeAlert | UIUserNotificationTypeSound
settings = UIUserNotificationSettings.alloc().initWithTypes_categories_(
                                types, [myCategory])

app=UIApplication.sharedApplication()
app.registerUserNotificationSettings_(settings)

NSDate=ObjCClass('NSDate')


import time

# CREATE replacement delegate method
def application_handleActionWithIdentifier_forLocalNotification_completionHandler_(_cmd,_sel,app,identifier,notif,completionhandler):
	print (ObjCInstance(identifier))
	print (ObjCInstance(notif))
	print (time.ctime())
	ObjCInstance( completionhandler).invoke()
	
	
# for some reason, the @? encoding for objcblocks is not working properly on 32 bit at least.. so just use pointer
application_handleActionWithIdentifier_forLocalNotification_completionHandler_.encoding='v@:@@@@'

handler=create_objc_class('handler',ObjCClass('PA3AppDelegate'),[application_handleActionWithIdentifier_forLocalNotification_completionHandler_],[])

handler_obj=handler.new()

#hang on to old delegate, then monkey patch.  this may not be robust!
retain_global(handler_obj)
def set_delegate():
	olddelegate=app.delegate()
	retain_global(olddelegate)
	app.delegate=handler_obj
	
def do_notification(delay):
	mynotification = UILocalNotification.new()
	mynotification.alertBody = 'This is a notification. Swipe for options'
	mynotification.fireDate = NSDate.dateWithTimeIntervalSinceNow_(delay)
	mynotification.category = 'MY_CATEGORY'
	#mynotification.repeatInterval = NSCalendarUnit.CalendarUnitMinute
	app.scheduleLocalNotification_(mynotification)
	
	
import webbrowser
set_delegate()
do_notification(10)
webbrowser.open('safari-http://') # just to show the effect

