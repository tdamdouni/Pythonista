# How I get my SQLite database onto my iOS devices using Pythonista

_Captured: 2016-07-17 at 12:52 from [www.thegeekblog.co.uk](http://www.thegeekblog.co.uk/the-geek-blog/2016/7/13/how-i-get-my-sqlite-database-onto-my-ios-devices-using-pythonista)_

[The Geek Blog](/?author=570688f022482ed0f69dc1f1)

[Post](/?category=Post)

Recently I have been looking for the best way to get my main SQLite database I use, onto my iOS devices.  This will enable me to run some tasks and kick off some automation tasks, pull information out etc like I do on my desktop machines.  

Now there are apps I can use if I want to run select statements etc, but I have many python scripts that do selects and formats data and does other things one it has the data, so I wanted more than just selecting, and not be tied to my desktop machine.

I thought I would have a look again at Pythonista.  I have always wanted to get into this more as I have read and heard many good things about the application.  Once I managed to connect to my dropbox account, it has opened up a new world of productivity.  I can now download and upload files to dropbox, and run some of the scripts that helps my pick out information for my current "proper" job wherever I am or if they are needed when offsite in meetings etc.

Now I can combine jobs from Pythonista and Workflow with my database, I am freed up more, and not so tied to a desktop machine.  Also now I can do this I can finish my migration from Bento to SQLite on my mac, its a shame I like Bento but as they no longer develop it for the Mac, I know if I upgrade I will always have my databases.

I have a Workflow created that runs this Pythonista Script and then gives me a nice notification after to say it's done, don't need to load any applications just click the one icon on my device.

There are a couple of pre-reqs, you need, one is you need to create an [Dropbox application](http://dropbox.com/developers/apps) to make API requests, you also need the piece of code dropboxlogin.  You can get that code from [this link](https://gist.github.com/omz/4034526). 

The gist of the code I use is 

> import dropbox
> from dropboxlogin import get_client
> import webbrowser
>  
> dropbox_client = get_client()
> download=dropbox_client.get_file_and_metadata('/Databases/jarvis.db')
> out=open('Jarvis/jarvis.db','wb')
> download,metadata=dropbox_client.get_file_and_metadata('/Databases/jarvis.db')
> out.write(download.read())
> out.close()
> webbrowser.open("workflow://")

The last line is only for if you want to open the workflow application after the code has run.  You can download the full script from my [Github.](https://github.com/geekcomputers/Pythonista/blob/master/update_jarvis.py)

I hope you find this useful, if I can be any help with this please feel free to reach out and contact me through one of the channels listed above.

I am always interested in your thoughts so if you have any comments or feedback then please feel free to add any comments, or you can mail me  [here](mailto:feedback@geekcomputers.co.uk?subject=Feedback%20- SQLite into Pythonista).

![Related Posts Plugin for WordPress, Blogger...](http://www.linkwithin.com/pixel.png) 

 

[The Geek Blog](/?author=570688f022482ed0f69dc1f1)

[Post](/?category=Post)

[iOS](/?tag=iOS), [Python](/?tag=Python), [Pythonista](/?tag=Pythonista), [programming](/?tag=programming), [iPad](/?tag=iPad), [iPhone](/?tag=iPhone), [dropbox](/?tag=dropbox)

[ Facebook0 ](https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2Fwww.thegeekblog.co.uk%2Fthe-geek-blog%2F2016%2F7%2F13%2Fhow-i-get-my-sqlite-database-onto-my-ios-devices-using-pythonista)[ Twitter ](https://twitter.com/intent/tweet?url=http%3A%2F%2Fwww.thegeekblog.co.uk%2Fthe-geek-blog%2F2016%2F7%2F13%2Fhow-i-get-my-sqlite-database-onto-my-ios-devices-using-pythonista&text=)[ Google ](https://plus.google.com/share?url=http%3A%2F%2Fwww.thegeekblog.co.uk%2Fthe-geek-blog%2F2016%2F7%2F13%2Fhow-i-get-my-sqlite-database-onto-my-ios-devices-using-pythonista) 0 Likes

[ ](/?author=570688f022482ed0f69dc1f1)

[The Geek Blog](/?author=570688f022482ed0f69dc1f1)

[Website](http://www.thegeekblog.co.uk)

[ ](/?author=570688f022482ed0f69dc1f1)

[The Geek Blog](/?author=570688f022482ed0f69dc1f1)

[Website](http://www.thegeekblog.co.uk)

