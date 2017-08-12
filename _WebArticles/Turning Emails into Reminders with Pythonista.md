# Turning Emails into Reminders with Pythonista

_Captured: 2015-12-10 at 23:57 from [pronetobits.net](http://pronetobits.net/post/56187383074/turning-emails-into-reminders-with-pythonista)_

This post documents a [Pythonista](http://omz-software.com/pythonista/) script that will create an iOS Reminder from your iOS clipboard via [Drafts](http://agiletortoise.com/drafts/) app. I use this when I receive an email on my phone that I need to act on at a later time. Here is how I use it. When reading an email that I decide needs to be followed up on at a later time, I long-press anywhere in the email body to select all and copy the email body. Then I go to the home screen and press the shortcut icon[1](http://pronetobits.net/post/56187383074/turning-emails-into-reminders-with-pythonista) for a Pythonista script that I have called "EmailTask." The script opens Drafts and creates a new Reminder with "Follow-up on this email" as the Reminder title and the email body as the notes for the Reminder. The Reminder is then ready to import into [Things](http://culturedcode.com/things/), my preferred task management app, the next time I launch Things.

You can tweak this so that Pythonista throws up a prompt for you to type in a unique Reminder title before proceeding to Drafts, but I chose to just use a standard title to minimize the effort required on my part on the front end. I prefer to process the task and give it a more descriptive name once I am back on my Mac. In an ideal world, you would be able to specify in the url scheme to return to the mail app after the Reminder is created; however, there is currently no url scheme that allows you to simply launch Mail.app.

So without further ado, here is the script.
    
    
    # EmailTask
    
    import clipboard
    import webbrowser
    import urllib
    
    body = clipboard.get()
    text = body.encode('utf-8')
    textEncoded = urllib.quote(text, safe='')
    
    webbrowser.open('drafts://x-callback-url/create?text=Follow-up%20on%20this%20email%0A'+textEncoded+'&action=Reminder')
    
