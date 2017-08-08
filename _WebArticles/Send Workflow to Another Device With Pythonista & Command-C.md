# Send Workflow to Another Device With Pythonista & Command-C

_Captured: 2015-12-02 at 18:59 from [plobo.net](http://plobo.net/send-workflow-to-another-device-with-pythonista-command-c/)_

I'm sure it's a matter of time until the Workflow team come up with a more elegant solution (iCloud or Dropbox sync possibly), but until then, I thought I'd resort to a few tools already in my arsenal, namely [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11l5Lz), [Command-C](https://itunes.apple.com/us/app/command-c-clipboard-sharing/id692783673?mt=8&uo=4&at=11l5Lz) and [Workflow](https://itunes.apple.com/us/app/workflow-powerful-automation/id915249334?mt=8&uo=4&at=11l5Lz) of course.

![](http://plobo.net/images/send-workflow-to-another-device_1.png)

[Workflow](http://my.workflow.is), a powerful and intuitive automation app for iOS, recently made its debut on the App Store and rather than write a review of it (you can read Viticci's rather extensive [review](http://www.macstories.net/reviews/workflow-review-integrated-automation-for-ios-8)), I decided to spend a little time tackling the lack of Sync.

I'm sure it's a matter of time until the Workflow team come up with a more elegant solution (iCloud or Dropbox sync possibly), but until then, I thought I'd resort to a few tools already in my arsenal, namely [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=11l5Lz), [Command-C](https://itunes.apple.com/us/app/command-c-clipboard-sharing/id692783673?mt=8&uo=4&at=11l5Lz) and [Workflow](https://itunes.apple.com/us/app/workflow-powerful-automation/id915249334?mt=8&uo=4&at=11l5Lz) of course.

## The Premiss

Akin to Launch Center Pro, Workflow allows users to share and install workflows via a simple web page like this [one](https://workflow.is/workflows/7c09c64a438f42fca0eef15b9dfe61ee). Behind the scenes, the install button is nothing more than a simple url-scheme that imports a workflow. For instance, the URL to import this workflow looks like this:
    
    
    workflow://import-workflow/?url=https%3A%2F%2Fworkflow-gallery.s3.amazonaws.com%2Fworkflows%2F6ddd0cf9fbc74880a4d50724e9c324d9.wflow&amp;name=Send%20Workflow
    

This got me thinking a little and I quickly reached the conclusion that I didn't need to share the web page url, instead I could simply share the import url between device.

My idea therefore was a simple one. Given the share URL, use Pythonista to scrape the page source, extract the workflow import url-scheme and then use Command-C to send it to another device, that in turn would execute the url-scheme and import the workflow. Simple right? Now let's set it up.

## The Process

Let's first create the Pythonista script we'll be using. Create a new script named `SendWorkflow` and add the following code to it:
    
    
    import re
    import urllib2
    import clipboard
    import webbrowser
    
    source = clipboard.get()
    mystring = urllib2.urlopen(source).read()
    
    clipboard.set(re.search("workflow://.*\\b",mystring,re.M).group(0))
    webbrowser.open('workflow://')
    

Unfortunately, until the Workflow team sorts out an [issue](https://twitter.com/WorkflowHQ/status/543560946652688385) with input to and from Pythonista, we need to rely on the clipboard to share data.

The script also assumes you already have the url of the workflow you want to send in your clipboard. You can get it by simply tapping the share button and choosing copy when viewing the workflow.

![](http://plobo.net/images/send-workflow-to-another-device_2.jpg)

The second piece of the puzzle is getting the right x-callback-url for Command-C. In my case, I'lll be sending data to either my iPhone or my iPad, so my x-callback-url will look something like `command-c://x-callback-url/copy?deviceName=iPhone`. You just need to adjust it to match the name of the device you have in Command-C.

Now that we have all the pieces, setting up the puzzle is quite simple. Install the this [workflow](https://workflow.is/workflows/7c09c64a438f42fca0eef15b9dfe61ee) and then tweak it to suit your needs, namely changing the Command-C x-callback-url and possibly adding or removing options from the menu.

That's all there is to it really. Now, any time you want to send a workflow to another device, simply copy the url and trigger this workflow. The great thing about this process is that if you change anything on one device, you can simply send it again to the other and the corresponding workflow will be updated.
