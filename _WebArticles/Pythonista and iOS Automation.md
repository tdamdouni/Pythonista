# Pythonista and iOS Automation

_Captured: 2015-09-30 at 18:13 from [randomfoo.net](http://randomfoo.net/2013/12/08/pythonista-and-ios-automation)_

While in general, iOS is pretty nifty, it has [some pretty annoying limitations](https://randomfoo.hackpad.com/iOS-vs-Android-dvwRU1OkJYr), particularly in regards to inter-app communications (more specifically, the lack thereof). While [Pythonista](http://omz-software.com/pythonista/) doesn't complete fix this terrible situation, it does provide some really interesting workarounds.

I'd heard of Pythonista when it first launched, but mostly ignored it since it just seemed like just another Python REPL. Now, it **is** a Python REPL (2.7) and editor, and it also includes its own 2D graphics and multitouch libs so you can make simple interactive apps with it. Where it starts to get really interesting is that it also includes a [bunch of modules](http://omz-software.com/pythonista/docs/ios/), that exposes the iOS [clipboard](http://omz-software.com/pythonista/docs/ios/clipboard.html), [contacts](http://omz-software.com/pythonista/docs/ios/contacts.html), location, notifications, etc.

Mostly importantly, it has urllib and webbrowser module support that supports [iOS URL callbacks](https://developer.apple.com/library/ios/DOCUMENTATION/iPhone/Conceptual/iPhoneOSProgrammingGuide/AdvancedAppTricks/AdvancedAppTricks.html#//apple_ref/doc/uid/TP40007072-CH7-SW18). Pythonista itself supports [its own URL scheme](http://omz-software.com/pythonista/docs/ios/urlscheme.html) of course, lending itself to being called remotely.

Another useful app to use in conjunction with Pythonista is [Agile Tortoise's Drafts](http://agiletortoise.com/drafts/). It's a text editor built specifically to interface with other apps and can serve as an easy briding tool.

There are a fair number of tutorials/guides/scripts available online.

First, some general reference:

  * [Automating iOS: How Pythonista Changed My Workflow](http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/) - a very good intro of what Pythonista can do
  * [Pythonista Modules](http://omz-software.com/pythonista/docs/ios/)
  * [handleOpenURL](http://handleopenurl.com/) - comprehensive list of iOS URL schemes. [This wiki page](http://wiki.akosma.com/IPhone_URL_Schemes) is also a useful list w/ examples
  * [x-callback-url interfaces](http://x-callback-url.com/apps/) - [x-callback-url](http://x-callback-url.com/) is used by many apps and is designed to help standardize IPC w/ result codes, etc
  * [omz:software Pythonista Forum](http://omz-forums.appspot.com/pythonista) - official forum

And some useful scripts:

  * [New from Gist.py](https://gist.github.com/omz/4076735) - this script will make it easier to copy scripts into Pythonista (iOS has restrictions on being able to sync/pull in interpreted code, so Pythonista does not have Dropbox or other syncing built in). Be sure to take a look at all of [omz's gists](https://gist.github.com/omz) for some really useful examples (like [how to install modules](https://gist.github.com/omz/7087359) or a [simple shell](https://gist.github.com/omz/4066688))
  * [pipista](https://gist.github.com/pudquick/4116558), [pipist 2.0](https://gist.github.com/pudquick/4317095) - you can use this script to easily install modules from the pypi repository. Save as 'pipista.py' and run like so:  


> `import pipista  
import pipista.pypi_install('tornado')  
`

  * [Pypi.py](https://gist.github.com/anonymous/5243199) - another similar installer script ([forum post](http://omz-forums.appspot.com/pythonista/post/4608963765075968))
  * [Quickly Import Pythonista Scripts via TextExpander or Bookmarklet](http://n8henrie.com/2013/02/quickly-import-pythonista-scripts-via-textexpander-or-bookmarklet/) - noticing a trend? This should be plenty for getting scripts into Pythonista
  * [Pythonista 101: The Scripting Community](http://ipad.appstorm.net/how-to/utilities/pythonista-101-the-scripting-community/) - includes links to lots of scripts

Specific HOWTOs:

  * [noDoze.py](https://gist.github.com/cclauss/6383054) - for keeping iOS device from sleeping
  * [Dropbox syncing](http://omz-forums.appspot.com/pythonista/post/6675908186341376) (see also [DroboxySync.py](https://gist.github.com/herbmann/5347372)
  * [exiting Pythonista programmatically](http://omz-forums.appspot.com/pythonista/post/6357874448007168) - currently not possible
  * [SimpleHTTPServer](http://omz-forums.appspot.com/pythonista/post/5636697899401216) - template for running a custom webapp
