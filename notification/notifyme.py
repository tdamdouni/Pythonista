# coding: utf-8
# coding: utf-8 (notifyme.py)

# https://forum.omz-software.com/topic/2565/notifications-and-callback-to-myself

from __future__ import print_function
import notification

notification.schedule('test', 5, 'default', 'pythonista://test.py?action=run')

#==============================

# coding: utf-8
import notification
print('hi')
notification.schedule('hello',5,action_url='pythonista://test.py?action=run')