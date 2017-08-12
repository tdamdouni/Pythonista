# Updated image merge script

_Captured: 2015-11-07 at 00:50 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/10/14/updated-image-merge-script/)_

Earlier on Twitter tonight, TJ Luoma ([@tjluoma](https://twitter.com/tjluoma)) asked about a better way to merge iOS screenshots.

> I'm assuming there is some limitation in iOS which makes it impossible to merge two full-size screenshots? Every app seems to crop them.  
-- TJ Luoma (@tjluoma) [October 13, 2014](https://twitter.com/tjluoma/status/521802016138338304)

I had a simple Pythonista script to do exactly what he asked. It was short, simple, and worked perfectly.

Until I tested it in iOS 8.

I wanted to test the script before sending it off, but I found that some images weren't responding the way they did in iOS 7. After a little work I got the script working again, but the more I worked with it, the more I saw limitations in the script.

  * The script assumed only portrait screenshots.
  * The script was written just for the iPhone. 
  * The script just pasted the two screen shots side by side. 

That's too many limitations in this age of iOS devices. So I started to look at ways to make the script more universal. The script needed to merge images from either landscape or portrait captures. The script also needed to be able to do screenshots from any iOS device. After a little work, I can up with this:

```python
# ** Universal iOS screenshot merge **

# Script will take two images of same orientation and merge them together. 

#

# By: Jason Verly (@mygeekdaddy)

# Date: 2014-10-13

# Ver: 1.02

import clipboard

import Image

import console

import photos

console.clear()

console.alert("Pick first image", "", "Select")

im1 = photos.pick_image(show_albums=True)

console.alert("Pick second image", "", "Select")

im2 = photos.pick_image(show_albums=True)

console.show_activity()

w,h = im1.size

print im1.size

print 'Ratio is ' + str((w*1.0)/h)

def image_merge(img):

if (w*1.0)/h > 1:

print 'Landscape screenshot...'

#(2048, 1536)

#Landscape screenshot

background = Image.new('RGB', ((w+20), ((h*2)+30)), (255,255,255))

print "Generating image..."

background.paste(im1,(10,10))

background.paste(im2,(10,(h+20)))

# background.show()

photos.save_image(background) 

else:

print 'Portrait screenshot...'

#(1536, 2048)

#Portrait screenshot

background = Image.new('RGB', (((w*2)+30),(h+20)), (255, 255, 255))

print "Generating image..."

background.paste(im1,(10,10))

background.paste(im2,((w+20),10))

# background.show()

photos.save_image(background) 

image = image_merge(im1)

print "\n\nImage saved to camera roll."
```

Sometimes when someone asks for a little help, you end up scratching you're own itch.
