# Secondary Pythonista: Solving Problems with Python

_Captured: 2015-09-29 at 00:04 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-solving-problems-with-python/)_

Programming languages are practical tools used to solve real-life problems. So naturally, the best way to learn a programming language -- and by extension a programming utility like _Pythonista_ -- is by solving a real-life problem with it. That's what we're going to do here in _Secondary Python_, take an idea for a program, something that solves a problem, and then use Python and _Pythonista_ to build a solution to that problem.

So without further ado, lets examine the project brief.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Our Script: The AppStorm Daily Report

Did you know there are now _[six_ AppStorm sites](http://appstorm.net/)? Yup. That's a lot of posts coming through each and every day. AppStorm certainly provides its readers with [a wide array of options](http://mac.appstorm.net/about/subscribe/) to get updated content as soon as it goes live. But, being a geek, I'm just not satisfied with that, not when I could imagine a different solution to this problem of wishing to be apprised of all these AppStorm posts published each and every day.

Instead, I have a different sort of reading experience in mind. I present to you, The AppStorm Daily Report. This Daily Report would correlate all the AppStorm posts published that day and present some important metadata about the article as well as a brief excerpt.

Let's get a little more specific here.

### The Data Being Displayed

Just what exactly do we want to see in our Daily Report? How much is too much? How much is too little?

Considering the volume of posts published each across all six AppStorm sites, full text of each and every article seems a bit much. Whatever form this Daily Report will eventually take, having thousands and thousands of words doesn't really seem to be the best experience. But now I'm getting ahead of myself. We'll discuss the user experience in a bit. Let's suffice it to say that full articles are not to be included in the Daily Report.

What is then? Some sort of summary seems to be the best choice, doesn't it? A nice middle ground between the full-article and no text what so ever.

If you notice the homepage of [any](http://mac.appstorm.net/) [of](http://web.appstorm.net/) [the](http://iphone.appstorm.net/) [AppStorm](http://ipad.appstorm.net/) [sites](http://android.appstorm.net/) you'll find just the sort of summary we're looking for, one corresponding with each article. Perfect. Now we even know that at least one part of our Daily Report already exists. That will make our job when coding it later that much easier.

I mentioned metadata earlier. Again, referring to any of the AppStorm homepages, you'll see some nice examples of this presented for each article. Title, author, article category, any tags present, or even any comments which have been posted. You may be wondering about the images you also see corresponding to each article. Lets cover that in a moment when we discuss the user experience.

Ok, so, in summary we're looking to compile:

  * all articles published on the AppStorm family of sites for a given day
  * the title of the article
  * the category it is in
  * article tags
  * comments on the article
  * a brief summary of the article

### The User Experience

Let's look for a moment at the user experience. What is that exactly? It's the experience one has when using a program. Thinking about the user experience is critical in crafting quality software. A script or program may succeed in accomplishing all the goals a user may have for it, but if it does so in a complicated, clunky, or even convoluted way, the software will be of little practical use.

People use things which are efficient, functional, even delightful. Things which are low on friction and high on usability.

Now lets apply these ideas to The AppStorm Daily Report.

We're building a new way of reading and reviewing content. This is something designed for content consumption, we aren't looking at excessive elements of interactivity. The emphasis should be on readability. Consider that the content we're compiling is textual in nature. Doesn't it make sense then that our presentation of that content should be designed to make the text shine? Of course.

Hopefully that explains the reason for excluding the image in the metadata which we are compiling. This over-arching idea then will inform further decisions which we make going forward.

As we continue to design our Daily Report, we'll keep these user experience ideas in mind:

  * we want practical, efficient, easy-to-use software
  * a purely text-based product with a design that highlights our textual content

## The Pieces We Will Use

Alright, we have our goals in mind, now what will we use to build this script?

This series is entitled _Secondary Pythonista_ after all, so we'll obviously be using the Python language and the app Pythonista as our development environment. But let's get a little more specific.

We know that we need to fetch data that's on the Web. There are a myriad of different ways to do that though. If we look at the sort of data we want you'll see it's prominently displayed on the homepages of the various AppStorm sites. That means we could make use of an HTML parser like [Beautiful Soup](http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html) to get the data we're looking for. But let's not forget that AppStorm publishes RSS feeds for all of its sites. That means that the [feedparser module](http://omz-software.com/pythonista/docs/ios/feedparser.html) is another valid place to fetch the desired data from.

Interesting, isn't it? We have more than one way to get the desired data. Instead of making the decision on which approach to take right now, we'll examine both modules in more detail during a later article.

What else do we need to achieve our desired end product? In addition to securing a data source, some thoughts need to be given to the form the final product will take. We've already established that it will be purely textual. Therefore we could simply print our Daily Report to the console and consider it done, couldn't we? Well, yes, we could. And for simplicity's sake, that's exactly the premise we will continue to work under: our Daily Report will print its contents to the Pythonista console.

## Our Plan of Attack

So, after looking our project goals over, and thinking about the tools we have at our disposal, it seems our script is practical and plausible. To give ourselves a sense of direction, let's outline a loose plan of attack for this script:

  * fetch the required data from the various AppStorm sites
  * use a module like [Beautiful Soup](http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html) or the [feedparser module](http://omz-software.com/pythonista/docs/ios/feedparser.html) to parse that data
  * output that data in the desired order for ease-of-reading

Looks simple when we put it like that, doesn't it? And really it is. Our script is far from complex. But that was also a very high-level view of the process needed to write this script. We'll be diving into much more detail over the course of this series.

## Next in _Secondary Pythonista_ …

So there we have it. Our project's goals, the sort of user experience we're after, the tools we'll need to build it, and even a basic plan of attack.

Next week we'll look at the two modules we could use to get the data we want in more depth, weighing the pros and cons of each approach, and finally begin writing our script. Stay tuned!
