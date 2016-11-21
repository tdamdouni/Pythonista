# http://unapologetic.io/posts/2014/01/20/time-delaying-url-actions/

import sys
import notification
import webbrowser
import console
import urllib

# Receive parameters from Drafts or Launch Center Pro and assign them to variables.
text = sys.argv[1]
action = sys.argv[2]
delay = sys.argv[3]

# Convert delay time into hours.
hours = float(delay) * 3600

# Encode action and text so they can bed used in URL action.
encoded_action = action.encode('utf-8')
encoded_action = urllib.quote(encoded_action, safe='')

encoded_text = text.encode('utf-8')
encoded_text = urllib.quote(encoded_text, safe='')

# Create URL. You can change this from a Drafts action to be something else if it better fits your needs.
url = 'drafts4://x-callback-url/create?text=' + encoded_text + '&action=' + encoded_action

# Schedule notification.
scheduled = notification.schedule('Run ' + action + ' on "' + text + '"', hours, 'default', url)

# Append text for action and what action was run on it to a file called "Scheduled Actions" in Pythonista.
scheduled_actions = open('Scheduled Actions', 'a')
scheduled_actions.write(action + ' on "' + text + '"\n')
scheduled_actions.close()

# Return you to source app after action is scheduled. (Delete these last lines to just stay in Pythonista.)
#webbrowser.open('launchpro://')
webbrowser.open('drafts://')
# Uncomment line 35 and comment line 34 to open Drafts after success instead of Launch Center Pro.

