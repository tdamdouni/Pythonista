# https://forum.omz-software.com/topic/3324/notification-get_scheduled-gives-an-error

import notification
#print(notification.get_scheduled())
scheduled = notification.app.scheduledLocalNotifications()
for each in scheduled:
	print(each.alertBody()) # shows the message

