# Python Functional Programming

_Captured: 2017-02-14 at 21:13 from [dzone.com](https://dzone.com/articles/intermediate-python-1?edition=268944&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-02-14)_

Make the transition to Node.js if you are a Java, PHP, Rails or .NET developer with [these resources to help jumpstart your Node.js knowledge](https://dzone.com/go?i=182121&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127833%26PluID%3D0%26ord%3D%5Btimestamp%5D) plus pick up some development tips. Brought to you in partnership with [IBM](https://dzone.com/go?i=182121&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127833%26PluID%3D0%26ord%3D%5Btimestamp%5D).

## Different Programming Paradigms

There are several approaches to computer programming utilized to solve similar tasks and some of them are more suited to specific tasks. The most prevailing ones are:

#### Procedural Programming

This type of programming is a list of instructions coded by the programmer and followed strictly by the computer. Many C examples can be seen as procedural (C can be used to program in other paradigms as well, but the language was designed with procedural programming in mind). C++ and Python can be used to program in a procedural style.

#### Declarative Programming

This type of programming becomes an activity to describe the problem you are trying to solve instead of telling the computer how to solve it. The most famous example of declarative programming languages is SQL. The programmer doesn't tell the SQL engine whether to use indexes or scan table or which sub-clause to execute first. The engine decides which is more efficient.

#### Object-Oriented Programming

In object-orientation, programs are interactions of objects which have internal states, interactions are performed as messages passed from and object to object. C++ and Python support object-orientation, but they don't restrict the programmer to this single paradigm. Java is strictly object-oriented (well kind of). Smalltalk is (really) strictly object-oriented.

#### Functional Programming

In the functional paradigms, internal state is largely avoided so that a function call's output only depends on its parameters. It is then no surprise that functional programming languages have functions as first-class language constructs. Such functions described above are called purely functional. In practice, purely functional routines are mixed with non-purely functional ones and at some cases using global variables or causing side effects happens as well. C++, Python, Java, Scala and many other languages can be used to program in a functional way.

The above categories are just a rough cut and they don't constitute solid distinctions. In fact, the opposite of declarative programming is imperative programming. Functional and logical programming can be seen as declarative because they avoid side effects and the programmer doesn't have a complete control on how the algorithm used is actually implemented.

## Characteristics of Functional Programming

Functional programming facilitates four major qualities of both theoretical and practical importance:

  * **Formal Provability** - to some degree proving a program correct is easier when no side effects are present because before and after constraints can be formulated more easily (side effects may cause inability to formulate after constraints, for example).

  * **Modularity **- functional programs are assemblies of small functions because functions are the unit of work, which results in largely modular programs.

  * **Composability** - it is easier to make a library developed to the functional paradigm because of constraints that are largely well defined especially in the case of absence of side effects.

  * **Testing and Debugging** - it is easier to test functional programs because of modularity and composability.

  * **Productivity** - in many cases (according to many people's experiences) functional programs are far shorter than procedural and object-oriented ones.

## Python for Function Programming

One of the most important constructs in [Python Functional Programming](http://docs.python.org/howto/functional.html) is iterators.

### Iterators

Iterators are objects that represent data streams, these streams can be finite of infinite. Python iterator protocol requires an object to have a method named `next()` that takes no argument and returns the next element in the data stream in order for the object to be an iterator. Iterators' `next()` must raise a `StopIteration` exception when there are no more elements in the stream. An object is iterable if it is an iterator or an iterator for it can be obtained, for example, by the built-in function `iter()`. Built-in iterable objects include dictionaries and lists. Note that Python iterator protocol supports only going in the forward direction. However, going in the back direction can be implemented.
    
    
    it = iter(l)  # acquire an iterator for the list

Iterable objects are expected in for loops:

is equivalent to:

The reverse operation can be carried as well: lists or tuples can be constructed from iterables:

Note that construction of a list or a tuple from an iterator drains the iterator and causes it to raise a `StopIteration` on the next call to iterator's `next()` .

This also means that if you try to construct a list out of a drained iterator, you get an empty list.

Sequence unpacking supports iterators as well.
    
    
    a, b, c = iter(l) # or a, b, c = l 
    
    
    print(a, b, c)    # outputs: 1 2 3

Several built-in functions accept iterators as parameters.

`in` and `not in` also support iterators. Notice that because iterators can be infinite, problems will happen if you supply such an iterator for `max()` , `min()` or `not in` , and if it is the case that item is not in the stream the same will happen with `in`; the call will never return.

### Dictionary Iterators

Dictionaries support multiple types of iterators. The basic one obtained by `keys()` iterates over dictionary keys.
    
    
    for key in d.keys(): # or d.iterkeys() for Python 2

`keys()` and `iterkeys()` are actually the default iterator for dictionaries, so the following can be done:

Note that for Python 2 `dict.keys()` returns a list of keys, not an iterator. The `moves` package provides compatiability constructs between different Python versions. Other types of iterators are `values()` and `items()` for Python 3 and, respectively, `itervalues()` and `iteritems()` for Python 2. `values()` iterates over values only whilst `items()` iterates over key/value pairs.
    
    
    for v in d.values(): print(v)
    
    
    for k, v in d.items(): print(k, v)

Note that for Python 2 `dict.values()` returns a list of values instead of an iterator whilst `dict.items()` returns a list of 2-tuples (key, value). The dict constructor accepts a finite iterator over a 2-tuples sequence as in (key, value).

### Iterator Usage

Iterators can be used to achieve many tasks, but the two most common tasks are: 1) applying a function to each element in a data stream; 2) selecting specific element of a data stream according to some criteria. There are several ways to do just that including `map()` and `filter()` built-in functions
    
    
    d = dict(a = 1, b = 2, c = 3)
    
    
    d = dict(a = 1, b = 2, c = 3)

`map()` applies a function to each item in an iterable. Remember that the default iterator for a dictionary iterates over its keys, so in the example above `map()`applies `str.upper()` to each key in dictionary `d` and appends `str.upper()` output to the returned list.

`filter()` applies a predicate function to each item in an iterable, if the predicate returns a true value that item is included in the output list, otherwise it is not.

These functions are great and all, but there are is a better way to do these two tasks in a more succinct way. List comprehension is a mechanism that is very efficient and compact.

List comprehension always returns a list be it empty or otherwise. A generator, on the other hand, returns an iterator object.

The only difference in syntax is that list comprehension uses `[]` whilst generators use `()` . Generators can be more useful for large data streams because list comprehension would physically construct a list in memory whilst generators wouldn't.

Generators could be constructed as parameters to functions that expect iterators, the rule is that parentheses around a generator expression can be dropped if the expression constitutes a single parameter to a function that takes a single argument.

Generators and list comprehension work as follows:

Expressions are included in output if they are in a sequence. All 'if' conditions are optional but if a condition is present an expression is only included in the output if the condition evaluates to true. Expressions are evaluated as follows:

This means that for each element in `sequence1`, `sequence2` is iterated over from the beginning then for each pair resulting from `(sequence1_item, sequence2_item)` `sequence3` is iterated over from the beginning, etc. Hence, sequences are not required to be of the same length and the final number of items are the overall product of the number of items in all sequences. So that if we have two sequences, the first has 2 items and the second has 3 items, there will be 6 items in the output iterator or list provided that there are no false condition.
    
    
    def even(x): return (x % 2) == 0

Introduce `()` if you want elements of the output list to be tuples as in `(x, y)` above to avoid syntax errors.

### Iterator Object Example

An iterator object must implement the iterator protocol. There are some subtleties about iterator implementation (check PEP 234), however, in essence, it is about an object having ` __iter__()` and `next()` methods. The following is a re-organised section of PEP 234 about constructing an iterator class:

  * `next()` returns the next value in the iteration, or raises StopIteration (or a derived exception class) to signal the end of the iteration. Any other exception should be considered to signify an error and should be propagated normally, not taken to mean the end of the iteration.

  * Classes can define how they are iterated over by defining an `__iter__()` method; this should take no additional arguments and return a valid iterator object. A class that wants to be an iterator should implement two methods: a `next()`method that behaves as described above, and an `__iter__()`method that returns self.

  * The two methods correspond to two distinct protocols:

1\. An object can be iterated over with `for` if it implements `__iter__()` or `__getitem__()` .

2\. An object can function as an iterator if it implements `next()`.

Container-like objects usually support protocol One. Iterators are currently required to support both protocols. The semantics of iteration come only from protocol Two; protocol One is present to make iterators behave like sequences; in particular so that code receiving an iterator can use a for-loop over the iterator.

So, let's write an iterator class.
    
    
        def __init__(self, start, end):
    
    
    r = self.current * self.current

### Generators

A usual function call always starts execution at the beginning of the body of the callee. Generators are an extension of this behavior that allows a function to be resumed at the instruction it was suspended at. One way to implement generators behavior in a crude way is using instance attributes to preserve the state of the function object. Another way is to use co-routines. In Python, the yield keyword allows functions to be generators, any function contains a yield keyword is a generator. A generator function outputs an iterator instead of a single value. Next continuation of a generator starts after the yield statement that produced the current output.

The above `SquareRoot`iterator class can be written as a generator as follows:

The above generator function is equivalent in all aspects to the `SquareRoot`iterator class except in one: it cannot be reset to its initial state (except when we know what the initial state was, more about this later).

Here are more examples of generators:
    
    
    list(gen1())['mentor', 'lycon', 'says hi']

A `return` statement without arguments can be used inside a generator to signal end of execution.

An example of an infinite generator is a generator to produce the Fibonacci sequence.

Differences between iterators and generators can be summarized as follows:

  1. With generators, there is no need to worry about the iterator protocol.

  2. Generators are one-time operations, once the generator is exhausted you have to construct another.

  3. Iterator objects may be used for iteration several times without a need to reconstruct them (a `list`for example).

### Generator Interaction

Generators are not only callables that take parameters, same as regular functions, but they also allow callers to pass values to them in the middle of execution. This feature requires Python >= 2.5. To pass a value into a generator use `g.send(val)` where `g` is a generator object. The following is an example of a generator that is ready to accept a value during execution:

Note that it is in principle not different from the previous generators we encountered, the differences are:

  1. `val` is assigned a value from a `yield` expression.
  2. We use parentheses around `yield` .

In Python 2.5, yield became an expression, so we can use it as any other right-hand expression. We have to prepare for `val` being `None` because `val` is going to be `None` except when `send()` is used with a value other than `None`. The parentheses around `yield` are not always required, but it is easier to always include them because it is easily overlooked where it is allowed not to include them. In short, you can forego the use of parentheses only if the `yield` is at the top-level of the right-hand expression (Look atPEP 342 for details).

With the above generator, we can do the following:

Notice the following:

while we can also do this using the same iterator

This clearly shows that we can control the execution of a generator as far as values sent via `send()` controls its execution. Let's try a tiny variation on the same generator above.

Running the same code above produces the following instead:

and as we did before

A `yield` statement can be used for both input and output. In addition to `send()`, generator objects have `close()`and `throw(type, value=None, traceback=None)`methods. Here is the generator method documentation for Python documentation:

`generator.next()`

Starts the execution of a generator function or resumes it at the last executed `yield` expression. When a generator function is resumed with a `next()` method, the current `yield` expression always evaluates to `None` . The execution then continues to the next `yield` expression, where the generator is suspended again, and the value of the `expression_list` is returned to `next()` 's caller. If the generator exits without yielding another value, a `StopIteration` exception is raised.

`generator.send(value)`

Resumes the execution and "sends" a value into the generator function. The value argument becomes the result of the current yield expression. The `send()` method returns the next value yielded by the generator, or raises `StopIteration` if the generator exits without yielding another value. When `send()` is called to start the generator, it must be called with None as the argument, because there is no yield expression that could receive the value.

`generator.throw(type[, value[, traceback]])`

Raises an exception of type at the point where generator was paused, and returns the next value yielded by the generator function. If the generator exits without yielding another value, a StopIteration exception is raised. If the generator function does not catch the passed-in exception, or raises a different exception, then that exception propagates to the caller.

`generator.close()`

Raises a `GeneratorExit` at the point where the generator function was paused [in the generator's code]. If the generator function then raises `StopIteration` (by exiting normally, or due to already being closed) or `GeneratorExit` (by not catching the exception), close returns to its caller. If the generator yields a value, a `RuntimeError` is raised. If the generator raises any other exception, it is propagated to the caller. `close()` does nothing if the generator has already exited due to an exception or normal exit.

For `close()`, clean up code may be best put in a `finally` clause (in some cases, in a `catch` clause).

Generators in that sense are coroutines. They are very nice as pipelines. They can be stacked on top of each other to simulate Unix pipe-lining, for example, with all the advantages of the generator's memory handling and its ability to process infinite streams. They can also implement producers/consumers patterns. As coroutines, they can be used to implement pseudo concurrency (pseudo threads), where one thread schedules a (theoretically) infinite number of execution units (check greelnets and Gevent if you are interested, we will cover that later on).

### Generators in Practice

Let's have a look at an example. In this example we will parse the HTML returned from a Web page, capitalize every word found and reverse it. Capitalized words will be stored in a list and reversed words will be stored in another list.
    
    
    def producer(words, * consumers):
    
    
        temp = data.translate(None, string.punctuation).strip().split()
    
    
    def produce(url, container1, container2):
    
    
    producer(p.data, consumer1(container1), consumer2(container2))

for Python 2, imports would be

`producer` acts as dispatcher, but if we route back the results from consumers to `producer` then `producer` can dispatch them to other processing consumers and so on. This way we can make a processing hub disguised in a very innocent function in a very straightforward manner.

Now let's see how we can combine two generators to capitalize and reverse a word by hand.
    
    
    if w is not None: print(w[::-1])
    
    
    >>> g = capitalise() >>> g.next() >>> g.send('ab')

Notice that `BA` is printed by `reverse()` , it is not yielded back to `capitalise()`.

We can simplify this a bit if we introduce a decorator to start the generator automatically so that we need not call `next()` upon creation.

The above code would be re-written as follows:
    
    
    if w is not None: print w[::-1]
    
    
    >>> g = capitalise() >>> g.send('ab')

It doesn't save much of typing, but it helps to build a better abstraction. This will be used later on.

At this point we could chain generators in a forward-direction manner, but could we make the communication two-way? Yes, we can and it is very simple.
    
    
                yield g.send(w[::-1]) if w

This is printed from inside `capitalise2()` . Two-way communication is actually nothing more than normal function call semantics.

For general-purpose scenarios, however, we need pluggable components. So, let's separate the generators and call them in row if we so desire.
    
    
                yield w.upper() if w
    
    
    multiplier(reverse3(capitalise3('ml'))) #outputs: LMLM

Note that `multiplier()` didn't change.

Let's have a practical example of why this programming style is helpful. Here are two functions that do the same thing: counting the number of words in a file. `f1()` is written in the traditional style, whilst `f2()` is written as a pipeline of generators.
    
    
        p = re.compile(r '\s+')
    
    
            words = p.split(line)
    
    
        p = re.compile(r '\s+')
    
    
        words = (p.split(line) for line in fi)
    
    
        l = (len(w) for w in words)

It is easily noted that `f2()` is shorter and is a bit weird, in fact. Let's look at performance (make sure to read the comment afterwards) and remember, _"there is a small lie, a big lie and the benchmark."_

_Note that benchmarking was carried on Python 2._

File size
f1() execution time  

f2() execution time 

232.4 MB
7.655333333
7.502666667

1.1 GB
51.694
37.136

File size
f1() average execution time
f2() average execution time

12 KB
0.004
0.006

82.1 MB
36.911
31.470

232.4 MB
91.042
39.363

1.1 GB
414.212
290.906

Measures of cProfile (standard python deterministic profiler).

### **Performance Comments**

Difference in timings for the two tables has to do with what's being measured by each method. The timings you would practically experience are the timings in the first table.

Results in the first table above are average times for function executions in row, `f1()` then `f2()` or `f2()` then `f1()` and each function followed by random user code.

For very small files, `f1()` outperforms `f2() ` and it seems that generators overhead is not compensated by file size. For large files, it matters whether each function is run in a row or not. If we compile the regular expression for each line, then if `f1()` is executed in a row with absolutely no user-code in between, the execution time will grow slower than for `f2()`. However, this is possible but not a typical scenario outside benchmarking.

On contrary, when random user code is executed between function invocations, `f2()` execution time remains stable whilst `f1()` execution time keeps increasing slowly.

It is important to note that especially for large files these functions spend more time managing memory allocation than on calculations. `f2()` can handle calculations of files larger than available memory as it is, however, `f1(` would require amendments. Such amendments will increase its execution time.

Learn why developers are gravitating towards Node and its ability to [retain and leverage the skills of JavaScript developers](https://dzone.com/go?i=182122&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127834%26PluID%3D0%26ord%3D%5Btimestamp%5D) and the ability to deliver projects faster than other languages can. Brought to you in partnership with [IBM](https://dzone.com/go?i=182122&u=http%3A%2F%2Fbs.serving-sys.com%2Fserving%2FadServer.bs%3Fcn%3Dtrd%26mc%3Dclick%26pli%3D20127834%26PluID%3D0%26ord%3D%5Btimestamp%5D).
