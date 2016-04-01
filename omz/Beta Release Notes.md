#  Build 160036

*  iPad: You can now view console output and documentation alongside the editor by using the new "docked" mode of the accessory panel (top-left button in the console).

*  Completely revamped `scene` module, including lots of new sample code.

   While most of the code is completely rewritten, it should be 99% backwards-compatible with the old `scene` module. For new projects, I would recommend using the new `Node`/`Action`-based API instead of implementing a `draw` method though (see documentation). The overall API design is very similar to both the old `scene.Layer` system, and the (now-defunct) `sk` module from previous beta. Unlike `scene.Layer`, it's implemented in native code, and you'll get much better performance as a result. You can also use custom fragment shaders now, which opens up quite a lot of new possibilities for visual effects.

   You'll find quite a few sample scripts that use the new `scene` APIs in the *Animation* and *Games* folders. I also intend to include a tutorial project in the final release, but that's not quite done yet (the game examples are somewhat complex).

*  iPhone 6s/plus: Editor actions can now be used as 3D Touch shortcuts from the homescreen.

*  Lots of new scripts in the Examples folder -- the examples are also organized by category now. If you had a previous beta installed, the old examples are moved to a backup folder (in case you made any changes there).

*  New `sound.set_honors_silent_switch()` function. Note that you need to call this (using `False`) if you want audio to play in the background. The default behavior has changed from previous betas, i.e. it *does* honor the silent switch now (as in 1.5).

*  Improved support for VoiceOver (Note: to access the console panel while VoiceOver is active, use the "magic tap" gesture, i.e. a double-tap with two fingers).

