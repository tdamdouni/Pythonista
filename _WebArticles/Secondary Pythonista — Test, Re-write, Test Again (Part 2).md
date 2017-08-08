# Secondary Pythonista — Test, Re-write, Test Again (Part 2)

_Captured: 2015-09-29 at 00:02 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/secondary-pythonista-test-re-write-test-again-part-2/)_

In [our last _Secondary Pythonista_ article](http://ipad.appstorm.net/how-to/secondary-pythonista-test-re-write-test-again/) we covered a lot of good ground. We went from no written code to a working script which collects ids corresponding to the articles we're looking to compile. And it's all been with less than 30 lines of code. Pretty fantastic.

But we still have a ways to go before we can consider our script even remotely "finished". Today we'll start harvesting the output we want to compile, storing it in the best manner possible to be retrieved later, all with a view towards final output.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## Using the _todays_articles_ List

At the conclusion of the last article we had a list containing something we're calling a _post id_. I figured out this was useful from an examination of the raw HTML using the Chrome Dev tools. If all this is confusing to you, [give our last article a read](http://ipad.appstorm.net/how-to/secondary-pythonista-test-re-write-test-again/).

How exactly will this _todays_articles_ list be useful? Well, in Python we'll loop over its contents and act on the data we find with the help of that _post id_. Let me try explaining this with showing rather than telling. Take a look at the code below:

![The todays_articles loop](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again1.jpg)

> _The todays_articles loop_

We've removed the _print todays_articles_ line and in its place we have a _for_ loop. This loop is going through the _todays_articles_ list and assigning the value it's using each time to the variable _post_id_. We're then searching through the HTML for the element with an id corresponding to the _post_id_.

The rest of the code following that is a fancy way of printing out our data for verification. There are newer ways of formatting strings for presentation but I've gone with a simple, if not old fashioned, way of doing so using the "%" character. [Here's some Python documentation which explains this a little better](http://docs.python.org/release/2.5.2/lib/typesseq-strings.html), including all the different conversion types you can use. Since we're working strictly with strings we'll be using the "%s" syntax.

If you run this code now you'll see we've successfully isolated the desired element, as well as the elements contained within it.

![console output from todays_articles loop](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again2.jpg)

> _The console output from todays_articles loop_

## Pulling the Needed Data

Let's move forward now and start pulling some more specific data out. We'll take them one by one.

### The Article Title

First let's extract the article title. From examining the HTML, we've determined that the title is found within our HTML segment in an _h1_ tag. Let's search it using the _Beautiful Soup find()_ method and print the results to verify.

![finding an h1](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again3.jpg)

> _Finding an h1_

![the console output from the search](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again4.jpg)

> _the console output from the search_

Well that's not too bad. It's definitely the data we wanted, but it still has all those pesky HTML tags in it. Let's strip those out like we have done before with the _get_text()_ method.

![adding the get_text method](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again5.jpg)

> _Adding the get_text method_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again6.jpg)

> _Console output to match_

Ah! There we have it. Much better, wouldn't you say? We now have the title -- let's move on from there.

### The Author

Next we'll pull out the author. From the HTML, you'll see somewhat buried inside an _a_ tag with the author's name inside it. What we'll use to distinguish it is the _rel_ attribute on the _a_ tag. It has the value of "author". Beautiful Soup's _find()_ method allows us to pass in what's called a _keyword argument_. It acts as a way to access elements based on their attributes. So we'll pass in _rel='author'_ to get the particular _a_ tag we want.

Like we learned in fetching the article title, we will need to use the _get_text_ method to pull just the text out of the HTML. You'll also see a print statement for verification at the end.

![finding the author](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again7.jpg)

> _Finding the author_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again8.jpg)

> _Console output to match_

### The Article Category

Let's move on to the article's category. Like the author information we just retrieved, we'll acquire the category that the article belongs in by means of a _rel_ attribute on an _a_ tag. Same as before, using the _get_text()_ method and a _print_ statement to finish.

![find the category](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again9.jpg)

> _Find the category_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again10.jpg)

> _Console output to match_

