# Pythonista 101: Building Blocks

_Captured: 2015-09-29 at 00:06 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/pythonista-101-building-blocks/)_

![Pythonista 101: Building Blocks](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130613-Header-Img.jpg)

If you've been with us since the beginning of Pythonista 101, you know that we've covered quite a bit of ground. Going from simply installing the app, navigating around the potentially intimidating interface, and even installing some scripts we found on the web. Then we graduated to breaking down those scripts we found, and making some modifications to them.

Well now it's time to graduate even further, and look at where the real power and potential in Pythonista comes from: modules.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## What Exactly _Are_ Modules?

Modules seem like special, magical little things that expand the capabilities of Pythonista and the scripts you write. That's really only half true. Yes, modules expand what you can do with Python, but they're not magical or unknowable.

The Python community as a whole discourages code that's indecipherable or behaves without a logical explanation. Code like that is often deemed "magical". Modules aren't like that. They're simply scripts by a different name. Modules solve the problem of how to reuse code from one project to another. Developers try to be as efficient as possible, so when they write something once, it's considered best practice to write it in such a way that it can be easily used later.

That's what modules do. The features you're calling with things like "module_name.feature" are really functions contained within the module. So don't be afraid of modules or think they're unexplainable. Think of them instead as a gigantic library of scripts full of useful functions you get to leverage in the scripts you write.

The modules found in Pythonista are baked into the app by the developer, and he's done a fine job of offering a wide array of features and functionality. The module library is also continuing to grow with each update to Pythonista. Lets look at some of these modules and what you can do with them.

## Module Review

### calendar

Designed to output a calendar, the _calendar_ function also contains other useful functions related to the calendar. I'll be the first one to admit that dealing with dates and time within programming can be tricky. But the simplicity of this is cool:

`import calendar  
c = calendar.TextCalendar(calendar.SUNDAY)  
c.prmonth(2012, 4)`

That prints a plaintext calendar to the console, the days of the week perfectly lined up with the number for each day. It's pretty neat. Try running the code above and you'll see what I mean.

### canvas

Programmatically draw shapes and lines. Maybe I simplified things down too much with that definition, but that is what the _canvas_ module lets you do. There's tremendous power in this though, and also the chance for a lot of complexity.

Take a look at what these 15 lines can produce:

`import canvas  
w = h = 512  
canvas.set_size(w, h)  
canvas.move_to(w*0.45, h*0.1)  
canvas.add_line(w_0.8, h_0.55)  
canvas.add_line(w*0.55, h*0.65)  
canvas.add_line(w_0.65, h_0.85)  
canvas.add_line(w*0.3, h*0.55)  
canvas.add_line(w_0.55, h_0.45)  
canvas.close_path()  
canvas.set_line_width(3)  
canvas.draw_path()  
canvas.fill_path()`

Look familiar? That's right, it's the AppStorm logo! Drawn in 15 lines of Python code.

### console

This is an important module to learn about. The _console_ is the environment you output your code to in Pythonista. But there's more to the _console_ than simply a place to spit plain text messages out to.

**console.set_font**  
Lets you change the font being used to something else for the duration of your script. For a full list of what fonts are available and what their proper names are on iOS, I recommend visiting [iOSFonts.com](http://iosfonts.com/).

**console.alert**  
This is a cool one, _console.alert_ lets you prompt the user with a dialog box containing up to 3 different buttons. You can then read the response back into your code and act accordingly within your script.

**console.show_activity_** and **console.hideactivity**  
These two work in conjunction to show and hide the network activity indicator. In case you aren't sure what that is, it's the little spinning circle that appears up in the top left hand corner of the iOS status bar. Cool thing to have control over, right? So if your script is accessing the Web for anything you can throw that activity indicator up there and let your users know that.

**console.write_link**  
Rather than outputting a URL which then would need to be selected, copied, and pasted into your browser, this function lets you right a tappable link to the console. What adds to the fun is that this doesn't need to be an HTTP URL, it could be a URL scheme which launches another app.

### csv

Perhaps you're unfamiliar with the term CSV, or Comma Separated Values, but it's a generic, plaintext format for displaying tables of data. Nearly every database and every spreadsheet program, including Excel, supports the CSV format for both importing and exporting data. If you're unfamiliar with what type of delimiter is used, that's no problem. The _csv_ module has a built-in function which examines the contents of the CSV file and determines how to interpret it.

If you have databases or spreadsheets of information you'd like to manipulate, the _csv_ module is the place to do it.

### dropbox

I could write an entire series of articles just about the _dropbox_ module, and if you're interested in one, sound off in the comments. The _dropbox_ module contain's three main parts: the _DropboxSession_, _DropboxClient_, and _REST Client_. The _REST Client_ shouldn't really be need be accessed by you when trying to manipulate Dropbox. Instead, it's the combination of a _DropboxSession_ with the _DropboxClient_ functions that lets you do all the things you want to.

Something important to keep in mind is that for the _Dropbox_ module to work, to be able to create a _DropboxSession_, you need to be registered with Dropbox as a developer and have the necessary tokens. If you have no idea what I'm talking about, then give the [Dropbox developer documentation](https://www.dropbox.com/developers/reference) a read, as well as the [Pythonista Dropbox module documentation](http://omz-software.com/pythonista/docs/ios/dropbox.html).

## And We're Just Getting Started…

Ok, so there's a brief overview of five of the modules found in Pythonista. But we're not done. We've only scratched the surface of what Pythonista is capable of. Next time we'll look at even more modules, and look at some ways we can pull these modules together to accomplish some useful tasks.
