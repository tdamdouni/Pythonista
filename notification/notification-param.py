# https://forum.omz-software.com/topic/3158/fyi-notifications-msg-param-seems-to-be-able-to-take-a-lot

import ui
import notification
str = 'a' * 100000
str = str + 'xxx'
notification.schedule(str ,delay = 60)

