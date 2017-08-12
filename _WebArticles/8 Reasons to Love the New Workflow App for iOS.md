# 8 Reasons to Love the New Workflow App for iOS

_Captured: 2015-11-16 at 01:28 from [www.geekswithjuniors.com](http://www.geekswithjuniors.com/note/8-reasons-to-love-the-new-workflow-app-for-ios.html)_

_This article was meant to be published on the same day when iOS 8 was available. But, we all know the story how **Workflow** was rejected for having buttons to launch itself in the **Today View** extension. After waiting for months (and removing said feature), finally Workflow is available for everyone today._

If you love iOS automation, you're probably already aware of [Launch Center Pro](http://www.geekswithjuniors.com/note/10-reasons-to-love-launch-center-pro-23.html) and [Drafts](http://www.geekswithjuniors.com/note/8-reasons-to-love-drafts-4.html). Together with URL Schemes and [x-callback-url](http://x-callback-url.com), they form the backbones of iOS automation. Well, today we have a new app that hopefully can make it easy for non-geeks to create their own workflows. And, here are a few reasons why I believe you would love the new Workflow app.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ce4b0f07e37b3a89d/1418314605005/1000w/Workflow01.jpg)

> _Workflow arranges its actions as tappable banners, similar to an Apple TV layout, scrollable to support (almost) unlimited number of actions._

### 1\. Workflow is Easy to Create

Workflow is designed to help you create automation workflows **visually** and **easily**. You don't need to understand how URL Schemes and x-callback-url work to create your own workflow. Everything is **drag and drop**. And, it can support as many actions as you want to include in the workflow.

If you install the app for the first time, you will be greeted with a nice tutorial that will guide you through the features. As a bonus, you get to create a cool workflow that lets you create a GIF from three or more photos that you just took with your camera.

The app has two main tabs: **My Workflows** and **Gallery**. The first tab consists of all workflows that you have created. And, the second tab consists of all workflows that are available in the official Workflow Gallery. These are workflows created by the developers to showcase the app and some user submissions that the developers decided to feature.

To create a new workflow, tap the `+` button on the top right corner of the My Workflows tab. Then, you can switch to the **Actions** tab to select which action you'd like to add first. Workflow includes plenty of actions, grouped into several categories such as Calendar, Contacts, Documents, Maps, Music, and Photo & Video. Tapping the category will show all available actions within that category.

To learn more about an action, tap the action name. Workflow will show the action description underneath, complete with the kinds of input data that it can receive and the kinds of output data that it will produce. For example, in the sample workflow, a **Make GIF** action receives various input data (such as images), and produces a GIF file.

To select the action, drag it to the right hand side of the screen. The app will automatically navigate you to the **Workflow** tab and let you drop it on any part of the workflow sequence. Some actions may have parameters that you can set, such as how many photos you want to take or which phone number you want to select. Once you're done, you can go back to the Actions tab and select the next action you want to include in your workflow.

To test your workflow, simply tap the `Play` button on the top of the screen. It will go through all the actions that you have put into the sequence. You can stop at anytime by tapping the `Stop` button. And, once you're done testing, tap the `Done` button to return to the list of workflows you have created.

You can change the name and icon associated with each workflow by tapping on the `Settings` gear icon inside each workflow. Then, you can choose whether to have the workflow accessible from within the app, make a shortcut on your **Home Screen**, or even inside Launch Center Pro.

### 2\. Accessible from Other Apps via iOS 8 Action Extension

You can also create custom action in Workflow and make it accessible from other apps. Simply have it listen to a particular data type - such that whenever the user triggers the **Share** button from any app within iOS, you can offer your workflow as one of the end-points.

For example, you can listen to a `URL` data type and have one or more workflows inside the Workflow app to handle such data. If you have [Quotebook](https://itunes.apple.com/us/app/quotebook-notebook-for-quotes/id423726272?mt=8&uo=4&at=10l9rH&ct=note), for example, you can create a workflow that listens to any attempt to share a `URL` data type and converts it into an entry in Quotebook. Then, you can use it in Safari to take the URL of the active tab alongside the quote that you've presumably stored into the clipboard, to create a new entry in Quotebook.

Open [this link](https://workflow.is/workflows/0dc502e1cd724e91b71600767eeee023) on your iOS device to automatically install the **Add to Quotebook** action extension in Workflow.

These Action Extensions will be shown as the **Run Workflow** icon on the bottom bar of the Sharing popup menu across the OS. You can also have more than one workflows that listen to a particular input data type. If you do, iOS 8 redirect you to the Workflow app where you decide which workflow you want to trigger.

Along these lines, a workflow can also listen to more than one input data types. Here are the applicable data types for the Action Extensions: images, contacts, text, PDFs, URLs, dates, locations, phone numbers, files, rich text, email addresses, and map links. Workflow makes it possible for you to create your own Action Extension without needing to know how to code.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b29f/1418315427014/1000w/Workflow06.jpg)

> _Workflow supports all kinds of scripting elements that many iOS automators have been dreaming of._

### 3\. Supports Complex Workflows with If and Loop

Another great thing about Workflow is its ability to define conditions and loops. Without forcing the users to learn about any particular programming language, Workflow allows you to set up a simple `if` conditionals. This allows you to adapt your workflow according to a runtime value.

The same can be said with the loops. As the tutorial workflow shows, repeating an action in Workflow is very easy. You can even ask for input on how many times you should repeat an action.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b2a0/1418315427067/1000w/Workflow05.jpg)

> _Workflow has plenty of actions to choose and download from its Actions gallery._

### 4\. Great Built-in Features

Workflow comes with many great built-in features. For example, you can get the upcoming events and reminders in your Calendar, or get the list of phone numbers and email addresses for entries in your Contacts. I've never seen an app that allows its user to do this programmatically. You can also generate a PDF document from any kind of data input.

You can work with Apple Maps to get the current location, directions and travel time; or you can work with the Google Maps to get the Street View image. There is a nice sample workflow in the Gallery that searches for nearby businesses, prompts you to choose one, and shows you a walking direction to the selected location

Workflow also allows you to interact with the Music app to play/pause music, skip back/forward, or set the volume. It also allows you to edit photos using the [Aviary SDK](https://developers.aviary.com). Again, the best way to explore these features is to install the sample workflows in the Gallery. Once you get the hang of what you can do with this app, feel free to create your own custom mix of actions.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b2a1/1418314605597/1000w/Workflow02.jpg)

> _This is an action extension that accepts an image to be posted to Instagram. You can trigger it from the Photos app, for example._

### 5\. Excellent Third Party Support (Beyond URL Schemes)

Throughout the past couple of years, there have been many more apps making their APIs available via URL Schemes. Nonetheless, there are still a few other apps that haven't made this possible.

Because the actions in Workflow don't work as a URL Scheme would, it's now possible to include these APIs as parts of your workflow. For example, you can now select a photo from your Camera Roll, define a caption for it, and share it on Instagram. This is something that you can't possibly do when you rely only on [Instagram's official URL Scheme](http://instagram.com/developer/mobile-sharing/iphone-hooks/).

Open [this link](https://workflow.is/workflows/dc46a4819775447fa6f35f457c076a81) on your iOS device to automatically install the **Post to Instagram** action extension in Workflow.

Workflow also has a nice integration with other apps such as Dropbox, Editorial, Evernote, Fantastical, Google Maps, Pythonista, Quotebook, Tweetbot, Things, Uber, and Venmo. For example, you can save the GIF you just created into Dropbox, or create a new note in Evernote based on the content you put into the clipboard as you're browsing in Safari (using the custom Action Extension). With the developers' commitment to continually add new third-party support, the possibilities are endless.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b2a2/1418314605068/1000w/Workflow03.jpg)

> _Workflow supports prompts, lists of values, and even variables for a more complex logic._

### 6\. Ability to Parse JSON as Dictionaries

If you're doing any web programming over the past decade, you're probably familiar with the ever-increasing public Web API, which typically are RESTful API with JSON or XML as its data structure. Now, Workflow makes it possible for us to access these real-time information as a part of our workflow -- thanks to its ability to parse the JSON in an HTTP Response into a Dictionary. Then, you can get the value for each key within that Dictionary for further processing.

For example, if you want to get a real-time currency conversion, you can use Google Exchange Rate API.

> `http://rate-exchange.appspot.com/currency?from=USD&to=IDR`

As a result, you will get a JSON response like this:

> `{"to": "EUR", "rate": 0.80526500000000001, "from": "USD"}`

I created a workflow that prompts you a list of currencies to choose from, and another list of currencies to convert the amount to; before sending the crafted URL. Then, I parse the JSON response into a Dictionary, and get the value for the "rate" key. Using this value, I can multiply the input amount to yield the final result.

Open [this link](https://workflow.is/workflows/d8133815969e410887207860b5f0995a) on your iOS device to automatically install the **Convert Currency** action in Workflow.

If you're really creative, there are tens of thousands of public APIs available for your mashups. Just look at the list in [ProgrammableWeb](http://www.programmableweb.com/category/all/apis?data_format=21173%2C21190&order=created&sort=desc), [Mashape API](http://www.publicapis.com), or [Data.gov](https://www.data.gov/developers/apis). I'd love to learn what you come up with.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b2a3/1418314605757/1000w/Workflow04.jpg)

> _Workflow also supports the hard-coded old-fashioned URL scheme for savvy automators._

### 7\. Supports x-callback-url

Workflow has a special URL Scheme that allows you to invoke its workflows by specifying its name. It fully supports the standard `x-callback-url` parameters, including `x-success`. Here's the syntax:

> `workflow://x-callback-url/run-workflow?name=[workflow-name]&input=[text-or-clipboard]`

Check out [Greg Pierce](http://twitter.com/agiletortoise)'s [example](http://drafts4-actions.agiletortoise.com/apps/1945) of how to send the current `[[draft]]` to Workflow, run an action in Workflow, and return to Drafts.

On the other side of the fence, you can also invoke any third-party app using their `x-callback-url` schemes. For example, you can send the current text to Drafts, run an action, and return to Workflow. You can specify `workflow%3A%2F%2F` as the `x-success` and `x-cancel` parameters of the **Open X-Callback URL** action. Unfortunately, there isn't any encoding helper in Workflow at the moment - forcing you manually encode the URL and making it impossible to encode the runtime value using Workflow alone.

Fortunately, we have Launch Center Pro to the rescue. Simply store the runtime value to the Clipboard, and run the following URL Scheme:

> `launch://x-callback-url/clipboard/convert?format=urlencode`

When the action returns to Workflow, you can get the encoded value from the Clipboard, and continue with your action.

I created an Action Extension that receives texts and URLs, and posts them to a Slack channel. For this purpose, I'm reusing my Launch Center Pro action to post to a channel in Slack, combined with an IFTTT recipe to do it.

Open [this link](launch://import?url=launch%3A%2F%2Fifttt%2Ftrigger%3Fname%3D%7B%7BPost%20to%20Slack%7D%7D%26value1%3D%5Bprompt-text%3AMessage%5D&title=Post%20to%20Slack&description=%3Cp%3EThis%20action%20allows%20you%20to%20post%20a%20quick%20message%20to%20a%20Slack%20channel%20you%20access%20most%20frequently.%20Requires%3A%20Launch%20Center%20Pro%202.3%20and%20IFTTT%20recipe%20connecting%20Launch%20Center%20Pro%20and%20Slack.%3C%2Fp%3E%0A) to automatically install this action on your iOS device.

With the new Action Extension in Workflow, I can easily share a URL in Safari or a text from any iOS 8 app to my colleagues via a specific Slack channel.

Open [this link](https://workflow.is/workflows/7069773c168b4c10a6b9e98ee21c1b21) on your iOS device to automatically install the **Post to Slack** action in Workflow.

![](https://static1.squarespace.com/static/54a612bee4b0421d698cf41e/551f548ce4b0f07e37b3a851/551f548ee4b0f07e37b3b2a4/1418315427233/1000w/Workflow07.jpg)

> _You can share your workflow easily from within the app, add it to your Home Screen, create a shortcut for it in Launch Center Pro, or even submit it to the Actions gallery._

### 8\. Sharing Made Easy

Taking hints from Launch Center Pro, sharing your workflow is quite easy. Tap on the `Settings` gear icon to share a workflow. In addition to creating a Home Screen icon or putting it inside Launch Center Pro, you can also export it as a public URL under the following format:

> `http://workflow.is/workflow/uniqueID`

This makes it easier to share on your blog or inside a tweet. If you have a great workflow, don't hesitate to submit your workflow to the gallery. All submissions will be reviewed by the developers and the great ones will be featured in the next update.

### Tips for Creating Your Own Workflows

Even though it's relatively simple to create your own workflows and there are already a lot of documentation built into this app, some of you may find it confusing to create the workflow the way you want it. Hence, I am offering a few tips to save first-timers some time:

  * Use the `[Ask for Input]-[Get Text from Input]-[Set Variable]` sequence to prompt a user for a runtime value and store it in a variable.
  * Use the `[List]-[Choose from List]-[Set Variable]` sequence to show a predefined list of values and prompt the user to select one (or more) and store them in a variable.
  * Use the `[Text]-[Get Contents of Web Pages]-[Get Dictionary from Input]-[Get Value for Key]-[Set Variable]` sequence to get a runtime value from a RESTful API that returns a JSON HTTP Response. Write the complete URL (along with any query string) into the `[Text]` action, before sending the request. 
  * Use the `[Text]-[URL]-[Open X-Callback URL]` sequence to define custom URL Scheme and execute it. Write your URL Scheme in the `[Text]` action, and pass it along to the `[URL]` action as an `Input`, before running it with the `[Open X-Callback URL]` action.

### Conclusion

Workflow is the perfect new app built for the iOS 8 era. It nicely showcases the iOS 8 Extensions by allowing its users to define hooks for the custom Action Extensions, and enabling parts of the workflow to run third-party Extensions. The excellent design makes it easy for anyone to create their own automation workflows without the need for coding savviness. It really is powerful automation made simple. I honestly can't wait to see what others would create with this app.
