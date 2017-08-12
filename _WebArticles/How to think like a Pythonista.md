# How to think like a Pythonista

_Captured: 2015-10-26 at 18:19 from [python.net](http://python.net/crew/mwh/hacks/objectthink.html)_

This is an archive of part of a thread on comp.lang.python, kept here so I can post links to it when it seems appropriate (it dealt with a question that comes up relatively often).

If you want you can read the thread [on google](http://groups.google.com/groups?hl=en&threadm=3CBD1C02.8AB2CF62%40yahoo.com&rnum=1) instead.

In the recent past (this is being written in April 2002, for reference), a searcher after enlightenment posted the following query to [comp.lang.python](news:comp.lang.python):

> 
>     Hello,
>     
>     one thing I like very much about Python is that statements
>     work like you would expect them to work. Take for example
>     the use of dict.values() for dictionaries: If you store the
>     result of dict.values(), and change the dictionary after-
>     wards, the previously stored result remains untouched.
>     
>     >>> dict = {'a':1,'b':2}
>     >>> list = dict.values()
>     >>> list
>     [1, 2]
>     >>> dict['a']=3
>     >>> list
>     [1, 2]
>     >>> dict
>     {'a': 3, 'b': 2}
>     
>     However, if a dictionary has lists as value entries, I get
>     a counterintuitive behavior (which, just recently, broke my
>     code): If you change the dict, the list you previously
>     created via dict.values() gets automagically updated. A nice
>     feature, but nothing I would have expected!
>     
>     >>> dict = {'a':[1],'b':[2]}
>     >>> list = dict.values()
>     >>> list
>     [[1], [2]]
>     >>> dict['a'].append(3)
>     >>> dict
>     {'a': [1, 3], 'b': [2]}
>     >>> list
>     [[1, 3], [2]]
>     
>     Looks like that in the first case a copy is returned while
>     in the latter case list references are returned. Ok, but
>     according to Python's philosophy I shouldn't mind if I work
>     with lists in the dictionary or anything else. If the
>     behavior depends on the knowledge of the type of values I
>     put into a dictionary, I find that somehow counterintuitive.
>     
>     Who is wrong here: my intuition or Python (2.2)? If it's
>     my intuition, how can I train my thinking about Python's
>     execution model, so that my intuition get's better ;-)
>     

Almost needless to say, it was the poster's intuition that was at fault, but he is (was) far from unique in having this sort of misconception.

Luckily for him, two more Pythonically experienced posters -- myself and Alex Martelli -- were in a particularly pedagogical mood that day¹, and wrote lengthy articles explaining in rather different ways where he was going wrong.

I ranted about thinking in terms of "names, objects and bindings", something I don't do enough, and drew some ascii art diagrams explaining what was going on under the covers of the interactive sessions the OP was confused about: 

> 
>     > one thing I like very much about Python is that statements
>     > work like you would expect them to work.
>     
>     Well, Python works very much as I expect it, but it's not clear if
>     this says more about me or Python <wink>.
>     
>     At the end of your email, you say:
>     
>     > Who is wrong here: my intuition or Python (2.2)? If it's
>     > my intuition, how can I train my thinking about Python's
>     > execution model, so that my intuition get's better ;-)
>     
>     It's you :) As I can't read my email at the moment[[1]](http://python.net/crew/mwh/hacks/objectthink.html), I have no
>     better way of wasting my time to hand than drawing you some ascii art.
>     
>     First, some terminology.  Actually, the very first thing is some
>     anti-terminology; I find the word "variable" to be particularly
>     uphelpful in a Python context.  I prefer "names", "bindings" and
>     "objects".
>     
>     Names look like this:
>     
>         ,-----.
>         | foo |
>         `-----'
>     
>     Names live in namespaces, but that's not really important for the
>     matter at hand as the only namespace in play is the one associated
>     with the read-eval-print loop of the interpreter.  In fact names are
>     only minor players in the current drama; bindings and objects are the
>     real stars.
>     
>     Bindings look like this:
>     
>         ------------>
>     
>     Bindings' left ends can be attached to names, or other "places" such
>     as attributes of objects and entries in lists or dictionaries.  Their
>     right hand ends are always attached to objects[[2]](http://python.net/crew/mwh/hacks/objectthink.html).
>     
>     Objects look like this:
>     
>         +-------+
>         | "bar" |
>         +-------+
>     
>     This is meant to be the string "bar".  Other types of object will be
>     drawn differently, but I hope you'll work out what I'm up to.
>     
>     > Take for example the use of dict.values() for dictionaries: If you
>     > store the result of dict.values(), and change the dictionary after-
>     > wards, the previously stored result remains untouched.
>     > 
>     > >>> dict = {'a':1,'b':2}
>     
>     After this statement, it would seem appropriate to draw this picture:
>     
>         ,------.       +-------+
>         | dict |------>|+-----+|     +---+
>         `------'       || "a" |+---->| 1 |
>                        |+-----+|     +---+
>                        |+-----+|     +---+
>                        || "b" |+---->| 2 |
>                        |+-----+|     +---+
>                        +-------+
>     
>     > >>> list = dict.values()
>     
>     Now this:
>     
>         ,------.       +-------+
>         | dict |------>|+-----+|             +---+
>         `------'       || "a" |+------------>| 1 |
>                        |+-----+|             +---+
>                        |+-----+|              /\
>                        || "b" |+-----.    ,---'
>                        |+-----+|     |    |
>                        +-------+     `----+----.
>                                           |    |
>         ,------.       +-----+            |    \/
>         | list |------>| [0]-+------------'   +---+
>         `------'       | [1]-+--------------->| 2 |
>                        +-----+                +---+
>     
>     > >>> list
>     > [1, 2]
>     
>     Which is of course, no surprise.
>     
>     > >>> dict['a']=3
>     
>     Now this:
>     
>     
>         ,------.       +-------+
>         | dict |------>|+-----+|             +---+
>         `------'       || "a" |+-.           | 1 |
>                        |+-----+| |           +---+
>                        |+-----+| |            /\
>                        || "b" |+-+---.    ,---'
>                        |+-----+| |   |    |
>                        +-------+ |   `----+----.
>                                  |        |    |
>         ,------.       +-----+   |        |    \/
>         | list |------>| [0]-+---+--------'   +---+
>         `------'       | [1]-+---+----------->| 2 |
>                        +-----+   |            +---+
>                                  |            +---+
>                                  `----------->| 3 |
>                                               +---+
>     
>     
>     > >>> list
>     > [1, 2]
>     > >>> dict
>     > {'a': 3, 'b': 2}
>     
>     These should also come as no surprise; just chase the arrows
>     (bindings) above.
>     
>     > However, if a dictionary has lists as value entries, I get
>     > a counterintuitive behavior (which, just recently, broke my
>     > code): If you change the dict, the list you previously
>     > created via dict.values() gets automagically updated. A nice
>     > feature, but nothing I would have expected!
>     
>     That's because you're not thinking in terms of Names, Objects and
>     Bindings.
>     
>     > >>> dict = {'a':[1],'b':[2]}
>     
>         ,------.       +-------+
>         | dict |------>|+-----+|     +-----+   +---+
>         `------'       || "a" |+---->| [0]-+-->| 1 |
>                        |+-----+|     +-----+   +---+
>                        |+-----+|     +-----+   +---+
>                        || "b" |+---->| [0]-+-->| 2 |
>                        |+-----+|     +-----+   +---+
>                        +-------+
>     
>     > >>> list = dict.values()
>     
>         ,------.       +-------+
>         | dict |------>|+-----+|             +-----+   +---+
>         `------'       || "a" |+------------>| [0]-+-->| 1 |
>                        |+-----+|             +-----+   +---+
>                        |+-----+|               /\
>                        || "b" |+-----.    ,----'
>                        |+-----+|     |    |
>                        +-------+     `----+-----.
>                                           |     |
>         ,------.       +-----+            |     \/
>         | list |------>| [0]-+------------'   +-----+   +---+
>         `------'       | [1]-+--------------->| [0]-+-->| 2 |
>                        +-----+                +-----+   +---+
>     
>     > >>> list
>     > [[1], [2]]
>     
>     Again, no surprises here.
>     
>     > >>> dict['a'].append(3)
>     
>                                                         +---+
>         ,------.       +-------+                     ,->| 1 |
>         | dict |------>|+-----+|             +-----+ |  +---+
>         `------'       || "a" |+------------>| [0]-+-'
>                        |+-----+|             | [1]-+-.
>                        |+-----+|             +-----+ |  +---+
>                        || "b" |+-----.         /\    `->| 3 |
>                        |+-----+|     |    ,----'        +---+
>                        +-------+     |    |
>                                      `----+-----.
>         ,------.       +-----+            |     \/
>         | list |------>| [0]-+------------'   +-----+   +---+
>         `------'       | [1]-+--------------->| [0]-+-->| 2 |
>                        +-----+                +-----+   +---+
>     
>     > >>> dict
>     > {'a': [1, 3], 'b': [2]}
>     > >>> list
>     > [[1, 3], [2]]
>     
>     And now these should not be surprising either.
>     
>     > Looks like that in the first case a copy is returned while
>     > in the latter case list references are returned. Ok, but
>     > according to Python's philosophy I shouldn't mind if I work
>     > with lists in the dictionary or anything else. If the
>     > behavior depends on the knowledge of the type of values I
>     > put into a dictionary, I find that somehow counterintuitive.
>     
>     If you haven't realised where you're misconceptions come from from the
>     above pictures, I'm not sure more prose would help.
>     
>     Cheers,
>     M.
>     [[1]](http://python.net/crew/mwh/hacks/objectthink.html) Does anyone know where the starship's gone?
>     [[2]](http://python.net/crew/mwh/hacks/objectthink.html) Anyone mentioning UnboundLocalError at this point will be shot.
>     
>     -- 
>       A.D. 1517: Martin Luther nails his 95 Theses to the church door and
>                  is promptly moderated down to (-1, Flamebait).
>             -- http://slashdot.org/comments.pl?sid=01/02/09/1815221&cid=52
>                                             (although I've seen it before)
>     

My access to email returned not long after posting, so my time wasting became more normal again. I might redraw the diagrams in [dia](http://www.lysator.liu.se/~alla/dia/) or something someday (although probably only if my email goes down again...).

Alex took a different, wordier strategy, explaining that Python doesn't copy when it doesn't have to, recounting a very nice anecdote about a statue in Bologna and suggesting that the OP read some Borges, Calvino, Wittgenstein or Korzibsky: 

> 
>     > Hello,
>     > 
>     > one thing I like very much about Python is that statements
>     > work like you would expect them to work. Take for example
>     > the use of dict.values() for dictionaries: If you store the
>     > result of dict.values(), and change the dictionary after-
>     > wards, the previously stored result remains untouched.
>     
>     The .values() method of a dictionary is defined to return
>     a new list of the values.  That's more or less inevitable, 
>     since a dictionary doesn't _have_ a list of its value 
>     normally, so it must build it on the fly when you ask for it.
>     It's not a copy -- it's a new list object.
>     
>     However, Python does NOT copy except in situations where
>     a copy is specifically defined to happen.  The .values()
>     method being in a vague sense such a situation, as mentioned...
>     a new object, rather than a copy of any existing one.
>     
>     In general, whenever possible, Python returns references 
>     to the same objects it already had around, rather than 
>     copying; if you DO want a copy you ask for it -- see module 
>     copy if you want to do so in a general way.  Of course,
>     building new objects is a different case.
>     
>     If this is counteintuitive, so be it -- there is really
>     no alternative in the general case without imposing huge
>     overhead, making copies of everything "just in case".
>     MUCH better to get copies only on explicit request (and
>     new objects, when there's no existing object that could
>     either be copied or referred-to).
>     
>     Of course there are in-between cases -- such as slices.
>     
>     The standard sequences give you a new object when you 
>     ask for a slice; this only matters for lists (for immutable
>     objects you shouldn't care if you get copies or what).
>     A list is not able to "share a part of itself", so when
>     asked for a slice it gives out a copy, a new list (for
>     generality, of course, it then also does when asked for
>     a slice-of-everything, thelist[:] -- so in that limit case
>     the new object can be seen as a copy of the existing one).
>     
>     The justly popular Numeric package, on the other hand,
>     defines an array type which IS able to share some or all 
>     data among several array objects -- so a slice of a Numeric 
>     array does share data with the array it's sliced from.  It's
>     a new object, mind you:
>     
>     >>> import Numeric
>     >>> a=Numeric.array(range(6))
>     >>> b=a[:]
>     >>> id(a)
>     136052568
>     >>> id(b)
>     136052728
>     >>>
>     
>     but the two distinct objects a and b do share data:
>     
>     >>> a
>     array([0, 1, 2, 3, 4, 5])
>     >>> b
>     array([0, 1, 2, 3, 4, 5])
>     >>> a[3]=23
>     >>> b
>     array([ 0,  1,  2, 23,  4,  5])
>     >>>
>     
>     
>     Each behavior has excellent pragmatics behind it -- lists 
>     are _way_ simpler by not having to worry about data sharing, 
>     arrays have different use cases by far -- but it's hard to 
>     be unsurprising when two somewhat similar objects differ 
>     in such details.
>     
>     But all of the copies which do "happen", e.g. by the
>     limit case of list slicing or whatever else (with ONE 
>     exception of which more later) are always SHALLOW copies.
>     
>     NEVER does Python embark on the HUGE task of _deep_ copying 
>     unless you very specifically ask it to -- specifically with 
>     function deepcopy of module copy.  DEEP copying is a serious 
>     matter -- function deepcopy has to watch out for cycles, 
>     reproduce any identity of references, potentially follow 
>     references to any depth, recursively -- it has to reproduce
>     faithfully a graph of objects referencing each other
>     with unbounded complexity.  It works, but of course it
>     can never be as fast as the mundane business of shallow
>     copying (which in turn is never as fast as just handing
>     out one more reference to an existing object, whenever
>     the latter course of action is feasible).
>     
>     
>     So, that's what has apparently snagged you here:
>     
>     > However, if a dictionary has lists as value entries, I get
>     > a counterintuitive behavior (which, just recently, broke my
>     > code): If you change the dict, the list you previously
>     > created via dict.values() gets automagically updated. A nice
>     > feature, but nothing I would have expected!
>     
>     Not really -- if you change _objects to which the dict refers_
>     (rather than changing the dict in se), then other references
>     to just-the-same-objects remain references to just the same
>     objects -- if the objects mutate, you see the mutated objects
>     from whatever references to them you may be using.
>     
>     
>     >>>> dict = {'a':[1],'b':[2]}
>     >>>> list = dict.values()
>     >>>> list
>     > [[1], [2]]
>     
>     Don't use the names of built-in types as variables: you WILL
>     be burned one day if you do this.  dict, list, str, tuple, file,
>     int, long, float, unicode... do NOT use these identifiers for 
>     your own purposes, tempting though they may be (an "attractive
>     nuisance", to be sure).  If you don't get into the habit of
>     avoiding them, one day you'll be trying to (e.g.) build a
>     list with x=list('ciao') and get puzzling errors... because
>     you have rebound identifier 'list' to refer to a certain list
>     object rather than to the list type itself.
>     
>     Use alist, somedict, myfile, whatever... nothing to do with
>     your problem here, just some other simple advice!-)
>     
>     
>     >>>> dict['a'].append(3)
>     
>     This does not "change the dictionary" -- the dictionary object
>     still contains exactly the same references, to objects with
>     the same id's (two string objects, the keys, and two list
>     objects, the values).  You're changing (mutating) one of those
>     objects, but that's quite another issue.  You could be
>     mutating said list object through any reference to it
>     whatsoever, e.g.:
>     
>     >>> alist=list('ciao')
>     >>> adict={'a':alist}
>     >>> adict
>     {'a': ['c', 'i', 'a', 'o']}
>     >>> alist.pop()
>     'o'
>     >>> adict
>     {'a': ['c', 'i', 'a']}
>     >>>
>     
>     If you wanted dictionary adict to refer to a COPY (a "snapshot",
>     if you will) of the contents of alist, you could have said so:
>     
>     >>> import copy
>     >>> alist=list('ciao')
>     >>> adict={'a':copy.copy(alist)}
>     >>> adict
>     {'a': ['c', 'i', 'a', 'o']}
>     >>> alist.pop()
>     'o'
>     >>> adict
>     {'a': ['c', 'i', 'a', 'o']}
>     >>>
>     
>     and then the dictionary object's string-representation would
>     be isolated from whatever changes to the list to which name
>     alist refers.  The string representation delegates part of its
>     job to the objects to which the dictionary object refers, so,
>     if you want to isolate it, you do need copies -- maybe deep
>     ones, in fact (<shudder>... well no, not really, but...:-).
>     
>     
>     >>>> dict
>     > {'a': [1, 3], 'b': [2]}
>     >>>> list
>     > [[1, 3], [2]]
>     > 
>     > Looks like that in the first case a copy is returned while
>     > in the latter case list references are returned. Ok, but
>     
>     Nope.  ALWAYS references.  .values() doesn't return a reference
>     to an existing object NOR a copy of an existing object, because
>     there's no "existing object" in this case -- so it always
>     returns a NEW object, suitably built as per its specs.
>     
>     > according to Python's philosophy I shouldn't mind if I work
>     > with lists in the dictionary or anything else. If the
>     > behavior depends on the knowledge of the type of values I
>     > put into a dictionary, I find that somehow counterintuitive.
>     
>     There is no such dependence.  Just a huge difference
>     between changing an object, and changing (mutating) some
>     OTHER object to which the first refers.
>     
>     In Bologna over 100 years ago we had a statue of a local hero
>     depicted pointing forwards with his finger -- presumably to
>     the future, but given where exactly it was placed, the locals
>     soon identified it as "the statue that points to Hotel
>     Belfiore".  The one day some enterprising developer bought
>     the hotel's building and restructured it -- in particular,
>     where the hotel used to be was now a restaurant, Da Carlo.
>     
>     So, "the statue that points to Hotel Belfiore" had suddenly
>     become "the statue that points to Da Carlo"...!  Amazing
>     isn't it?  Considering that marble isn't very fluid and the
>     statue had not been moved or disturbed in any way...?
>     
>     This is a real anecdote, by the way (except that I'm not
>     sure of the names of the hotel and restaurant involved --
>     I could be wrong on those), but I think it can still help
>     here.  The dictionary, or statue, has not changed at all,
>     even though the objects it refers/points to may have been
>     mutated beyond recognition, and the name people know it
>     by (the dictionary's string-representation) may therefore
>     change.  That name or representation was and is referring
>     to a non-intrinsic, non-persistent, "happenstance"
>     characteristic of the statue, or dictionary...
>     
>     
>     > Who is wrong here: my intuition or Python (2.2)? If it's
>     > my intuition, how can I train my thinking about Python's
>     > execution model, so that my intuition get's better ;-)
>     
>     Your intuition, which led you astray here (Python does just
>     what it should do), can be trained in several ways.  The
>     works of J. L. Borges and I. Calvino, if you like fiction
>     that's reasonably sophisticated but still quite pleasant,
>     are good bets.  If you like non-fiction written by
>     engineers fighting hard to dispell some of the errors of
>     philosophers, Wittgenstein and Korzibsky are excellent.
>     
>     I'm not kidding, but I realize that many Pythonistas don't
>     really care for either genre.  In which case, this group
>     and its archives, essays by GvR and /F, and the Python
>     sources, may also prove interesting reading.
>     
>     
>     Alex
>     

The essay by /F that Alex was referring to was probably [this one](http://effbot.org/guides/python-objects.htm) (and even if it wasn't, you should still read it). It talks about some of the same issues in a terser style.

And just to prove that there is some point in all this, the OP went away a satisfied customer: 

> 
>     Dear Michael, dear Alex,
>     
>     you are excellent teachers!!!
>     
>     Michael, you helped me really getting the point with your
>     drawings. Thanks a lot for your art work!
>     
>     Alex, the anecdote about the statue pointing to Hotel Belfiore
>     made my wrong intuition so obvious! I like that and will never
>     ever forget it anymore! Thanks for your answer!
>     
>     I think, today I learnt a lot on my way becoming a real Pythoniac!
>     

I hope you found these answers useful too.

¹ Well, he was lucky to catch me in such a mood. Alex writes articles like this all the time.

If you want to translate this document, by all means feel free. It would be nice if you sent me a link to your translation. So far I know about

  * Hernan Martinez Foffani's [Spanish](http://www.orgmf.com.ar/condor/objectthink.html) translation
