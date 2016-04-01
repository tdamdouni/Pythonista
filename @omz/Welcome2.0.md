#  Welcome to Pythonista

Thank you for downloading Pythonista! You now have everything you need to build and run Python scripts directly on your iPhone or iPad. 

To give you an idea of what you can do with the app, various sample scripts are included in the *Examples* folder. Feel free to use them as starting points for your own experiments. To share your creations, get help with coding problems, or just to meet fellow Pythonistas, please visit our [community forum](http://forum.omz-software.com).


#  Getting Started

If you're new to Pythonista, here are some tips to help you get up and running:

*	To create a new script, first tap `≡` to reveal the file browser, then `+` (at the bottom). You can also use left and right swipe gestures to switch between the file browser, editor, and console panels.

*	The settings ("gear" button in the file browser) contain useful options to customize the editor font, color theme, indentation type (tabs/spaces), and more.

*	Swipe left to show the **console** panel. This is where text output appears, and you can use the prompt at the bottom to evaluate individual lines of Python code directly.

*	You'll also find the included **documentation** in the console panel; simply tap the `(?)` button to open it in a separate tab. Reference documentation is also available while you're editing code -- simply select a word (e.g. a function name), and choose *Help…* from the menu.

*	For easier navigation in long scripts, tap the file name at the top to show a list of classes and functions. This is also where you can rename the current file.

*	A lot of keys in the extra keyboard row have multiple mappings. For example, you can tap and hold the `=` key to insert `!=` more quickly.

*	If you enjoy coding in Pythonista, please consider leaving a rating or review in the App Store. Thank you!


#  What's New in 2.0

## General

*	Pythonista is now compatible with all iOS screen sizes -- from iPhone 4 to iPad Pro, and everything in-between.

*	For larger projects, you can now use multiple editor tabs to switch between related files more quickly.

*	The Pythonista app extension allows you to run Python scripts directly within other apps, using the standard iOS share sheet. Depending on the context, you can use the new `appex` module to access data that was passed to the share sheet, e.g. images in the Photos app, URLs in Safari, text in Notes, etc. The app extension also provides an interactive console and a basic code editor for small tweaks.

*	New and refined color themes are available in the settings; selecting a different theme now changes the entire app's UI instead of just syntax highlighting.

*	The file browser and editor have much better support for non-Python files. HTML, CSS, JavaScript, and Markdown files are syntax-highlighted in the editor, Zip archives can be extracted, and a QuickLook preview is available for most common file types, e.g. images, PDFs, and audio/video.

*	Additional templates are available in the improved "new file" menu. You can also import photos from your camera roll as image files there.

*	The console's interactive prompt is now syntax-highlighted, and provides better support for Bluetooth keyboards (you can use the up/down keys to navigate the command history).

*	You can now read the (pure Python) source code of the included standard library (and third-party modules) directly in the app. Simply enable the "Show Standard Library" setting if you're interested in looking "under the hood".

*	The UI editor contains a much improved inspector panel, undo/redo support, the possibility to set custom attributes, and a lot of other refinements.

*	On the iPad, the console panel has a new "sidebar" mode that allows you to keep it visible while using the editor.

## Code Editor

*	The new traceback navigator allows you to get a lot more information about errors in your programs. When an exception occurs, a brief summary is shown at the top of the screen, and the line where the exception occurred is highlighted in the editor. By tapping on the exception summary, you can navigate the entire traceback, even if the source of the exception is in a different file. You can also tap the `<...` marker in the editor to inspect variable values in the selected stack frame.

*	The editor actions ("wrench") menu has been improved significantly. You can now assign custom icons and colors to your script shortcuts. It's also possible to invoke the standard iOS share sheet from the actions menu. If you have an iPhone 6s or 6s Plus (with 3D Touch), you can launch shortcuts directly from the homescreen by pressing the Pythonista icon.

*	The improved asset picker (`[+]` button) contains more free image and sound effect collections that can be used with the `scene`, `ui`, and `sound` modules. The UI for opening the asset picker is also consistent between iPad and iPhone now.

*	When the cursor is inside a color string (e.g. '#ff0000' or 'red') or built-in image name, a preview overlay is shown automatically. You can also tap the preview overlay to select a different color or image.

*	The new *Highlight All* option in the copy/paste menu allows you to quickly find all occurrences of a word (e.g. variable name), without typing anything in the search bar.

*	You can adjust the indentation of a selected block of code more easily with the new `⇥ Indent` menu items (in the copy/paste menu).

*	iPad only: The extended keyboard has a more compact layout by default. If you prefer a larger keyboard with an additional number row, you can enable this in the settings.

## Python / Modules

*	The completely revamped `scene` module gives you a lot more possibilities for building 2D games and animations in Pythonista. You can even use custom OpenGL fragment shaders. Lots of new sample code and a tutorial for building a simple game are available in the included *Examples* folder.

*	The `ctypes` module from the standard library is finally available in Pythonista, and the custom `objc_util` module uses this as the foundation for an Objective-C bridge that makes it possible to call native APIs using familiar Python syntax. A few sample scripts are included in the *Examples* folder.

*	You can customize the startup process of the Python interpreter by creating a file named "pythonista_startup.py" in the site-packages folder. When the app is launched, the interpreter will execute this module, so that all variables/functions/classes in the script become available globally. A common use case might be `from math import *` (if you want to use the console as a calculator). Note: If Pythonista becomes unusable due to a misbehaving startup script, you can launch the app in a "clean" state by entering `pythonista://` in Safari's address field.


# Feedback

I hope you enjoy coding in Pythonista. If you have any feedback, please send an email to <pythonista@omz-software.com>, or visit the [community forum][forum] to share code and get help with your programming questions. You can also find me on Twitter:[@olemoritz][twitter].

---

[forum]: https://forum.omz-software.com
[twitter]: http://twitter.com/olemoritz
