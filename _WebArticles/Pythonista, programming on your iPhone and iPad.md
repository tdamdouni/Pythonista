# Pythonista, programming on your iPhone and iPad

_Captured: 2016-04-10 at 13:48 from [ryancollins.org](http://ryancollins.org/2013/08/07/pythonista-programming-on-your-iphone-and-ipad/)_

I feel like a teenager again while playing around with [Pythonista (Universal, $6.99)](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8), an app for iOS allows you to program in python directly on the device. It reminds ...

I feel like a teenager again while playing around with [Pythonista (Universal, $6.99)](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8), an app for iOS allows you to program in python directly on the device. It reminds me a lot about when I was learning to program in BASIC on my Atari 800XL (my favorite computer ever, although my iPod Touch is a close second). With Pythonista, I can finally write little apps to make my day easier. A lot nicer than going to the App store, downloading a bunch of free apps, all which have obnoxious ads and don't do quite what I want.

My first script was written to automate my 365 project. A project that I am terrible at keeping up, but now my DOY script will make it easier when I post once a month. I always struggle with the text I add at the end of my description for the picture, where I calculate the day of the year:

I'd end up having to go to a website to find out what the day of the year it was. Well, at least that's what I did in the past. Now I have written the following script and created a [shortcut to it](http://omz-software.com/pythonista/shortcut/):
    
    
    # We're going to need work with dates, access to the clipboard,
    # and to launch an app (you use the webbrowser to do that).
    import datetime
    import clipboard
    import webbrowser
    
    # Figure out the day of the year
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    
    # Create out tag line
    clip = " #365 (" + str(day_of_year) + "/365)"
    
    # Put it in the clipboard
    clipboard.set(clip)
    
    # Open Camera+
    webbrowser.open('cameraplus://')
    

Camera+ has a shoot and share mode, which is what I have set as the default. So now I click on the DOY icon, Pythonista does its thing and Camera+ opens up. I take the picture, type my witty caption, and paste the tagline. Very, very cool.

Pythonista can also export your script as an XCode project, one that you can load into XCode and create an actual iOS app. I haven't had the chance to try that out yet. A couple of negatives. Getting scripts into Pythonista can be a lesson in patience. Due to Apple's limitations on loading code, you cannot simply load code from your Dropbox or other sources, you have to copy and paste. This also means that scripts on your iPhone are automatically synced to your iPad. There is a Dropbox workaround, but I haven't had the chance to try it out yet. The other negative that I've found so far is that there isn't a built in user interface library, so you're limited to text or creating your own graphics for things like buttons.

All in all, it's well worth the price (especially since it's universal!).
