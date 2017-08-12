# Pythonista Review – Programming iOS with Python for iPad iPhone

_Captured: 2015-11-14 at 10:27 from [www.jackenhack.com](http://www.jackenhack.com/scripting-programming-iphone-ipad-python-pythonista-review/)_

![Pythonista icon](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_icon.jpg)

> _Pythonista icon_

## Pythonista, finally programming workflow automation for iOS?

I'm doing most of my writing on my iPad or occasionally on my iPhone, and I write everything in [Markdown](http://daringfireball.net/projects/markdown/). There are some great scripts in my current favorite language **Python** out there for doing **Markdown** conversions, image manipulations etc, but unfortunately Apples rules regarding programming apps on **iOS** devices are pretty stringent. But an app for programming Python on iOS called [Pythonista](http://www.jackenhack.com/go/pythonista-python-ios/) have some smart ways of getting around some of Apples restrictions. And one of the nice things you can do is home screen shortcuts, making your scripts available directly from your home screen of your iOS device. All you have to do to [create a **Pythonista** home screen shortcut](http://omz-software.com/pythonista/shortcut/) is to go to a web page and enter the script name and optional arguments. After that, just add the page home-screen with Safari's bookmarks button. Another way of starting your scripts is directly as bookmarks in Safari or other web browser.  
I found the app from this [article about making life easier by scripting with **Pythonista**](http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/), a great read of all the functions available in the app.

Because they added a Python library for managing the clipboard, you can copy pictures or text to it, then start your script that reads from the clipboard and then put the new modified text/picture back to the clipboard, ready for pasting into any app. Very handy!

## URL Schemes

[Pythonista has an URL Scheme](http://omz-software.com/pythonista/docs/ios/urlscheme.html#pythonista-urlscheme), so it can be called from other programs. This makes it perfect for apps on the iPhone like [Launch Center Pro on iPhone](http://appcubby.com/launch-center/) that supports URL Schemes to start your Python scripts.

With more and more apps supporting [handleOpenURL](http://handleopenurl.com), the things you can do starts to look very handy indeed.

## x-callback-url

Applications that support [the x-callback-url specification](http://x-callback-url.com) makes it possible to send information to one app and get the results back and then continue process it or sending it to yet another app. Hopefully more apps will **support x-callback-url**, but some great ones already do.

  * **Pythonista (of course!)**
  * **Instapaper**
  * **Google Chrome**
  * **Terminology**
  * **Due**
  * **Definition**
  * **Drafts**
  * **Scanner Go**
  * **iCab Mobile**
  * **Phraseology**
  * **iZettle**
  * **Notesy**
  * **Poster**

So far I own **nine** of these applications, **four of them bought just because they support x-callback-url, so listen up developers!**

## Editor

![Pythonista editor completion](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_editor_completion-300x400.jpg)

> _[Pythonista editor completion](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_editor_completion.jpg)_

The editor is a treat to work with! Fast, responsive and very clever. It's really easy to use. Most of my editing has been modifying existing scripts and change them so I can use the clipboard, but I have no problem of seeing someone developing longer programs. There's a built-in interactive prompt where you can try out commands and test. Great for trying out a concept or try to find a bug. It's also handy for people like me who just started to learn Python and need to try out stuff.

## Extended keyboard

![pythonista_extra_keyboard](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_extra_keyboard-600x288.jpg)

There is a great extended keyboard with the most used keys you need when programming Python. You can move the cursor in the text by just sliding your finger from back and forth across the extended part of the keyboard, and the cursor moves accordingly. Very clever!

## Libraries

The standard libraries are included for **Python**, but the developer of **Pythonista** has also created some handy libraries for things specific to the iPhone/iPad

  * **canvas** -- Vector Graphics
  * **clipboard** -- Copy and paste
  * **console** -- Functions for working with the text output and keyboard input
  * **editor** -- Functions for scripting Pythonista's text editor
  * **keychain** -- Secure Password Storage
  * **scene** -- 2D Graphics and Animation
  * **sound** -- Play simple sounds

Other handy libraries that are included are:

  * **bs4** -- BeautifulSoup 4
  * **Dropbox**
  * **feedparser** -- Universal Feed Parser
  * **Markdown**
  * **Python** Imaging Library
  * **Requests** - HTTP for Humans

So there are plenty of libraries available, and more more are coming.

## Documentation

![Pythonista iOS app documention screenshot](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_documentation-300x400.jpg)

> _[Pythonista iOS app documention screenshot](http://www.jackenhack.com/wp-content/uploads/2013/02/pythonista_documentation.jpg)_

The complete documentation for Python and the standard libraries are included in the app. All the information on the graphics library, Dropbox and clipboard library as well.

## Examples

Here you get a couple of examples of how it works and what you can do.

  * [Interactive example of using the built-in web server in Pythonista to create MultiMarkdown tables](https://gist.github.com/mcsquaredjr/4450031).

  * [Here's a github repository with a lot of examples, mostly related to Markdown, but also some with image manipulation](https://github.com/viticci/pythonista-scripts) because **Pythonista** contains not only the standard Python libraries but also the [Python Imaging Library](http://omz-software.com/pythonista/docs/ios/PIL.html), making it excellent for doing automatic image manipulations.

  * [I've written a little snippet for posting directly from Mobile Safari to the Poster app on my iPad or iPhone](http://www.jackenhack.com/blog-post-ios-safari-poster-app-pythonista-script/).

I hate that I can't look at the HTML code when surfing on Mobile Safari, so here's a little script for using Pythonista to display the HTML source, nicely formatted for easier reading.

```python
# A simple script for showing the HTML code of a page directly from mobile Safari.  
# add a bookmark in the browser with the JavaScript code:   
# javascript:window.location='pythonista://showHTML?action=run&argv='+encodeURIComponent(document.location.href);  
#  
# _ _   
# | | | |   
# | | __ _ ___| | _____ _ __   
# _ | |/ _` |/ __| |/ / _ \ '_ \   
# | |__| | (_| | (__| < __/ | | |  
# \\____/ \\__,_|\\___|_|\\_\\___|_| |_|

import sys  
import console  
import urllib  
from bs4 import BeautifulSoup

numArgs = len(sys.argv)  
print numArgs  
if numArgs != 2:  
console.alert('This script needs an URL as an argument.')  
else:  
url = sys.argv[1]  
usock = urllib.urlopen(url)  
data = usock.read()  
usock.close()  
soup = BeautifulSoup(data)  
console.clear()  
print(soup.prettify())
```

## Inconveniences

The major problem I have with the app is the way to import scripts into it. Most of the blame goes to **Apple** for not allowing importing of scripts from **Dropbox** or by other means[[1]](http://www.jackenhack.com/scripting-programming-iphone-ipad-python-pythonista-review/). Apple wants to keep the iOS out of the troubles of malicious code execution, and that's understandable, but the apps are already jailed, so they can't access files outside its own folders. But I guess the more avenues you give for a hacker, bad stuff will happen.

For now, I have a folder in **Dropbox** with the scripts I find or develop on my Mac, and then open them with a text editor app and paste them into **Pythonista**.

It's nice to finally have the ability to script tedious and repetitive tasks on iOS. With more libraries being added, this app will become even more useful. It's also a fun and convenient way of learning **Python**, a really great programming language!
