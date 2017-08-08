# What Should I Learn as a Beginner: Python 2 or Python 3?

_Captured: 2016-06-25 at 22:34 from [learntocodewith.me](http://learntocodewith.me/programming/python/python-2-vs-python-3/)_

![python-2-vs-python-3](http://learntocodewith.me/wp-content/uploads/2014/06/python-2-vs-python-31-780x350.jpg)

What's the difference between Python 2 and Python 3? Or more specifically Python 2.7 and 3.3. (Since those appear to be the main versions in debate.)

Instead of trying to answer this questions myself (a newbie in the world of Python), I decided to turn to the experts…AKA the internet. So, let the great debate begin! _Sarcasm_…it's not too much of a fiery debate.

(Also--there is an update at the bottom of this article, written in more recent times.)

### Python 2 vs. Python 3: Overall Picture

[Wiki.python.org](https://wiki.python.org/moin/Python2orPython3) goes into depth on the differences between Python 2.7 and 3.3, saying that there are benefits to each. It really depends on what your are trying to achieve. But, in summation: "Python 2.x is legacy, Python 3.x is the present and future of the language."

There are subtle differences between the two. But the biggest difference is the print statement.

### What's Different About The Print Statement

Taken from a discussion on [Stack Overflow](http://stackoverflow.com/questions/442352/python-2-vs-python-3-and-tutorial),

> "The most visible (difference) is probably the way the "print" statement works. It's different enough that the same script won't be able to run on both versions at the same time, but pick one and you'll be fine."

A similar view from the Twitterverse:

> [@learncodewithme](https://twitter.com/learncodewithme) The most important change is the print. On Py2, is print "hello" and in Py3 is print("Hello"). >> -- Nikolas Moya (@nikolasmoya) [June 3, 2014](https://twitter.com/nikolasmoya/statuses/473975520527261696)

Essentially, the print statement has been [replaced with a print () function](https://docs.python.org/3/whatsnew/3.0.html).

### Important: Python 2 Has Libraries

So beyond this difference in the print statement, across the web I see lots of mention to the library support in 2.7:

> [@learncodewithme](https://twitter.com/learncodewithme) Also, some libraries (like PyImage), only work on python 2.* versions. -- Nikolas Moya (@nikolasmoya) [June 3, 2014](https://twitter.com/nikolasmoya/statuses/473975702870429696)

More on the Twitterspace, I Tweeted:

> But is it? "Python 3.3: Trust Me, It's Better than 2.7" -> <http://t.co/BIMMyG3Gro> via [@YouTube](https://twitter.com/YouTube) [#letmeknow](https://twitter.com/search?q=%23letmeknow&src=hash) [#python](https://twitter.com/search?q=%23python&src=hash) -- Laurence Bradford (@SEAdevelopment) [June 3, 2014](https://twitter.com/SEAdevelopment/statuses/473963722755411970)

Responses:

> [@SEAdevelopment](https://twitter.com/SEAdevelopment) That is to say few ports of 2.7 to 3.3. Though Arch Linux has set python 3.3 as the default, which is a pain sometimes -- Michael Gattozzi (@mgattozzi) [June 4, 2014](https://twitter.com/mgattozzi/statuses/473990089068908545)

This article on [Medium](https://medium.com/@deliciousrobots/python-3-is-killing-python-5d2ad703365d), mentioned in the Tweet above and titled "Python 3 is killing Python", has a lot of information that goes over my head as a beginner. But it's clear this writer, Stephen A. Goss, is very passionate about **not moving to Python 3** and keeping Python 2 alive. He also points to 3rd party libraries as one of Python 2's greatest strengths.

### Why Some Say Python 3.3 Is Better

In this talk (here's [a video](https://www.youtube.com/watch?v=f_6vDi7ywuA)) Brett Cannon, who works for Python, is all about Python 3.3. He admits off the bat he has an obvious bias. But still has enough to say to fill up a forty minute talk.

Beyond the guy's opinion who works for Python, across the internet I was stumbling upon similar sentiments that I think are expressed well from a discussion I found on [Quora](http://qr.ae/shQ8q):

> "The main advantage of 3.x is that it is on the cutting edge, so all the new features will be implemented in there rather than being added to 2.x. The other thing you may want to consider is that it is the common python of the future, so looking a couple of years down the line, this will be the mature branch that people go to."

Basically, it seems Python 3 is where the future is heading. But Python 2 has far more documentation available.

### As A Beginner, Which Should I Learn?

I'm sure if you're a beginner, like me, you're thinking: "Umm cool. But which should I learn?" Because when you're new to programming, you're still trying to wrap your head around a function. Not deeply analyze the subtleties between versions of the same language.

Found in the same [Stack Overflow discussion](http://stackoverflow.com/questions/442352/python-2-vs-python-3-and-tutorial) mentioned earlier, (however, this time from a different commenter):

> "Python 3 is a nicer and more consistent language, BUT, there is very limited third-party module support for it. This is likely to be true for at least a couple of years more. So, all major frameworks still run on Python 2, and will continue to do so for a significant time. Therefore, if you learn Python today, **you should learn Python 2**, because that is the version you are going to end up actually using."

At the same time, one could certainly start off learning Python 3.3. It is where the language is heading, anyways.

However, I do believe it is wise to start off with 2.7 as a beginner for the main reason that there is far more documentation to help you along the way. Plus computers (well, at least my Mac OS X) come with Python 2.7 built in already. So you don't have to go out and download 3.3.

### Conclusion: Python 2 is the Winner…for now

For now I will continue learning with 2.7. It seems like the differences between 2x and 3x are relatively minor. My main goal is to_ just learn_ a programming language -- I don't want to get caught up in the minor variations between the two versions.

Besides, it seems like both are acceptable.

**UPDATE**: **January 29, 2015:**

As of January 6, 2015:

[The StackOverflow discussion posted above has been updated ](https://stackoverflow.com/questions/442352/python-2-vs-python-3-and-tutorial)to reflect that one **SHOULD start with Python 3 if they are learning today, in 2015.**

Nonetheless, **do your research.** Make your own conclusions about which would be better for you to learn -- depending on what you want to do with the language.

_But if I were to start today learning Python, I'd start with Python 3. _
