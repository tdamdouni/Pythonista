![gitsynchista icon](https://raw.githubusercontent.com/marcus67/gitsynchista/master/lib/gitsynchista_64.png)

# Step-by-Step Tutorial for gitsynchista

This is a step-by-step tutorial to use gitsynchista with Pythonista. It shows the usage of the GUI mode only since
the functionality of the command-line mode is rather limited.

## Prerequisites

  * You will need Pythonista. Youare probably aware of this since you would not have found your way to this page in the first place. Currently, only the 2.x versions of Pythonista are supported but this will hopefully change soon.
  * You will need a WebDav server hosting your repository. It can be hosted on an iDevice-local repository such as the iOS app [working copy](https://itunes.apple.com/it/app/working-copy/id896694807?l=en) but it should be possible to configure any other WebDAV server.
  * You need to have the Python WebDav client installed. See my clone at https://github.com/marcus67/easywebdav. Place the script `easywebdav/client.py` into the `site-packages` directory. 
  * Install gitsynchista itself by downloading the [self-extracting archive](https://github.com/marcus67/gitsynchista/blob/master/build/gitsynchista_zip.py), placing it into the root directory of your Pythonista app, and executing the script. Afterwards you will have a `gitsynchista` subdirectory. The downloaded archive can then be deleted.

## Preparing the First Repository on the WebDav Server

The main task of gitsynchista is to synchronize the files of a repository located on your iDevice with the corresponding 
repository on the WebDAV server (which may also be on the iDevice as mentioned above). If you already have such a repository 
you are all set to start. Otherwise create a new repository on your WebDav server. Of course, how this is done is outside
the scope of this tutorial.

From now on we assume that the repository has the path `/dummyproject` on the WebDav server. 

## Preparing the Same Repository with gitsynchista

The next step will be create a base directory in the Pythonista directory structure. Although it is not really required it is usually a good practive to use the same directory name in Pythonista. So from now on we assume that the base directory is called `dummyproject`.

Now, create a configuration file named `gitsynchista_config.txt` in the base directory or the `etc` subdirectory with the following content:

    [repository]
    name = My Dummy Project
    local_path = ../dummyproject
    remote_path = /dummyproject


This is the minimal configuration. Note that the path for `remote_path` is absolute on the WebDav server whereas the path for `local_path` is relative to the location of the script `gitsynchista.py`. You may need to add credentials to log into the WebDav server by using the para meters `username` and `password`:

    [repository]
    name = My Dummy Project
    local_path = ../dummyproject
    remote_path = /dummyproject
    username = mylogin
    password = mypassword


If you intend to use working copy as your WebDav server you must also add a value to correct for different handling of the timestamps and see to it that working copy is "woken up" by gitsynchista (otherwise the WebDav server will not be active). So, in this case your configuration file would look like this:

	[webdav]
	epoch_delta = 3600
	
	[repository]
	name = My Dummy Project
	local_path = ../dummyproject
	remote_path = /dummyproject
	working_copy_wakeup = True

## Creating an Action Shortcut

The easiest way to call gitsynchista is to create an Pythonista Action Shortcut. Press the wrench symbol in the Pythonista top bar (you have to be in a script to see the wrench).

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/action_shortcut_step1.png" WIDTH="400px"></CENTER>

Press the "Edit" button to add a new shortcut.

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/action_shortcut_step2.png" WIDTH="400px"></CENTER>

Choose an empty slot by pressing the plus sign.

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/action_shortcut_step3.png" WIDTH="400px"></CENTER>

Choose the `gitsynchista` script and optionally add a logical name, an icon and the icon color. Save the settings.

## Calling the GUI
Start the GUI by using the Action Menu Entry or by starting the script `gitsynchista.py` without any parameters. If everything is configured correctly the GUI will start up showing this window:

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1.png" WIDTH="400px"></CENTER>

There is one line representing the repository with the current state "Requires scan". Selecting the entry and pressing the "Scan" button will show the next state (only the upper part of the window is shown in the following screen shots):

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step2.png" WIDTH="400px"></CENTER>

The entry contains a short description of how many files need to be updated (either way: local to remote or vice versa) and the number of files which need to be created (either location: local or remote). In case an error is shown refer to the section handling errors below.

Pressing the "i" icon on the right side of the entry opens a popup window with an itemized list of all pending changes: 

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step2_info.png" WIDTH="400px"></CENTER>

If at least one file is to be updated or created, use the "Sync" button to trigger the synchronization. After a few seconds (if no errors occur) the window will be in the "in sync" state:

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step3.png" WIDTH="400px"></CENTER>

Congratulations! After closing the app the local directory of the dummy projects reflects the files which have been retrieved from the WebDav server:

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_done.png" WIDTH="800px"></CENTER>

## Error Handling 
In case gitsynchista runs into an error during scanning or synchronizing there will be a short error message presented as the state of the repository entry:

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1_error.png" WIDTH="400px"></CENTER>

Pressing the "i" icon on the right side of the entry will open a popup window with more detailed information (usually the text retrieved from the exception).

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_step1_error_info.png" WIDTH="400px"></CENTER>

## Additional Configuration (All WebDav Servers)

### Automatic Scan

For frequently used repositories it makes sense to make gisynchista automatically scan the repository when the GUI is started. Use the parameter `auto_scan` to use this feature:

  [repository]
  auto_scan = True

### Correcting a Time Shift

The up-to-date-check of the files is based upon their timestamps on both the local filesystems and the remote filesystem on the WebDav server. This, of course, requires the clocks to be (more or less synchronized) on both systems. If this is not the case the setting

	[webdav]
	epoch_delta = DELTA_IN_SECONDS

can be used to automatically *add* the configured number of seconds to the timestamps of the WebDav server. For working copy the value has to be set to `3600`.

### Supressing the Synchronization of Certain Files/Patterns

The app will scan directories for files named `gitsynchista_ignore.txt` or `.gitignore`. If found it will suppress the files and patterns contained in the file from being synchronized. Note that currently the use of `.gitignore` is not really possible with Pythonista since dot files are not visible in the built-in file browser!

A typical use case would be to suppress the synchronization of the `gitsynchista_config.txt` file since it contains site-specific and/or user-specific settings which should not be under version-control.

### Login with Credentials

The default authentication mode with the WebDav server is anonymous. This may not be desired when accessing a remote server which is publically available. In this case the credentials can be set using the `username` and `password` parameters. 

    [repository]
    username = mylogin
    password = mypassword
    
If only the username is set the password will prompted upon first access to the WebDav server and saved to the iOS key chain. The "service" for which the password is saved in the key chain will be composed of the prefix "Webdav Server" and the name of the repository as can be seen in the following screenshot:

<CENTER><IMG SRC="https://raw.githubusercontent.com/marcus67/gitsynchista/master/doc/gitsynchista_gui_sync_password.png" WIDTH="400px"></CENTER>

This requires the repository name to be unique across all repositories with authentication!

### Changing the Authentication Method

The default authentication method with the WebDav server is "Digest HTTP" which is also the one required for Working Copy (if authentication is activated). The method can be *downgraded* to "Basic HTTP" by supplying the `auth_mode` parameter:

	[webdav]
	auth_mode = basic

## Additional Configuration (Working Copy)

### Automatic Wake Up

Although this has been mentioned above we repeat the special setting for Working Copy for reasons of completeness. Due to Apple regulations most iOS apps are usually not allowed to stay active in the background. In case of a server application this is disadvantageous since usually the app accessing the server (gitsynchista in this case) will be running in the foreground. However, Apple allows apps a certain "grace period" between the point of time when they are pushed into the background and the point of time when they have to stop all background activity. Working Copy takes advantage of this and provides the WebDav service until the grace period is over. gitsynchista uses published URL schemes to activate the WebDav server of Working Copy and then uses the grace period to scan and sync files if the following parameter is set:

	[repository]
	working_copy_wakeup = True
	
Note that - although this is a per-repository setting - the wake up is done only once before opening the GUI. This means that as soon as the grace period is over gitsynchista will generate runt-time errors when tring to scan or sync files with the Working Copy WebDav server. See this [ticket](https://github.com/marcus67/gitsynchista/issues/18).