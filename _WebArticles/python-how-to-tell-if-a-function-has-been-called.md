# Python — How to Tell if a Function Has Been Called

_Captured: 2017-03-16 at 21:25 from [dzone.com](https://dzone.com/articles/python-how-to-tell-if-a-function-has-been-called?edition=283884&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-03-16)_

Last year I ran into a situation where I needed to know if a function had been called. Basically we were trying to prevent shutting down a Twisted event loop twice or starting two of them. Anyway, in my research I stumbled across a fun post on [StackOverflow](http://stackoverflow.com/a/9882439/393194) that showed a couple of ways to do this.

The first made use of the fact that everything in Python is an object, including the function itself. Let's take a look at a simple example:

In this example, we create an attribute on the function that we named **has_been_called**. We set it to True when the function is called. When you start your program, you will want to initialize that attribute to False, which we do above. Then we use a for loop to loop twice. The first time through it will check if the function has been called. Since it hasn't, you will see it fall to the else statement. Now that we called the function, the second time through the loop the first part of the if statement executes.

That StackOverflow post also mentions a neat way to use a decorator to track function calls. Here's an example I wrote:

In this example, I import **functools** and create a decorator that I dubbed **calltracker**. In this function, we set up the same attribute that we did in the previous example, but in this case we attach it to our wrapper (i.e. the decorator). Then we decorate a function and give our code a try. The first **if statement** checks to see if the function has been called yet. It hasn't, so we go ahead and call it. Then we confirm that the function was called in our second if statement.

## Wrapping Up

While this stuff is certainly useful at runtime, you can also do similar things using Python's [trace](https://docs.python.org/2/library/trace.html) module to trace through the execution of your code. This sort of thing is also done via coverage tools. You will also find this kind of functionality in [Python Mock objects](http://stackoverflow.com/questions/3829742/assert-that-a-method-was-called-in-a-python-unit-test) as a Mock can tell when it has been called.

Anyway, you will hopefully find this exercise as interesting as I did. While I already knew that everything in Python was an object, I hadn't thought about using that functionality to add attributes to functions.
