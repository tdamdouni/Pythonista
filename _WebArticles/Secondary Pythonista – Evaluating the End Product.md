# Secondary Pythonista – Evaluating the End Product

_Captured: 2015-09-29 at 00:03 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-evaluating-the-end-product/)_

Well, we've come to the conclusion of our _Secondary Pythonista_ series. "Evaluating the End Product" is the title, but if you've been following along at home, you know our script is _not_ complete. In the first part of this article we'll finalize the script. In the second part we'll review what we've done through this series, and where we could go with our little script.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Refining Our Code

Alright, off the bat we have some code clean up to do. We seem to have gotten a little carried away with ourselves in our efforts to just get the data we wanted. There aren't any code comments to speak of, and our output could be a bit cleaner. On top of that we should think about the modularity needed to expand our script out from just fetching data on iPad.AppStorm.

### Commenting Our Code

If you ask any programmer if they value code comments when reading and using another developer's script, you'll probably get an enthusiastic yes. If you ask them how often they comment their own code though, you may get a more hesitant reply. Truth is, code comments are something we love to enjoy in other people's scripts, but we often don't take the time to go back and add in our own scripts.

When it comes to code, the value of comments is in their ability to explain what the code does without you needing to mentally walk through the code in your mind. Instead of examining variables and walking through loops in your mind you can simply review the comment to get a basic understanding of what each part of the code does.

There usually isn't a need to comment on every line in a program. Often times it's enough to use the comments as sign posts laid out at important parts of the script. Another important place to put a comment is when you do something unique or not easily understood in your code. Your solution to a particular programming problem may be creative and efficient, but that also means it may not be easily understood by anyone else -- or even by yourself a few months or years in the future.

So, rather than take you through each comment I make to our script, I'll leave it up to you to follow the suggestions I just mentioned and put some comments where you think they'll be most beneficial.

I will leave you with a small excerpt of what my comments look like though.

![code comments](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product1.jpg)

> _Code comments._

### Add a Network Activity Indicator

Perhaps you've noticed that our script takes a little while to pull the data off the website before processing it. A nice way to give the users of this script an indication that things _are_ happening and the script hasn't crashed is to make use of the iOS Network Activity Indicator. That's a fancy way of saying the small spinning circle that appears in the top left corner of the status bar.

We'll need to import a new module, the _console_ module, to get access to the network activity indicator. From there we'll make two simple calls, the first being _show_activity()_ and the second _hide_activity()_. Now the placement of these two calls could be debated a bit. I believe it makes sense to begin showing the indicator right before we request the page. We could have the indicator cease immediately after that call, as technically the network activity will have ceased at this point. But because the Beautiful Soup parsing takes an additional second or two, I think it makes sense to wait until after the Beautiful Soup parsing has been completed before hiding the indicator.

Here's the code I've added:

![activity indicator](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product2.jpg)

> _Activity indicator._

If you run the script again you'll see our activity indicator appearing soon after the script is launched, then disappearing moments before the code is sent to the console. Excellent.

### Cleaning up the Output

Alright, something else to consider here is the formatting of what we're outputting. At this point it's just a list of information without any real explanation of what it is information _about_. So why don't we see about adding in some descriptions for some of the content, formatting our output a bit better?

If you run the script now and examine the output, you'll see we start off with the date and then dive right into the first article. Doesn't it make sense to have some sort of title area? And perhaps we should differentiate the articles from that title area with some whitespace or some other sort of visual divider?

From there we come to the article title and author information. Those are pretty self-explanatory. I like the idea of maybe adding "by " before the author's name. It gives it a nice touch if you ask me. For the category, tag, and comment information, those should all get labels so we know what they are. As for the summary at the end, that too seems pretty straightforward to me. I don't think it needs any further explanation.

Let's take those changes one by one then. First we have the title information.

Really we just have a _print_ statement at the top of our script to kick things off.

We needed a way of distinguishing the articles from the title area, didn't we? Well let's jump into the loop which outputs our article information and print out a divider at the top.

![adding Daily Report Title](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product3.jpg)

> _Adding the top divider._

![adding top divider](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product4.jpg)

> _Console output to match._

Nicely done. In case you're curious, the "\n" character you see here is the way we refer to a "new line" in code. It allows us to add whitespace to our output.

Onto the author. To add content before we print the author's name, we'll use the following syntax.

![adding top divider](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product5.jpg)

> _Adding "By " to the author._

