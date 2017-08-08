# Custom Homescreen Icons with Pythonista

_Captured: 2015-10-31 at 01:44 from [olemoritz.net](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)_

Back in the day, when there was no iPhone SDK, you could already add web apps to your homescreen - basically glorified bookmarks that could specify their own icon and look (more or less) like a native app. Unfortunately, not all websites specify a proper `[apple-touch-icon`](https://developer.apple.com/library/ios/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html#//apple_ref/doc/uid/TP40002051-CH3-SW4), and sometimes you end up with a static screenshot instead. You also can't override the website's preference of whether it's launched in full-screen mode (without Safari's UI) or not.

Another limitation of these Safari "webclips" is that you can only use them to launch _web_ (i.e. http[s]) URLs, not mailto:, tel:, maps:, or any of the myriads of [third-party app URL schemes](http://handleopenurl.com).

However, there's one other way of adding webclips to your homescreen: You can install _configuration profiles_ from a web page, or using the [iPhone Configuration Utility](http://support.apple.com/downloads/#iphone%20configuration%20utility). Icons that are installed with configuration profiles can override the website's icon and full-screen settings, and it's also possible to use custom URL schemes.[1](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)

The iPhone configuration utility is pretty easy to use, but it obviously requires that you have a Mac or PC at hand. It would be easy to write a web app that allows you to create/download custom configuration profiles[2](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html), but I wanted to see if I could do it just using Pythonista, without requiring an internet connection.[3](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)

After a little bit of tinkering with the iPhone Configuration Utility, `[plistlib`](http://omz-software.com/pythonista/docs/library/plistlib.html) and `[BaseHTTPServer`](http://omz-software.com/pythonista/docs/library/basehttpserver.html), I came up with this script:

**->[ ShortcutGenerator.py [GitHub]](https://gist.github.com/omz/7870550)**

Here's how it works:

  * Using a few Pythonista-specific functions from the `console` and `photos` modules (that would also work in [Editorial](http://editorial-app.com)), it requests a title, URL, and icon (picked from the camera roll) for the shortcut icon.

  * From these things, it generates an xml plist file that contains the configuration profile (using `[plistlib`](http://omz-software.com/pythonista/docs/library/plistlib.html) for generating xml and `[PIL`](http://omz-software.com/pythonista/docs/ios/PIL.html) for encoding the image data). I used a profile that I generated with the iPhone Configuration Utility as a template.

  * Then, a local web server is started, so that Safari can access the file. Local servers are a mechanism of inter-app communication that is rarely used, but works just fine. The server could only run for 10 minutes in the background, but for our purposes, that's more than enough, and in this case, it actually stops after serving one request.

  * Using the `webbrowser` module, we switch to Safari, pointing it to the URL of the local web server.

  * After downloading the profile from our local server (which then stops serving requests), Safari switches to the Settings app, where an installation dialog is shown. When you tap the "Install" button, you have a new icon on your homescreen.

![Screenshot](http://olemoritz.net/static/images/config_profile_screenshot.png)

> _I can think of a couple of use cases for this:_

  * Use a custom icon for a web app if you don't like its default one (or it doesn't specify an icon at all).

  * Launch a web app in full-screen mode that normally wouldn't (I find this especially useful for some shops, like [Audible](http://audible.com)).

  * Dial a contact's number (using a tel: URL) or create a new email (mailto:) by tapping on the photo of a person (the icon is cropped/resized automatically, so you don't have to create a square image first).

  * Launch a [Pythonista script](http://omz-software.com/pythonista/docs/ios/urlscheme.html) directly from the home screen, or open an often-used document [in Editorial](http://omz-software.com/editorial/docs/ios/editorial_urlscheme.html).

  * Open the maps app with navigation directions to a favorite location, perhaps using a Maps screenshot or a photo as the icon.

One thing to keep in mind with these configuration profiles is that they can clutter the Settings app. When you remove the icon from the homescreen, the profile is not removed automatically, so you might want to clean up the "Profiles" section from time to time (under "General").

  1. One caveat: A white screen is shown briefly before iOS launches the actual URL. Custom URL schemes also didn't work in iOS 7.0, but this has been fixed with 7.0.3. [↩](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)

  2. I haven't done any research, but I'm sure something like this already exists. [↩](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)

  3. There are also some privacy concerns when using a web app because some custom URLs can contain sensitive data (e.g. tel: URLs with private phone numbers). [↩](http://olemoritz.net/custom-homescreen-icons-with-pythonista.html)