OK, things look good, as expected, right? Well, not quite. Perhaps you noticed that the first article in our list, the [Dropcam review by Phillip Johns](http://ipad.appstorm.net/reviews/utilities-reviews/dropcam-drop-in-from-anywhere/), has two categories associated with it. When you view it on the website you can see that, it's "Hardware \ Utilities". Well we wouldn't want to lose that data now would we?

Right now we're using the _find()_ method when it looks like we need to be using the _find_all()_ method, giving us more than just one result. Let's replace _find()_ with _find_all()_. Then we'll run our code again and examine the output.

![using find_all](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again12.jpg)

> _Using find_all_

![error message](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again11.jpg)

> _The error message_

Oops.

Did you notice that? We have an error. Looks like we can't use our _get_text()_ method anymore. Now this makes sense, because we know from our use of _find_all()_ earlier in our script that it returns a list. So, we'll need to do the same thing we did earlier when looping through the articles on the page. We'll create a new _clean_categories_ list for us to populate, a _for_ loop to traverse the _article_category_ list, and now using the _get_text()_ method throw a cleaned up version of the category into our _clean_categories_ list. Finally we'll print out _clean_categories_ for verification.

![clean_categories list](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again13.jpg)

> _clean_categories list_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again14.jpg)

> _Console output to match_

OK, we're getting there. We still have a list which needs to become a string. And in the case of there being multiple categories, we want to join them in a manner which is similar to their presentation on the AppStorm homepage. Why don't we try using the _join()_ method to do this. We'll join them with a "/".

![join statement](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again15.jpg)

> _join statement_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again16.jpg)

> _Console output to match_

Nicely done! This is really starting to take shape, isn't it? Let's move onto tags next.

### The Article Tags

Now, when it comes to the tags, we'll be grabbing them based on a class. We've learned the trick of finding an element based on its attributes, but with classes it's a bit different. You see "class" is a reserved word in Python. So Beautiful Soup gives us the ability to target an element based on its class by using the _class__ keyword. So we'll be finding a _ul_ tag with the class of _tags_. Let's start there, printing it out for verification.

![finding tag ul](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again17.jpg)

> _Finding the tag ul_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again18.jpg)

> _Console output to match_

Alright. So we can clearly see that once again, further processing will be needed to get the plain tag info that we want. We'll need another _for_ loop to cycle through the _li_ elements within the _ul_ we just selected. We'll also need to access the text within, not the _li_ element but what's in the _a_ tag within the _li_ element. Like we've done before we'll create a _clean_tags_ list to store this info in. For clarity's sake why don't we rename the variable containing our _ul_ to _tag_list_. Makes a little more sense -- at least it does to me.

![new tag for loop](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again19.jpg)

> _The new tag for loop_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again20.jpg)

> _Console output to match_

Did you notice we did something interesting when we built our _tag_list_? We chained together a _find()_ method with a _find_al()_ method. Chaining together these methods limits the field of their search. It's an efficient way of selecting a particular element of series of elements.

Now that we have our cleaned up list of tags, why don't we join them together like we did with the categories. Except instead of a "/" we'll use a ",".

![cleaned up tag output](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again21.jpg)

> _cleaned up tag output_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again22.jpg)

> _console output to match_

Excellent! On to the comment count.

We'll be accessing the number of comments for the page by using the same "find by class_" _method we used when grabbing the tags_. _Then we'll finish it off with the_ gett__ext()_ method and a print statement. Seems to be getting pretty standard at this point, isn't it? Hope you're getting the hang of this.

![comment count](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again23.jpg)

> _The comments count_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again24.jpg)

> _Console output to match_

### The Article Summary

Last but certainly not least we have the article summary. At this point I'm almost inclined to just have you figure it out on your own. We'll be targeting the data within a _div_ element with a class of "entry". _get_text()_ and _print_ are your friends as usual.

![article summary](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again25.jpg)

> _The article summary_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again26.jpg)

> _Console output to match_

Did what you program match what we see above? Great. Now, we could leave it right here. But, considering how simple that was for us after doing it so many times before, why don't we try something else here. That "(more…)" line is at the end of every article summary. On the homepage it's a link to the main article. Here in our world of plain text, it's just redundant.

Fortunately we can target that link with the class "more-link". To remove it though we'll use a new method called _decompose()_. It takes the element we've targeted and completely removes it from the HTML.

![adding decompose line](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again27.jpg)

> _Adding the decompose line_

![console output to match](http://cdn.appstorm.net/ipad.appstorm.net/ipad/files/2013/08/130828-Test-Re-write-Test-Again28.jpg)

> _Console output to match_

Sweet. One line to fix that pesky "(more…)" line.

## Where We're At

Now, we've made a tremendous amount of progress here. We've collected together all the information we want. But, it isn't in the most readable layout. And our code has succumbed to our enthusiasm. It could use some comments to properly explain what's where for future debugging purposes, and frankly just because it's good practice. We also have to consider that our script right now is simply outputting data from iPad.AppStorm. We have five more sites to care for. To do that in the most efficient way possible, we'll need to make our code more modular and start utilizing some custom functions.

In our next article we'll address all these issues.
