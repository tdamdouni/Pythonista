#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""Convert Markdown markup text to a PDF file.

Converts Markdown text to HTML first with python-markdown2 and then converts
its HTML output to PDF with xhtml2pdf.

"""

__all__ = [
    'DEFAULT_CSS',
    'DEFAULT_EXTRAS',
    'html2pdf',
    'markdown2pdf'
]

from markdown2 import markdown
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_CSS

__author__  = 'Christopher Arndt'
__version__ = '1.0'

DEFAULT_CSS += """\
html {
    font-family: Times New Roman, serif;
    font-size: 14pt;
}

pre,
code,
kbd,
samp,
tt {
    font-size: 12pt;
}

"""

DEFAULT_EXTRAS = [
    'fenced-code-blocks',
    'footnotes',
    'metadata',
    'pyshell',
    'smarty-pants',
    'tag-friendly',
    'wiki-tables'
]

def html2pdf(html, filename, css=DEFAULT_CSS):
    with open(filename, "wb") as fp:
        # convert HTML to PDF
        status = pisa.CreatePDF(html, dest=fp, default_css=css)
        return status.err

def markdown2pdf(text, filename, css=DEFAULT_CSS, extras=DEFAULT_EXTRAS, **kw):
    return html2pdf(markdown(text, extras=extras, **kw), filename, css)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.ERROR)

    with open(sys.argv[1]) as fp:
        markdown2pdf(fp.read(), sys.argv[2])

