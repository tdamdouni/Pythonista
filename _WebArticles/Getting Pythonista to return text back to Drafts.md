# Getting Pythonista to return text back to Drafts

_Captured: 2015-11-07 at 00:45 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/02/16/getting-pythonista-to-return-text-back-to-drafts/)_

Drafts has become my digital text hub for my iOS devices. But one of the downsides of iOS automation, and relying on URL schemes, is when you find an app you want to use doesn't support a full x-callback-url scheme. I do some text transformations in [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4), but Pythonista doesn't support a full x-callback-url scheme. So here's a small work around I use to get my transformed text from Pythonista back into Drafts.

#### The Old Way

Let's start off with the script I need to run in Pythonista:
    
    
    # pythonista script - encode.py
    import clipboard
    import urllib   
    basetxt = clipboard.get()   
    encodetxt = urllib.quote(basetxt, '')
    clipboard.set(encodetxt)
    

Pretty basic script - get the contents of the clipboard, percent encode the text, and then paste the encoded text back into the clipboard. So to do a simple text transformation, like this one, I would need to do the following: paste the text into the clipboard, go to Pythonista, run the script, go back to Drafts, and then paste the clipboard back into a new note.

That's the old way of business.

#### The New Way

Assuming the snippet was saved in Pythonista, an action in Drafts could be written to run the Pythonista script like this:
    
    
    pythonista://encode?action=run
    

This Drafts action would take the text in the clipboard, open Pythonista, run the script, and paste the transformed text back into the clipboard. I still needed to paste the text into the clipboard, return to Drafts, and paste the text back into a new note.

Close… but I just want one big red button.

Pythonista allows scripts to call out URL's and open them using the `webbrowser` module. So here's a modified version of the script:
    
    
    # pythonista script - encode.py
    import clipboard
    import urllib
    import webbrowser
    basetxt = clipboard.get()
    encodetxt = urllib.quote(basetxt, '')
    clipboard.set(encodetxt)
    webbrowser.open('drafts://x-callback-url/create?text&afterSuccess=Delete&action=paste_draft')
    

In this case we're using Drafts x-callback-url scheme to have Pythonista re-open Drafts, create a new note, and then run a specific action. In this case, the `paste_draft` action will create a new note in Drafts from the contents of the clipboard.

So now that I got Pythonista to return the text to Drafts, I just needed to modify the way I was triggering the Pythonista action in Drafts. I did this by chaining together an action that would create a new note from the current note and paste the contents of the new note to the clipboard. Once that was done, I could use the _x-success_ parameter to trigger Pythonista to run the encode script, which would return the encoded text back to Drafts. The full action looks like this:
    
    
    drafts://x-callback-url/create?text=[[draft]]&action={{Copy to Clipboard}}&afterSuccess=Delete&x-success={{pythonista://encode?action=run}}
    

#### Piecing it all together

So now the only step I have to take to percent encode a note in Drafts is to trigger the `encode` action and wait for the process to complete. When it's all done I'll have a new note with all my text percent encoded. To do this I put the following pieces in place:

  1. In Pythonista, copy/paste the 2nd version of the `encode.py` script and save the script.
  2. In Drafts, make sure the `encode` action is installed. This action is the big red button. Click to install [encode](drafts://x-callback-url/import_action?type=URL&name=encode&url=drafts%3A%2F%2Fx-callback-url%2Fcreate%3Ftext%3D%5B%5Bdraft%5D%5D%26action%3D%7B%7BCopy%20to%20Clipboard%7D%7D%26afterSuccess%3DDelete%26x-success%3D%7B%7Bpythonista%3A%2F%2Fencode%3Faction%3Drun%7D%7D) action for Drafts.
  3. In Drafts, make sure the `paste_draft` action is installed. You can place the action in the Hidden section and still have the action be called upon by other actions. Click to install [paste_draft](drafts://x-callback-url/import_action?type=URL&name=paste_draft&url=drafts%3A%2F%2Fx-callback-url%2Fcreate%3Ftext%3D%5B%5Bclipboard%5D%5D) action for Drafts.

_Update:_ I've posted a [part 2](http://mygeekdaddy.net/2014/02/17/sharing-text-with-drafts-pythonista-part-2/) to this article after the [@drdrang](https://twitter.com/drdrang) pointed out an alternate solution.

Got any questions? Feel free to hit me up on Twitter at [@MyGeekDaddy](http://twitter.com/mygeekdaddy).
