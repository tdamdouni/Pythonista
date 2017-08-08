# Simple expense report with Drafts and Pythonista

_Captured: 2015-06-08 at 00:37 from [www.leancrew.com](http://www.leancrew.com/all-this/2013/10/simple-expense-report-with-drafts-and-pythonista/)_

I suppose there are dozens, if not hundreds, of expense-tracking apps in the App Store. I mostly want to track travel expenses, and I don't travel for work all that much, so my needs for such an app are pretty modest. My standards for usability, though, are high. I don't want to have to categorize my expenses or tap through field after field; I just want to enter them as quickly as I can as they arise and then get a total when I'm done. Basically, I just want to type the expenses into a text file and have the total pop out on its own. Which led me to [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&at=10l4Fv) and a [Drafts](https://itunes.apple.com/us/app/drafts/id502385074?mt=8&at=10l4Fv) action.

Before explaining the script and the action, I should mention that [Soulver](https://itunes.apple.com/us/app/soulver-notepad-calculator/id348142037?mt=8&at=10l4Fv) would be a pretty reasonable expense tracker, because it allows you to mix numbers and words and knows how to keep a running total of the numbers. It doesn't format the result, though, which is another feature I'd like to have. Also, since I'm a [PCalc](https://itunes.apple.com/us/app/pcalc-the-best-calculator/id284666222?mt=8&at=10l4Fv) user, I have Soulver buried in a folder that makes it inconvenient to bring up quickly. Drafts, on the other hand, is in my Dock.

Here's how the action works. I start with a draft that I add expenses to during the trip. The format for each expense line is
    
    
    Description Cost

where the description can be several words and there can be any number of spaces between it and the cost. The important thing is that the cost goes last.

![Raw expenses](http://farm3.staticflickr.com/2820/10238065086_aed1c9cc64_z.jpg)

> _[Raw expenses](http://www.flickr.com/photos/drdrang/10238065086/)_

When all the expenses have been added to the draft, I invoke the Total Expenses action and, after it takes a trip to Pythonista and back, I get this:

![Totalled expenses](http://farm8.staticflickr.com/7379/10238076135_a6b973828c_z.jpg)

> _[Totalled expenses](http://www.flickr.com/photos/drdrang/10238076135/)_

Boom.

The Pythonista script that does the work is this, which I have saved under the name "total":

     1  # To call script from Drafts, use the following URL as URL Action:
     2  # pythonista://total?action=run&argv=[[body]]&argv=[[title]]
     3  
     4  import sys
     5  import webbrowser
     6  import urllib
     7  
     8  raw = sys.argv[1].split('\n')
     9  title = sys.argv[2]
    10  cleaned = [title, '']
    11  numbers = []
    12  
    13  for line in raw:
    14    try:
    15      desc, cost = line.rsplit(None, 1)
    16      cost = float(cost.strip('$ '))
    17      numbers.append(cost)
    18      cleaned.append('{:<25}{:>10,.2f}'.format(desc, cost))
    19    except ValueError:
    20      cleaned.append(line)
    21  total = sum(numbers)
    22  while cleaned[-1].strip() == '':
    23    del cleaned[-1]
    24  cleaned.append('')
    25  cleaned.append('Total{:>30,.2f}'.format(total))
    26  cleaned = '\n'.join(cleaned)
    27  
    28  webbrowser.open("drafts://x-callback-url/create?text=" + urllib.quote(cleaned))

The body of the draft is passed to the script as its first argument and the title as the second. Line 8 reads the body and splits it into a list of lines. Lines 9-10 initialize the list of output lines with the title and a blank line.

The loop that starts on Line 13 goes through the list of lines, splitting them into the description and cost parts. Line 15 uses `[rsplit`](http://docs.python.org/2/library/stdtypes.html#string-methods) with a second argument of 1 to keep multiword descriptions intact. Line 16 then turns the cost string into a floating point number after stripping off any extraneous spaces or dollar signs. Line 17 then appends the cost to a separate list of numbers that we'll sum up after finishing the loop. Line 18 uses the `[format` method](http://docs.python.org/2/library/string.html#formatstrings) to get the description and the cost neatly aligned and appends it to a list of text lines we'll use for the output.

You'll note that the splitting and converting and formatting are all in a `try` block. That's because I expect some of the lines--blank or comment lines, for example--to not follow the "Description Cost" format. These lines will just be passed through unchanged, as shown in Line 20 in the `except` block.

When the loop is done, Line 21 adds all the numbers collected earlier. Lines 22-24 get rid of extraneous blank lines at the end of the list and put exactly one blank line before the total. Line 25 formats the totals line and appends it to the output list. Line 26 turns that output list into a block of text lines. Finally, Line 28 sends the cleaned-up block of output text back to Drafts.

The URL Action in Drafts is defined this way:

    pythonista://total?action=run&argv=[[body]]&argv=[[title]]

I call it Total Expenses and have it at the bottom of my second set of actions (the ones labeled II).

By sending the title and the body of the draft as separate entities to the script, I don't have to worry if there's a number at the end of my title line. A title of

    Expenses for October 12, 2013

won't cause 2,013.00 to be inadvertently added to the total.
