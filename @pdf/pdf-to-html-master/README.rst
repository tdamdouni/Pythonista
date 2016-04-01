.. contents :: :local:

Introduction
----------------

This is a Python script to convert a PDF to series of HTML `<img>` tags with alt texts.
It makes the presentation suitable embedded for a blog post and reading on a mobile device and such.

Example Workflow:

* Export presentation from Apple Keynote to PDF file. On Export dialog untick *include date* and *add borders around slides*.

* Run the script against generated PDF file to convert it to a series of JPEG files and a HTML snippet with `<img>` tags

* Optionally, the scripts adds a full URL prefix to `<img src>`, so you don't need to manually link images to your hosting service absolute URL

* Copy-paste generated HTML to your blog post

Tested with Apple Keynote exported PDFs, but the approach should work for any PDF content.

See `example blog post and presentation <http://opensourcehacker.com/2013/04/24/meet-plone-the-most-awesome-open-source-community-in-the-world/>`_.

Installation
--------------

Dependencies (OSX)::

    sudo port install ghostscript

Please note that Ghostscript 9.06 crashed for me during the export. Please upgrade to 9.07.

`Setting up virtualenv <http://opensourcehacker.com/2012/09/16/recommended-way-for-sudo-free-installation-of-python-software-with-virtualenv/>`_ and insllating the code::

    git clone xxx
    cd pdf-presentation-to-html
    curl -L -o virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py venv
    . venv/bin/activate
    pip install pyPdf

Usage
----------

Example::

    . venv/bin/activate
    python pdf2html.py test.pdf output

Advanced example::

    . venv/bin/activate
    python pdf2html.py test.pdf output

Even more advanced example with hardcoded URL::

    GHOSTSCRIPT=/usr/local/bin/gs python pdf2html.py test.pdf output http://opensourcehacker.com/wp-content/uploads/wpd2013/

Then upload to the server for Wordpress to access::

    rsync -av pycon2014 yourserver.example.com:/srv/yoursite/wordpress/wp-content/uploads

Author
--------------

Mikko Ohtamaa (`blog <https://opensourcehacker.com>`_, `Facebook <https://www.facebook.com/?q=#/pages/Open-Source-Hacker/181710458567630>`_, `Twitter <https://twitter.com/moo9000>`_, `Google+ <https://plus.google.com/u/0/103323677227728078543/>`_)