This is an interesting syntax, and perhaps a little old fashioned. But it's straightforward. We place _%s_ in our string and then following the _%_ put the variable we want _%s_ to replace. If you run the code and examine the output you'll note the "by" right where we want it.

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product6.jpg)

> _Console output with "by" in it._

Using this same technique we'll add in labels for categories, tags, and the comment count.

![adding labels to categories, tags, comment count](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product7.jpg)

> _Adding labels to categories, tags, comment count._

Did you notice I did something a little different with the comment count? Just to mix it up I added "comment(s)" after the number, rather than a label like "Number of Comments:". It helps to break up the monotony of similar information.

There are two more things I noticed that need adjusting. First, there should be a matching divider at the end of the article excerpt. That's a simple enough fix. We'll add a line after we print the article summary. Mirror the syntax we used the first time, a simple _print '\- - -'_ statement will do the trick.

Secondly, we need to establish what site these are from. To do that we'll first need to make our code modular, adding support for the multiple sites we'll be pulling data from.

## Modularity

Technically we could just copy and paste this code we've written thus far multiple times, once for each site we're looking to support. But that's repetitive and difficult to debug. There's a much better way. We'll take the code we need for each site, the code that prints out the relevant articles, and turn it into a function.

To figure out what code needs to be included in the function we need to think about what would need to change. For each site we need a different source page. So our _requests.get()_ call needs to be different each time. But that doesn't mean we need to duplicate that particular line each time. Technically what needs to change is the URL being passed into the _requests.get()_ method.

That's right, we can wrap our entire codebase in a function. We'll call it _fetch_data()_. And since the thing we need to change each time is the URL, well add a parameter to our function called _url_ which we'll pass in when we call it.

Here's what the start of that function would look like:

![calling the fetch_data function](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product8.jpg)

> _Defining the fetch_data function._

The syntax for writing a function uses _def_, short for "definition", followed by the function name and a pair of parentheses. Inside those parens, you define whatever parameters you want your function to have. Finally we have a colon denoting the beginning of the function. The way Python determines what's inside your function is by whitespace. That would be the one part of this process which is frustrating in Pythonista. To put our code inside a function we'll need to go down the whole script and indent the code to make it a part of the function.

Once you finish that we'll then call our function like this:

![our new function definition](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product9.jpg)

> _Calling the function._

If you run the script again you'll see our code output just like before. We've successfully modularized our script. Congratulations.

Before we leverage that, let's address the issue I mentioned earlier, not knowing which site these articles belong to. Why don't we add _site_name_ as an additional parameter to our function. We can then place that site name right before our function divider.

![using site_name](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product10.jpg)

> _Our new function definition._

![our new function call](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product11.jpg)

> _Using site_name._

![the new console output](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product12.jpg)

> _Our new function call._

When we look at our output, the site name is now nicely displayed before each article. Wonderful. The time has come now for us to try the rest of the sites.

![calling the rest of the sites](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product13.jpg)

> _Calling the rest of the sites._

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product14.jpg)

> _Console output to match above._

Interesting. We have ourselves a bug. Instead of appearing just once at the top, our title and date are being printed at the top each time the function is called. And really this makes sense. Our entire script was wrapped in that function, title information included.

Let's pull that section of code out and place it above our function definition.

![moving title info](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product15.jpg)

> _Moving title info._

If we run our script now we'll see it's exactly the way we want. Fantastic!

![moving title info](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130830-Evaluating-The-End-Product16.jpg)

> _Our final output._

## How Far We've Come

Wow. You, dear reader, are to be congratulated. Over the course of this series we went from a blank file to a working script. You've wrangled some Python code and come out on the other side victorious. And to top it all off you've done this on _an iPad_. Who says it isn't for content creation?! The iPad can write respectable computer programs which create content of their own! Extraordinary, isn't it?

## Room to Grow

This does bring us to the conclusion of _Secondary Pythonista_. But it doesn't have to be the end of our humble little script. If our AppStorm Daily Report is something you'd like to make a part of your life in more ways then just an exercise in writing Python on an iPad, consider some suggestions for how this script could be extended:

  * try adapting the script to run on a scheduled basis and trigger a notification alerting you to new articles
  * instead of simply outputting to the console, have the script generate an email which gets sent to your inbox each day
  * leverage Markdown and do even fancier formatting of our content here, perhaps presenting it using the built-in browser rather than just the console

Those are just three suggestions. This is the fun part of programming, let your imagination run wild!

I really hope you've enjoyed my _Secondary Pythonista _series. If you did, sound off in the comments at let us know what you'd like to see in future tutorial series!
