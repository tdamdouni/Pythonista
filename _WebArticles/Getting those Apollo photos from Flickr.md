# Getting those Apollo photos from Flickr

_Captured: 2015-11-24 at 23:17 from [leancrew.com](http://leancrew.com/all-this/2015/10/getting-those-apollo-photos-from-flickr/)_

I'm sure you've heard about [this new Flickr account](https://www.flickr.com/photos/projectapolloarchive/albums) with about 13,000 scanned photos from the Apollo program. You may have scrolled through the albums and downloaded a few photos. And you may have thought it would be cool if you could just download all of them. If you have about 60 GB of disk space free, you can.

First, I should mention that Ryan M got there before me. I knew he was working on it because of this Twitter exchange between him and Stephen Hackett:

> If anyone has a clever way to scrape these, let me know.  
  
Not that I would try it.  
  
Ahem.  
  
[512pixels.net/blog/2015/10/t…](http://www.512pixels.net/blog/2015/10/the-project-apollo-archive)  
-- Stephen Hackett ([@ismh](http://twitter.com/ismh)) [Oct 2 2015 8:50 PM](https://twitter.com/ismh/status/650125757528670208)

I didn't know until today that he'd posted [the code he used](https://gist.github.com/rjames86/eefb6aabe5ab41377126) as a Gist, which would've saved me some of the time I spent writing my my own scripts. By the time I saw his code, I'd already done my own clumsy job, but I have shamelessly stolen some of his good ideas and incorporated them into my scripts to make me look smarter in this post.

Ryan and I both access the Flickr API through [Sybren Stuvel's `flickrapi` Python library](http://stuvel.eu/flickrapi), [which I've used before](http://www.leancrew.com/all-this/2011/08/more-flickr-api-stuff/) for several little utility scripts and snippets. And we both go through the same steps:

  * Use the Flickr API to march through the Apollo collection, gathering album names, photo names, and image URLs.
  * Downloading the images and saving them into a local folder structure that mimics the album structure on Flickr.

The fundamental difference between our approaches is this: Ryan does both of these steps in a single script, whereas I use one script for the first step and another for the second. I save the information gathered in the first step in a file that the second script reads.

Breaking up the functionality this way didn't help me, but it will help you, because I'm making the file with all the information gathered through the Flickr API available to download. All you'll need to download the Apollo photos are a standard Python distribution (the one that comes with OS X will do), the information file, and my second script. No need to install the `flickrapi` library, and more important, no need to wait through all the API calls. For whatever reason, Flickr's responses are incredibly slow. Far and away, most of the time is spent gathering the information from the API--the downloads themselves are relatively quick. Having the information file will allow you to skip the most time-consuming part of the process.

Of course, I'm still going to show you both of my scripts. Here's `apollo-photo-list`, the one that gathers the information:
    
    
     1  #!/usr/bin/env python
     2  
     3  from flickrapi import FlickrAPI
     4  import json
     5  
     6  # Flickr parameters
     7  fuser = 'username'
     8  key = 'apikey'
     9  secret = 'apisecret'
    10  nasa = '136485307@N06'
    11  
    12  def getOriginalURL(id):
    13    s = flickr.photos.getSizes(photo_id=id)
    14    for i in s['sizes']['size']:
    15      if i['label'] == 'Original':
    16        return i['source']
    17  
    18  flickr = FlickrAPI(key, secret, format='parsed-json')
    19  psets = flickr.photosets.getList(user_id=nasa)
    20  
    21  for set in psets['photosets']['photoset']:
    22    print '"{}": '.format(set['title']['_content'].replace('/', '-'))
    23    photos = []
    24    pList = flickr.photosets.getPhotos(photoset_id=set['id'])
    25    for p in pList['photoset']['photo']:
    26      pDict = {}
    27      pDict['photoID'] = p['id']
    28      pDict['photoTitle'] = p['title']
    29      pDict['photoURL'] = getOriginalURL(p['id'])
    30      photos.append(pDict)
    31    print json.dumps(photos)
    32    print
    
    

The `fuser`, `key`, and `secret` values on Lines 7-9 come from [registering with Flickr](https://www.flickr.com/services/apps/create/). I got the `nasa` user ID on Line 10 by interactively making API queries on one of the photos in the gallery. The rest of the script is pretty standard stuff. What the user-facing part of Flickr calls "albums," the API calls "photosets," so that's why you see that term so often in the code.

I will say that getting the information as parsed JSON (see Line 18) instead of in the default [ElementTree format](https://docs.python.org/2/library/xml.etree.elementtree.html) makes the script much easier to read and write. This is what I stole from Ryan. In my first go-around, I used the default format, and it was a big mistake. The Flickr data formats are deeply nested, and it's difficult and time-consuming to work out the structure when it's in ElementTree format. Printing an ElementTree value usually results in an opaque response like this:
    
    
    <Element rsp at 0x105d88560>

Printing a parsed JSON value, on the other hand, shows you everything. It tells you which items are dictionaries and which are lists, and it gives you the keys for all the dictionaries, no matter how deeply nested they are. I would've saved a lot of time if I'd used JSON from the start.

The result of running `apollo-photo-list`, which took a few hours to complete, is a giant text file that looks almost like a JSON file. A little editing in BBEdit turned it into a legitimate JSON file that can be read and parsed by the second script.

You may be wondering why `apollo-photo-list` didn't just create a large data structure and `dump` it out as a JSON file at the end. Why bother with `print` statements within the main loop? The reason is that sometimes the connection to Flickr craps out and the program stops because of a response error. Rather than lose all the information when that happens, I have the script print out what it collects as it goes. If there's an interruption, I can see how far it's gotten and restart the script from that point. For example, if the connection fails after printing out information on 15 albums, I can change Line 21 to
    
    
    21  for set in psets['photosets']['photoset'][15:]:
    
    

This will cause it to skip over the first 15 albums and start printing again with the 16th. I feel certain that if I hadn't written the script this way I'd still be waiting for it to run once with out a hiccup.

OK, when the first script is finally finished and I've edited the result into proper JSON format, I have a 1.8 MB text file called `apollo.json`. You can download a 300 kB zipped version of this, `apollo.json.zip`, from [here](http://leancrew.com/all-this/downloads/apollo.json.zip) and expand it on your local machine. It's going to be the input file for the next script.

The script that actually does the downloading is `get-apollo-photos`:
    
    
     1  #!/usr/bin/env python -u
     2  
     3  import urllib2
     4  import os
     5  import sys
     6  import json
     7  
     8  # Make a holder directory for photos on the user's Desktop.
     9  apolloDir = os.environ['HOME'] + '/Desktop/apollo'
    10  os.mkdir(apolloDir)
    11  
    12  # Read in the JSON from the file given on the command line
    13  sets = json.load(open(sys.argv[1]))
    14  
    15  # Make a subfolder for each set and download all the photos.
    16  for k in sets.keys()[4:6]:
    17    sys.stdout.write("Downloading set {}".format(k))
    18    subdir = "{}/{}".format(apolloDir, k)
    19    os.mkdir(subdir)
    20    for p in sets[k]:
    21      name = "{}/{}.jpg".format(subdir, p['photoTitle'])
    22      url = p['photoURL']
    23      image = urllib2.urlopen(url).read()
    24      imgFile = open(name, 'w')
    25      imgFile.write(image)
    26      imgFile.close()
    27      sys.stdout.write('.')
    28    sys.stdout.write('\n')
    
    

Assuming you have both it and `apollo.json` on your Desktop, you run it like this from the command line:
    
    
    cd ~/Desktop
    ./get-apollo-photos apollo.json

It will first create an `apollo` folder on your Desktop (Lines 9-10) and then fill it with subfolders and photos. The subfolders will have the same names as the Flickr albums, and the photo files will have same names as the Flickr photos. The photos you end up with are the highest resolution versions because why bother with anything else?

To let you know that things are working, a message is printed whenever the script moves to a new album (Line 17) and a dot is printed whenever a photo has been downloaded (Line 27). Python would normally buffer this kind of output and display it only after the script is finished--which would defeat the purpose of the messages. The `-u` switch at the end of the shebang line (Line 1) tells Python to run unbuffered and display the messages as the script runs.

Many of the photos are out of focus, poorly framed, or just plain dull. But then there are the good ones, and they are really good. I suspect most people will like the images of the Earth or the Moon or the various pieces of equipment. I do, too, but my favorite is this one, which I've seen many times before:

![Neil Armstrong](http://leancrew.com/all-this/images2015/20151009-Neil%20Armstrong.jpg)

> _Neil Armstrong_

This is Neil Armstrong back in the LEM after he and Buzz Aldrin have taken their walk on the Moon. The mixture of exhaustion, elation, pride, amazement, and wonder on his face is just delightful.

This work is licensed under a [Creative Commons Attribution-Share Alike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).
