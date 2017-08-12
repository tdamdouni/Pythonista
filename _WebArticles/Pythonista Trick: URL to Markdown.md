# Pythonista Trick: URL to Markdown

_Captured: 2015-11-16 at 00:17 from [www.macdrifter.com](http://www.macdrifter.com/2012/09/pythonista-trick-url-to-markdown.html)_

Here's a nice little tool I made in [Pythonista](http://click.linksynergy.com/fs-bin/stat?id=Ssqi/JNIy7o&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1=http%253A%252F%252Fitunes.apple.com%252Fus%252Fapp%252Fpythonista%252Fid528579881%253Fmt%253D8%2526uo%253D4%2526partnerId%253D30) for iOS ([review](http://www.macdrifter.com/2012/07/pythonista-app-from-toy-to-tool.html)). This script is using Brett Terpstra's awesome [heckyesmarkdown](http://heckyesmarkdown.com) web service, which is extremely useful and underrated.

To use this script, I copy a URL to the iOS clipboard and jump into Pythonista. I trigger this script to get the web page in Markdown encoded text.

This URL: <http://www.macdrifter.com/2012/09/nfc-is-a-crutch.html>

is turned into plain text and put back on the clipboard. The results are displayed in a popup Pythonista browser window:

![](http://www.macdrifter.com/uploads/2012/09/2012-09-13%2018.37.05_600px.png)

Here's the script:
    
    
    import clipboard
    import urllib2
    import webbrowser
    
    clipString = clipboard.get()
    
    marky = 'http://heckyesmarkdown.com/go/?u='
    
    queryString = marky + clipString
    
    reqMD = urllib2.Request(queryString)
    openMD = urllib2.urlopen(reqMD)
    content = (openMD.read().decode('utf-8'))
    clipboard.set(content)
    
    webbrowser.open(queryString)
    

The script started life with a mess of URL validations steps, but Brett's service is so awesome that it just fails gracefully with bad URL's. But I did try out the new Pythonista console.alert() method. I like it.

![](http://www.macdrifter.com/uploads/2012/09/2012-09-13%2009.15.23.png)
