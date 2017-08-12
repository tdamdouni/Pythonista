# Pythonista 101: Building Blocks – Part Two

_Captured: 2015-09-29 at 00:05 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/pythonista-101-building-blocks-part-two/)_

![Pythonista 101: Building Blocks – Part Two](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/06/130621-Header-Img.jpg)

In the [last Pythonista 101 article](http://ipad.appstorm.net/how-to/utilities/pythonista-101-building-blocks/) we discussed modules. Modules are Python scripts that come bundled with Pythonista giving us access to new and interesting features. Because of the sandboxed nature of iOS, what comes bundled in with apps like Pythonista is really all that we have to work with. When compared with the free reign found on Mac OS X, Linux, and even Windows, this may seem restrictive. Fortunately the developers of Pythonista have done a fantastic job packing as many modules into Pythonista as possible. Today we're going to look over some more, as well as examine some real-world scenarios that Pythonista could assist with.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Module Review

### email

A simple idea, send an email, and yet the _email_ module can get rather complicated pretty quickly. I wouldn't recommend this one to beginners, but the _email_ module allows you to create a properly formatted email message, headers and all, and with the assistance of the _smtplib_ module, send the message as well.

Take a look at [this example script](https://gist.github.com/omz/4073599), written by the creator of Pythonista, to see how the _email_ module is used in practice.

### feedparser

This one may seem like more a niche module, what with people proclaiming the death of RSS and whatnot. In my opinion RSS isn't dying, it's simply dropping underneath new interfaces, becoming the plumbing through which web content flows.

So in that same spirit, having module which lets you manipulate RSS feeds seems rather useful, at least to me.

`  
import feedparser  
d = feedparser.parse('http://daringfireball.net/index.xml')  
print('# %s' % d['feed']['title'])  
print('_%s_' % d['feed']['subtitle'])  
print('- - -')`

`for entry in d['entries'][:10]:  
print(entry['title'])  
print(entry['published'])  
print('- - -')  
`  
This small piece of code takes an RSS feed (in this case from [Daring Fireball](http://daringfireball.net)) and displays some basic feed data as well as the 10 most recent posts.

As a news junkie I really love having such powerful programmatic control over RSS feeds in a simple and easy-to-use tool like Pythonista.

### markdown and markdown2

Markdown has become all the rage these days. With the advent of more capable mobile devices, our content is being spread across these different operating systems and different apps, and the plaintext file format of Markdown is perfect for just that sort of travel.

If you're an iPad power user who's already familiar with what Markdown is so good for, then Pythonista can add a nice new set of tools at your disposal. Coupling the _markdown_ module's conversion abilities with some of the other modules like the _dropbox_ one, and you can create some automated tools to speed up any writer's workflow.

The _markdown2_ module is very similar to the _markdown_ module, just with a few extra items supported through new syntaxes. Feel free to [refer to the documentation](http://omz-software.com/pythonista/docs/ios/markdown2.html) for specifics on what extras are included and how to make use of them.

### notification

I got really excited the first time I saw this module. This might be my personal favorite when it comes to sparking the imagination. The _notification_ module lets you schedule notifications to go off after a set delay, as well as giving you options to set a sound to play and a URL which is triggered when the notification is activated, such as when it's tapped in Notification Center. Something important to note is that the notification _will_ trigger even without the script, or even the app as whole, running.

### os

This one is for all you Linux/Unix geeks out there. The _os_ module contains a lot of miscellaneous functions that are usually of the most interest to sysadmins and such. Having that kind of capability on an iOS device is rather unprecedented, and can be useful when trying to solve some problems with code. Again, my suggestion is to skim over the [documentation](http://omz-software.com/pythonista/docs/library/os.html#module-os) if you're curious about all that _os_ has to offer.

### photos

This one is quite tailored to the iOS experience, though it ties in closely to the Python Image Library modules mentioned earlier. The _photos_ module is what lets you use photos from the Camera Roll or even lets you activate the OS-level Camera app. The image returned is compatible with any of the PIL modules and can be further processed from there.

### PIL, Python Image Library

Where to begin with the _Image_ and related modules? There is truly a tremendous amount that can be done with this module. These 11 modules are a part of the Python Image Library, and give Pythonista control over a wide range of image-related tasks. An entire series could be written just about these modules alone, and if that's something you'd be interested in then say so in the comments section below.

For now, suffice it to say that everything from basic image manipulation to rendering different built-in system fonts is covered within these modules.

### sqlite3

Another module with an incredible amount of power and potential, but which really needs to be coupled with another module or two in order to really shine. The _sqlite3_ module gives standard database access via Pythonista. That may not sound all that useful at first, but the more you think about the ability to access and update a SQL database located on something like Dropbox, or that can be downloaded from somewhere and then reuploaded, all while you're on _your iPad_. Sounds cool, doesn't it?

### urllib

When you want to get something from off the web, the _urllib_ module is the way to get it. But this module does more than simply download resources. It also includes _urlencode()_ functions which take a list of parameters and properly escape and format them to be appended to a URL and used with either a GET or a PUT request. So using Pythonista you can automate web requests and even submit form programmatically.

### urlparse

This module almost feels a bit magical the first time you use it, because it takes something we're all very familiar with, a URL, and then slices it into all the right pieces.

`  
from urlparse import urlparse  
url = urlparse('http://ipad.appstorm.net/how-to/utilities/pythonista-101-building-blocks/')  
print(url)  
`

And just like that you have a delightfully parsed URL. The result looks like this:  
`  
ParseResult(scheme='http', netloc='ipad.appstorm.net', path='/how-to/utilities/pythonista-101-building-blocks/', params='', query='', fragment='')  
`

### webbrowser

The name really says it all, the _webbrowser_ module lets you open a URL inside a built-in web browser. A handy feature when you think about combining it with any of the URL modules we just mentioned. Something to note is that this is a pared-down version of the full Python _webbrowser_ module. So refer to [the Pythonista documentation](http://omz-software.com/pythonista/docs/library/webbrowser.html#module-webbrowser) and not some other docs you may find online.

## Real-World Scenarios

After examining some of these modules in a little more depth, I hope you have a better appreciation of the wide array of tasks that Pythonista can accomplish. For instance:

  * **Markdown to HTML with built-in Preview** -- by combining the _markdown_ module with the _webbrowser_ module you could create a script that converted your Markdown docs and let you preview the resulting HTML
  * **Markdown from Dropbox to HTML to Dropbox with built-in Preview** -- then add in the _dropbox_ module to our previous script and you can round-trip text files stored in Dropbox, written in Markdown, converted into HTML, previewed within the web browser, and then saved back into Dropbox
  * **Convert CSV files from Dropbox into a SQLite Database in Dropbox** -- if you remember the _csv_ module from [the last Pythonista 101 article](http://ipad.appstorm.net/how-to/utilities/pythonista-101-building-blocks/) then you remember that it's a plaintext way of storing tabular data, usually from a spreadsheet app or something similar. Using the _csv_ module and the _sqlite3_ module you could take those data files and store them in a SQLite database which could then be used with a web app or some other piece of software for more robust control over your data.

## The Power Is In Your Hands

So there you have it. After four articles, this Pythonista 101 course has come to an end. I hope you've learned at least a little more about Python as a language or Pythonista as a tool. I'd encourage you to play around with the scripts you can find online or that have been mentioned in this series.

And get ready for the next edition of the Pythonista 101, coming in August.
