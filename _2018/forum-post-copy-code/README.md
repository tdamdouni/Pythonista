* Copy `forum-post-copy-code.py` script into the Pythonista
* Go to Settings - Share Extension Shortcuts
* Tap on `+` button and add `forum-post-copy-code.py` there
* Open Safari, visit forum, find a topic & post with some code
* Make sure that URL ends with /NUMBER, like /5, /6, ... (it's a post number)
* Tap on action button in Safari
* Tap on Run Pythonista Script
* Tap on shortcut you did previously add
* All code elements are copied to the clipboard

Sample URL:

* https://forum.omz-software.com/topic/4622/notification-module-api/6

Clipboard content:

```
# <code> element no 1

import notification

'''
Simple example to show setting a notification in a loop each minute
for x mins.

In my real implementation I am using Arrow.span.
For example, I would like to set notifications for:
    from (a local time) every 1 hour with a message
    from (a local time) every 3 hours with a message
    from (a local time) every 24 hours with a message
    etc... With a repeat/duration I set.

I can set this up and do it using arrow correctly. But the behaviour of the
notifications module makes it unsuable for this senerio.
'''

num_mins = 5
delays = [60 * (i + 1) for i in range(num_mins)]

for i, d in enumerate(delays):
    x = notification.schedule('Your Game Notification, Mins={}'.format(i + 1),
                              delay=d,
                              sound_name='arcade:Powerup_1',
                              action_url=None)

# A notification so you know this msg group is finished
x = notification.schedule('Game Nofications are over!!!',
                          delay=delays[num_mins - 1] + 10,
                          sound_name='arcade:Powerup_3',
                          action_url=None)

# just put this here in testing so you aviod running multiple times
print('Finished Running')
```