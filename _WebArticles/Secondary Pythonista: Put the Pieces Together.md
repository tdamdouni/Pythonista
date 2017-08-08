# Secondary Pythonista: Put the Pieces Together

_Captured: 2015-09-29 at 00:03 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-put-the-pieces-together/)_

Hopefully you've been keeping pace with [our new _Secondary Pythonista_ series](http://ipad.appstorm.net/tag/secondary-pythonista/). [In our last article](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-solving-problems-with-python/) we were presented with the project brief for our script. This kind of brief, some sort of starting point, is essential to creating a good script. Without a sense of direction, without a clear goal in mind, the script will be aimless, essentially useless, and may never end up being completed to any functional degree.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

We don't want that kind of future for our script, so we took the goals we had in mind and formulated a plan-of-attack. The goal is to have an AppStorm Daily Report, and to achieve that end result we determined that the following steps were needed:

  * fetch the required data from the various AppStorm sites
  * use a module like [Beautiful Soup](http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html) or the [feedparser module](http://omz-software.com/pythonista/docs/ios/feedparser.html) to parse that data
  * output that data in the desired order for ease-of-reading

I know what you're thinking, the third article into this series and we still haven't written any code! But I think there's an important lesson to be learned in this. Programming is a thoughtful exercise, and it takes time. It's not simply a matter of diving headfirst into a text editor and slinging code around. Just as much time and effort, if not more, needs to be dedicated to thinking about what you _need_ to write your program successfully, determining how to actually do that. Only then are you ready to step into your text editor and start writing that code.

## Fetching Our Data

Alright, first things first, we need data to process. If you remember [from our last lesson](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-solving-problems-with-python/), we're building an AppStorm Daily Report, cataloging summaries of all the articles published on AppStorm for a given day.

Here's specifically what we're looking for:

  * all articles published on the AppStorm family of sites for a given day
  * the title of the article
  * the author
  * the category it is in
  * article tags
  * comments on the article
  * a brief summary of the article

From our plan of attack we realize we have two different Python modules to use to parse the data we receive. Our choice in parsing method actually determines the step before it, how we fetch the data. Why?

Because our two potential parsers need two different kinds of input. [Beautiful Soup](http://omz-software.com/pythonista/docs/ios/beautifulsoup.html) parses raw HTML text while the [feedparser module](http://omz-software.com/pythonista/docs/ios/feedparser.html) parses RSS feeds. This is why we take the time to think through our program before sitting down and writing code. We could devise an ingenious way of accessing the raw HTML of the various AppStorm sites, but if we determine the [feedparser module](http://omz-software.com/pythonista/docs/ios/feedparser.html) is actually the more useful parser, then all that code to fetch raw HTML is for nought.

So lets take a little time now and look at these two modules then, keeping in mind the data we need to compose our Daily Report.

## Examining Beautiful Soup

Beautiful Soup is a Python library which allows you to pull data out of HTML and XML files. It's a very neat tool and one that can help us tremendously in acquiring the data we need to build our Daily Report. How do we know this? Well, [check out the documentation for Beautiful Soup](http://omz-software.com/pythonista/docs/ios/beautifulsoup.html). This is the first place to go when you're considering using a module, a library, or really any piece of code written by someone else. Documentation helps to explain the code, and hopefully _why_ the programmer wrote it in the way they did.

That being said, documentation isn't always of the highest caliber. Bad documentation can lead to incredible frustration and frequently to the pursuit of a different solution to use. Many an open source project has withered on the vine because of insufficient or just flat-out poorly written documentation.

Fortunately that isn't the case here with Beautiful Soup. We'll be referring to the Pythonista version of the documentation here, it removes the mention of custom parsers which unfortunately aren't an option for us when we're developing on iOS and in Pythonista.

Now, looking at that documentation, how then can I say that it will help us in acquiring the data we need? By reading through that Beautiful Soup Guide, specifically [the Quick Start section](http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html#quick-start). If you can, give it a read now.

Back? Ok great. Did you notice towards the bottom? Specifically the tools for navigating the HTML data structure? Pretty cool, right? You can retrieve data based on element name, on attributes associated with those elements, you can even search through the document and retrieve multiple results. Fantastic!

## Examining feedparser

Now lets investigate the feedparser module. You could say that our AppStorm Daily Report is a specialized RSS reader. So in line with that, we have the feedparser module which allows us to parse the RSS feeds for each of our AppStorm sites. Up to now I've been referring you to [the Pythonista documentation](http://omz-software.com/pythonista/docs/ios/feedparser.html) for this module. If you can, open that up and briefly read it over.

Back? Wonderful. Maybe you thought it was a little sparse. From it perhaps you gathered that we could take an arbitrary RSS feed, read it with the feedparser.parse() function, and then in some manner call up the contents of that feed. Let's take a look at some more comprehensive documentation on [the feedparser website](http://pythonhosted.org/feedparser/). In particular we'll look at [the Reference section](http://pythonhosted.org/feedparser/reference.html).

Even a simple review of the Reference section here can reveal to us what we'll have access to. And if you compare it to the list, it seems adequate. We should have access to the date the article was published on, the article title, category and tag information for the article, the author, even a summary of the article. However, it should be noted that one thing we won't have is the number of comments on a given article. That may end up being significant.

## Making a Choice

Well now, it's decision time, isn't it? Recall the limitation we encountered with the feedparser module? It wouldn't give us access to the number of comments on a given article. This is admittedly a very minor issue. How we choose to view this limitation determines what we do next. We could say that it is an acceptable loss and move forward. We could investigate other means of getting just the number of comments on the various articles. Or we could look for another solution to getting all of the data, one that would tell us the number comments as well as all the other information we're looking for.

Considering that the Beautiful Soup module gives us access to _all_ of the data we need in a simple and easy to use manner, we're going to move forward with the Beautiful Soup module in our script.

## Next in _Secondary Pythonista_…

In the next article, we'll look at getting that raw HTML for Beautiful Soup to parse, and begin actually developing our code! Exciting!
