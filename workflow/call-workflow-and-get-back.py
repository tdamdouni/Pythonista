https://github.com/humberry/Workflow

import webbrowser
import clipboard
import time

text = 'empty'
clipboard.set(text)
webbrowser.open('workflow://x-callback-url/run-workflow?name=workflow-script&x-success=pythonista://')

while text == 'empty':
  text = clipboard.get()
  time.sleep(0.3)
if text == '':
    print 'No text in clipboard'
else:
    print text

#Workflow:
#Text (e.g. This text is for Pythonista.)
#Copy To Clipboard
