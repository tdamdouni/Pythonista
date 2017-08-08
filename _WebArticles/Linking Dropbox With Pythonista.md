# Linking Dropbox With Pythonista

_Captured: 2016-04-20 at 20:08 from [unapologetic.io](http://unapologetic.io/posts/2014/01/23/linking-dropbox-with-pythonista/)_

(▼)

Pythonista has a built in Dropbox module to allow you to manipulate files on your Dropbox. The module itself is fairly simple and straightforward (assuming you know some basic Python), but when I first started scripting on my iPad, I found the online instructions for linking my Dropbox account to Pythonista to be unclear and overly complex. Since the implications of being able to write scripts which access and manipulate files on your Dropbox account are very powerful, I think that everyone should be able to do it. As a result, I've written below what I hope are significantly simplified, step by step instructions to help you circumvent the confusion I ran into trying to give Pythonista access to a Dropbox account.

## Linking Your Dropbox to Pythonista

The first thing you should do to link your Dropbox to Pythonista is to copy and paste [this script](https://gist.github.com/omz/4034526) into a new empty script in Pythonista. You can name the script whatever you want, but I named mine "dropboxlogin", and that's how I will be referring to it for the rest of this post (and in future posts involving Dropbox).

The first few lines of the dropboxlogin script are the only ones that you need to think about, don't touch the rest of the script. These lines are as follows:
    
    
    # YOU NEED TO INSERT YOUR APP KEY AND SECRET BELOW
    # Go to dropbox.com/developers/apps to create an app.
    
    app_key = 'YOUR_APP_KEY'
    app_secret = 'YOUR_APP_SECRET'
    
    # access_type can be 'app_folder' or 'dropbox', depending on
    # how you registered your app.
    access_type = 'app_folder'
    

The directions here make the process seem pretty simple, but it gets a bit more complicated when you actually attempt to follow them. To start out, go to [the URL in the script](http://dropbox.com/developers/apps), as it tells you to. That will direct you to a page prompting you to log into your Dropbox account (assuming you aren't logged in already). After signing in you should be presented with a page that has a "Create App" button. Tap that button to get started.

The first option that you will be presented with will ask you if you want to create a "Drop-ins app" or a "Dropbox API app". Choose the latter. Once you've selected Dropbox API app, the next option will appear below automatically. For this one, choose "Files and datastores", for the next, choose "No - My app needs access to files already on Dropbox.", and for the one after that choose "All file types - My app needs access to a user's full Dropbox." Finally, choose a name for your app. Now press the "Create app" button.

The next thing you should see is an overview of your new "app". You can ignore everything on here except for the "App key" and "App secret". These two strings of characters need to be copied and pasted into the corresponding regions of your python script in Pythonista. Make sure you replace only the text "YOUR_APP_HERE" and "YOUR_SECRET_HERE", so that the strings of characters are still between the apostrophes.

To finish off your script, change the access type from "app_folder" to "dropbox", because we want Pythonista to have full access to our Dropbox for the most versatility with future uses of the Dropbox Module.

The dropboxlogin script comes with a built-in main method to test whether your efforts have been successful. Run the script from Pythonista and the interactive prompt should slide over, displaying the output "Getting account info...". A few seconds later, a string of data should be written to the screen with information about your account. If there is an error then check to make sure your app is completely set up, that you correctly copied your app key and app secret into the right places, and that you chose the proper access type for the app you set up.

If you've followed all the steps correctly, you should be ready to go. Now anytime you want to be able to access your Dropbox via the Dropbox module in a different python script, simply include the line `from dropboxlogin import get_client` at the top of your script. The get_client method begins a Dropbox session, so if you include another line beneath the import command, `dropbox_client = get_client()`, then you can now call methods from the Dropbox module on your "dropbox_client" variable.

Happy scripting.
