# A better way to view page sources in iOS

_Captured: 2015-11-07 at 00:53 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/09/22/a-better-way-to-view-page-sources-in-ios/)_

With release of iOS 8, the number of imaginative apps that have come out in the last couple of days has been amazing. One of the newly touted apps, [View Source](https://itunes.apple.com/us/app/view-source-html-javascript/id917660039?mt=8&uo=4), is a mix of app and iOS extension that can let a user view the page source of a web page on their iOS device.

![](http://share.mygeekdaddy.me/_img_BLOGX_View_source_in_iOS_2014_09_22_223210.png)

I worked with View Source for a bit over the weekend, but found getting the raw HTML from View Source to an editor app to be a hassle. Federico did a [review on View Source](http://www.macstories.net/reviews/view-source-code-in-safari-with-an-action-extension/) and he came to some of the same conclusions as I did.

> I wish that View Source could do more. Notably, there is no support for search or browsing of specific HTML tags, which combined with the lack of line-wrapping makes it difficult to read source code as you need to constantly scroll horizontally on the screen (especially a problem on the iPhone's smaller screen in portrait mode). I'm hoping that a text reflow mode will be added soon, and I wouldn't mind the more advanced options for viewing source code found in Mac apps such as Coda. 

Looking at the potential of View Source, I started thinking there had to be a better way to do this in iOS.

#### Doing it my own way

In all the gushing over iOS extensions, I think we (or at least I did) forgot our roots in iOS automation. Most iOS apps have a native URL that will allow you to open the app from Safari. One of my favorite apps is [Textastic](https://itunes.apple.com/us/app/textastic-code-editor-for/id550156166?mt=8&uo=4), can [be used to open a webpage to see the source code](http://www.textasticapp.com/v4/manual/x-callback-url.html).

> In addition to _x-callback-url_ support, the textastic:// scheme can be used to easily download the server response of HTTP URLs. You can use this feature to **view the source code of a website** or download files into Textastic. This is what you need to do: 
> 
>   * Make sure your iPad or iPhone has an active internet connection
>   * Open a website in Safari or another browser app like Chrome
>   * Tap on the address bar
>   * Replace http:// with textastic://
>   * Hit Return
>   * Textastic will open and start to download the file at the URL. It will be saved to the root directory in the local file system. When the file is downloaded, it will be opened in the editor.

Now I knew there should be a way to automate viewing a page source with my existing tools. The goal was to find a workflow to take the current URL in Safari, push the URL into Textastic, and do it without having to manually edit the URL address.

#### First attempt

The first way I tried doing this was to use a bookmarklet to parse the URL with a bookmarklet and send it to Textastic.
    
    
    javascript:window.location='textastic://'+encodeURIComponent(window.location.host)+'/'+encodeURIComponent(window.location.pathname);
    

No matter how I tweaked it, Textastic would not open with the bookmarklet. All I got was Safari opening up Textastic. I'm not sure if this was a limitation of how Safari was trying to parse the URL from the bookmarklet or if Textastic wasn't responding to an indirect call from Safari - aka sandboxing.

#### Second time wins

Since the direct the method wasn't working, I fell back on the go to app for iOS automation, Pythonista. I used a similar technique to get the URL to Textastic that I've used to [pass Safari information to Drafts](http://mygeekdaddy.net/2014/02/16/getting-pythonista-to-return-text-back-to-drafts/).

First step is to use a bookmarklet to pass the current URL information to Pythonista:
    
    
    javascript:window.location='pythonista://ShowSource?action=run&argv='+encodeURIComponent(window.location.host)+'&argv='+encodeURIComponent(window.location.pathname)
    

The second step is to use a Pythonista script to pull the two variables passed from the bookmarklet and join them into a URL to pass to Textastic:
    
    
    import webbrowser
    import sys
    
    url = sys.argv[1]
    path = sys.argv[2]
    
    webbrowser.open('textastic://'+url+'/'+path)
    

With one click the URL is passed to Textastic and it opens up with the raw page source HTML.

![](http://share.mygeekdaddy.me/_img_BLOGX_View_source_in_iOS_2014_09_22_220248.png)

Now with the HTML file in Textastic, I have the full resources of Textastic to work with the information as I need.

2014-09-24 Update: I got two responses on getting a javascript bookmarklet to open a URL directly from Safari to Textastic.

A comment from 'Architect' on the post shared the following:
    
    
    javascript:(function()%7Blocation.href='textastic'+location.href.substring(4);%7D)();
    

The other one was a reply via Twitter from Phillip Gruneich ([@Pgruneich](https://twitter.com/Pgruneich)) on [his blog post](http://philgr.com/blog/review-2013-source-codes-in-textastic) of the same topic:
    
    
    javascript:location.href='textastic'+location.href.substring(4)
    

#### Comments from original WP Post:

**[Jason.Verly](http://mygeekdaddy.net/2014/09/22/a-better-way-to-view-page-sources-in-ios/):** I knew there would be a way to get a javascript bookmarklet to work! Thx for passing this along. I'll make an update to the post shortly.

**[Architect](http://mygeekdaddy.net/2014/09/22/a-better-way-to-view-page-sources-in-ios/):** This bookmarklet works for me `javascript:(function()%7Blocation.href='textastic'+location.href.substring(4);%7D)();`
