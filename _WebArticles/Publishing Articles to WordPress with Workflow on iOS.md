# Publishing Articles to WordPress with Workflow on iOS

_Captured: 2015-11-24 at 20:51 from [www.macstories.net](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/)_

![Posting to MacStories with Workflow.](https://2672686a4cf38e8c2458-2712e00ea34e3076747650c92426bbb5.ssl.cf1.rackcdn.com/2015-11-24-125421.jpeg)

> _Posting to MacStories with Workflow._

For the [past two years](https://www.macstories.net/stories/editorial-for-ipad-review/), I've been publishing articles and linked posts on MacStories via [Python](https://docs.python.org/2/library/xmlrpclib.html). This inelegant solution was my only option to automate the process of publishing directly from [Editorial](https://itunes.apple.com/us/app/editorial/id673907758?mt=8&uo=4&at=10l6nh&ct=ms_inline) (most [recently](https://www.macstories.net/ios/markdown-and-automation-experiments-with-1writer/), [1Writer](https://itunes.apple.com/us/app/1writer-note-taking-writing/id680469088?mt=8&uo=4&at=10l6nh&ct=ms_inline)): when it comes to writing on iOS, I'm too fussy to accept primitive copy & paste into WordPress' [official client](https://itunes.apple.com/us/app/wordpress/id335703880?mt=8&uo=4&at=10l6nh&ct=ms_inline). Despite its minimal GUI, crude Python code, and lack of advanced features, my 'Publish to WordPress' script served me well for two years.[1](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/) 99% of my MacStories articles since late 2013 have been published with it.

Still, I knew that something better would come along _eventually_. When the [Workflow](https://itunes.apple.com/us/app/workflow-powerful-automation/id915249334?mt=8&uo=4&at=10l6nh&ct=ms_inline) team pinged me about a new action they were developing to enable WordPress publishing from the app, I couldn't believe they were considering it. Workflow, an app that [I employ on a daily basis](https://www.macstories.net/tag/workflow/) to speed up core parts of my job, combined with the single task that powers my entire business - posting new content. It was almost too good to be true.

Fortunately, great things do happen in the third-party iOS ecosystem. Today's update to Workflow (version 1.4.2) adds, among more actions, a brand new WordPress action to publish posts and pages to configured WordPress blogs (both wordpress.com and self-hosted ones) and which can be combined with any other existing action or workflow for deeper automaton. After using a beta of this action for the past few weeks, I can say that it's, by far, the best automated publishing workflow I've ever had, and I don't want to go back to anything else.

## Post to WordPress

With the new Post to WordPress action, the Workflow team has taken parameters for posts, pages, and media that you can post to a WordPress blog and they've enabled them as fields in a single action that's completely under your control.

![](https://2672686a4cf38e8c2458-2712e00ea34e3076747650c92426bbb5.ssl.cf1.rackcdn.com/2015-11-24-125751.jpeg)

The action is split in two categories - basic settings and Advanced options. For any new item, you can configure:

  * Title
  * Type (post, page, media)
  * Format (see list of WordPress formats [here](https://codex.wordpress.org/Post_Formats))
  * Status (published, draft, pending review, private)
  * Categories
  * Tags

If you want more control, you can tap on 'Advanced' and set up the following:

  * Slug
  * Excerpt
  * Publish Date
  * Featured Image
  * Custom Fields

The action accepts text, rich text, and images as input; you can configure multiple WordPress accounts in the action's settings by tapping the gear icon next to its name.

With the WordPress action, the Workflow team has opened up the app to the [biggest publishing platform](http://ma.tt/2015/11/seventy-five-to-go/) on the Internet, leveraging its integration with iOS and third-party apps to allow users to post content no matter the text editor they use. Unlike other WordPress clients that came before it[2](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/), the action offers a good selection of parameters that can be changed manually and programmatically: in my case, featured image, slug, and custom fields are values which I was never able to fully automate in Python and which I couldn't find in third-party apps that only offered basic WordPress integration.

The Workflow team has worked hard to build a WordPress action that can fit a lot of user needs at once: while I may require traditional post types with a single custom field, perhaps you need to publish asides to WordPress with three custom fields and a custom slug set each time. This action can do all that, with _automation_.

The important aspect to note here is that every field in the action can be integrated with variables or user input from a workflow. Want your post's title to be the contents of the iOS clipboard? Just use a `clipboard` variable in the Title field. Need to choose from a list of URLs for a custom field? Show a list in Workflow and tap your choice. Want to type an excerpt manually? Use an 'Ask When Run' token and you'll get a native input field upon running the action.

I've always dreamed of having a visual WordPress action that mixed the benefits of automation and GUIs while eschewing the complexity of Python code. Workflow's WordPress action is what I've been looking for, and, more importantly, it makes WordPress blogging integrated with iOS thanks to the app's extension, enabling all kinds of users and apps to take advantage of it.

## My 'Publish to WordPress' Workflow

As I've [teased](https://www.macstories.net/ios/markdown-and-automation-experiments-with-1writer/) in some articles over the past weeks, I've been using the new WordPress action to publish content to MacStories in a semi-automated fashion that doesn't involve manual interaction with the WordPress admin interface or Python.

I've come up with a workflow to integrate 1Writer with WordPress via Workflow, but you can use any other text editor (as long as it implements the iOS share sheet). Thanks to Workflow's open approach, you can set the action to receive input from its extension or get text from the system clipboard. If you don't want to use anything else to write, you can even type your posts in a text field in Workflow.

In my case, the first order of business was coming up with a way to send the text _and_ file name of a 1Writer document [to Workflow via URL scheme](https://workflow.is/developer). As we've seen before, 1Writer offers good flexibility with [JavaScript actions](http://1writerapp.com/docs/js), which allowed me to put together this bit of code to accomplish what I needed:
    
    
    title = title.substring(0, title.length - 4)
    

You may be wondering why I chose a JavaScript action instead of calling the Workflow extension. The reason is twofold: 1Writer doesn't seem to offer a way to share plain text with the iOS share sheet (it shares a plain text _file_, which I don't want), and I need to share the contents of the file and the file name simultaneously. With JavaScript, I can set the iOS clipboard to the name of the file, remove '.txt' from it, and send the document's text to Workflow.

You can download the action [here](http://1writerapp.com/action/69368), but keep in mind that you may need to tweak it if you use a different file extension or workflow name. If you don't use 1Writer, the basic steps (copying the future post's title to the clipboard first and sending text to the Workflow URL scheme) will work for other iOS apps like Editorial and [Drafts](https://itunes.apple.com/us/app/drafts-4-quickly-capture-notes/id905337691?mt=8&uo=4&at=10l6nh&ct=ms_inline), too.

The real fun happens in Workflow. First, the article's text is saved to a variable and previewed with Quick Look to make sure that everything looks good.[3](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/) Next, the workflow fetches the post's title from the clipboard, runs it through Brett Terpstra's [Title Case API](http://brettterpstra.com/titlecase/) (a work in progress, but it already works very well), and displays an alert to confirm that the title looks okay (the title is editable so you can make changes if you want). The title is then saved to another variable.

At this point, the workflow takes a turn for my specific needs. I publish two types of articles to MacStories: regular posts (such as this one) and [linked posts](https://www.macstories.net/category/linked/). Both are post types according to WordPress, but the linked ones use a custom field to set the external link parameter that makes their titles clickable when pointing to another website.

![Choosing from a list of URLs for a linked post on MacStories.](https://2672686a4cf38e8c2458-2712e00ea34e3076747650c92426bbb5.ssl.cf1.rackcdn.com/2015-11-24-130523.jpeg)

> _Choosing from a list of URLs for a linked post on MacStories._

Because I want to choose whether a post is a regular post or a linked one, I put in a choice in the workflow that takes a different route depending on what's picked. If it's a linked post, the workflow asks me to select a URL for the custom field by listing all URLs found in the document (I always repeat the destination URL in the body text) and then uses that value for the custom field when posting to WordPress. Note how a routine that would take a few lines of regex and custom UIs in Python - scanning text for URLs and displaying them in a list - can be done with two drag & drop actions in Workflow.

If the post is not a linked one, I pick 'Normal' and the workflow posts my document's text to WordPress as a regular post.

The best part of this action - and the biggest difference with my old Python script - is performance: Workflow can fetch dozens of categories and hundreds of tags in a couple of seconds, and by using an 'Ask When Run' variable I can make sure I choose these taxonomy values from a searchable list every time.

Those who don't use WordPress on iOS won't see this new action as a big deal. But if you, like me, have been looking for a solution to integrate WordPress publishing at a system level because you've always been unhappy with WordPress clients on iOS, you can see why this is an important addition to the blogging workflows of iPhone and iPad users. With a single action and through the automation engine of Workflow, I can now publish content to my site from _anywhere_ on iOS; if I decide to stop using 1Writer for Editorial or any other text editor, that won't affect my ability to automate WordPress publishing as I long as I have Markdown. That's the freedom of plain text and iOS extensions.

Workflow's WordPress action is now powering my iOS blogging setup, which is faster and more reliable than ever. You can download my workflow [here](https://workflow.is/workflows/fbfb8b61e04b48b79adc3045ccaeea7f).

## Other New Features

In addition to WordPress, Workflow's latest update brings some nice changes to actions for Messages, iCloud, Slack, Notes, and more.

For Slack users, the good news is that Workflow can keep multiple accounts signed in, so you'll be able to create blocks of actions to post in different teams within the same workflow. Messages and Mail actions can now open their respective apps when activated from the widget. This has been particularly useful for messages I always send at a certain location or time of the day (such as texting my girlfriend after I've gotten home), as I can open a pre-filled iMessage conversation from Notification Center.

![These message templates now open the Messages app directly.](https://2672686a4cf38e8c2458-2712e00ea34e3076747650c92426bbb5.ssl.cf1.rackcdn.com/2015-11-24-125930.jpeg)

> _These message templates now open the Messages app directly._

The 'Create Notes' action is also capable of attaching files to Notes now - a welcome improvement considering the app's [Attachments Browser on iOS 9](https://www.macstories.net/stories/ios-9-review/8/#attachments-browser).

Speaking of files, the most notable change is in the Get File and Save File actions, which can save files in Workflow's local iCloud container and retrieve them programmatically. While saving and retrieving files was possible before with Dropbox and other services, iCloud's native integration on iOS lets Workflow save files even when offline and upload them once an Internet connection is available.

While I won't be using these actions much (I don't trust iCloud Drive for critical work files), they open up some interesting use cases for a permanent local/remote storage location implemented in workflows (Workflow's Ari Weinstein mentioned creating a clipboard manager based on this; imagine storing text snippets, addresses, or other user data in text files stored in Workflow's iCloud folder _and_ accessible from iCloud Drive).

### My Most Used Workflows

A few readers have asked me to share my most used workflows, so I thought I could have a brief recap for those who missed my previous coverage of Workflow (you can read all my posts [here](https://www.macstories.net/tag/workflow/)).

  * [Combine Images](https://workflow.is/workflows/b691234488564da5bab2afc9d74f1228) - Combine screenshots in a single image, placing them next to each other. Can be used from the extension in Photos.
  * [Clipboard Image](https://workflow.is/workflows/2b7e714623194945a2cda09658721e80) - Given an image copied to the system clipboard, this workflow offers to share it with extensions. Useful to share images copied from the web or spreadsheets without saving them to Photos first.
  * [Simple URL](https://workflow.is/workflows/b5b8991beaaf4ed0858d8e610a945f5a) - Expand a URL previously copied in the clipboard until it's unfurled.
  * [MD Selection](https://workflow.is/workflows/2e100ac7e0e04bef8d50d4ba442c4419) - Convert a webpage selection in Safari to Markdown and copy it to the clipboard. To be used in combination with [this Pythonista script](https://gist.github.com/3b332dfb00a1ca67f230).
  * [Linked Selection](https://workflow.is/workflows/9e94c2d038bb4655bf7c6c2cc53967f0) - Create a new file in 1Writer with quoted text from a webpage selection in Safari. To be used with the Pythonista script mentioned above. Action detailed [here](https://www.macstories.net/ios/markdown-and-automation-experiments-with-1writer/).
  * [Extract Image Links](https://workflow.is/workflows/998a6d84c0dd400c8e6081eb810259e0) - Display a list of all image URLs found on a webpage, and copy the selection.
  * [Events](https://workflow.is/workflows/7820316fbf664817874e230a932fe2dd) - Display a list of upcoming calendar events. Can be used in Notification Center as a widget.
  * [Resize Safari Image & Share](https://workflow.is/workflows/d93e23c92487464a9998096d6feaabcd) - Outputs a smaller version of an image selected in Safari. I use this for thumbnails in MacStories' featured posts.

Furthermore, [Club MacStories members](https://www.macstories.net/club/) will be able to access a new 'Workflow Corner' section in MacStories Weekly, starting this week.

In the new section, I'll be taking workflow requests from members looking for ideas or inspiration for their iOS workflows. It'll have a special focus on Workflow, but it'll also include general questions about iOS productivity apps. Workflows and content shared in this section will be exclusive to Club members.

If you're a member, you can send in your questions at the same email address used for Weekly Q&As. If you're not a Club MacStories member yet, [you should consider becoming one](https://www.macstories.net/club/).

## A Workflow for Blogging

In [just a year](https://www.macstories.net/reviews/workflow-review-integrated-automation-for-ios-8/), Workflow has become the centerpiece of my iOS writing and blogging workflow. I use it to create linked posts thanks to its Safari integration, and I've run its extension thousands of times in Photos to assemble screenshots for MacStories reviews. Now, I can use Workflow to communicate with WordPress and publish posts in seconds, with automated rules and conditions that save me time every day. I've been [trying to do this for a long time](https://www.macstories.net/reviews/blogsy-a-better-blogging-app-for-ipad/). Workflow can't access the full stack of WordPress functionalities yet (such as updating an existing post), but its integration is off to a great start.

In a way, Workflow has become the [Minecraft for productivity on iOS](https://twitter.com/viticci/status/668810854297653249): not an oxymoron, but a playground where building blocks can be mastered and remixed, personalized and shared with others. The Workflow team is continuing to iterate on their original vision. They're not stopping, there's more to do, and their app keeps getting better.

Workflow 1.4.2 is [available on the App Store](https://itunes.apple.com/us/app/workflow-powerful-automation/id915249334?mt=8&uo=4&at=10l6nh&ct=ms_inline).

  1. Programmers wouldn't like looking at my code. And yet, it did its job for over two years. There's an argument about practicality to be made here. [↩](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/)
  2. It'd be nice to have proper (Multi)Markdown previews with HTML and syntax highlighting options here instead of plain text shown in Quick Look. [↩](https://www.macstories.net/ios/publishing-articles-to-wordpress-with-workflow-on-ios/)
