**Basics**

This is a very basic scraper-spider for those html books where there's a table of contents page that links to a bunch of sub-pages with actual content (like the documentation for a bunch of libraries).

Dependencies: Beautiful Soup 4 on Python 2.7+ (including Python 3.x).
 
It assumes all content is vanilla html or at least can be accessed through vanilla html.  

**Usage**

`python spideyscrape.py http://url/for/table_of_contents/toc.html`

Run script from terminal (etc.), then pass the script a url to the table of contents (ToC) page through the prompt you get (or via a command line argument, thanks to a kind contribution from @cclauss). This script scrapes every unique page linked from the ToC and concatenates the contents of their html bodies into one big html page.
 
The point is to save those things for offline reading, for planes etc.  

You can also `import` this as a module from some other script, in which case `spideyscrape.scrape('http://url/for/table_of_contents/toc.html')` will return the offline-capable HTML document as a string, which you can then handle as you please.

**Pythonista** 

This script targets [Pythonista](http://omz-software.com/pythonista/) on iPad for optimum usefulness as offline reader (but also works fine on real computers).  

The easiest way to scrape something then get it right out of Pythonista is to download the wrapper script scrapewrap.py from the pythonista-wrappers directory.  You can run that script from Mobile Safari, and it will grab the url to the open page and send it right to SpideyScrape.  When it's done scraping, it will pop up an "open in" menu ("share sheet"), and you can send the resulting file directly to Dropbox, PDF converter, or whatever.  Note that this wrapper will also quietly delete the original file from the pythonista internal filesystem (sandbox) to keep the clutter down, so the file you open in the other application will be the only one that exists. 

To use the wrapper script, you need to either have updated Pythonista 2.0 (released Jan 11, 2016, I believe), in which case you can use the new share sheet functionality to add the wrapper script to the share sheet that pops up from Mobile Safari.  That's the easiest method.  Alternatively, if for some reason you can't update, you can use the bookmarklet below:

    javascript:window.location='pythonista://scrapewrap.py?action=run&args='+window.location.href;

If you really want to use a clunkier method altogether, you can just leave off the wrapper altogether and use this bookmarklet:

    javascript:window.location='pythonista://spideyscrape.py?action=run&args='+window.location.href;

For any of those tools, just navigate to the ToC page you want to scrape and activate the share sheet/bookmarklet.

**Lawful uses**

Please only scrape content with copyright terms that permit copying.  Be kind to writers.  

The primary intended use of this is to scrape documents offered to the public under licenses that permit copying, but which are often distributed in clueless formats (such as the documentation for many open-source software packages, which is often provided under Creative Commons or MIT licenses, permitting scraping).

**Contributing**

PRs are welcome.  Go wild.  :-)  However, I'd like to keep this runnable on both Pythonista on iOS and full-sized computers, so please don't rely on any Pythonista-specific libraries (like the clipboard module) without also providing a fallback for big machines.  (The exception is for wrapper scripts in the pythonista-wrappers directory.  Also, more wrapper scripts eagerly solicited!) Likewise please don't rely on any libraries that can't be installed in Pythonista without providing a more vanilla fallback.  Finally, please don't break compatibility with both Python 2 and 3.  If lots of people want to contribute I suppose I'll have to write a test suite...

**Future**

1.  Down the road, I'd like to extend to make it possible to specify a crawl depth to recursively scrape to, and figure out some sensible way to order the sub-pages in that context. 

2.  It would also be cool to download and include images embedded in the original page.  Not sure if there's a good way to do this at all, though.  Right now absolute url images should work as plain html links in resulting documents, but relative url images will probably break (not tested).  

**Terms**

The MIT License (MIT)
Copyright (c) 2015 Paul Gowder <http://paul-gowder.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,  publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do  so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR CPYRIGHT HOLDERS BE LIABLE  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
