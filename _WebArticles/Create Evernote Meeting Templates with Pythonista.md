# Create Evernote Meeting Templates with Pythonista

_Captured: 2015-06-11 at 23:59 from [www.movingelectrons.net](http://www.movingelectrons.net/blog/2013/12/06/create-evernote-meeting-templates-with-pythonista.html)_

[Evernote](http://www.evernote.com) is arguably the best note taking application out there. There are versions for all major operating systems, including mobile ones. I have been an **Evernote** user for more than 5 years now, and I use it for both work related and personal notes.

All my meeting notes end up in Evernote, although I'm careful not to include client/work sensitive information in it. Even though you can encrypt individual notes, I rather keep that information out of the cloud.

## The Problem

Every time I went to a meeting, I ended up retyping the same information inside notes over and over again. You can create Templates in the Desktop versions of Evernote, but they haven't been implemented in the iOS version of the program yet. Additionally, There is no way to create a customized note based on a pre-formatted template.

## The Solution

[Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11lqkH) for iOS is truly an impressive application created by [Ole Zorn](https://twitter.com/olemoritz). In a nutshell, it's a Python interpreter for iOS devices. You can import scripts from GitHub and share yours as well. It includes many key Python libraries and several methods that allow you to interact with the iPhone/iPad.

We are going to use Pythonista to access our Evernote account (internet connection required) and create a meeting template which will be customized based on certain info related to that particular event.

## What Do You Need?

  * An **[Evernote](http://www.evernote.com)** account.
  * **Pythonista** for iOS (link and description below).
  * **Evernote API _in_ Pythonista**. Although installing a Python API can be relatively easy on a desktop OS, it is not as straight forward on iOS. Thankfully, Ole's has put together a [script](http://omz-forums.appspot.com/pythonista/post/5486219425218560) which does just that. 
  * **Evernote Developer Token**. Go [here](https://www.evernote.com/api/DeveloperToken.action) to get your token from Evernote. Keep in mind that the token is usually **good for just on year**, so you will need to get a new one when it expires.
  * **My script**. You can get it [here](http://www.movingelectrons.net/blog/2013/12/06/http://gist:%20https://gist.github.com/Moving-Electrons/7000517)

Pythonista brings the Zen of Python™ to your iPad or iPhone. Create interactive experiments and prototypes using multi-touch, animations, and sound - or just use the interactive prompt as a powerful calculator. Pythonista is also a great tool for learning Python - The interactive prompt helps you explore the language with code completion, the entire documentation is accessible right within the app and you can get started with lots of ready-to-run examples. Features: >>> Full-featured, scriptable code editor with syntax highlighting and code completion >>> Extended keyboard, designed specifically for Python >>> Interactive prompt with code completion and history >>> Complete documentation with quick lookup directly from the editor >>> Multiple color themes for syntax highlighting >>> Includes most of the standard library and additional modules for graphics and sound >>> UI module with visual User Interface Editor >>> Lots of examples included Based on Python 2.7.5; the name "Pythonista" is used with kind permission of the Python Software Foundation.

The script was put together based on [this](http://omz-software.com/pythonista/docs/ios/evernote.html) example in the Pythonista Documentation. I had to dig into Evernote's API to find out how to write a note in a Notebook _different_ from the default one (in the case of my script, it is the **Work** Notebook, but that can be easily modified in the code).

The template generated includes the following fields shown in Evernote Markup Language: Date, Time, Attendance, Objective, Remarks and Action Items.

When run, the script lists all notebooks in a user's account (just as reference), asks for the new note's title (automatically adding the current date at the end in ISO format YYYY-MM-DD), and finally requests the tags to be assigned to the note which will be created in a pre-defined notebook (hard coded in the `ntbkName` variable).

See below a couple of images showing the interaction with the script in the iPad and the final result (click to enlarge).
