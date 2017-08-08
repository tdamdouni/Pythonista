# How to Implement String Interpolation in Python

_Captured: 2017-01-24 at 04:23 from [dzone.com](https://dzone.com/articles/how-to-implement-string-interpolation-in-python-br?edition=262907&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-01-23)_

[Start coding today](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) to experience the powerful engine that drives data application's development, brought to you in partnership with [Qlik](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).

String interpolation is a process of substituting values of local variables into placeholders in a string.

It is implemented in many programming languages such as Scala:

Perl:

CoffeeScript:

... and many others.

At first sight, it doesn't seem that it's possible to use string interpolation in Python. However, we can implement it with just 2 lines of Python code.

But let's start with basics. An idiomatic way to build a complex string in Python is to use the "format" function:
    
    
    >>> Hi, I am John and I am 26 years old

Which is much cleaner than using string concatenation:
    
    
    print "Hi, I am " + name + " and I am " + str(age) + " years old"
    
    
    Hi, I am John and I am 26 years old

But if you use the `format` function in this way, the output depends on the order of arguments:

To avoid that we can pass key-value arguments to the "format" function:

Here we had to pass all variables for string interpolation to the "format" function, but still we have not achieved what we wanted, because "name" and "age" are not local variables. Can "format" somehow access local variables?

To do it we can get a dictionary with all local variables using the `locals` function:

Now we just need to somehow pass it to the `format` function. Unfortunately we cannot just call it as `s.format(locals())`:
    
    
    ---------------------------------------------------------------------------
    
    
    <ipython-input-5-0fb983071eb8> in <module>()
    
    
    ----> 1 print "Hi, I am {name} and I am {age} years old".format(locals())

This is because `locals` returns a dictionary, while `format` expects key-value parameters.

Luckily, we can convert a dictionary into key-value parameters using `\\*\\*` opeartor. If we have a function that expects key-value arguments:

We can pass parameters packed in a dictionary:

Now we can use this technique to implement our first version of string interpolation:

It works but looks cumbersome. With this approach every time we need to interpolate our string we would need to write `format(\\*\\*locals())`.

It would be great if we could write a function that would interpolate a string like this:

At first it seems impossible, since if we move interpolation code to another function it would not be able to access local variables from a scope where it was called from:

And yet, it is possible. Python provides a way to inspect the current stack with the `sys.\\_getframe` function:

So the only thing that is left is to combine frames introspection with the `format` function. Here are 2 lines of code that would do the trick:

[Create data driven applications](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) in Qlik's free and easy to use coding environment, brought to you in partnership with [Qlik](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).
