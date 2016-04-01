# MarkdownView

MarkdownView is a [Pythonista](http://omz-software.com/pythonista/) UI library component. It is a drop-in replacement for ui.TextView that supports both editing [markdown](https://daringfireball.net/projects/markdown/) tagged text and viewing it as HTML.

![Demo](https://espq1q.by3301.livefilestore.com/y3mRxyyKwIANcZia4VSQ5SBJfFFlZsCb-qoReBY49SXjkdYFjhlRCI6btZ7dWxlqBwHMDM9oFqD34rj9Q1rzhgqqPraNV0jji0XjxN4ee2-md8CHmcqkjVsQ1Z-eohQNQ6LD5hNJSztGKmOcUKTWdwzWwYpTwG6sa5GAPMLQLGBn4Y/20151222_081323000_iOS.gif?psid=1)

##Contents
 
1. [Features](#features)
1. [Quick start](#quick-start)
1. [Link behavior](#link-behavior)
1. [Additional keys](#additional-keys)
1. [Component motivation and design principles](#component-motivation-and-design-principles)
1. [Constructor](#constructor)
1. [Attributes](#attributes)
1. [Methods](#methods)
1. [To do](#to-do)

## Features

* Integrated markdown editing and HTML viewing modes - end editing and HTML is shown, click somewhere on the HTML text and markdown editing starts in the same position.
* Markdown editing supported by additional keys. (Thanks JonB for help on Obj-C.)
* Implements ui.TextView API for easy integration to existing code.
* Customizable through attributes or CSS.

##Quick start

Download (from [Github](https://github.com/mikaelho/pythonista-markdownview)) both the `MarkdownView.py` script and this `readme.md` file into same directory, and you can run the script in Pythonista to view and try out editing this readme file.

Import MarkdownView as a module and use wherever you would use a TextView. Markdown text can be set and accessed with the _text_ attribute. Implement a delegate with `textview_did_end_editing` or  `textview_did_change` method - see the end of the MarkdownView.py file for an example. 

## Link behavior

When you click a link in the HTML view:

* `http:` and `https:` links are opened in Safari
* Document-internal links (`#something`) are followed within MarkdownView
* `file:` links are opened in Pythonista built-in browser
* All other links like `twitter:` are opened as defined by the OS, i.e. in the relevant app, if installed.

If you want to change any of these, implement a delegate class with the `webview_should_start_load` method.

## Additional keys

Extra keys help with markdown editing, but are in no way required, and can be turned off with `additional_keys = False` argument at instantiation. Please refer to markdown [syntax](https://daringfireball.net/projects/markdown/syntax) if not already familiar.

Keys:

* __&#8677;__ - Indent - Repeat adds more spaces, 2 at a time.
* __&#8676;__ - Outdent - Removes 2 spaces at time.
* __>__ - Quote - Repeat adds levels; there is no special support for removing levels.
* __[]__ - Links and images - If a range is selected, the contents of the range is used for both visible text and the link; for images, you have to add the exclamation mark at the front.
* __#__ - Headings - Adds a level with each click; fourth click removes all hashes.
* __`1.`__ - Numbered list - Replaces unordered list markers if present. Repeat removes. Indenting increases the list level.
* __•__ - Bullet list - Regular unordered list, otherwise like the numbered list.
* __`_`__ - Emphasis - If a range is selected, inserts an underscore at both ends of the selection. Once for emphasis, twice for strong, three times for both. Fourth time removes the underscores.
* __`__ - Backtick - Insert backtick or backticks around selection to indicate code. Removes backticks if already there.

For all of the above, where it makes sense, if several lines are selected, applies the change to all the lines regardless of whether they have been selected only partially.

## Component motivation and design principles

* Provide some rich-text editing capabilities for Pythonista UI scripts
* In a format that is not locked to specific propietary format & program
* Easy to deploy to an existing solution
* Is robust (unlike straight HTML that tends to get confusing with styles etc.)
* Make markdown editing as easy as possible, with the transition between editing and viewing as seamless as possible (no 'Edit' button)
* Do not require thinking about or taking screen space for UI elements like toolbars (i.e. be conscious of and support small screens like iPhone)
* Is lightweight, understandable and manageable by a Python programmer (which would not be the case when using e.g. TinyMCE in a WebView)
* Not a web browser

## Constructor

`MarkdownView(frame = None, flex = None, background_color = None, name = None, accessory_keys = True, extras = [], css = None)`

Parameters:

* `frame`, `flex`, `background_color`, `name` - As standard for a view.
* `accessory_keys` - Whether to enable the additional keys for markdown editing or not; see the section on additional keys, above.
* `extras` - Any [markdown2 extras](https://github.com/trentm/python-markdown2/wiki/Extras) you want active, as an array of strings. As an example, this document relies on `"header-ids"` for the table of contents links.
* `css` - Provide your own CSS styles as a string; see the attribute description, below.

## Attributes

* `alignment` - As TextView, affects WebView as well
* `autocapitalization_type` - As TextView
* `autocorrection_type` - As TextView
* `auto_content_inset` - As TextView
* `background_color` - As TextView, affects WebView as well
* `css` - Provide your own CSS styles, or set to an empty string to get the WebView defaults. Note that if you provide this, you have to provide all styles, not just your additions. Include `$font_size`, `$font_family`, `$text_color` and `$text_align` keywords in the appropriate places if you still want to have e.g. the `font` attribute of `MarkdownView` affect also the `WebView`.
* `delegate` - Set an object that handles `TextView` and `WebView` delegated method calls. Following methods are supported:
  * `textview_should_begin_editing`, `textview_did_begin_editing`, `textview_did_end_editing`, `textview_should_change`, `textview_did_change`, `textview_did_change_selection`
  * `webview_should_start_load`, `webview_did_start_load`, `webview_did_finish_load`,  `webview_did_fail_load`
* `editable` - True by default. Setting to False means you get the HTML view only. Could be useful if your app has different users and modes for "editor" and "viewer".
* `editing` - True if currently in markdown editing mode
* `font` - As TextView, affects WebView as well
* `keyboard_type` - As TextView
* `margins` - Tuple (), default is no margins
* `scales_page_to_fit` - as WebView
* `selectable` - As TextView, does not affect WebView
* `selected_range` - As TextView, does not work on WebView mode
* `spellchecking_type` - As TextView
* `text` - The markdown text
* `text_color` - As TextView, affects WebView as well

## Methods

* `preferred_size()` - returns a size (width, height) tuple based on what size the component would want to be, based on its contents. This is based on the TextView or the WebView contents, depending on whether we are currently editing or not. If you want to explicitly use one or the other, pass a `using=markdown` or `using=html` parameter. You can control min/max dimensions returned by providing some of the following parameters: `min_width`, `max_width`, `min_height`, `max_height`. (The processing of these parameters is optimized for horizontal text.)
* `replace_range()` - as TextView
* `size_to_fit()` - sizes the component based on the TextView or the WebView contents, depending on whether we are currently editing or not. See `preferred_size()` for optional parameters.
* `to_html()` - returns the HTML of the WebView. This contains all MarkdownView-specific styles and JavaScript code. If you need just the markdown content converted to HTML, include `content_only=True` as a parameter.

## To do

* Increase reliability of the HTML-to-markdown transition 
* Swipe right to go back after following an in-document link