*  Added documentation for `sound.Player` and `sound.MIDIPlayer` (these classes have been there for a while, but they weren't documented before).

*  Some fixes in the `reminders` documentation (`notes` attribute was incorrectly referred to as `title`, and it wasn't clear that a `Calendar` can be used as a parameter when initializing a `Reminder`).

*  Color values in the `scene` and `ui` modules can use CSS-style RGBA strings now (e.g. `'rgba(255, 0, 0, 0.5)'`).

*  A link to the community forum is now shown in new tabs.

*  Fixed: The extended keyboard in the console should work again.


#  Build 160034

*  Improvements for the extended keyboard on iOS 9 (iPad only) -- the primary row of keys is now shown in the shortcut bar, so that the keyboard is smaller overall. I've also tweaked the set of available keys a little bit.

*  Improved support for soft tabs (backspace key and "Indent/dedent selection" should work better).

*  Improved detection of external changes in the editor (when you change a file in the extension or programmatically, its tab should be reloaded automatically).

*  The editor actions (wrench) menu is also available in empty tabs now.

*  When using QuickLook to preview images, the preview now shows other images in the same directory as well (swipe left/right).

*  Zip files are now extracted into a separate folder.

*  Improved support for external keyboard shortcuts (on iOS 9, a list of shortcuts is now shown when holding down the Cmd key)

*  It's easier to insert triple quotes (hold `'` key) -- you can also enclose selected text in triple quotes this way.

*  When adding a new editor action, the current script is now selected by default

*  Added a simple file template for the `scene` module

*  Fixed various crashes when using the `canvas` module.

*  Fixed a potential crash when using `webbrowser.open('safari-http://...')`

*  Fixed rendering of retina images in `scene` module.

*  Fixed `console.write_link()`

*  Added limited support for `console.hud_alert()` in the app extension (`icon` parameter is ignored).

*  Fixed scroll-to-top (status bar tap) on iPhone

*  Fixed: `sys.argv` no longer contains a duplicate script path.

*  Fixed: `ImageFont.truetype` should work again.


#  Build 160033

*  Completely redesigned Editor Actions menu. It didn't really make sense to put script shortcuts (editor actions) into the standard share sheet for a couple of reasons:

   - Editor actions don't necessarily have anything to do with sharing, so using the standard share icon for these was potentially confusing.
   - Not a lot of custom icons fit into the standard share sheet without having to scroll horizontally.
   - The share sheet is somewhat slow to bring up, even on recent hardware.
   - Having to go into settings to add or remove shortcuts was annoying.

   The new UI looks somewhat similar, but it's a bit faster and much more customizable. You can now set a custom icon and color for each script shortcut. Shortcuts can be edited directly, instead of in the settings.

*  Redesigned app extension (similar to the new editor actions panel). You can now view/edit all scripts from the extension, not just the ones in the special "Extension" folder (which doesn't get special treatment anymore).

*  You can now customize the startup process of the interpreter. The basic procedure is to put a file/module named "pythonista_startup.py" into your site-packages folder. When the app is launched, the interpreter will execute this module, so that all variables/functions/classes in the script become available globally. A common use case might be something simple like "from math import *". A few more notes about this:
   - You can print to the console in your startup script (for debugging purposes), but any exceptions will be ignored silently.
   - If you somehow end up with a startup script that causes a crash (making the app unusable), you can force Pythonista to skip the startup script by entering "pythonista://" in Safari. Note that for any other "pythonista://" URLs, the startup script *will* be executed.
   - The mechanism that clears global variables etc. before a script is run (_pythonista_preflight.py if you're curious) will skip any variables that are defined in your startup script, so you can use the startup script to define helper functions etc. that you want to keep around.
   - The startup script will only run when the app is actually launched, not if it's already running in the background when you tap the icon on your homescreen.
   - The startup script will also be executed in the app extension, but not necessarily every time you invoke it (extensions also keep running in the background in some cases). If you want your startup script to behave differently in the app extension, you can use `appex.is_running_extension()` to check which mode you're in.

*  Automatically reloading user-defined modules should be much more reliable. Using the `reload()` function manually should no longer be necessary at all if you develop custom modules that you import elsewhere.

*  Replaced PIL with Pillow -- I've made a minor change to make sure that `import Image` still works (so that old sample code doesn't break), but you should really use `from PIL import Image` for new code instead.

*  When global variables are cleared (before a script is run), variable names that begin with `__` (double underscores) are always skipped now.

*  Properties of `ObjCInstance` objects can now be set more intuitively, using regular attribute access syntax, e.g. `foo.bar = baz` instead of `foo.setBar_(baz)` -- they both do exactly the same thing, but the first variant looks much nicer. Note that *getting* a property value still requires parentheses, i.e. `b = foo.bar()`, *not* `b = foo.bar`. One difference compared to using the setter method directly is that trying to set a property that doesn't exist will not fail with an exception. Instead, `__setattr__` will fall back to setting a regular Python attribute.

*  Fixed: Code completions in the editor were not inserted if you selected them directly after typing the ".".

*  Fixed missing `canvas` module.

*  Added `images2gif` module (for reading/writing animated GIFs).

*  Some minor tweaks in the "Cool Glow" and "Solarized Light" themes.

*  Changed color of the "Open in new tab" swipe action.

*  Fixed incomplete documentation for `dialogs` module.


#  Build 160032

*  The download is quite a bit smaller, mostly due to more code and resources being shared between the app and the extension (as a framework). Another benefit of this is that all the built-in images and sound effects are also available in the extension now.

*  A couple of popovers are modal sheets now ("move files", "add view" etc.) -- I might change this back, it's mostly a quick workaround for some issues on iOS 9.

*  All functions in the `console` and `dialogs` modules should be safe to call from the main thread now. This makes it a lot less error-prone to use these modules in combination with the `ui` module because you can e.g. show a dialog from a button's action without having to decorate it with `@ui.in_background`.

*  Changed the order of `sys.path` once more, so that files in the main documents folder can't shadow standard library modules anymore. Imports from the current directory should also work again.

*  (Hopefully) fixed various crashes with `ctypes` and `objc_util` on iPad Air 2. This affected all things involving callback functions, most notably `on_main_thread()`, `create_objc_class`, and `ObjCBlock`.

*  On iPad, "shake to undo" is no longer enabled.

*  Fixed `SystemError` when importing the `notification` module.

*  Fixed `scene.SceneView` (was completely unusable in previous build)

*  Restored some documentation pages that somehow went missing in one of the previous builds (`cb`, `appex`, `twitter`, `dialogs`).

*  Objective-C properties should work better in `objc_util`.

*  Lots of internal changes for iOS 9 -- at the moment, submitting iOS 9 builds to TestFlight isn't supported, so you don't see any of this now, but when I can flip the switch (hopefully soon), Pythonista should be completely ready for split screen mode etc.


#  Build 160025

*  All scripts are now stored within the same folder hierarchy -- this makes it possible for extension scripts to access the same data as scripts in the main app. Your files should be migrated automatically, and hopefully you won't notice this change much at all. `os.environ['HOME']` also points to the shared folder now, so things like `os.path.expanduser('~/Documents')` should work as expected.

*  Improved UI for moving files.

*  The order of the default import path (`sys.path`) has changed, so that site-packages come *before* the standard library etc. This makes it easier to use a different version of a bundled module if you want to.

*  Editor: The tab key now inserts the first code completion suggestion (if there is any, otherwise it behaves as before).

*  Fixed: The traceback inspector now works for exceptions in the `scene` module.

*  Fixed: When a custom view is presented in 'panel' style, `will_close()` is now called when the tab is closed.

*  Fixed incorrect console autocompletion for package imports.

*  `objc_util.create_objc_class` now validates that the number of arguments of a method match the inferred selector.

*  Fixed crashes when calling Objective-C methods that return a struct on 32-bit devices.

*  iTunes File Sharing is no longer enabled (this was temporary anyway, but with the new internal directory structure, it wouldn't actually work anymore).

*  Known issue: `keychain.set_master_password` is currently unavailable, and master passwords set previously have no effect.


#  Build 160024

*  Syntax errors shouldn't crash the app anymore... :/


#  Build 160023

*  Improved traceback navigator -- when an exception occurs, you can now tap on the red arrow (on the highlighted line of code) to view local variables in the selected stack frame. Tap on the error message at the top to select a different stack frame (as before).

*  Code completion in the console is now case-insensitive (and the results are sorted differently).

*  The console's code completion list now adapts to the width of the longest suggestion (this is particularly useful for Objective-C stuff, where method names are often extremely long).

*  Fixed: The corner radius attribute in pyui files is no longer ignored by `ui.load_view()`.

*  Changes in `objc_util`:
   - Improved parser for Objective-C type encoding strings -- among other things, it now supports arbitrary structs (even nested ones). It dynamically creates a subclass of `ctypes.Structure` for this (the fields are simply named a...z because the actual names can't be inferred from the encoding).
   - Struct arguments can now be passed as tuples (e.g. `((0, 0), (200, 100))` instead of `CGRect(CGPoint(0, 0), CGSize(200, 100))`) -- this is primarily meant to enable passing struct parameters where the class of the struct is dynamically generated, but it also helps making code less verbose.
   - New `create_objc_class()` factory method to make creating new Objective-C classes easier. It does a lot of work behind the scenes to infer type encodings and selector names for methods automatically in common cases (see docs or source code for details).
   - Experimental support for blocks (see `ObjCBlock` documentation for details -- this is *really* experimental, and I've seen a couple of crashes. If possible at all, I'd recommend using APIs that don't require blocks, but this isn't always an option).
   - `ObjCInstance` has a new `weakrefs` attribute, which is a `WeakValueDictionary` that makes it a bit easier to associate Python objects with an Objective-C instance without creating a reference cycle (memory leak) if the Python object also holds a reference to the Objective-C instance (which is probably common).
   - `dir(objc_object)` no longer lists most methods from `NSObject` While you may *sometimes* want to see them, in most cases, it's just an enormous amount of useless cruft from various completely unrelated categories. These methods will still be listed if you call `dir()` with an actual instance of `NSObject` (not a subclass). Some very common methods, like `-init`, `+new`, `-copy`, etc. are still listed in any case.
   - Objective-C classes are now cached, so for example `ObjCClass('UIApplication')` always returns the same object.
   - Objective-C instances are also cached, so as long as at least one `ObjCInstance` exists for a given pointer (Objective-C object), you always get the same one. This can be convenient if you want to associate auxiliary data with an instance.
   - If a method expects a selector parameter, you can now simply pass it as a Python string.
   - `on_main_thread()` should be reentrant now (which means that it's possible to nest calls that are executed to the main thread -- while this *mostly* worked before, there were cases in which it would result in corrupted return values).
   - Fixed a couple of issues that could lead to crashes and/or mysterious exceptions when calling any Objective-C methods simultaneously from multiple threads.
   - More correct handling of pointer arguments -- this was mostly an issue for methods that have an `NSError**` parameter. You can now create a pointer via `error_ptr = c_void_p()` and then pass it by reference to the method call, e.g. `NSDataDetector.dataDetectorWithTypes_error_(foo, byref(error_ptr))`. If an error occurred, you can wrap the pointer in an `ObjCInstance` to get an `NSError` object that you can inspect. If you're not interested in the error, you can just pass `None` of course.
   - Various performance tweaks

*  Warnings that occur during (jedi) code completion are now suppressed.

*  `ui.convert_point` now accepts `Point` objects instead of tuples.


#  Build 160022

*  Fixed incorrect position of the console's bottom bar in some cases (when keyboard is hidden while the console is inactive)

*  More improvements and bugfixes in the `objc_util` module:
   - Fixed a bug that caused `void` methods to fail with an exception (accidentally introduced in previous build)
   - Fixed a bug that caused boolean methods to return a byte string on 32-bit devices (this had various side effects, e.g. `__getitem__` not working correctly for `NSDictionary` instances)
   - New `on_main_thread` function, mostly intended to be used as a decorator (see docs for an example) – this can be helpful to deal with Objective-C APIs that *must* be called from the main thread (e.g. the majority of UIKit).
   - An `ObjCInstance` can now be constructed directly from a `ui.View` (you can use `obj = ObjCInstance(some_view)` instead of `obj = ObjCInstance(some_view._objc_ptr)`)
   - If an Objective-C method expects an object argument that can be converted via `ns()` (e.g. `NSString`, `NSArray`...), you can now just pass a Python object, and the conversion will happen automatically. For example, instead of `NSURL.URLWithString_(ns('http://...'))` you can just write `NSURL.URLWithString_('http://...')`. While this doesn't save a lot of typing, forgetting the `ns()` call would previously have resulted in a crash.
   - For argument/return types that are not directly supported by the encoding string parser, you can now pass `restype` and `argtypes` explicitly, as keyword arguments to an Objective-C method call. This should only be necessary for structs that aren't very common (see docs for an example).
   - Fixed a potential reference cycle ("memory leak") between `ObjCInstance` and `ObjCInstanceMethod` that could prevent `ObjCInstance` objects from ever being garbage-collected.

*  I've changed some internals in the `ui` module with regards to how the GIL (global interpreter lock) is handled. This needs some more testing, and it's possible that you see deadlocks ("hangs") as a result of this, most likely in custom views. If that's the case, I'd really appreciate bug reports (ideally with a reproducible code sample).

*  Fixed: The new `ui.load_view` implementation didn't call `did_load()` for custom views in previous builds.


#  Build 160021

*  Some improvements in the `objc_util` module:
   - Methods that return a struct should no longer crash on 32-bit devices
   - `ObjCInstance` supports reflection via the builtin `dir()` function now
   - It's now possible to call Objective-C methods that contain underscore characters

*  Fixed a number of bugs in `ui.load_view()` that could cause it to fail if the .pyui file contained labels, text fields etc. with empty text

*  Fixed a potential crash on launch, if the first tab in the previous session was a UI editor

*  Included standard library documentation for the `ctypes` module


#  Build 160020

*  New and improved UI editor with support for copy/paste, undo/redo, zoom, and more (not completely finished yet, e.g. inline editing for the text of labels, text fields etc. is currently not supported). Tip: You can tap on a number in the new inspector to edit it directly via keyboard, and you can also enter simple math expressions there (e.g. add "*2" to the current value to double it quickly).

*  `ui.View` now supports setting arbitrary attributes, so you don't have to subclass in order to attach some auxiliary data to a view (or any subclass of `ui.View`). Note that this might hide bugs/typos in your code because something like `my_view.fame = ...` (instead of `my_view.frame`) no longer throws an exception (but this is consistent with the way most objects in Python work).

*  The UI editor now supports setting custom attributes for views. You can use this to attach arbitrary data to a view or to set built-in attributes that aren't supported directly in the UI editor's inspector (e.g. `ui.TextField.keyboard_type`).

*  I've rewritten `ui.load_view` in pure Python -- this might be a little slower than the previous implementation, but it's a lot easier to maintain. Another advantage is that you can actually read the source code to see what's going on (if you turn on "Show Standard Library" in the settings, you can open `ui.py` in the editor). There's also a new `ui.load_view_str` function that accepts a JSON string instead of a file path. This can come in handy to embed .pyui files as strings in single-file scripts.

*  New `objc_util` module: This is essentially a "bridge" for calling Objective-C APIs from Python with *a lot* less boilerplate and low-level code than by using `ctypes` directly. You still might need some familiarity with Objective-C/Cocoa to make much use of it, but it is *significantly* easier than using `ctypes` directly, and the resulting code looks more 'pythonic'. Have a look at the examples in the documentation, I think they're quite readable.

*  Fixed a crash when using `ctypes.CFUNCTYPE` on 64-bit devices.

*  Removed the `sk` module and related functionality. As I've mentioned before, I hope to bring it back at some point, but probably not in version 1.6 (if you're new to the beta: this module was added in a previous build, it was never part of the App Store version)

*  Fixed a bug in ImageFilter.GaussianBlur that caused the radius parameter to be ignored (the radius was hard-coded to 2)

*  Fixed an `ImportError` in the `appex` module (due to the removed `appex.watch` submodule)


#  Build 160018

*  NOTE: I will probably remove the `sk` module and the scene editor in one of the next builds. Unfortunately, there are a number of issues with this on iOS 9, and I don't really want to risk shipping a major feature that breaks as soon as iOS 9 is released. I will definitely keep an eye on how the situation evolves with new iOS 9 betas, but for now, I would recommend that you don't rely on this module.

*  I've enabled iTunes file sharing in this build to make backups etc. easier during the beta, but please note that I'll remove this in the final release (Apple doesn't allow features that allow importing executable code).

*  Removed the Watch app – this just wasn't very useful overall; I might rewrite it as a native app at some point after watchOS 2 is out, but it's not a high priority right now, and probably won't happen before the 1.6 release.

*  New PDF export for scripts (via share menu) -- this is primarily intended for use in education (iTunes U etc.), but can also be useful for printing.

*  Fixed disappearing editor actions after rearranging them in the share sheet

*  Fixed a bug that could potentially overwrite existing scripts with empty data

*  Slightly improved support for the new two-finger keyboard gestures in iOS 9 (the previous implementation was kind of a hack, using an official API now)

*  A few global functions that are defined in the `site` module should now work out of the box, like on other platforms (`copyright`, `license`, `quit`...)

*  Various internal changes in preparation for iOS 9 – I'm making good progress with the split-screen support, but it isn't quite ready yet, and even if you do have the iOS 9 beta installed, you cannot test this easily because it's not yet possible to distribute apps that are built with the iOS 9 SDK via TestFlight... If you're adventurous, you can get split-screen support for iOS 8 apps by tampering with iTunes backups, but I wouldn't really recommend this.


#  Build 160016

*  Some fixes for text selection on iOS 9 (beta 1):
   - Two-finger gestures on the new keyboard should work much better
   - Fixed incorrect cursor positioning when tapping on the right margin


#  Build 160015

*  No major changes


#  Build 160014

*  Experimental Apple Watch support – the Pythonista Watch App allows you to launch scripts in the special "Watch" folder. The scripts still run on the iPhone (usually in the background) – the Watch basically just acts a remote control. Console output appears on the watch, including images, but things like `console.set_font()` or `console.clear()` are not supported. The only way to get user input is currently to call `raw_input()`. This brings up the dictation interface on the Watch with an optional list of suggestions to pick from. To set the list of text input suggestions, call `appex.watch.set_input_suggestions()` *before* `raw_input`. I'm not sure yet how useful this actually is, and if I'll include it in the final release.

*  Added a *Done* button in the console output panel of the app extension

*  Cmd-Left/Right shortcuts (external keyboard) should work properly now

*  Background audio (experimental) – Note: This has the side effect of the mute switch being ignored when playing audio (like in pretty much all music/video player apps). You can also abuse this to make your script run in the background indefinitely by looping a silent track (can be useful for servers and the like).

*  New `is_authorized()` functions in the `location`, `contacts`, `reminders` and `photos` modules

*  New `console.is_in_background()` function to determine whether Pythonista is currently the foreground app or not

*  Fixed crash when importing `requests` in the app extension

*  Fixed crash when initializing `sound.MIDIPlayer` without an explicit soundbank path (the "Random MIDI Melody" example shouldn't crash anymore)

*  Fixed crashes related to code completion (somewhat hard to reproduce, so I'm not 100% sure)

*  Fixed `ui.View.bounds` (and a couple of other attributes) returning a `Rect`, but accepting only a tuple (any 4-number sequence should work now)

*  Reverted to an older version of `requests` for now to get rid of "InsecurePlatform" warnings that are logged to the console. I'm well aware that this isn't an actual solution, but a real fix turns out to be non-trivial to implement (the cleanest approach would be to upgrade to Python 2.7.9, but this is quite a lot of work and I'm not sure if I want to get into that for 1.6)


#  Build 160013

## New Features

*  Refreshed look and feel with new and improved color themes, refined toolbar icons, additional editor font choices, and a new app icon.

   Selecting a different theme in the settings changes the look of the app much more profoundly than before, especially with one of the new dark themes.

*  App extension + `appex` module: This is basically a mini version of Pythonista that you can use in many system and third-party apps via the standard iOS share sheet. With the `appex` module, you can get the data that was passed to the share sheet (e.g. text, images, URLs) and use it in your scripts. The extension contains a basic editor (not all features of the main app, but good enough for minor changes) and an interactive console for ad-hoc experimentation. Please note that if you want to make a script (or other file) accessible from the app extension, it has to be in the special *Extension* folder. There are a couple of templates for extension scripts and the Extension folder also contains a few sample scripts by default.

*  Tabbed editor: You can now have multiple files open at once and quickly switch between them. On the iPad, there's a traditional tab bar interface (only shown when there are at least two tabs), on the iPhone, tabs are shown in a thumbnail grid when you tap the "tabs" button in the toolbar. If you have an iPhone 6 or 6 Plus, there's an option in the settings to use a tab bar instead (this doesn't work well on smaller screens, so the option isn't available on other iPhones or the iPod touch).

*  Significantly improved support for non-Python files: All files are now opened in a tab, so that all types of files can be renamed (it's also possible to change the file extension for all file types, which can be useful e.g. if you want to view a .pyui file as text). Apart from that, you can show a QuickLook preview for lots of files, open them in another app, extract zip archives, and play audio files.

*  The editor has basic syntax highlighting support for HTML, CSS, JavaScript (useful for `bottle`, `Flask` etc.), Markdown (which you see right now), and TaskPaper (if you want to keep a todo list next to your script).

*  Commands in the console are syntax-highlighted now. The history UI has also changed a little and works better with Bluetooth keyboards (up/down arrow keys), and the code completion is a little smarter about when to add a space after you select a suggestion.

*  New setting to show the standard library in the file browser (you can't edit these files, but it can be quite interesting to read the source code nevertheless)

*  New "traceback navigator": When an exception occurs, you can tap on the error marker in the title bar to view the traceback in a much more readable format than before. You can also tap on individual lines to view them in the editor (even if they're in different files)

*  Improved sharing in the editor and file browser – instead of the custom 'Actions' menu, the editor now uses the standard iOS share sheet. You can still add custom scripts to this sheet in the settings (*Editor Actions*). You can also invoke a share sheet in the file browser (*Edit* mode), and customize this sheet via the *File Actions* setting. This is useful for scripts that operate on a list of files (e.g. to create a zip archive, upload them somewhere...) because the selected files are passed to the script (as part of `sys.argv`) automatically.

*  Improved asset/color picker and new built-in images and sound effects for games (mostly Public Domain, thanks to [Kenney](http://kenney.nl))

*  Improved in-editor search, including find/replace (currently only on iPad)

*  New setting to use "true" division in the console (this is basically equivalent to `from __future__ import division` in a script, you might want to turn this on if you often use the console as a calculator)

*  New setting for using a more compact keyboard (one row instead of two, iPad only)

*  New Indent/dedent menu items in the editor (copy/paste menu) – note: dedenting currently doesn't work very well if you use soft tabs/spaces

*  New "Highlight all" menu item in the editor (copy/paste menu) – this can be very useful for highlighting all occurrences of a variable/function name etc.

*  Improved "new file" menu with more templates and the ability to import photos and other saved images from the camera roll

*  New sound.MIDIPlayer class (plus `midiutil` module, currently both undocumented, but there's a "Random MIDI Melody" sample script)

*  Color and image previews in the code editor (when the cursor is inside a string that contains a built-in image asset name or a hex color, a preview is shown as an overlay)


## Notes and Known Issues

*  iOS 8.0 or later is required now

*  This version is built as a 64-bit app. Not only is this a requirement for submitting to the App Store very soon (starting in June), but app extensions require a 64-bit slice to work at all. Hopefully you won't notice this much, but it's possible that there are bugs related to this that I haven't caught yet.

*  Built-in images and sounds are currently not available in the app extension

*  The editor and console sometimes don't adjust their sizes correctly after the keyboard is hidden

*  The `'sidebar'` presentation style (`ui` module) is currently not supported

*  The console currently doesn't have its own *Run* button

*  Renaming a file that is open in multiple tabs may result in duplicates

*  On iOS 8.3 and later, the extended keyboard doesn't respond to touches if they occur too quickly after a regular key was pressed. This appears to be an intentional change by Apple (probably to avoid mistakes when typing quickly), and it doesn't look like there's anything I can do about it.

*  Automatic indentation doesn't work in some cases (e.g. when splitting a line)

*  The new color picker doesn't support alpha values yet

*  The keyboard is sometimes dismissed when it shouldn't be (usually after a popover is dismissed when any kind of modal view was presented before)

*  The `modal` and `stop_when_done` parameters for `webbrowser.open()` are currently ignored

*  Changing the editor font size can be slow
