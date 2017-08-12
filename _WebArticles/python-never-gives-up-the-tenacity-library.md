# Python Never Gives Up: The tenacity Library

_Captured: 2017-03-08 at 09:15 from [dzone.com](https://dzone.com/articles/python-never-gives-up-the-tenacity-library?oid=twitter&utm_content=bufferc6eac&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer)_

Discover [how to focus on operators for Reactive Programming](https://dzone.com/go?i=190137&u=https%3A%2F%2Fblog.wakanda.io%2Freactive-programming-operators%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral) and how they are essential to react to data in your application. Brought to you in partnership with [Wakanda](https://dzone.com/go?i=190137&u=https%3A%2F%2Fblog.wakanda.io%2Freactive-programming-operators%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral).

A couple of years ago, I [wrote about the Python _retrying_ library](https://julien.danjou.info/blog/2015/python-retrying). This library was designed to retry the execution of a task when a failure occurred.

I've started to spread usage of this library in various projects, such as [Gnocchi](http://gnocchi.xyz), these last few years. Unfortunately, it started to get very hard to contribute and send patches to the upstream _retrying_ project. I spent several months trying to work with the original author. But after a while, I had to come to the conclusion that I would be unable to fix bugs and enhance it at the pace I would like to. Therefore, I had to make a difficult decision and decided to fork the library.

## Here Comes _tenacity_

I picked a new name and rewrote parts of the API of _retrying_ that were not working correctly or were too complicated. I also fixed bugs with the help of Joshua and named this new library _tenacity_. It works in the same manner as _retrying_ does, except that it is written in a more functional way and offers some nifty new features.

## Basic Usage

The basic usage is to use it as a decorator:

This will make the function `do_something_and_retry_on_any_exception` be called over and over again until it stops raising an exception. It would have been hard to design anything simpler. Obviously, this is a pretty rare case, as one usually wants to wait for some time between retries. For that, _tenacity_ offers a large panel of waiting methods:
    
    
    @tenacity.retry(wait=tenacity.wait_fixed(1))

Or a simple exponential back-off method can be used instead:
    
    
    @tenacity.retry(wait=tenacity.wait_exponential())

## Combination

What is especially interesting with _tenacity_, is that you can easily combine several methods. For example, you can combine `tenacity.wait.wait_random` with `tenacity.wait.wait_fixed` to wait a number of seconds defined in an interval:
    
    
    @tenacity.retry(wait=tenacity.wait_fixed(10) + wait.wait_random(0, 3))

This will make the function being retried wait randomly between 10 and 13 seconds before trying again.

_tenacity_ offers more customization, such as retrying on some exceptions only. You can retry every second to execute the function only if the exception raised by `do_something` is an instance of `IOError`, e.g. a network communication error.
    
    
    @tenacity.retry(wait=tenacity.wait_fixed(1),

You can combine several conditions easily by using the `|` or `&` binary operators. They are used to make the code retry if an `IOError` exception is raised, or if no result is returned. Also, a stop condition is added to the `stop` keyword arguments. It allows you to specify a condition unrelated to the function result of exception to stop, such as a number of attempts or a delay.

The functional approach of _tenacity_ makes it easy and clean to combine a lot of conditions for various use cases with simple binary operators.

## Standalone Usage

_tenacity_ can also be used without decorators by using the object `Retrying`, that implements its main behavior, and using its `call` method. This allows you to call any function with different retry conditions, or to retry any piece of code that does not use the decorator at all - like code from an external library.

This also allows you to reuse that object without creating a one new each time, saving some memory!

I hope you'll like it and will find it of some use. Feel free to fork it, report bug, or ask for new features on [its GitHub](https://github.com/jd/tenacity)!

[Learn how divergent branches can appear in your repository](https://dzone.com/go?i=190138&u=https%3A%2F%2Fblog.wakanda.io%2Fanimated-git-4-understand-divergent-branches-appear-fetching-remote-repository%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral) and how to better understand why they are called "branches". Brought to you in partnership with [Wakanda](https://dzone.com/go?i=190138&u=https%3A%2F%2Fblog.wakanda.io%2Fanimated-git-4-understand-divergent-branches-appear-fetching-remote-repository%2F%3Futm_source%3Ddzone%26utm_campaign%3Dblog-article%26utm_medium%3Dreferral).
