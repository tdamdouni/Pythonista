# https://files.slack.com/files-pri/T0M854UF2-F2JESH4HK/notificationstuff.py

# 
import ctypes
import objc_util
import time
​
UNMutableNotificationContent = objc_util.ObjCClass("UNMutableNotificationContent")
UNNotificationAction = objc_util.ObjCClass("UNNotificationAction")
UNNotificationCategory = objc_util.ObjCClass("UNNotificationCategory")
UNNotificationRequest = objc_util.ObjCClass("UNNotificationRequest")
UNTimeIntervalNotificationTrigger = objc_util.ObjCClass("UNTimeIntervalNotificationTrigger")
UNUserNotificationCenter = objc_util.ObjCClass("UNUserNotificationCenter")
​
def userNotificationCenter_willPresentNotification_withCompletionHandler_(self, _cmd, unc, notification, handler):
	pass
​
def userNotificationCenter_didReceiveNotificationResponse_withCompletionHandler_(self, _cmd, unc, response, handler):
	print(objc_util.ObjCInstance(response))
​
DGUNUNCDelegate = objc_util.create_objc_class(
	"DGUNUNCDelegate",
	methods=[
		userNotificationCenter_willPresentNotification_withCompletionHandler_,
		userNotificationCenter_didReceiveNotificationResponse_withCompletionHandler_
	],
	protocols=[
		"UNUserNotificationCenterDelegate"
	]
)
​
unc = UNUserNotificationCenter.currentNotificationCenter()
unc.requestAuthorizationWithOptions_completionHandler_((1<<2) | (1<<1) | (1<<0), None)
unc.setDelegate_(DGUNUNCDelegate.alloc().init())
doit = UNNotificationAction.actionWithIdentifier_title_options_("doit", "Just DO IT!", 0)
ornot = UNNotificationAction.actionWithIdentifier_title_options_("ornot", "Or not", 0)
foocat = UNNotificationCategory.categoryWithIdentifier_actions_intentIdentifiers_options_("foocat", [doit, ornot], [], 0)
unc.setNotificationCategories_({foocat})
​
def errorhandler_imp(_cmd, error):
	if error is None:
		print("No errors!")
	else:
		print("Error!")
		print(objc_util.ObjCInstance(error))
​
errorhandler = objc_util.ObjCBlock(errorhandler_imp, None, [ctypes.c_void_p, ctypes.c_void_p])
​
def main():
	foocontent = UNMutableNotificationContent.alloc().init()
	foocontent.setTitle_("Motivation")
	foocontent.setBody_("Don't let your dreams be dreams.")
	foocontent.setCategoryIdentifier_("foocat")
	footrigger = UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(3, False)
	foorequest = UNNotificationRequest.requestWithIdentifier_content_trigger_("foorequest", foocontent, footrigger)
	unc.addNotificationRequest_withCompletionHandler_(foorequest, errorhandler)
​
if __name__ == "__main__":
	main()
​
