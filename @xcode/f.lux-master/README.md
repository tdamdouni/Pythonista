f.lux-xcode
===========

This installs the f.lux iOS app on your device without requiring a jailbreak.
Learn more about f.lux at <https://justgetflux.com/>

Why isn't this in the app store?
--------------------------------

This app changes the color of all running apps on your phone, even when f.lux is
not directly open. Such functionality is not allowed in the [App Store Review
Guidelines](<https://developer.apple.com/app-store/review/guidelines/>), however
this type of app is possible.

How do I get this on my phone?
------------------------------

1.  Download (click releases above for file), then open with XCode

2.  Plug in your phone

3.  Select your phone from the device menu (next to the "Play" and "Stop"
    buttons)

4.  Click "Play"

How does it work?
-----------------

There is an opaque, non-open-source app called `iflux` in this project. We trick
Xcode into signing and installing this app on your phone by:

1.  Building a dummy app "just an app"

2.  Splicing in the opaque binary during the build process

3.  Letting Xcode sign and install the app as normal

There are build errors
----------------------

We are building the binary twice, once using source code, and again by splicing.
This duplication is reported as an error by XCode.
