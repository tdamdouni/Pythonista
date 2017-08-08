# Python List Functions Easy Guide

_Captured: 2017-04-14 at 20:38 from [dzone.com](https://dzone.com/articles/python-list-functions-easy-guide?edition=290908&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-04-14)_

Need to build an application around your data? [Learn more](https://dzone.com/go?i=200129&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) about dataflow programming for rapid development and greater creativity.

A Python list is a sequence of values. It can consist of any types, strings, numbers, floats, mixed content, whatever. In this post, we will talk about Python list functions and how to create elements, add elements, append elements, reverse elements, and perform many other Python list functions.

## Create Python Lists

There are several ways to create a Python list. The easiest way is to enclose your elements in square brackets like this: `mylist = [10, 20, 30, 40, 50]`.

You can make a list of strings like this: `mylist = ['first', 'second', 'third', 'fourth', 'fifth']`.

The elements of a list don't have to be the same type. You can mix them like this: `mylist = ['first', 20, 5.5, [10, 15], 'fifth']`.

You can write nested lists, which means lists inside lists live the above example. Also, you can access any element of the list by its index, which is zero-based: `third_elem = mylist[2]`.

List indices work the same way as string indices. You can review my [Python programming basics](https://dzone.com/articles/python-programming-basics-with-examples) post for more info.

## Mutable Lists

Unlike strings, lists are mutable because you can change the order of items in a list or reassign an item in a list.

If we have a list like `mylist = ['first', 'second', 'third', 'fourth', 'fifth']`, we can change the third item like this: `mylist[2] = "New item"`.

Now, if you print the list, you should see the new list: `['first', 'second', 'New item', 'fourth', 'fifth']`.

If you try to read or write an element that does not exist, you get an `IndexError`.

Like strings, if an index has a negative value, it counts backward from the end of the list.
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

The output of this code will be `fifth`.

## Traverse a List

You can traverse the elements of a list using a `for` loop like this:
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

This works well if you need to read the elements of the list. But if you want to update the elements, you need the indices like this:
    
    
    for i in range(len(mylist)):

The result will be `[6, 7, 8, 9, 10]`.

`len()` returns the number of elements in the list, while `range()` returns the list of indices.

Keep in mind that the nested list still counts as a single element, regardless of how many elements are inside it.

The result of the above code is `5`.

## Slice a List

The slice operator also works on lists like this:
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

The result from the above code will be `['second', 'third']` .

If you omit the first index, the slice starts from the beginning. If you omit the second, the slice goes to the end.

If you omit both, the slice is a copy of the whole list.
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

The result of the above code will be:
    
    
    ['second', 'third', 'fourth', 'fifth']
    
    
    ['first', 'second', 'third', 'fourth', 'fifth']

Since lists are mutable, you can change elements using the slice operator:

The result will be `['first', 'Hello', 'Guys', 'fourth', 'fifth']`.

## Insert Into a List

You can insert a new element to the list using the `insert` method like this:

The result will be `[1, 'Hello', 2, 3, 4, 5]`.

Also, the index of the inserted element is zero-based.

## Append to a List

You can add a new element to the end of a list using the `append` method like this:

The result will be `['first', 'second', 'third', 'fourth', 'fifth', 'new one']`.

You can append more than one element using the `extend` method like this:
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

The result will be `['first', 'second', 'third', 'fourth', 'fifth', 'Hello', 'Guys']`.

Of course, `list2` will remain untouched.

## Sort a List

The `sort` method sorts the elements of the list from low to high.
    
    
    mylist = ['cde', 'fgh', 'abc', 'klm', 'opq']

The output will be:

## Reverse a List

You can reverse the order of a python list using the `reverse` method like this:

The output will be `[5, 4, 3, 2, 1]`.

## Index of an Element

You can get the index of an element using the index method like this:

The result will be `1`.

If you have more than one element with the same name supplied to the `index` function, it will return the first index that matches the supplied value.

## Delete an Element

There are several ways to delete elements from a list. If you know the index of the element you want to delete, you can use the pop method like this:
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']

The result will be:

If you don't specify an index for the `pop` method, it will delete the last element.

The result will be:

If you don't know the index of the element, but you know the element itself, you can remove it using like this:

The result will be `['first', 'third', 'fourth', 'fifth']`.

If you don't need the removed value, you can use the `del` operator like this:

The result will be `['first', 'second', 'fourth', 'fifth']`.

Also, you can delete multiple elements using the slice operator like this: The result will be `['first', 'fourth', 'fifth']`.

## Aggregate Functions

There are a number of built-in aggregate functions that can be used on lists that allow you to go through the list without writing a loop.

The `sum()` function only works when the list elements are numbers.

The other functions (`max()`, `len()`, etc.) work with lists of strings and other types that can be comparable.

## Compare Lists

If you are using Python 2, you can compare elements of two lists using the `cmp` function like this:

It will return `-1` if there's no match and `1` if it matches.

If you are using Python 3, you can compare two lists using the `==` operator like this:
    
    
    mylist = ['first', 'second', 'third', 'fourth', 'fifth']
    
    
    list2 = ['fourth', 'first', 'second', 'fifth', 'third']

The result will be `No match`.

## List Operations

The `+` operator concatenates lists like this:

The output will be `1, 2, 3, 4, 5, 6]`.

Also, you can repeat a list using the multiply operator like this:

The result will be `[1, 2, 3, 1, 2, 3]`.

## Lists and Strings

A string is a sequence of characters and a list is a sequence of values, but a list of characters is not the same as a string.

To convert a string to a list of characters, you can use the `list` function like this:

The result will be `['L', 'i', 'k', 'e', 'G', 'e', 'e', 'k', 's']`.

The `list` function breaks a string into individual letters as shown.

If you want to break a string into words, you can use the `split` method instead:

The result will be `['Welcome', 'to', 'likegeeks', 'website']`.

As you can see, the returned output is a normal list; you can get any word by index and manipulate it.

Also, you can specify a delimiter for the `split` method. So, instead of the default delimiter (which is the space), you can supply another one.

## Join a List

The opposite process of splitting a string to a list of strings is to join them to make a string.

You can concatenate a list of strings to make a string using the join method like this:

The output will be `Welcome to likegeeks website`.

## Aliasing

When two variables referencing the same object like below, an object with more than one reference has more than one name. So, we say that the object is aliased.

Since Python lists are mutable, changes made with one alias affect the other:

The result will be `['Welcome', 'to', 'likegeeks', 'page']`.

We made a change to `list2`, but since they are referencing to the same object and that object is mutable, the changes affect the original list.

It is safer to avoid aliasing when you are working with mutable objects like lists.

It can be useful, but it can also be a source of errors -- so be careful when working with mutable objects when they are aliased.

Working with a Python list is very easy, as we've seen. I hope you find the post useful and interesting. Keep coming back!

[Check out](https://dzone.com/go?i=200130&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) the Exaptive data application Studio. Technology agnostic. No glue code. Use what you know and rely on the community for what you don't. [Try the community version](https://dzone.com/go?i=200130&u=https%3A%2F%2Fexaptive.city%2F%23%2Flanding%3Freferrer%3DGeneral).
