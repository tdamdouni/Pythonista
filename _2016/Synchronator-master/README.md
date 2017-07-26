# Synchronator

_https://github.com/markhamilton1/Synchronator_

Python module to synchronize files between Pythonista on an iOS device and Dropbox

There are other Python synchronization apps, but they all use the original Dropbox
API V1, which is deprecated and soon to be discontinued.  The Synchronator module
was created using the new V2 API to synchronize Python scripts between iOS devices
and to backup to Dropbox.

Synchronator is dependent on another module, called DropboxSetup, which saves and
loads Dropbox access tokens for use by other Python modules.

For Synchronator to work properly it needs the latest version of the dropbox Python
package, which I use Stash to install. The latest version of the dropbox package has
support for both the original V1 API as well as the newer V2 API, which Synchronator
needs to operate.

Once these pieces are all in place on your iOS device, you will need to configure
Synchronator for it to work. The following steps can be used to do this.

1. Go to the [Dropbox developer web page](https://www.dropbox.com/developers).
2. Create an app that uses the Dropbox API V2. (**Not** the Dropbox for Business API)
3. Select the App Folder option.
4. Enter a name for the app. I recommend `Synchronator-<your name>`.
    * If the previous steps were successful then you have created an app and should
      now be on the app page where you can edit the properties of the app.
5. Find the property `Generated Access Token` and select the Generate button.
6. Select and copy the Access Token to the clipboard.
7. Execute Synchronator in Pythonista on your iOS device.
8. Enter the Access Token at the prompt. Paste it if you performed steps 1 thru 6
   on the same iOS device that Pythonista is on.

If everything was successful then Synchronator will begin synchronizing with Dropbox.

As changes are made to Synchronator.py you will need to update to the latest version.
There is a function in Synchronator.py named download that will get the code from GIT
and save it to Pythonista. To do this, go to the console in Pythonista and type the
following:

```python
import Synchronator
Synchronator.download()
```

You should see the message 'Synchronator.py Downloaded Successfully'.

