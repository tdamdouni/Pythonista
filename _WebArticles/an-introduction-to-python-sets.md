# An Introduction to Python Sets

_Captured: 2017-06-27 at 20:49 from [dzone.com](https://dzone.com/articles/an-introduction-to-python-sets?edition=305152&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-06-26)_

Effortlessly power IoT, predictive analytics, and machine learning applications with an [elastic, resilient data infrastructure](https://dzone.com/go?i=207144&u=https%3A%2F%2Fmesosphere.com%2Fsolutions%2Fdata%2F%3Futm_source%3Ddzone%26utm_medium%3Dbig-data%26utm_term%3Dpre-article%26utm_content%3D101). Learn how with [Mesosphere DC/OS](https://dzone.com/go?i=207144&u=https%3A%2F%2Fmesosphere.com%2Fproduct%2F%3Futm_source%3Ddzone%26utm_medium%3Dbig-data%26utm_term%3Dpre-article%26utm_content%3D101).

Python supports sets, which are a collection of unique elements and provide operations for computing set unions, intersections, and differences.

## Introduction

A set is a collection of unique elements. A common use is to eliminate duplicate elements from a list. In addition, it supports set operations like union intersection and difference.

## Creating a Set

This involves brace construction and set comprehension.

### **Brace Construction**

Creating a set looks similar to creating a dictionary; you enclose a bunch of items within braces.

Notice that the `set` contains unique elements only even though we put duplicates into it.

A set need not contain elements of the same type. You can mix and match element types as you like.

### **Set Comprehension**

Similar to dictionaries and lists, you can use set comprehension as in the following example of a set of squares.
    
    
    a = {x*x for x in xrange(10)}
    
    
    set([0, 1, 4, 81, 64, 9, 16, 49, 25, 36])

## Using the `set()` Constructor

Create a set from a list using the `set()` constructor.

How about creating a set of characters comprising a string? This shortcut will work.

Creating a set of unique random numbers:
    
    
    a = [random.randint(0, 10) for x in xrange(10)]

## Methods of `set`

The following sections explain the most commonly used methods of sets.

### Membership Testing

The boolean expressions `elem in a` and `elem not in a` allow checking for membership of a set.
    
    
    a = {'apple', 'orange', 'banana', 'melon', 'mango'}
    
    
    set(['melon', 'orange', 'mango', 'banana', 'apple'])

### Set Size

You can obtain the size of a set (the number of elements) using the `len()` function.
    
    
    a = {'apple', 'orange', 'banana', 'melon', 'mango'}
    
    
    set(['melon', 'orange', 'mango', 'banana', 'apple'])

### Adding Elements to a Set

Use the `add()` method to add an element to the set. If the element does not exist, it is added. No errors are raised if the element does exist, though.
    
    
    a = [random.randint(0, 10) for x in xrange(10)]
    
    
    list => [3, 4, 7, 2, 8, 0, 4, 1, 0, 4]
    
    
    set => set([0, 1, 2, 3, 4, 7, 8])
    
    
    after add => set([0, 1, 2, 3, 4, 7, 8, 10])

You will need to use a loop to add multiple elements since the `add()` method accepts only a single argument.

You cannot add a `list` to a `set` since the list cannot be hashed.
    
    
    ----> 7 s.add([21, 22])

However, a `tuple` can be added since it is not mutable and hence hashable.

### Removing Elements from a Set

Remove a single element from a set using `remove()`.
    
    
    a = [random.randint(0, 10) for x in xrange(10)]
    
    
    list => [6, 6, 7, 6, 7, 5, 10, 3, 8, 3]
    
    
    set => set([3, 5, 6, 7, 8, 10])
    
    
    after remove => set([3, 5, 6, 7, 8])

A `KeyError` is raised if the element is not in the set. (Running the same code as above a couple of times generates a random sequence without `10` in the set.)
    
    
    list => [0, 4, 4, 4, 6, 6, 9, 5, 9, 6]
    
    
    ----> 5 s.remove(10)

Need to remove an element from a set without the pesky `KeyError`? Use `discard()`.

Remove all elements from a set? Use `clear()`.

## Set Operations

Let's now learn about set operations supported by a `set`.

### Disjoint Sets

A set is disjoint with another set if the two have no common elements. The method `isdisjoint()` returns `True` or `False` as appropriate.

Another example:

### Checking for Subset and Superset

Check whether all elements of a set are contained in another set using the `issubset()` method. You can also use the boolean form `setA <= setB`.

Using the form `setA < setB` checks for `setA` being a proper subset of `setB` (that is `setB` containing all elements from setA and then some more).

Need to check for a superset? Use `issuperset()` or `setA >= setB` or `setA > setB` for a proper superset.
    
    
    print 'issubset', a.issubset(b)

### Set Union

Compute the union of two or more sets using the `union()` method. A new set containing all elements of all sets is returned.

You can also use the _pipe_ operator (`|`) as shown below.
    
    
    set(['a', 1, 2, 3, 4, 5, 6, 'b', 'c', 'd'])
    
    
    set(['a', 1, 2, 3, 4, 5, 6, 'b', 'c', 'd'])

### Set Intersection

How about identifying elements common to two or more sets? Use the `intersection()` method or the `&` operator.

### Set Difference

Set difference returns a new set containing all elements in the argument set that are not in the other sets.

## Iterating Over Sets

There are several ways of iterating over sets, most common ones are presented here.

  * A set is an iterable and hence can be used in a `for` loop for iterating over the elements.
    
        a = set([random.randint(0, 10) for _ in xrange(10)])

  * The ever-present `enumerate()` function is available, which returns a tuple of loop index and the element. Note that the loop index does not have any correlation to the set; in other words, a set does not have a concept of any ordering, so the _index_ is not an index into the set. It is just a loop counter.

## Conclusion

And that's it for now with sets. We learned how to create sets using the brace notation as well as the `set` constructors. Next up were the various commonly used operations with sets.

Learn to design and build better data-rich applications with this [free eBook from O'Reilly](https://dzone.com/go?i=207145&u=https%3A%2F%2Fmesosphere.com%2Fresources%2Fdesigning-data-intensive-applications%2F%3Futm_source%3Ddzone%26utm_medium%3Dbig-data%26utm_campaign%3Doreilly-data-apps-ebook%26utm_term%3Dpost-article%26utm_content%3D202). Brought to you by [Mesosphere DC/OS](https://dzone.com/go?i=207145&u=https%3A%2F%2Fmesosphere.com%2Fproduct%2F%3Futm_source%3Ddzone%26utm_medium%3Dbig-data%26utm_campaign%3Doreilly-data-apps-ebook%26utm_term%3Dpost-article%26utm_content%3D202).
