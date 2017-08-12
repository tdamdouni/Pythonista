# PEP 0008 -- Style Guide for Python Code

_Captured: 2015-12-13 at 20:29 from [www.python.org](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)_

Many projects have their own coding style guidelines. In the event of any conflicts, such project-specific guides take precedence for that project.

One of Guido's key insights is that code is read much more often than it is written. The guidelines provided here are intended to improve the readability of code and make it consistent across the wide spectrum of Python code. As [ PEP 20 ](https://www.python.org/dev/peps/pep-0020) says, "Readability counts".

A style guide is about consistency. Consistency with this style guide is important. Consistency within a project is more important. Consistency within one module or function is most important.

But most importantly: know when to be inconsistent -- sometimes the style guide just doesn't apply. When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!

In particular: do not break backwards compatibility just to comply with this PEP!

Some other good reasons to ignore a particular guideline:

  1. When applying the guideline would make the code less readable, even for someone who is used to reading code that follows this PEP. 
  2. To be consistent with surrounding code that also breaks it (maybe for historic reasons) -- although this is also an opportunity to clean up someone else's mess (in true XP style). 
  3. Because the code in question predates the introduction of the guideline and there is no other reason to be modifying that code. 
  4. When the code needs to remain compatible with older versions of Python that don't support the feature recommended by the style guide. 

Use 4 spaces per indentation level.

Continuation lines should align wrapped elements either vertically using Python's implicit line joining inside parentheses, brackets and braces, or using a _ hanging indent _ [ [5] ](https://www.python.org/dev/peps/pep-0008/) . When using a hanging indent the following considerations should be applied; there should be no arguments on the first line and further indentation should be used to clearly distinguish itself as a continuation line.

Yes:
    
    
    # Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two,
                             var_three, var_four)
    
    # More indentation included to distinguish this from the rest.
    def long_function_name(
            var_one, var_two, var_three,
            var_four):
        print(var_one)
    
    # Hanging indents should add a level.
    foo = long_function_name(
        var_one, var_two,
        var_three, var_four)
    

No:
    
    
    # Arguments on first line forbidden when not using vertical alignment.
    foo = long_function_name(var_one, var_two,
        var_three, var_four)
    
    # Further indentation required as indentation is not distinguishable.
    def long_function_name(
        var_one, var_two, var_three,
        var_four):
        print(var_one)
    

The 4-space rule is optional for continuation lines.

Optional:
    
    
    # Hanging indents *may* be indented to other than 4 spaces.
    foo = long_function_name(
      var_one, var_two,
      var_three, var_four)
    

When the conditional part of an if -statement is long enough to require that it be written across multiple lines, it's worth noting that the combination of a two character keyword (i.e. if ), plus a single space, plus an opening parenthesis creates a natural 4-space indent for the subsequent lines of the multiline conditional. This can produce a visual conflict with the indented suite of code nested inside the if -statement, which would also naturally be indented to 4 spaces. This PEP takes no explicit position on how (or whether) to further visually distinguish such conditional lines from the nested suite inside the if -statement. Acceptable options in this situation include, but are not limited to:
    
    
    # No extra indentation.
    if (this_is_one_thing and
        that_is_another_thing):
        do_something()
    
    # Add a comment, which will provide some distinction in editors
    # supporting syntax highlighting.
    if (this_is_one_thing and
        that_is_another_thing):
        # Since both conditions are true, we can frobnicate.
        do_something()
    
    # Add some extra indentation on the conditional continuation line.
    if (this_is_one_thing
            and that_is_another_thing):
        do_something()
    

The closing brace/bracket/parenthesis on multi-line constructs may either line up under the first non-whitespace character of the last line of list, as in:
    
    
    my_list = [
        1, 2, 3,
        4, 5, 6,
        ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
        )
    

or it may be lined up under the first character of the line that starts the multi-line construct, as in:
    
    
    my_list = [
        1, 2, 3,
        4, 5, 6,
    ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
    )
    

Spaces are the preferred indentation method.

Tabs should be used solely to remain consistent with code that is already indented with tabs.

Python 3 disallows mixing the use of tabs and spaces for indentation.

Python 2 code indented with a mixture of tabs and spaces should be converted to using spaces exclusively.

When invoking the Python 2 command line interpreter with the -t option, it issues warnings about code that illegally mixes tabs and spaces. When using -tt these warnings become errors. These options are highly recommended!

Limit all lines to a maximum of 79 characters.

For flowing long blocks of text with fewer structural restrictions (docstrings or comments), the line length should be limited to 72 characters.

Limiting the required editor window width makes it possible to have several files open side-by-side, and works well when using code review tools that present the two versions in adjacent columns.

The default wrapping in most tools disrupts the visual structure of the code, making it more difficult to understand. The limits are chosen to avoid wrapping in editors with the window width set to 80, even if the tool places a marker glyph in the final column when wrapping lines. Some web based tools may not offer dynamic line wrapping at all.

Some teams strongly prefer a longer line length. For code maintained exclusively or primarily by a team that can reach agreement on this issue, it is okay to increase the nominal line length from 80 to 100 characters (effectively increasing the maximum length to 99 characters), provided that comments and docstrings are still wrapped at 72 characters.

