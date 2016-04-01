# coding: utf-8
import clipboard
import console
import urllib
import webbrowser

addnew = 'taskmator://x-callback-url/add?title='

addtime = '&secslater='

newtask = console.input_alert('First Task', 'Type your reminder below')

newtime = console.input_alert('When?', '3600 for 1 hour, 1800 for 30 minutes, 300 for 5')

seqtask = console.input_alert('What next?', 'Type your reminder below')

seqtime = console.input_alert('Second Task?', '3600 for 1 hour, 1800 for 30 minutes, 300 for 5')

secondR = urllib.quote(seqtask, safe='')

newlink = 'taskmator://x-callback-url/add?title=' + secondR + '&secslater=' + seqtime

encoded = newtask + ' ' + newlink

text = urllib.quote(encoded, safe='')

openDue = addnew + text + addtime + newtime

webbrowser.open(openDue)