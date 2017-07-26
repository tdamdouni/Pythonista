#! /usr/bin/env python
# -*- coding: utf-8 -*-

# https://gist.github.com/wcaleb/5478130

## docvert.py
## by W. Caleb McDaniel
## http://wcm1.web.rice.edu

## This is a wrapper script for sending documents to Docverter
## for conversion from markdown to PDF. It offers a python
## alternative to using cURL. For more information, see:
## http://www.docverter.com/api.html

## Helper functions for posting multipart/form-data request
## using standard libraries. Updated to reflect changes to
## httplib in Python 2.0
## {{{ http://code.activestate.com/recipes/146306/ (r1)

import httplib, mimetypes

def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    response = h.getresponse()
    output = response.read()
    return output
    # return h.file.read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

## end of http://code.activestate.com/recipes/146306/ }}}

## Now let's do this.

## Create a two-word input file to send to Docverter.
f = open("doctest.txt", "w").write("Testing docverter")

## Set Docverter options and define fields using lists.
## Other options available at http://www.docverter.com/api.html#toc_2
fields = [("from", "markdown"), ("to", "pdf")]
files = [("input_files[]", "@doctest.txt", open("doctest.txt", "r").read())]

## Post to Docverter using post_multipart()
output = post_multipart("c.docverter.com", "/convert", fields, files)

## Write output to a PDF file.
o = open("doctest.pdf", "w").write(output)
