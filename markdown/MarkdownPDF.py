# https://gist.github.com/SpotlightKid/0efb4d07f28af1c8fc1b

# https://forum.omz-software.com/topic/1037/convert-markdown-to-pdf-with-pythonista-offline-no-other-apps

# Markdown to PDF Conversion
#
# This script converts Markdown markup to PDF directly on your iOS device.
#
# Please see the "Requirements" section in the docstring below for required 
# dependencies and the "Installation" section for instructions on how to
# install them.
#
# Run this script directly or put it into the Pythonista editor action menu 
# with one of the following options as the first and sole argument:
#
# -e     Use the text of the current editor buffer as input
# -c     Use the file currently opened in the editor as input
#
# These two options will use different input if the current editor buffer
# contains unsaved changes.
#
# You can also pass the path of a file to use as input directly as a command
# line argument. Called without arguments, the script will present a dialog
# where you can choose either to convert the text from the clipboard, from
# a URL or the README. 
#
"""Markdown to PDF Conversion
==========================

**Markdown** is a plain text formatting language invented by [John Gruber] [1].


Overview
--------

*Yes, it is possible:* convert Markdown markup text to PDF files on iOS with
Python - without the use of external apps or a web service. The conversion is
done *purely* in Python, which means it can be done *offline* and without
requiring additional paid apps (you need [Pythonista] [2], of course).

The Markdown text is first converted to HTML with [markdown2] [4] and then its
HTML output is converted to PDF with [xhtml2pdf] [4] and written to a file with
the given name.


Usage
-----

Here is the most basic code to convert some Markdown text:

    from markdown2pdf import markdown2pdf
    markdown2pdf('This is a *test*', 'test.pdf')

The Markdown to HTML conversion supports standard Markdown syntax with the
following extras enabled by default (see the [markdown2] [3] web site for
more information on these extras):

* fenced-code-blocks
* footnotes
* metadata
* pyshell
* smarty-pants
* tag-friendly
* wiki-tables

To use additional extras or disable some, pass a list of extra names via the
`extras` keyword argument, which will override the default extras list:

    markdown2pdf(text, 'test.pdf', extras=['code-friendly', 'smarty-pants'])

The appearance and layout of the PDF output is determined by the default CSS
definitions used by `xhtml2pdf`. You can overwrite the default CSS by passing
in a string of CSS definitions via the `css` keyword argument. If you only
want to change certain styles, you can import the default CSS from `xhtml2pdf`
and add to it:

    from xhtml2pdf.default import DEFAULT_CSS

    DEFAULT_CSS += \"""
    html {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 12pt;
    }
    \"""

    markdown2pdf(text, 'test.pdf', css=DEFAULT_CSS)

See the [xhtml2pdf usage guide] [5] for more information on the supported CSS
properties and page layout directives.


Requirements
------------

The `markdown2pdf` module requires the following Python packages:

* [markdown2] [3] \*
* [html5lib](http://pypi.python.org/pypi/html5lib) \*
* PIL or [Pillow](http://python-pillow.github.io/) (optional) \*
* [PyPDF2](http://mstamy2.github.io/PyPDF2/) (optional)
* [ReportLab](http://reportlab.com)
* [xhtml2pdf] [4]

Packages marked with an asterisk are already included with Pythonista. All
these packages, except PIL / Pillow, are pure-Python code or the included
C extensions are optional (ReportLab).


Installation
------------

I have created a bundle of all the above libraries, which are not already
included in Pythonista, as a Zip archive. You have to extract this archive into
the `site-packages` sub-directory of your Pythonista document folder. You can
use the following code in the Pythonista console to download and extract the
Zip archive:

    import os, requests, zipfile

    ZIPFN = 'markdown2pdf.zip'
    ZIPURL = 'http://chrisarndt.de/projects/markdown2pdf/' + ZIPFN

    with open(ZIPFN, 'wb') as f:
        f.write(requests.get(ZIPURL).content)

    with zipfile.ZipFile(ZIPFN) as z:
        z.extractall('site-packages')

    os.unlink(ZIPFN)

You can also download a version of the above script, which also checks the
integrity of the downloaded Zip file, from this Gist:

[download_md2pdf.py](https://gist.github.com/SpotlightKid/9e03a7823827a1841b6b)

[1]: http://daringfireball.net
[2]: http://omz-software.com/pythonista
[3]: https://github.com/trentm/python-markdown2
[4]: http://www.xhtml2pdf.com
[5]: https://github.com/chrisglass/xhtml2pdf/blob/master/doc/usage.rst

"""

__author__  = 'Christopher Arndt'
__version__ = '1.1'

import argparse
import logging
import os
import sys
import tempfile

from os.path import basename, join, splitext

import console
import editor

from markdown2pdf import markdown2pdf


def make_pdf_filename(fn):
    return splitext(basename(fn))[0] + '.pdf'

def main(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--current-file', action='store_true',
        help='Use file currently opened in editor as input')
    ap.add_argument('-e', '--edit-buffer', action='store_true',
        help='Use content of current editor buffer as input')
    ap.add_argument('infile', nargs='?', help='Input file name')
    
    args = ap.parse_args(args if args is not None else sys.argv[1:])

    if args.edit_buffer or args.current_file:
        pdf_bn = make_pdf_filename(editor.get_path())

    if args.current_file:
        with open(editor.get_path()) as f:
            md = f.read()
    elif args.edit_buffer:
        md = editor.get_text()
    elif args.infile:
        pfd_bn = make_pdf_filename(args.infile)
        with open(args.infile) as f:
            md = f.read()
    else:
        pdf_bn = 'markdown2pdf.pdf'

        try:
            choice = console.alert('Markdown to PDF', '',
                'Show README', 'Convert Clipboard', 'Convert URL')
        except KeyboardInterrupt:
            return

        if choice == 1:
            md = __doc__
        elif choice == 2:
            import clipboard
            md = clipboard.get()
        elif choice == 3:
            import re
            import clipboard
            try:
                cb = clipboard.get().strip()
                if not re.search('^(ht|f)tps?://', cb):
                    cb = ''
                url = console.input_alert('Enter URL', 'Download Markdown from URL:',
                    cb, 'Download')
            except KeyboardInterrupt:
                return
            else:
                import urllib2
                import urlparse
                try:
                    r = urllib2.urlopen(url)
                except urllib2.URLError as exc:
                    print(exc)
                    console.hud_alert("Download error (see console)", 'error')
                    return
                else:
                    md = r.read()

                url = urlparse.urlparse(r.geturl())
                fn = make_pdf_filename(url.path)
                if fn:
                    pdf_bn = fn

    if not md:
        return

    tempdir = tempfile.mkdtemp()
    pdf_path = join(tempdir, pdf_bn)
    console.show_activity()
    status = markdown2pdf(md, pdf_path)
    console.hide_activity()

    try:
        choice = console.alert('Select Ouput', '',
            'Save to file...', 'Open in...', 'View')
    except KeyboardInterrupt:
        return

    if choice == 1:
        try:
            filename = console.input_alert("Filename",
                "Enter PDF output filename\n(will overwrite existing files!):",
                pdf_bn, 'Save')
            os.rename(pdf_path, filename)
        except KeyboardInterrupt:
            return
        except (IOError, OSError) as exc:
            console.alert("Error", "Error writing PDF file:\n\n%s" % exc)
            return 1
    elif choice == 2:
        console.open_in(pdf_path)
    elif choice == 3:
        console.quicklook(pdf_path)

    try:
        os.unlink(pdf_path)
        os.rmdir(tempdir)
    except: pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    main(sys.argv[1:])
