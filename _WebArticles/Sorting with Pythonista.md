# Sorting with Pythonista

_Captured: 2015-09-30 at 17:52 from [www.leancrew.com](http://www.leancrew.com/all-this/2013/08/sorting-with-pythonista/)_

I saw this tweet from [hiilppp](http://twitter.com/hiilppp) yesterday:

I pretty much knew what to expect before I followed [the link](https://gist.github.com/hiilppp/6139407): a short, elegant [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&at=10l4Fv) script that `split` the input on newlines, `sort`ed the resulting list, `join`ed the sorted list back into a series of lines, and sent the results back to [Drafts](https://itunes.apple.com/us/app/drafts/id502385074?mt=8&at=10l4Fv). And that's exactly what hiilppp had written.

It's really a wonderful little script--the kind that makes you wonder why you didn't think of it yourself. It reminded me of a project from several years ago in which common Unix shell commands were reimplemented in Perl to make them available on non-Unix systems (which, unfortunately, I can't find a link to). I can imagine Pythonista (via URL callbacks) serving the same purpose to filter text in Drafts.

But instead of writing a Pythonista version of `uniq`, I decided to take hiilppp's elegant code and garble it up to handle a situation I run into fairly often: alphabetizing a list of names. Here's the script I came up with:
    
    
     1  # To call script from Drafts, use the following URL as URL Action:
     2  # <pythonista://namesort?action=run&argv=[[draft]]>
     3   
     4  import urllib
     5  import webbrowser
     6  
     7  def lastname(s):
     8    n = s.split()
     9    if len(n) == 1:
    10      return n
    11    if n[-1] in ('Jr.', 'Sr.', 'I', 'II', 'III', 'IV', 'V'):
    12      suffix = n[-1:]
    13      firstnames = n[:-2]
    14      if n[-2][-1] == ',':
    15        return [n[-2][:-1]] + firstnames + suffix
    16      else:
    17        return [n[-2]] + firstnames + suffix
    18    else:
    19      firstnames = n[:-1]
    20      return [n[-1]] + firstnames
    21  
    22  a = sys.argv[1].split("\n")
    23  a.sort(key=lastname)
    24  a = "\n".join(a)
    25   
    26  webbrowser.open("drafts://x-callback-url/create?text=" + urllib.quote(a))
    
    

It's called `namesort`, and it's called from Drafts using URL scheme shown in Line 2,
    
    
    pythonista://namesort?action=run&argv=[[draft]]

which sends the current draft off to Pythonista for processing as the argument to the `namesort` script. After processing, a draft that looked like
    
    
    Julian Lennon
    Grover Washington, Jr.
    George P. Bush
    George Bush
    John Lennon
    Grover Washington
    Cher
    John Davison Rockefeller III

becomes
    
    
    George Bush
    George P. Bush
    Cher
    John Lennon
    Julian Lennon
    John Davison Rockefeller III
    Grover Washington
    Grover Washington, Jr.

As you can see, `namesort` handles one-word names, middle names and initials, and suffixes. The list of suffixes it knows about are in Line 11--you could extend that to others if you need to handle things like M.D. and Ph.D. It would also be easy to handle titles like Mr., Ms., and Dr., if needed. I never need those, so I kept the code as simple as I could.

One glaring deficiency in `namesort` is its inability to deal with compound surnames that aren't hyphenated. So if I were alphabetizing the list of British Prime Ministers, `namesort` would put David Lloyd George before William Gladstone instead of after. Pity. I can't think of a foolproof algorithm to handle this; there are just too many possible compound names. My kludgey workaround is to hyphenate the compounds before sorting and then dehyphenate them afterward.

The key (literally) to `namesort` is the `lastname` function, which takes a name and returns a list in the form `[last, first, middle, suffix]`, where some of the items could be missing and there could be more than one `middle`. This function is fed to the `sort` command on Line 23 and determines how the items in list `a` are compared. The rules for comparing lists are given [here](http://docs.python.org/2/reference/expressions.html#not-in)--basically, they're compared item by item.

I should turn this into a [BBEdit](https://itunes.apple.com/us/app/bbedit/id404009241?mt=12&at=10l4Fv) text filter.
