from __future__ import print_function
import clipboard
import console
import webbrowser

mytext = clipboard.get()
mytext = mytext.replace('https://twitter.com/', 'tweetbot://')
mytext = mytext.replace('statuses', 'status')
mytext = mytext.replace('http://twitter.com/', 'tweetbot://')
mytext = mytext.replace('http://mobile.twitter.com/', 'tweetbot://')
mytext = mytext.replace('https://mobile.twitter.com/', 'tweetbot://')

console.clear()
print(mytext)

webbrowser.open(mytext)

