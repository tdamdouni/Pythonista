# https://forum.omz-software.com/topic/1918/using-workflow-app-with-pythonista/11

# coding: utf-8

import sys
import console
import clipboard
import webbrowser

console.alert('argv', sys.argv.__str__(), 'OK')
clipboard.set('here is some output!')
webbrowser.open('workflow://')

#Hey there - this is Ari, one of the creators of Workflow. Awesome that you all are trying to get this to work!

#Workflow should work great with Pythonista, but as some of you mentioned, there is currently an issue which prevents Workflow's Pythonista action from working correctly. This will be fixed in an update this week! Once the update is out, here is the general process I've used for integrating workflows with Pythonista scripts:

#Make a new workflow with some sort of content to be passed to the Pythonista script. For example, maybe a Text action. Then add Run Script and Get Clipboard.

#Make a corresponding Pythonista script and put its name into the Run Script action in your workflow. Start with this as your python script:

#import sys
#import console
#import clipboard
#import webbrowser

#console.alert('argv', sys.argv.__str__(), 'OK')
#clipboard.set('here is some output!')
#webbrowser.open('workflow://')

#This example shows how Workflow can provide input to the Python script (in this case, the Python script will show its input as an alert), and how the Python script can pass output back to Workflow via the clipboard.

#(Optionally, you could preserve the clipboard by backing it up when running the workflow. At the beginning of your workflow, add Get Cilpboard and Set Variable, and give the variable a name. Then, at the end of the workflow, add Get Variable followed by Set Clipboard.)