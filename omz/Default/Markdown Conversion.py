# Markdown Conversion
# 
# This script demonstrates how you can convert Markdown documents
# to HTML and view the results in the built-in browser.

import os, tempfile, codecs
import console, clipboard, webbrowser
from markdown2 import markdown

DEMO = '''
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
'''

# Basic HTML document structure and CSS styling:
TEMPLATE = '''
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<style>
body {
	font-family: helvetica;
	font-size: 18px;
	color: #333;

}
blockquote {
	border-left: solid 3px #bbb;
	margin-left: 0px;
	padding-left: 10px;
}
pre {
	border: 1px solid #bbb;
	border-radius: 3px;
	padding: 3px;
	background-color: #f8f8f8;
}
code {
	font-family: DejaVuSansMono, monospace;
}
#wrapper {
	margin: 20px;}
</style>
</head>
<body>
<div id="wrapper">
{{CONTENT}}
</div>
</body>
</html>
'''

def main():
	choice = console.alert('Markdown Conversion', '', 'Demo', 'Convert Clipboard')
	md = DEMO if choice == 1 else clipboard.get()
	html = markdown(md, extras=['smarty-pants'])
	tempdir = tempfile.gettempdir()
	html_path = os.path.join(tempdir, 'temp.html')
	html = TEMPLATE.replace('{{CONTENT}}', html)
	with codecs.open(html_path, 'w', 'utf-8') as f:
		f.write(html)
	file_url = 'file://' + html_path
	webbrowser.open(file_url)

if __name__ == '__main__':
	main()
