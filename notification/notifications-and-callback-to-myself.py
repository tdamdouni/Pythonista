# coding: utf-8

# https://forum.omz-software.com/topic/2565/notifications-and-callback-to-myself

import notification

notification.schedule('test', 5, 'default', 'pythonista://test.py?action=run')

