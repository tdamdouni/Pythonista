# Python 3 vs Python 2: It’s Different This Time

_Captured: 2017-02-03 at 13:58 from [dzone.com](https://dzone.com/articles/python-3-vs-python-2-its-different-this-time)_

[Start coding today](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) to experience the powerful engine that drives data application's development, brought to you in partnership with [Qlik](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).

A difficult decision for any Python team is whether to move from Python 2 and into Python 3. Although this is not a new decision for Python development teams, 2017 brings with it several important differences that make this decision crucial for proper forward planning. It feels like this is the year that we're really seeing the move to Python 3. It has been a long road, but Python 3 may finally have the upper hand.

## How Did We Get Here?

The different major Python versions have been a divisive issue inside the Python community for a long time. There was a desire by the core team (and creator Guido van Rossum) to improve upon Python 2, but they would have to make changes that would break backward compatibility. As a result, they created Python 3 and it was released in 2008. Nine years later and there are still significant divisions in the userbase between these two major versions of Python. However, reflecting on where we are in 2017, the landscape has changed in favor of Python 3. Examples of this shift can be seen in some of the larger projects, like TensorFlow and Thrift, both adding Python 3 support in the past 12 months.

## The Changing Landscape: The Rise of Python 3

Of the top 360 packages listed on <http://py3readiness.org/>, 95% are Python 3 compatible. Unless you have very specific needs, and you should always check for support of a specific package on [PyPI](https://pypi.python.org/pypi), you will find what you need on Python 3 in 2017.

Python 3 now has over nine years of releases and the core team does a great job of releasing at a steady cadence to progress the language.

We've seen the shift to using Python 3--ActivePython 3 is being downloaded as a higher percentage of our overall ActivePython downloads than at any time in our history. We are also seeing a greater number of customers starting migration projects as well as new projects on Python 3 on a wide variety of platforms. For enterprises, the tide is also turning towards Python 3. Python 2.7, the latest in the 2 series, will only have bug and security fixes going forward. This signals an end to the Python core team's willingness to backport new functionality into Python 2 and thus putting all their energy into the 3 series. 2.7.13 has no scheduled successors [at this point](https://www.python.org/dev/peps/pep-0373/). Remember the 2.7 series first came out in 2010!

## Why Move to Python 3?

So the question is: If you're in a company, at what point do you decide to move on to Python 3?

The official end-of-life date for the Python 2 series is 2020 which means you have three years of support from the community. After that, you'll have to find ways to get support for this series as new vulnerabilities can always arise. Since 2.7.13 is expected to be the last major release in the 2.7 series, new features won't be backported, and only security and bug fixes will be going in from now until 2020. (ActiveState will continue to support the Python 2 series for a very long time, but new language features will be only available in Python 3.)

In addition to the reasons mentioned above, you want to move to Python 3 because there have been a lot of improvements in the language. Probably the biggest reason is integer division which is much simpler and stronger in Python 3. Other reasons include asynchronous support, better exception handling, Unicode support, and you can mix tabs and spaces. Python 3 also gives you function annotations and range memory objects which are significantly more memory efficient.

### Making the Migration…

There are Python packages like Six (we ship this package with our ActivePython distribution) that help companies make that migration, but the nice thing about moving from Python 2 to Python 3 is that the core of the language is quite similar. While there is not too much rewriting, there are items that have to be converted which can be done with the help of migration libraries.

A solid list of the most important changes, put together by Ed Schofield, are here: <http://python-future.org/compatible_idioms.html>

Another issue with moving to Python 3 is that in rare cases the third-party packages that you may rely on aren't available. Make sure you check your packages for compatibility just in case there is a rare show stopper...you want to know that up front.

By making the migration, you'll get better performance and new improvements, an active community working on the save version you are on, and the community has [many helpful resources](https://docs.python.org/3/howto/pyporting.html) to help you cross the road to Python 3.

## Breaking Bad

Although the direction is very positive and the tide is turning in Python 3's favor, we can't ignore that there has been a lot of resistance in the community to move to Python 3. As soon as you break backward compatibility, it is just hard to get the community to coalesce around the new version. It creates quite a bit of friction and it takes many years to resolve.

The bottom line is IT and development managers don't want their older apps to break if they upgrade them--they are providing value just fine with the old code base. If it breaks, it means they need to find the personnel and budget to fix it. There are a lot of enterprises out there with large codebases created by people who are now long gone... and, it's a big deal to assign a resource to upgrade something knowing you take the risk of breaking it. And that's when you get managers in organizations saying, "I just don't want to move versions." They are locked in to the version "forever" (or until they find the application becomes obsolete or the cost to maintain it is greater than the cost to rewrite).

Companies using older versions is not good for the language community because they want to move things along and don't want their language to be known as having large security holes based on these older versions. The community can't continuously be backporting fixes so enterprises must get support to stay on the legacy version or move with the times. The good news is, it is not a rewrite...most of the code will remain the same, and the same great Python developers that built it can be the ones to help migrate it.

[Create data driven applications](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) in Qlik's free and easy to use coding environment, brought to you in partnership with [Qlik](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).
