# Python’s re Module

_Captured: 2016-05-14 at 16:59 from [regular-expressions.mobi](http://regular-expressions.mobi/python.html)_

**[Easily use the power of regular expressions in your Python scripts](http://www.regexbuddy.com/python.html) with RegexBuddy.**  
Create and analyze regex patterns with RegexBuddy's intuitive regex building blocks. Implement regexes in your Python scripts with instant Python code snippets. Just tell RegexBuddy what you want to achieve, and copy and paste the auto-generated Python code. [Get your own copy of RegexBuddy now](http://www.regexbuddy.com/).

Python is a high level open source scripting language. Python's built-in "re" module provides excellent support for [regular expressions](http://www.regular-expressions.info/tutorial.html), with a modern and complete regex flavor. The only significant features missing from Python's regex syntax are [atomic grouping](http://www.regular-expressions.info/atomic.html), [possessive quantifiers](http://www.regular-expressions.info/possessive.html), and [Unicode properties](http://www.regular-expressions.info/unicode.html).

The first thing to do is to import the regexp module into your script with import re.

## Regex Search and Match

Call re.**search**(regex, subject) to apply a regex pattern to a subject string. The function returns None if the matching attempt fails, and a Match object otherwise. Since None evaluates to False, you can easily use re.search() in an if statement. The Match object stores details about the part of the string matched by the regular expression pattern.

You can set [regex matching modes](http://www.regular-expressions.info/modifiers.html) by specifying a special constant as a third parameter to re.search(). re.I or re.IGNORECASE applies the pattern case insensitively. re.S or re.DOTALL makes the [dot match newlines](http://www.regular-expressions.info/dot.html). re.M or re.MULTILINE makes the [caret and dollar](http://www.regular-expressions.info/anchors.html) match after and before line breaks in the subject string. There is no difference between the single-letter and descriptive options, except for the number of characters you have to type in. To specify more than one option, "or" them together with the | operator: re.search("^a", "abc", re.I | re.M).

By default, Python's regex engine only considers the letters A through Z, the digits 0 through 9, and the underscore as "[word characters](http://www.regular-expressions.info/shorthand.html)". Specify the flag re.L or re.LOCALE to make \w match all characters that are considered letters given the current locale settings. Alternatively, you can specify re.U or re.UNICODE to treat all letters from all scripts as word characters. The setting also affects [word boundaries](http://www.regular-expressions.info/wordboundaries.html).

Do not confuse re.search() with re.**match**(). Both functions do exactly the same, with the important distinction that re.search() will attempt the pattern throughout the string, until it finds a match. re.match() on the other hand, only attempts the pattern at the very start of the string. Basically, re.match("regex", subject) is the same as re.search("[\A](http://www.regular-expressions.info/anchors.html)regex", subject). Note that re.match() does _not_ require the regex to match the entire string. re.match("a", "ab") will succeed.

Python 3.4 adds a new re.**fullmatch**() function. This function only returns a Match object if the regex matches the string entirely. Otherwise it returns None. re.fullmatch("regex", subject) is the same as re.search("[\A](http://www.regular-expressions.info/anchors.html)regex[\Z](http://www.regular-expressions.info/anchors.html)", subject). This is useful for validating user input. If subject is an empty string then fullmatch() evaluates to True for any regex that can find a [zero-length match](http://www.regular-expressions.info/zerolength.html).

To get all matches from a string, call re.**findall**(regex, subject). This will return an array of all non-overlapping regex matches in the string. "Non-overlapping" means that the string is searched through from left to right, and the next match attempt starts beyond the previous match. If the regex contains one or more [capturing groups](http://www.regular-expressions.info/brackets.html), re.findall() returns an array of tuples, with each tuple containing text matched by all the capturing groups. The overall regex match is _not_ included in the tuple, unless you place the entire regex inside a capturing group.

More efficient than re.findall() is re.**finditer**(regex, subject). It returns an iterator that enables you to loop over the regex matches in the subject string: for m in re.finditer(regex, subject). The for-loop variable m is a Match object with the details of the current match.

Unlike re.search() and re.match(), re.findall() and re.finditer() do not support an optional third parameter with regex matching flags. Instead, you can use [global mode modifiers](http://www.regular-expressions.info/modifiers.html) at the start of the regex. E.g. "(?i)regex" matches regex case insensitively.

## Strings, Backslashes and Regular Expressions

The backslash is a [metacharacter](http://www.regular-expressions.info/characters.html) in regular expressions, and is used to escape other metacharacters. The regex \\\ matches a single backslash. \d is a [single token](http://www.regular-expressions.info/shorthand.html) matching a digit.

Python strings also use the backslash to escape characters. The above regexes are written as Python strings as "\\\\\\\" and "\\\w". Confusing indeed.

Fortunately, Python also has "raw strings" which do not apply special treatment to backslashes. As raw strings, the above regexes become r"\\\" and r"\w". The only limitation of using raw strings is that the delimiter you're using for the string must not appear in the regular expression, as raw strings do not offer a means to escape it.

You can use \n and \t in raw strings. Though raw strings do not support these escapes, the regular expression engine does. The end result is the same.

## Unicode

Prior to Python 3.3, Python's re module did not support any [Unicode regular expression tokens](http://www.regular-expressions.info/unicode.html). Python Unicode strings, however, have always supported the \uFFFF notation. Python's re module can use Unicode strings. So you could pass the Unicode string u"\u00E0\\\d" to the re module to match a followed by a digit. The backslash for \d was escaped, while the one for \u was not. That's because \d is a regular expression token, and a regular expression backslash needs to be escaped. \u00E0 is a Python string token that shouldn't be escaped. The string u"\u00E0\\\d" is seen by the regular expression engine as a\d.

If you did put another backslash in front of the \u, the regex engine would see \u00E0\d. If you use this regex with Python 3.2 or earlier, it will match the literal text u00E0 followed by a digit instead.

To avoid any confusion about whether backslashes need to be escaped, just use Unicode raw strings like ur"\u00E0\d". Then backslashes don't need to be escaped. Python does interpret Unicode escapes in raw strings.

In Python 3.0 and later, strings are Unicode by default. So the u prefix shown in the above samples is no longer necessary. Python 3.3 also adds support for the \uFFFF notation to the regular expression engine. So in Python 3.3, you can use the string "\\\u00E0\\\d" to pass the regex \u00E0\d which will match something like a0.

## Search and Replace

re.**sub**(regex, replacement, subject) performs a search-and-replace across subject, replacing all matches of regex in subject with replacement. The result is returned by the sub() function. The subject string you pass is not modified.

If the regex has [capturing groups](http://www.regular-expressions.info/brackets.html), you can use the text matched by the part of the regex inside the capturing group. To substitute the text from the third group, insert \3 into the replacement string. If you want to use the text of the third group followed by a literal three as the replacement, use \g<3>3\. \33 is interpreted as the 33rd group, and is substituted with nothing if there are fewer groups. If you used [named capturing groups](http://www.regular-expressions.info/named.html), you can use them in the replacement text with \g<name>.

The re.sub() function applies the same backslash logic to the replacement text as is applied to the regular expression. Therefore, you should use raw strings for the replacement text, as I did in the examples above. The re.sub() function will also interpret \n and \t in raw strings. If you want c:\temp as the replacement text, either use r"c:\\\temp" or "c:\\\\\\\temp". The 3rd backreference is r"\3" or "\\\3".

## Splitting Strings

re.**split**(regex, subject) returns an array of strings. The array contains the parts of subject between all the regex matches in the subject. Adjacent regex matches will cause empty strings to appear in the array. The regex matches themselves are not included in the array. If the regex contains [capturing groups](http://www.regular-expressions.info/brackets.html), then the text matched by the capturing groups is included in the array. The capturing groups are inserted between the substrings that appeared to the left and right of the regex match. If you don't want the capturing groups in the array, convert them into [non-capturing groups](http://www.regular-expressions.info/brackets.html). The re.split() function does not offer an option to suppress capturing groups.

You can specify an optional third parameter to limit the number of times the subject string is split. Note that this limit controls the number of splits, not the number of strings that will end up in the array. The unsplit remainder of the subject is added as the final string to the array. If there are no capturing groups, the array will contain limit+1 items.

## Match Details

re.search() and re.match() return a Match object, while re.finditer() generates an iterator to iterate over a Match object. This object holds lots of useful information about the regex match. I will use m to signify a Match object in the discussion below.

m.**group**() returns the part of the string matched by the entire regular expression. m.**start**() returns the offset in the string of the start of the match. m.**end**() returns the offset of the character beyond the match. m.**span**() returns a 2-tuple of m.start() and m.end(). You can use the m.start() and m.end() to slice the subject string: subject[m.start():m.end()].

If you want the results of a capturing group rather than the overall regex match, specify the name or number of the group as a parameter. m.group(3) returns the text matched by the third [capturing group](http://www.regular-expressions.info/brackets.html). m.group('groupname') returns the text matched by a [named group](http://www.regular-expressions.info/named.html) 'groupname'. If the group did not participate in the overall match, m.group() returns an empty string, while m.start() and m.end() return -1.

If you want to do a regular expression based search-and-replace without using re.sub(), call m.**expand**(replacement) to compute the replacement text. The function returns the replacement string with backreferences etc. substituted.

## Regular Expression Objects

If you want to use the same regular expression more than once, you should compile it into a regular expression object. Regular expression objects are more efficient, and make your code more readable. To create one, just call re.**compile**(regex) or re.**compile**(regex, flags). The flags are the matching options described above for the re.search() and re.match() functions.

The regular expression object returned by re.compile() provides all the functions that the re module also provides directly: search(), match(), findall(), finditer(), sub() and split(). The difference is that they use the pattern stored in the regex object, and do not take the regex as the first parameter. re.compile(regex).search(subject) is equivalent to re.search(regex, subject).

## Make a Donation

Did this website just save you a trip to the bookstore? Please [make a donation](http://www.regular-expressions.info/donate.html) to support this site, and you'll get a **lifetime of advertisement-free access** to this site! Credit cards, PayPal, and Bitcoin gladly accepted.
