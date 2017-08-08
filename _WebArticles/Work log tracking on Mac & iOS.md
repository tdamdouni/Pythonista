# Work log tracking on Mac & iOS

_Captured: 2015-11-07 at 00:55 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/07/26/work-log-tracking-on-mac-ios/)_

One of the challenges I've had recently is getting a better understanding on what I'm really working on and whether or not it's something I _should_ be working on. I poked around the iOS and Mac app stores looking for a task tracker. I found quite a few apps, but most turned out to be either time sheet/billing apps or simple to do list managers.

So I poked around the interwebs a bit and found a recent post on [so, it's come this](http://soitscometothis.net/post/logging-time-per-visit-with-keyboard-maestro) related to logging patient visits.

The opening paragraph is what caught my eye:

> I wanted a better idea of how much time I was spending per visit. This data could also be used when billing by time. I wrote three small macros to complete this task. All three macros use the same trigger, ⌘⌥⌃⇧b. This brings up a menu for me to choose what part of the macro-system I want. 

As I read through Michael's post I knew this could be the blueprint for what I wanted:

  * Date/time of when the task was worked on.
  * Duration of how long I worked on a given task.
  * Easy start/stop method while working on my Mac.
  * Basic running list of task in a text file.

It was everything I was looking for as a starting point. But I also knew I wanted to have some additional features:

  * A dialog box to enter a description of the task I was working on. 
  * A method to have the same information captured from my iPad or iPhone.
  * Validation check if a task had already been started.

### WorkLog for Mac

The Mac side of things was fairly straight forward. Michael had already given me a great blueprint on what I wanted. I made some minor tweaks to his Start Task [Keyboard Maestro](http://www.keyboardmaestro.com/main/) macro. I added a dialog box to enter a task description and expanded the time detail.

**Start Work Log:** The first KM macro takes the current date/time, the dialog box entry and then appends them to a file on Dropbox.

![](http://share.mygeekdaddy.me/worklog_start_timer_2014-07-24.png)

**Stop Work Log:** The stop timer macro is similar to the previous one. The KM macro takes the a current date/time, does a difference of the start time to calculate the task duration, and appends the text file on Dropbox.

![](http://share.mygeekdaddy.me/worklog_stop_timer_2014-07-24.png)

Download a copy of the KM macros: [WorkLog Macro](http://share.mygeekdaddy.me/KM_WorkLog.kmmacros_2014-07-24.zip).

### WorkLog for iOS

Replicating the same process for iOS was a bigger job, but something I knew that I could handle with [Drafts](https://itunes.apple.com/us/app/drafts-quickly-capture-notes/id502385074?mt=8&uo=4) and [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4). The iOS workflow consists of four Drafts Actions and two Pythonista scripts. The tasks are logged to the `WorkLogFile.md` document, the same as the KM macros.

#### Drafts Actions

**New Work Log:** This is the action that starts the work log process. The Drafts action will call two other actions - Copy the note to the clipboard and then run a script in Pythonista. The script, explained below, calls on another Drafts action to append the WorkLogFile.md file on Dropbox.

![](http://share.mygeekdaddy.me/_img_BLOGX_Automated_Task_Logger_R2_2014_07_25_210631.png)

[Install New Work Log Action](drafts://x-callback-url/import_action?type=URL&name=New%20Work%20Log&url=drafts%3A%2F%2Fx-callback-url.com%2Fcreate%3Ftext%3D%5B%5Bdraft%5D%5D%26action%3D%7B%7BCopy%20to%20Clipboard%7D%7D%26afterSuccess%3DDelete%26x-Success%3D%7B%7Bpythonista%3A%2F%2FstartTimer%3Faction%3Drun%7D%7D)

**Close Work Log:** This is the action that ends the work log process. The Drafts action will call a Pythonista script to document the closure and calculate how long the task has been open.

![](http://share.mygeekdaddy.me/_img_BLOGX_Automated_Task_Logger_R2_2014_07_25_210653.png)

[Install Close Work Log Action](drafts://x-callback-url/import_action?type=URL&name=Close%20Work%20Log&url=pythonista%3A%2F%2FstopTimer%3Faction%3Drun)

**WorkLog_Entry:** This is the action that appends the `WorkLogFile.md` file with the task description and the start time. This action is what is called on from Pythonista from the _New Work Log_ action.

![](http://share.mygeekdaddy.me/_img_BLOGX_Automated_Task_Logger_R2_2014_07_25_211320.png)

[Install WorkLog Entry Action](drafts://x-callback-url/import_action?type=dropbox&name=WorkLog_Entry&path=%2FApps%2FWorkLog%2F&filenametype=2&filename=WorkLogFile&ext=md&writetype=2&template=%5B%5Bdraft%5D%5D%20started%20at%20%5B%5Bdate%7C%25Y-%25m-%25d%20%25I%3A%25M%20%25p%5D%5D)

**WorkLog Closure:** This action documents the closure details of the current task. This action is called from stopTimer script called from the _Close Work Log_ action.

![](http://share.mygeekdaddy.me/_img_BLOGX_Automated_Task_Logger_R2_2014_07_25_211339.png)

[Install WorkLog Closure Action](drafts://x-callback-url/import_action?type=dropbox&name=WorkLog%20Closure&path=%2FApps%2FWorkLog%2F&filenametype=2&filename=WorkLogFile&ext=md&writetype=2&template=%5B%5Bdraft%5D%5D)

#### Pythonista Scripts:

**startTimer.py:** This script will document the time the work task began, create a temporary 'timer.txt' file, and then return to Drafts. In the event the timer was already started on a different task it will alert the user and then return to Drafts.

```python
# startTimer.py - writes epoch time to text file for work log

# by: Jason Verly

# rev date: 2014-07-25

import time

import console

import os

import os.path

import clipboard

import webbrowser

import urllib

if os.path.isfile('timer.txt'):

console.clear()

console.hud_alert('File exists', 'error')

webbrowser.open('drafts://')

else:

console.clear()

curDate = time.time()

f = open('timer.txt', 'w')

f.write(str(curDate))

f.close()

console.hud_alert('Timer started','success')

worklogtext = clipboard.get() 

encodetxt = urllib.quote(worklogtext, safe='')

draft_url = 'drafts://x-callback-url/create?text='

action = '&action%3DWorkLog_Entry&afterSuccess%3DDelete'

webbrowser.open(draft_url + encodetxt + action)
```

**stopTimer.py:** This script will document the end of the work task, calculate how long the task was open, and then return to Drafts to append the `WorkFlowFile.md` file.

### Putting it all together

Now with the actions in place, I can go on my iOS device and start a task log entry

In the event I've already started the timer for a work log, I would get an error from Pythonista.

#### Comments from original WP Post:

**[Michael](http://mygeekdaddy.net/2014/07/26/work-log-tracking-on-mac-ios/):** Very cool.
