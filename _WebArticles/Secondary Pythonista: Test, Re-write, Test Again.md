# Secondary Pythonista: Test, Re-write, Test Again

_Captured: 2015-09-29 at 00:00 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/secondary-pythonista-test-re-write-test-again/?utm_source=buffer&utm_campaign=Buffer&utm_content=buffer71e0f&utm_medium=appdotnet)_

Welcome to the fourth installment of _Secondary Pythonista_. After careful consideration and research over the last two articles we now have a project brief, a plan of attack, and have chosen the tools we'll need to execute on that plan.

In this article, using the information we've compiled previously, we'll begin executing on those plans. We'll begin writing code in Pythonista. As we do that, the value of all the pre-work that we did will become quickly apparent. There's a strong temptation to dive head-first into writing code, but the careful and methodical approach we've gone with for this tutorial as many benefits, including giving you, dear reader, a better understanding of the _why_ we're programming a certain way in addition to the _how_ to program in that manner.

So let's get to it!

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Prepare A Foundation

Without waiting any longer, let's create a new script within Pythonista.

In the bottom left corner, click the "+" icon and choose the bottom option, "Empty".

![Creating a New Script](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again1.jpg)

> _Creating a New Script_

We'll rename the script by tapping on the name in the center of the toolbar and then tapping on the pencil icon to the right. I've chosen the name "AppStorm Daily Report", but feel free to call it something else if you'd like. We'll use some comments at the top of the script to identify it, give it a brief description too if you'd like. You should have something like what you see below here:

![Code Comments](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again2.jpg)

> _Code Comments_

Alright, not a bad start, huh? Next we'll start accessing the data we need to compile our report.

## Working with the _requests_ module

