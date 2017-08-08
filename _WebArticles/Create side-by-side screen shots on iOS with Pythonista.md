# Create side-by-side screen shots on iOS with Pythonista

_Captured: 2015-09-28 at 23:53 from [soitscometothis.net](http://soitscometothis.net/Create-side-by-side-screen-shots-on-iOS-with-Pythonista/)_

First, I have to thank [Federico Viticci](https://twitter.com/viticci), whose [detailed](http://www.macstories.net/tutorials/chaining-tweetbot-pythonista-drafts-and-imessage-for-urls/) [blog](http://www.macstories.net/tutorials/from-instapaper-and-pythonista-to-dropbox-and-evernote-as-pdf/) [posts](http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/) on his use of Pythonista inspired me to use it and learn Python as well.

I don't use iOS devices as exclusively as he does, but when I am using them I want them to be as powerful and automated as my Mac is. One use case that Federico demonstrated was using Pythonista to take two screen shots (such as of an app before and after an update) and create a new image of both screen shots side by side, such as he might need for an app review blog post. His old script was a bit hacky due to the situation at the time.

Pythonista was [recently updated](http://www.macstories.net/reviews/pythonista-1-3-brings-camera-roll-and-notification-center-support-new-library-view-and-more/) to include the ability to pick images from the camera roll from inside Pythonista as well as the ability to save generated images to the camera roll.

I decided to fork his original code to include these features and to remove some options that I don't need.

When you run this script you will be prompted to choose an image from the camera roll. This will be the image on the left of the combined final image. Then you will be prompted to choose a second image. Naturally, this image will be on the right. The image will be generated and saved to the camera roll.

You can get the script from Gist [here](https://gist.github.com/nuclearzenfire/5090763).
    
    
    """
    This code takes two screenshots from the camera roll combines them into one image and saves the new image to the camera roll.
    
    This is adapted from Federico Viticci's blog post at:
    http://www.macstories.net/stories/automating-ios-how-pythonista-changed-my-workflow/
    It removes the option to change which picture is where, automatically assigning the first one chosen as the leftmost image.
    It also removes the necessity to copy the images to the clipboard outside of Pythonista using the new photos library in version 1.3. Finally, it removes the clipboard output.
    """
    
    import photos
    import Image
    import console
    
    im1 = photos.pick_image(show_albums=False)
    im2 = photos.pick_image(show_albums=False)
    
    background = Image.new('RGBA', (746,650), (255, 255, 255, 255))
    
    console.clear()
    print "Generating image..."
    console.show_activity()
    
    _1 = im1.resize((366,650),Image.ANTIALIAS)
    _2 = im2.resize((366,650),Image.ANTIALIAS)
    background.paste(_1,(0,0))
    background.paste(_2,(380,0))
    photos.save_image(background)
    console.hide_activity()
    print "Image saved to camera roll."
    

Here's an image I created with it for an upcoming comparison of the text-parsing of Pocket vs. Instapaper:

![](http://soitscometothis.net/images/sidebyside.jpg)

> _Next, I need to make a way for this image to be uploaded to my public Dropbox folder and the public link to be placed in the clipboard._

I can't wait for more posts by Frederico so I can keep learning.
