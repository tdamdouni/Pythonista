# Markdown Conversion Demo

**Markdown** is a plain text formatting language
invented by [John Gruber][1].

You can use this script to convert markdown
documents to html and preview them in the
built-in browser.

Markdown makes it easy to make text **bold** or *italic*,
and to add [links][2].

You can also format block quotes:

> Any intelligent fool can make things bigger, more
> complex, and more violent. It takes a touch of genius
> -- and a lot of courage -- to move in the opposite
> direction.

*-- Albert Einstein*

...and code blocks:
	
    from markdown2 import markdown
    text = "*hello world*"
    html = markdown(text)
    print html

For more detailed information about Markdown,
please read the [introduction and syntax reference][3]
on the project page.

[1]: http://daringfireball.net
[2]: http://omz-software.com/pythonista
[3]: http://daringfireball.net/projects/markdown