"""

    PDF to HTML converter.

"""
from __future__ import print_function

import os
import sys

import pyPdf
from pyPdf.pdf import ContentStream
from pyPdf.pdf import TextStringObject


SLIDE_TEMPLATE = u'<p class="slide"><img src="{prefix}{src}" alt="{alt}" /></p>'

# You can pass Ghostscript binary to the script as an environment variable.
GHOSTSCRIPT = os.environ.get("GHOSTSCRIPT", "gs")


def create_images(src, target, width=620, height=480):
    """ Create series of images from slides.

    http://right-sock.net/linux/better-convert-pdf-to-jpg-using-ghost-script/

    :param src: Source PDF file

    :param target: Target folder
    """

    if target.endswith("/"):
        target = target[0:-1]

    # Generated filenames
    ftemplate = "%(target)s/slide%%d.jpg" % locals()

    # gs binary
    ghostscript = GHOSTSCRIPT

    # Export magic of doing
    # Note: Ghostscript 9.06 crashed for me
    # had to upgrade 9.07
    # This command does magic of anti-aliasing text and settings output JPEG dimensions correctly
    cmd = "%(ghostscript)s -dNOPAUSE -dPDFFitPage -dTextAlphaBits=4 -sDEVICE=jpeg -sOutputFile=%(ftemplate)s -dJPEGQ=80 -dDEVICEWIDTH=%(width)d -dDEVICEHEIGHT=%(height)d  %(src)s -c quit"
    cmd = cmd % locals()  # Apply templating

    if os.system(cmd):
        raise RuntimeError("Command failed: %s" % cmd)


def extract_text(self):
    """ Patched extractText() from pyPdf to put spaces between different text snippets.
    """
    text = u""
    content = self["/Contents"].getObject()
    if not isinstance(content, ContentStream):
        content = ContentStream(content, self.pdf)
    # Note: we check all strings are TextStringObjects.  ByteStringObjects
    # are strings where the byte->string encoding was unknown, so adding
    # them to the text here would be gibberish.
    for operands, operator in content.operations:
        if operator == "Tj":
            _text = operands[0]
            if isinstance(_text, TextStringObject):
                text += _text
        elif operator == "T*":
            text += "\n"
        elif operator == "'":
            text += "\n"
            _text = operands[0]
            if isinstance(_text, TextStringObject):
                text += operands[0]
        elif operator == '"':
            _text = operands[2]
            if isinstance(_text, TextStringObject):
                text += "\n"
                text += _text
        elif operator == "TJ":
            for i in operands[0]:
                if isinstance(i, TextStringObject):
                    text += i

        if text and not text.endswith(" "):
            text += " "  # Don't let words concatenate

    return text


def scrape_text(src):
    """ Read a PDF file and return plain text of each page.

    http://stackoverflow.com/questions/25665/python-module-for-converting-pdf-to-text

    :return: List of plain text unicode strings
    """

    pages = []

    pdf = pyPdf.PdfFileReader(open(src, "rb"))
    for page in pdf.pages:
        text = extract_text(page)
        pages.append(text)

    return pages


def create_index_html(target, slides, prefix):
    """ Generate HTML code for `<img>` tags.
    """

    out = open(target, "wt")

    print("<!doctype html>", file=out)
    for i in xrange(0, len(slides)):
        alt = slides[i]  # ALT text for this slide
        params = dict(src=u"slide%d.jpg" % (i+1), prefix=prefix, alt=alt)
        line = SLIDE_TEMPLATE.format(**params)
        print(line.encode("utf-8"), file=out)

    out.close()


def main():
    """ Entry point. """

    if len(sys.argv) < 3:
        sys.exit("Usage: pdf2html.py mypresentation.pdf targetfolder [image path prefix]")

    src = sys.argv[1]
    folder = sys.argv[2]

    if len(sys.argv) > 3:
        prefix = sys.argv[3]
    else:
        prefix = ""

    if not os.path.exists(folder):
        os.makedirs(folder)

    alt_texts = scrape_text(src)

    target_html = os.path.join(folder, "index.html")

    create_index_html(target_html, alt_texts, prefix)

    create_images(src, folder)


if __name__ == "__main__":
    main()