To access the raw HTML for the various AppStorm sites, we'll employ a module called _requests_. We haven't looked at this module yet. There is some [Pythonista documentation](http://omz-software.com/pythonista/docs/ios/requests.html) describing the functions of this module. If you're interested in some more, including some simple sample code, then you can look at [the official _requests_ documentation](http://docs.python-requests.org/en/latest/user/quickstart/) as well.

Suffice it to say, _requests_ is a full-featured module offering quite a bit of power when it comes to interacting with web services. Our use of it will be quite simple. Start by importing the module for our use.

![Importing the module](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again3.jpg)

> _Importing the module_

We'll now make use of the _get()_ function in the _requests_ module. The page we'll be fetching, for now anyway, will be the iPad.AppStorm homepage. Let's store the data from the iPad.AppStorm homepage in a variable called _page_.

![Fetching the page.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again4.jpg)

> _Fetching the page._

Next we'll try printing the fetched data into the console.

![Outputting to the console](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again5.jpg)

> _Outputting to the console_

If you're confused by the _page.text_ section, take a look at [the _requests_ documentation](http://omz-software.com/pythonista/docs/ios/requests.html). That explains that the _text_ method of the _requests.Response_ object contains the content of our _get()_ request. In other words, we just got access to the raw HTML in unicode. The _print_ statement allows us to verify the data by having it sent to the console.

Alright, not too bad. With 3 lines of code we've gained access to the raw HTML we'll need to compose our Daily Report. Next, we'll parse this data using Beautiful Soup.

## Parsing our Data With _Beautiful Soup_

Lets go back up to the start of our document and import the Beautiful Soup module.

![Importing Beautiful Soup](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again6.jpg)

> _Importing Beautiful Soup_

Now that we have Beautiful Soup at our disposal, we'll begin extracting the data we need. To do this we'll be creating a new variable to store the data in, the data that's been run through the Beautiful Soup constructor. I'm going to call it _soup_.

Because the previous _print_ statement was simply for verification purposes, I've removed it, and in its place we have the statement creating our new _soup_ variable. We can verify that the _soup_ variable has been created properly by calling one of its methods. We'll add a _print_ statement that prints the cleaned up plain text of the page, removing all of the HTML elements.

![A new print statement.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again7.jpg)

> _A new print statement._

If you run the script again now, you'll see some potentially odd output, but the text is now stripped of its HTML tags, leaving just the content.

![Plain text output.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again12.jpg)

> _Plain text output._

Excellent. Time to start pulling the data we want and stuffing it into some variables, isn't it? Just to keep our memories fresh, let's look over that list of the data that we want again:

  * the title of the article
  * the author
  * the category it is in
  * article tags
  * comments on the article
  * a brief summary of the article

Something else of note is the date that a given article was published on. We've sort of been glossing over that, the fact that this is a _daily_ report, as in we only want content from today. There are really two problems which need solving here. The first, is how we find the date which corresponds to the article and by extension the data we're pulling. The second is how do we determine what the date is via Python?

### A Little Outside Help

Well, before I give you the answer to the first question, I have a bit of a confession to make. To actually scour the raw HTML of the iPad.AppStorm homepage, I've used the Developer Tools within Chrome. There's still no good way to do this sort of thing solely on an iPad. If you're unfamiliar with the Chrome Dev Tools, then I recommend giving [the Chrome Dev Tools series on Net.Tutsplus](http://net.tutsplus.com/tutorials/tools-and-tips/chrome-dev-tools-markup-and-style/) a read. That being said, I'll tell you now that the date is stored in a _span_ tag with a class of "author_meta". It is also in the format of "Month, Day, Year".

### Formatting Dates with Python

Onto the second problem, how do we get today's date in Python, specifically in the format we need to match the one found on the AppStorm homepages? That's an interesting problem. We can use the _datetime_ module to get the date, specifically the _strftime()_ method to get it in the right format. Formatting dates in code can seem like black magic to many a beginning programmer. [Give this documentation](http://omz-software.com/pythonista/docs/library/datetime.html#strftime-strptime-behavior) a read. It helps explain what those obtuse codes used in the _strftime()_ method. So lets write up the code to get today's date formatted the way we need, importing the datetime module, storing the formatted date in a variable, and then throwing a _print_ statement at the end to verify our code.

![Formatting today's date](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again8.jpg)

> _Formatting today's date_

If you run that code you should see the date output to the console looking like this: "August 23 2013″. Well now that isn't' quite right, is it? AppStorm actually has the date in this format: "August 23rd 2013″. Huh. Interesting. Python has no native way to programmatically format the date with a suffix like that. What are we going to do?

As we've already seen in this series, there's often more than one way to solve a problem we encounter when programming. If you do some Googling, you may come across [this Stackoverflow question](http://stackoverflow.com/questions/5891555/display-the-date-like-may-5th-using-pythons-strftime/5891598#5891598). It contains one potential solution, one which would get today's date formatted with the suffix. But I'd like to explore another potential solution, one that involves how we extract the date from the page.

### Pulling the Articles Dates from the HTML

Lets try pulling the date out from the page with Beautiful Soup. I mentioned that it's contained within a _span_ tag with the class of _author_meta_. Take a look at the code below for a minute, review it, and then we'll go over it line by line:

![Loop over the fetched dates.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again9.jpg)

> _Loop over the fetched dates._

The piece of our code begins with a _for_ loop. We're finding all of those _span_ tags that I mentioned contain the date. The next line assigns the content of that _span_ tag to a variable, and the line after that splits that variable into a list. We want the content of the _span_ tag in a Python list because then we're able to pick and choose what parts of the content we want to keep. The _span_ tags' content is consistent: the first and last name of the author, the word "on", and the month, day with suffix, and year that the article was posted on.

The next line is selectively accessing words from the _span_ tag. Notice the _[x]_ syntax? This is the way to access sections of a list in Python. Lists are powerful tools, as is demonstrated in the second argument we have here. It is _author_plus_date_list[4][:-2]_. That may seem confusing to you. Let me try to explain. We're accessing the fourth section of the list, in this case it happens to be the day with suffix. _[:-2]_ is being used to eliminate the last two characters from the day with suffix string. Yes, that's right, you can manipulate individual strings as though they were lists of characters. Pretty cool, isn't it? Finally we're joining our list together so it forms a complete string. When the cleaned up dates are printed out to the console you'll find that the syntax matches our formatting of today's date as well.

Now, this piece of code is a bit more complex then the other code we've written thus far. It makes use of list manipulation which may be a difficult concept for a beginning programmer to grasp. I recommend taking these lines one by one and printing the output of each new variable assignment. Try and ascertain the effect that each line is having on the data we are working with.

### Making Use of These Dates

Recall what the purpose in ascertaining the date was again? To ensure that we're processing data for articles that have been published on today's date. As of right now all we really have is a list of the dates listed on the iPad.AppStorm homepage. So we still have two more problems to solve, the first being how to use the date to give us a way to identify the article it corresponds with, and the second being to eliminate the unneeded data published on a different day.

We'll tackle the process of using the date as a means to identify the article itself first. The HTML element which contains the date is buried inside a _div_ with a very useful _id_ attribute. These _div_s contain post ids which we can use to reference the data we'll be picking from later. Using the _parent_ method from _Beautiful Soup_, we'll navigate our way back up to the _div_ with the post id and then save that id into a variable.

Take a look at the code below:

![Storing the article_id.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again10.jpg)

> _Storing the article_id._

We've added two lines to our loop. If you run the code now you'll see that a post id is now outputted to the console as we loop through. Very nice. Now to compare the dates and discard the rest.

![The todays_articles list.](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130823-Test-Re-write-Test-Again11.jpg)

> _The todays_articles list._

Looking at the above code you can see some changes. We've removed the _print_ statements from within the _for_ loop. Just outside the _for_ loop we're creating a variable called _todays_articles_ which is going to be a list of the articles published today. At the end of the loop we've added an _if_ statement which checks today's date with the date within the loop. If it matches then we add it to the _todays_articles_ list. Finally we're printing out the _todays_articles_ list to the console to verify our changes are correct.

## Where We're At

Ok, so where does all this bring us? We've created a new script, named it, and imported the modules we'll need. We then fetched the page we wanted, parsed it with _Beautiful Soup_ for future use, and properly formatted the date. That properly formatted date, used in conjunction with a modified version of the date found on the AppStorm homepage, let us determine which articles were published today. From there we built a list containing the post ids for the articles we were looking for. That list can now be used to pull all the data we need to build our Daily Report. And that's exactly what we'll do in our next article.