The Python standard library is conservative and requires limiting lines to 79 characters (and docstrings/comments to 72).

The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

Backslashes may still be appropriate at times. For example, long, multiple with -statements cannot use implicit continuation, so backslashes are acceptable:
    
    
    with open('/path/to/some/file/you/want/to/read') as file_1, \
         open('/path/to/some/file/being/written', 'w') as file_2:
        file_2.write(file_1.read())
    

(See the previous discussion on [ multiline if-statements ](https://www.python.org/dev/peps/pep-0008/) for further thoughts on the indentation of such multiline with -statements.)

Another such case is with assert statements.

Make sure to indent the continued line appropriately. The preferred place to break around a binary operator is _ after _ the operator, not before it. Some examples:
    
    
    class Rectangle(Blob):
    
        def __init__(self, width, height,
                     color='black', emphasis=None, highlight=0):
            if (width == 0 and height == 0 and
                    color == 'red' and emphasis == 'strong' or
                    highlight > 100):
                raise ValueError("sorry, you lose")
            if width == 0 and height == 0 and (color == 'red' or
                                               emphasis is None):
                raise ValueError("I don't think so -- values are %s, %s" %
                                 (width, height))
            Blob.__init__(self, width, height,
                          color, emphasis, highlight)
    

Surround top-level function and class definitions with two blank lines.

Method definitions inside a class are surrounded by a single blank line.

Extra blank lines may be used (sparingly) to separate groups of related functions. Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations).

Use blank lines in functions, sparingly, to indicate logical sections.

Python accepts the control-L (i.e. ^L) form feed character as whitespace; Many tools treat these characters as page separators, so you may use them to separate pages of related sections of your file. Note, some editors and web-based code viewers may not recognize control-L as a form feed and will show another glyph in its place.

Code in the core Python distribution should always use UTF-8 (or ASCII in Python 2).

Files using ASCII (in Python 2) or UTF-8 (in Python 3) should not have an encoding declaration.

In the standard library, non-default encodings should be used only for test purposes or when a comment or docstring needs to mention an author name that contains non-ASCII characters; otherwise, using \x , \u , \U , or \N escapes is the preferred way to include non-ASCII data in string literals.

For Python 3.0 and beyond, the following policy is prescribed for the standard library (see [ PEP 3131 ](https://www.python.org/dev/peps/pep-3131) ): All identifiers in the Python standard library MUST use ASCII-only identifiers, and SHOULD use English words wherever feasible (in many cases, abbreviations and technical terms are used which aren't English). In addition, string literals and comments must also be in ASCII. The only exceptions are (a) test cases testing the non-ASCII features, and (b) names of authors. Authors whose names are not based on the latin alphabet MUST provide a latin transliteration of their names.

Open source projects with a global audience are encouraged to adopt a similar policy.

  * Imports should usually be on separate lines, e.g.: 
    
        Yes: import os
         import sys
    
    No:  import sys, os
    

It's okay to say this though: 
    
        from subprocess import Popen, PIPE
    

  * Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants. 

Imports should be grouped in the following order: 

    1. standard library imports 
    2. related third party imports 
    3. local application/library specific imports 

You should put a blank line between each group of imports. 

Put any relevant __all__ specification after the imports. 

  * Absolute imports are recommended, as they are usually more readable and tend to be better behaved (or at least give better error messages) if the import system is incorrectly configured (such as when a directory inside a package ends up on sys.path ): 
    
        import mypkg.sibling
    from mypkg import sibling
    from mypkg.sibling import example
    

However, explicit relative imports are an acceptable alternative to absolute imports, especially when dealing with complex package layouts where using absolute imports would be unnecessarily verbose: 
    
        from . import sibling
    from .sibling import example
    

Standard library code should avoid complex package layouts and always use absolute imports. 

Implicit relative imports should _ never _ be used and have been removed in Python 3. 

  * When importing a class from a class-containing module, it's usually okay to spell this: 
    
        from myclass import MyClass
    from foo.bar.yourclass import YourClass
    

If this spelling causes local name clashes, then spell them 
    
        import myclass
    import foo.bar.yourclass
    

and use "myclass.MyClass" and "foo.bar.yourclass.YourClass". 

  * Wildcard imports ( from <module> import * ) should be avoided, as they make it unclear which names are present in the namespace, confusing both readers and many automated tools. There is one defensible use case for a wildcard import, which is to republish an internal interface as part of a public API (for example, overwriting a pure Python implementation of an interface with the definitions from an optional accelerator module and exactly which definitions will be overwritten isn't known in advance). 

When republishing names this way, the guidelines below regarding public and internal interfaces still apply. 

[ [5] ](https://www.python.org/dev/peps/pep-0008/)
_ Hanging indentation _ is a type-setting style where all the lines in a paragraph are indented except the first line. In the context of Python, the term is used to describe a style where the opening parenthesis of a parenthesized statement is the last non-whitespace character of the line, with subsequent lines being indented until the closing parenthesis. 

Source: <https://hg.python.org/peps/file/tip/pep-0008.txt>
