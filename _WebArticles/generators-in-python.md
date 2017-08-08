# Generators in Python

_Captured: 2017-01-28 at 22:20 from [dzone.com](https://dzone.com/articles/generators-in-python?edition=265887&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-01-28)_

Make the transition to Node.js if you are a Java, PHP, Rails or .NET developer with [these resources to help jumpstart your Node.js knowledge](https://dzone.com/go?i=182121&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127833%26PluID%3D0%26ord%3D%5Btimestamp%5D) plus pick up some development tips. Brought to you in partnership with [IBM](https://dzone.com/go?i=182121&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127833%26PluID%3D0%26ord%3D%5Btimestamp%5D).

In previous articles, I've written about how to create an iterator in Python by implementing iterator protocol or using the **yield** keyword. In this article, I'll describe generators: a piece of Python syntax that can turn many iterators into one-liners.

Generators syntax is very similar to list comprehension. The only difference is the usage of parentheses instead of square braces:
    
    
    >>> gen = (i for i in range(3))

As opposed to the list comprehension generator expression does not generate all values at once. But instead it returns an iterator that can be used to get values one-by-one:
    
    
      File "<pyshell#14>", line 1, in <module>

Generators may be especially useful in situations when the creation of each value requires an extensive amount of computation. Instead of generating all values in advance, generators create the next value only when it is requested (when the **next** method is called on the result iterator).

Let's say we want to generate the first few Fibonacci numbers. At first, we need to implement a function that will calculate n-th Fibonacci number:
    
    
        for i in range(1, n+1):
    
    
            a, b = b, a + b

Now, we can create an iterator for the first 100 Fibonacci numbers.
    
    
    >>> it = (fib(i) for i in range(100))

As you may notice there is no output from the **fib** function. This is because all calls to it were postponed until actual values are requested:

In contrast, if we use list comprehension all 100 calls to the fib function would be performed before the result list is created:

As you can see all numbers were created in advance.

We can build more complicated generators using the same constructions we can use for list comprehensions. Similarly, we can filter some values using the **if** statement at the end of a generator expression:

For example, if we want to generate all numbers less than 100 that can be divided by 9 we can write code like:

We can also combine multiple loops in one generator using the following construction:

Which is equivalent to the following code:

Learn why developers are gravitating towards Node and its ability to [retain and leverage the skills of JavaScript developers](https://dzone.com/go?i=182122&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127834%26PluID%3D0%26ord%3D%5Btimestamp%5D) and the ability to deliver projects faster than other languages can. Brought to you in partnership with [IBM](https://dzone.com/go?i=182122&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127834%26PluID%3D0%26ord%3D%5Btimestamp%5D).
