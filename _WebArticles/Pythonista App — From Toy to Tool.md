# Pythonista App — From Toy to Tool

_Captured: 2015-11-16 at 00:38 from [www.macdrifter.com](http://www.macdrifter.com/2012/07/pythonista-app-from-toy-to-tool.html)_

[The Pythonista app for iPad](http://click.linksynergy.com/fs-bin/stat?id=Ssqi/JNIy7o&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Fapp%252Fpythonista%252Fid528579881%253Fmt%253D8%2526uo%253D4%2526partnerId%253D30) is a Python interpreter for iOS.[1](http://www.macdrifter.com/2012/07/pythonista-app-from-toy-to-tool.html) I have used and the Python for iOS and it is a nice facsimile of running Python on a Mac. But Pythonista is more than a Python interpreter.

### Background

I've used the [Python for iOS app on my iPad](http://click.linksynergy.com/fs-bin/stat?id=Ssqi/JNIy7o&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Fapp%252Fpython-for-ios%252Fid485729872%253Fmt%253D8%2526uo%253D4%2526partnerId%253D30). It's a solid iOS app that does one thing well. It allows me to work with core Python modules and run them. It has one major blind-spot though: No clipboard. That's right, there is no way to get a result out of the app and put it on the clipboard. This is because iOS prohibits the use of the `subprocess` module which is available on the Mac to access the pasteboard. I understand the OS limitation but the lack of clipboard support was maddening. I still fiddle with code on the app but that's about all it is good for.

### Enter Pythonista

Pythonista is developed by Ole Zorn, maker of [NewsRack for iOS](http://click.linksynergy.com/fs-bin/stat?id=Ssqi/JNIy7o&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Fapp%252Fnewsrack%252Fid288815275%253Fmt%253D8%2526uo%253D4%2526partnerId%253D30), and it is designed to be more than a Python app on iOS. It's designed to **build** iOS apps in Python on iOS. Pythonista comes with some custom libraries for on-screen drawing, audio and touch interactions, and it's pretty amazing.

### The Design

Pythonista is an attractive app. There are all of the subtle shading and non-standard UI controls that I expect in a premium iOS app. A lot of thought has gone into this application and it shows. The extra keyboard rows for code editing, the library of scripts, even the documentation have all received the attention of a designer.

For example, the documentation is available at any time while composing code. The docs are attractive and easy to use. The current position in the documentation saved when returning to the editor so I was able to quickly jump back and forth while working.

![Documentation Browser](http://www.macdrifter.com/uploads/2012/07/2012-07-14%2018.11.51_600px.png)

> _Documentation Browser_

### The Editor

The keyboard is a standard code-editing variant with two rows of additional keys for the more unique functions required for writing Python. There's a lot to like about the editor. For example, there is optional code completion and auto pairing. Each of these features are implemented with style. The code completion is a translucent set of buttons that hover just out of the way. The list of completions change as the function name is typed out.

![Code Completion](http://www.macdrifter.com/uploads/2012/07/PyAutoComplete.png)

> _Code Completion_

The editor also incorporates gesture controls. Slide a finger on the programming key rows to move the cursor horizontally. To switch between the code editor and the output console screen, just drag the vertical divider at the edge of the screen to reveal the other mode. The effect is smooth and satisfying.

The Pythonista editor has plenty of support for those of us that are not experienced Python developers. I really appreciated the easy onscreen documentation. Double tapping on a Class or Method name presents a popover of the documentation for quick reference. Tapping the expand-icon switches to the full documentation viewer for more lengthy research.

![Function Documentation](http://www.macdrifter.com/uploads/2012/07/PyFuncHelp.png)

> _Function Documentation_

While there is no in-editor search function, there is a handy document browser that shows class and method names in a pop-over outline.

![Document Map](http://www.macdrifter.com/uploads/2012/07/PyDocBrowser.png)

> _Document Map_

The entire application is pleasing to the eye and that includes the editor. The editor has several color schemes available. Each one is attractive and the styled text is Retina quality. There's not a lot of tweaking, but I found the included color schemes to be sufficient. Font and font size can be adjusted in the settings window.

![Style Themes](http://www.macdrifter.com/uploads/2012/07/PytThemeStyle.png)

> _Style Themes_

### The Console

The console is where all the action happens. All of the script results are displayed in the console and users interact with the results through touch or the console entry line.

![Script Console](http://www.macdrifter.com/uploads/2012/07/2012-07-14%2018.07.54_600px.png)

> _Script Console_

The console is not a dead-end. Text can be selected and copied. Images can be copied or saved to the camera roll. For example, here is the results of one of the demo scripts that comes with Pythonista:

![Image Export](http://www.macdrifter.com/uploads/2012/07/2012-07-14%2019.54.49_600px.png)

> _Image Export_

### Document Management

The document library is easy to navigate _when there are only a few scripts_. There are no folders or hierarchy to the library. Each script is presented in a alphabetical grid. This is fine in the beginning but will be a major nuisance for anyone with a large collection of scripts. The thumbnails are nice, but superfluous. I can see a small portion of easy script in the thumbnail, but that does not provide much help when I'm hunting for a particular script.

![Document Library](http://www.macdrifter.com/uploads/2012/07/2012-07-14%2018.08.25_600px.png)

> _Document Library_

### True Power

Pythonista's extra libraries are impressive. The clipboard module alone is a huge bonus. It provides a few crucial methods for reading and writing to the iOS clipboard. But Pythonista is intended to be a development environment for making graphical touch enabled apps. To that end they include several modules directed at drawing on screen, styling text and objects, and generating audio.

![iOS Modules](http://www.macdrifter.com/uploads/2012/07/PyiOSMethods.png)

> _iOS Modules_

While editing an additional object manager option appears in the upper right corner of the editor. Pythonista comes with a small library of images but new images can be added through pasting into an image palette in the editor. There is also a handy color and font picker available.

![](http://www.macdrifter.com/uploads/2012/07/PyImageLibrary.png)

Pythonista ships with some impressive demos of touch controlled games, graphing tools and piano simulators. Unfortunately I do not have the use-case, desire or skill to travel that road. I appreciate that someone _could_ use this app to make an impressive new app.

### The Bad

It's not all peaches and cream with Pythonista. There are some very minor rough edges. For example, there is no way to load external modules into the app. This is likely due to Apple's rules about side loading new code into an app. This stymies any effort to use `easy_install` or `pip`. However, I would love to see an option for loading the module in through Dropbox. I'd be happy to unpack the Markdown, WordPress or Pinboard Python modules and upload them to Dropbox if it meant I could import them into my scripts.

There are a few other minor issues with the app that I would like to see fixed.

  1. There is no search function within a script. Search is only available in the docs.
  2. There is no documentation for the app. There is plenty of Python documentation, but nothing about the app features.
  3. No Dropbox support. Shouldn't every document based app provide Dropbox support out of the gate?
  4. No TextExpander support. It's not a huge issue but would be a nice addition.

I want to give credit where it is due. **_This is a 1.0 version_** and it is mighty impressive. The rough edges are minor when I consider what a great first version this is.

### Example

Of course I have been putting Pythonista through its paces. It's a fun app to work in and it is also a handy tool on my iPad.

Here's a quick example I put together for formatting text blocks. This script grabs some text off of the clipboard when the script is run. The user is then asked for one of several methods for formatting the text. The result of the script is pushed back onto the clipboard ready for use somewhere else.

Here's the script:
    
    
    import sys
    import re
    import urllib
    import clipboard
    
    def titleCase(s):
        newText = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),s)
        return newText
    
    print "Convert to:"
    print "[1] Title Case"
    print "[2] lowercase"
    print "[3] UPPERCASE"
    print "[4] Capital case"
    print "[5] Strip Leading"
    print "[6] Strip Trailing"
    print "[7] Strip All"
    print "[8] URL Quote"
    print "[x] Exit"
    
    formatType = raw_input("Select Conversion: ")
    if formatType == "x":
        print "Exited"
    else:
    
        #userInput = getClipboardData()
            userInput = clipboard.get()
    
        #userInput = raw_input("Input String: ")
            print "\n\n"
    
    if formatType == "1":
        outString =  titleCase(userInput)
    elif formatType == "2":
        outString = userInput.lower()
    elif formatType == "3":
        outString = userInput.upper()
    elif formatType == "4":
        outString = userInput.capitalize()
    elif formatType == "5":
        outString = userInput.lstrip()
    elif formatType == "7":
        outString = userInput.strip()
    elif formatType == "8":
        outString = urllib.quote(userInput)
    print outString
    print "\nThe text was copied to the clipboard"
    clipboard.set(outString)
    

Here's what a typical console session looks like in Pythonista:

![Example Script Results](http://www.macdrifter.com/uploads/2012/07/2012-07-14%2018.25.17_600px.png)

> _Example Script Results_

### Conclusion

Pythonista was made for someone else. It's made for someone that wants to do amazing things with Python on an iPad. But I get to take advantage of all of their hardwork. I get a Python tool that, while not perfect, is extremely powerful. I'll probably never use the canvas and touch modules but damn do I like the clipboard module. **This is a must- have app for anyone that works in Python.**

[Pythonista](http://click.linksynergy.com/fs-bin/stat?id=Ssqi/JNIy7o&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Fapp%252Fpythonista%252Fid528579881%253Fmt%253D8%2526uo%253D4%2526partnerId%253D30) | $5 | iPad Only
