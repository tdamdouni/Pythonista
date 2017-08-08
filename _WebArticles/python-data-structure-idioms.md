# Python Data Structure Idioms

_Captured: 2017-01-24 at 20:53 from [dzone.com](https://dzone.com/articles/python-data-structures-idioms-brewing-codes?edition=265881&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-01-24)_

[Start coding today](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) to experience the powerful engine that drives data application's development, brought to you in partnership with [Qlik](https://dzone.com/go?i=155124&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).

A significant portion of our time as developers is spend writing code that manipulates basic data structures: traverse a list, create a map, filter elements in a collection. Therefore, it is important to know how effectively do it in Python and make your code more readable and efficient.

## Iterate Over a List

There are many ways to iterate over a list in Python. The simplest way would be just to maintain current position in the list and increment it on each iteration:

This works, but Python provides a more convenient way to do using the **[range](https://docs.python.org/2/library/functions.html#range)** function. The **range** function can be used to generate numbers from 0 to N and this can be used as an analog of a **for** loop in C:

While this is more concise, there is a better way to do it since Python lets iterate over a list directly, similarly to **foreach** loops in other languages:

## Iterate a List in Reverse Order

How can we iterate a list in the reverse order? One way to do it would be to use an unreadable three arguments version of the **range** function and provide position of the last element in a list (first argument), position of an element before the first element in the list (second argument) and negative step to go in reverse order (third argument):

However, as you've may already guessed, Python should offer a much better way to do it. We can just use the **[reversed](https://docs.python.org/2/library/functions.html#reversed)** function in a **for** loop:

## Access the Last Element

A commonly used idiom to access the last element in a list would be to get the length of a list, subtract one from it, and use result number as a position of the last element:

This is cumbersome in Python since it supports negative indexes to access elements from the end of the list. So, -1 is the last element:

Negative indexes can also be used to access a next to last element and so on:

## Use Sequence Unpacking

A common way to extract values from a list to multiple variables in other programming languages would be to use indexes:

However, Python supports sequence unpacking that lets us extract values from a list to multiple variables:

## Use Lists Comprehensions

Let's say that we want to filter all grades for a movie posted by users of age 18 or bellow.

How many times did you write code like the following?

Do it no more in Python. Use list comprehensions with an **if** statement instead.

## Use Enumerate Function

Sometimes, you need to iterate over a list and keep track of the position of each element. For example, if you need to display menu items in a shell, you can simply use the **range** function:
    
    
    for i in range(len(menu_items)):
    
    
      print "{}. {}".format(i, menu_items)

A better way to do it would be to use the **[enumerate](https://docs.python.org/2/library/functions.html#enumerate)** function. It is an iterator that returns pairs, each of which contains the position of an element and the element itself:
    
    
    for i, menu_items in enumerate(menu_items):
    
    
      print "{}. {}".format(i, menu_items)

## Use Keys to Sort

A typical way to sort elements in other programming languages is to provide a function that compares two objects along with a collection to sort. In Python, it would look like this:
    
    
    people = [Person('John', 30), Person('Peter', 28), Person('Joe', 42)]
    
    
    def compare_people(p1, p2):
    
    
    sorted(people, cmp=compare_people)
    
    
    [Person(name='Peter', age=28), Person(name='John', age=30), Person(name='Joe', age=42)]

However, this is not the best way to do it. Since all we need to do to compare two instances of **Person** class is to compare values of their **age** field. Why should we write a complex compare function for this?

Specifically for this case, the **[sorted](https://docs.python.org/2/library/functions.html#sorted)** function accepts the **key** function that is used to extract a key that will be used to compare two instances of an object:
    
    
    sorted(people, key=lambda p: p.age)
    
    
    [Person(name='Peter', age=28), Person(name='John', age=30), Person(name='Joe', age=42)]

## Use All/Any Functions

If you want to check if all or any value in a collection is True, one way would be iterate over a list:

However, Python already has **[all](https://docs.python.org/2/library/functions.html#all)**/**[any](https://docs.python.org/2/library/functions.html#any)** functions for that. **all** returns True if all values in an iterable passed to it are True, while **any** returns True if at least one of values passed to it is True:

To check if all items comply with a certain condition, you can convert a list of arbitrary objects to a list of booleans using a list comprehension:
    
    
    all([person.age > 18 for person in people])

However, you can pass a generator (just omit square braces around the list comprehension):
    
    
    all(person.age > 18 for person in people)

Not only will this save you two keystrokes; it will also omit the creation of an intermediate list (more about this later).

## Use Slicing

You can take apart a list using a technique called slicing. Instead of providing a single index in a square bracket when accessing a list, you can provide the following three values:

All of these parameters are optional and you can get different parts of a list if you omit some of them. If only the start position is provided, it will return all elements in a list starting with the specified index:

If only the end position is provided, slicing will return all elements up to the provided position:

You can also get part of a list between two indexes:

By default, step-in slicing is equal to one, which means that all elements between start and end positions are returned. If you want to get only every second element or every third element, you need to provide a step value:

## Do Not Create Unnecessary Objects

**range** is a useful function if you need to generate consistent integer values in a range, but it has one drawback: it returns a list with all generated values:

The solution here is to use the **[xrange](https://docs.python.org/2/library/functions.html#xrange)** function. It immediately returns an iterator instead of creating a list:

The drawback of **xrange** comparing to the **range** function is that its output can be iterated only once.

## New in Python 3

In Python 3, **xrange** was removed and the **range** function behaves like **xrange** in Python 2.x. If you need to iterate over an output of **range** in Python 3 multiple times, you can convert its output into a list:

## Use izip

If you need to generate pairs from elements in two collections, one way to do it would be to use the **zip** function:

Instead, we can use the **[izip](https://docs.python.org/2/library/itertools.html#itertools.izip)** function that would return a return an iterator instead of creating a new list:

In Python 3, the **izip** function is removed and **zip** behaves like **izip** function in Python 2.x.

## Use Generators

Lists comprehensions is a powerful tool in Python, but since it can use an extensive amount of memory, each list comprehension will create a new list:

A way to avoid this is to use generators instead of list comprehensions. The difference in syntax is minimal: you should use parenthesis instead of square brackets, but the difference is crucial. The following example does not create any intermediate lists:
    
    
    lst_1 = (i + 1 for i in lst)

This is especially handy if you may need to process only part of the result collection to get a result, such as to find a first element that match a certain condition.

## Avoid using keys() function

If you need to iterate over keys in a dictionary you may be inclined to use **keys** function on a hash map:

However, there is a better way. You use **iterate** over a dictionary and it performs iteration over its keys, so you can simply do:

Not only it will save you some typing; it will also prevent youfrom creating a copy of all keys in a dict as **keys** method does.

## Iterate Over Keys and Values

If you use the **keys** method, it's really easy to iterate keys and values in a dictionary like this:

There is a better way. You can use the **items** function, which returns key-value pairs from a dictionary:

Not only is this method is more concise, but it's more efficient, too.

## Use Dictionaries Comprehension

One way to create a dictionary is to assign values to it one-by-one:

Instead, you can use a dictionary comprehension to turn this into a one-liner:

## Use Collections Module

If you need a struct like this, you may just define a class with an **init** method and a bunch of fields:

However, the **[collections](https://docs.python.org/2/library/collections.html)** module from the Python library provides a **[namedtuple](https://docs.python.org/2/library/collections.html#collections.namedtuple)** type that turns this into a one-liner:

In addition, **namedtuple** implements **__str__**, **__repr__**, and **__eq__** methods:

If we need to count the number of times an element is encountered in a collection, we can use a common approach:

The **collections** module provides a very handy class for this case called **defaultdict**. Its constructor accepts a function that will be used to calculate a value for a non-existing key:

To rewrite counting example, we can pass the **int** function to **defaultdict**, which returns zero if called with no arguments:

**defaultdict** is useful when you need to create any kind of grouping of items in a collection, but if you just need to get a count of elements, you may use the **Counter** class instead:
    
    
    Counter({4: 3, 1: 2, 2: 1, 3: 1, 5: 1})

[Create data driven applications](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome) in Qlik's free and easy to use coding environment, brought to you in partnership with [Qlik](https://dzone.com/go?i=155123&u=http%3A%2F%2Fplayground.qlik.com%2Fhome).
