# Pythonista Script to Get Raw Image URL and URL Scheme for an Instagram Share URL

_Captured: 2015-09-28 at 23:41 from [myword.jeffreykishner.com](http://myword.jeffreykishner.com/users/kishner/essays/030.html)_

[Home](http://jeffreykishner.com)

Last month, I wrote some javascript to [grab the image and URL scheme for an Instagram share URL](http://myword.jeffreykishner.com/users/kishner/essays/013.html). Today, I've written the same thing but using [Pythonista](http://omz-software.com/pythonista/).

You will need to install Pythonista, [Launch Center Pro](http://contrast.co/launch-center-pro/) , and [Drafts](http://agiletortoise.com/drafts/) on your iOS device to make this work.

First, install the following py script in Pythonista:

    
    import requests
    import json
    import sys
    import urllib
    import webbrowser
    url = sys.argv[1]
    data = requests.request('GET','http://api.instagram.com/publicapi/oembed/?url=' + url)
    if data.status_code == 200:
        embed = json.loads(data.text)
        img = embed['thumbnail_url']
        img2 = urllib.quote(img, '')
        mid = 'instagram://media?id=' + embed['media_id']   
        mid2 = urllib.quote(mid, '')
        webbrowser.open('drafts://x-callback-url/create?text=' + img2 + '%0A%0A' + mid2)
        

(Or you can pull it from [this gist](https://gist.github.com/jkishner/28f539d04d2e32c755d2).)

If you are using the latest version of Drafts (i.e., Drafts4), change `drafts` to `drafts4` in the last line of the script.

Name the py script `instagramImage`.

Then create an URL action in LCP:

`pythonista://instagramImage?action=run&args=[clipboard]`

To make this work, tap on the ... next to an Instagram post (in the iOS app) and then tap on "Copy Share URL." Then go to LCP and tap on the URL action you created. Pythonista will create a new draft in Drafts with two URLs. The first one will be the raw image link. If you tap on it, you can download the image to your photo library. The second URL is an URL scheme that, if you tap on it, will bring you to that post in the Instagram app.

## How It Works

Instagram has an oembed API. I use the `requests` and `json` modules in Pythonista to get the values of the thumbnail_url and media_id objects, append the media_id to the beginning of the Instagram URL scheme, and send these URLs to Drafts.
