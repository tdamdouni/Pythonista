# Python 101: Equality vs Identity

_Captured: 2017-03-10 at 19:25 from [dzone.com](https://dzone.com/articles/python-101-equality-vs-identity?edition=278882&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-03-10)_

[Evolve your approach to Application Performance Monitoring](https://dzone.com/go?i=161135&u=http%3A%2F%2Fwww.bmc.com%2Fforms%2FPA-APM-BMCcom-FY17-eBook-Form.html) by adopting five best practices that are outlined and explored in this [e-book](https://dzone.com/go?i=161135&u=http%3A%2F%2Fwww.bmc.com%2Fforms%2FPA-APM-BMCcom-FY17-eBook-Form.html), brought to you in partnership with [BMC](https://dzone.com/go?i=161135&u=http%3A%2F%2Fwww.bmc.com%2Fforms%2FPA-APM-BMCcom-FY17-eBook-Form.html).

People who are new to the Python programming language can get a bit confused about the difference between `==` (equality) and Python's keyword `is` (identity). I have even seen experienced programmers who will find the difference subtle enough that they will introduce logic errors in their code due to a misunderstanding between the two. In this article, we will look at this interesting topic.

## Equality in Python

Many programming languages have the concept of equality and several use the double equals sign (`==`) to designate this concept. Let's take a look at equality in action:
    
    
    >>> num = 1 >>> num_two = num >>> num == num_two True

Here, we create a variable that we call `num` and assign it to the integer `1`. Next, we create a second variable called `num_two` and assign it to the value of `num`. Finally, we ask Python if `num` and `num_two` are equal. In this case, Python tells us that this expression is `True`.

Another way to think of equality is that we are asking Python if two variables contain the same thing. In the example above, they both contain the integer `1`. Let's see what happens when we create two lists with the same values:
    
    
    >>> list_one = [1, 2, 3] >>> list_two = [1, 2, 3] >>> list_one == list_two True

This worked out the way we expected.

Now let's see what happens if we ask Python about their identity:

What happened here? The first example returned `True`, but the second returned `False`! We will look into that in the next section.

## Identity in Python

When you ask Python about whether one object is the same as another object, you are asking if they have the same identity. Are they actually the same object? In the case of `num` and `num_two`, the answer is yes. Python provides an easy way to prove it via it's built-in `id()` function:

The reason that these two variables share the same identity is because we told Python they should back when we assigned num to num_two (i.e. `num_two` = `num`). If you come from C or C++, you can think of the identity as a pointer where num and `num_two` are both pointing to the same place in memory. If you use Python's `id()` function on the two list objects, you will quickly see that they have different identities:

Thus, when you ask Python the question `list_one is list_two`, you receive `False`. Note that you can also ask Python if one object is not another object:
    
    
    >>> list_one = [1, 2, 3] >>> list_two = [1, 2, 3] >>> list_one is not list_two True

Let's take a moment to find out what happens when you mix equality and identity up.

## Mixing It Up

I know when I was starting out as a Python programmer, these sorts of things would lead to silly mistakes. The reason is that I would see recommended statements like this one:

So, I would assume naively that you could do something like this:
    
    
    >>> def func(): return [1, 2, 3]   >>> list_one = [1, 2, 3] >>> list_two = func() >>> list_one is list_two False

Of course, that doesn't work as I now have two different objects with different identities. What I wanted to do here was this:

Another issue that is tangential to this one is when you create two variables that point to the same object, but you think you can work on them independently of each other:
    
    
    >>> list_one = list_two = [1, 2, 3] >>> list_one == list_two True >>> list_one is list_two True >>> list_two.append(5) >>> list_one [1, 2, 3, 5]

In this example, I created two variables that both pointed at one object. Then I tried adding an element to just `list_two`. What a lot of beginners don't realize is that they just added that element to `list_one` as well. The reason for this is that both `list_one` and `list_two` are pointing at the exact same object. This is proven when we asked Python is `list_one is list_two` and it returned `True`.

## Wrapping Up

Hopefully, by now you understand the differences between equality (`==`) and identity (`is`) in Python. Equality is basically just asking if the contents of the two object are the same and in the case of lists, it needs to be in the same order as well. Identity in Python refers to the object you are referring to. In Python, the identity of an object is a unique, constant integer (or long integer) that exists for the length of the object's life.

Learn tips and best practices for optimizing your capacity management strategy with the [Market Guide for Capacity Management](https://dzone.com/go?i=161136&u=http%3A%2F%2Fwww.bmc.com%2Fforms%2FPA-BCO-GartnerMarketGuide-CapMgmtTools-AR.html), brought to you in partnership with [BMC](https://dzone.com/go?i=161136&u=http%3A%2F%2Fwww.bmc.com%2Fforms%2FPA-BCO-GartnerMarketGuide-CapMgmtTools-AR.html).
