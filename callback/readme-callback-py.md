# callback 

A simple small module for Pythonista (http://omz-software.com/pythonista) which aims to make an easy callback URL handling & argument passing system. 

# Usage

1. `import callback`
2. Create a handler instance `handler = callback.InfoHandler(sys.argv)`
3. Decorate command handlers with `@handler.cmd(cmdname)`
4. Call `handler.handle()` (and if it returns False, there was nothing to handle!)
5. To create a callback url for a certain command use `callback.url(cmdname[,script][,a=1,b=2,....)` (defaults to current script) and assign this to any `x-callback-url` compliant URL argument!

# How It Works

The resulting callback URL will have the first argv set to `'callback'`, and the second argv to a JSON object string.  The JSON object has a key called `'cmd'` for the command name, and other keys are named arguments for the command.

The `InfoHandler` class checks if `argv[0]` is `'callback'` and if so, parses the JSON object in `argv[1]`.  Each function decorated with `@handler.cmd()` gets added to a command map and when `handler.handle()` is called, the appropriate function is called with the arguments from the JSON object (except for `'cmd'`).

# Examples

###tweetprocessor.py 

This uses the `TweetBot` module (https://gist.github.com/djbouche/5079739).  `tweetprocessor.py` when normally run, will read `tweets.txt` and process each line as a separate tweet via TweetBot.

    import TweetBot
    import callback
    import sys

    handler = callback.InfoHandler(sys.argv)

    @handler.cmd("process_next")
    def process_next(tweets):
        if len(tweets):
            t = tweets.pop() #process next tweet on the list
            #tweet, and send the list of remaining tweets down
            TweetBot.tweet(t,callback.url('process_next',tweets=tweets))
        else: #no more tweets
            print 'Finished processing tweets!'

    if name == "__main__" and not handler.handle():
        #first entry point
        f = open("tweets.txt","r") #read tweets from a file called 'tweets.txt'
        a = f.read()
        f.close()
        tweets = a.splitlines() #one line per tweet
        tweets.reverse() #so we can pop them off
        process_next(tweets) #start processing!

###listtweet.py

Of course, you can use the handler command from another script as normal.

    import tweetprocessor

    tweetprocessor.process_next(['tweet 1','tweet 2','tweet 3'].reverse)

###facetweet.py 

You could also use it in a callback in another script.  `facetweet.py` will have the posted text to `tweetprocessor.py` `process_next()` after the post to Facebook is completed.  This uses the `Drafts` module (https://gist.github.com/djbouche/5079537).

    import Drafts
    import callback

    sometext = "Hello, world!"

    # Use 'tweetprocessor' as the callback script
    Drafts.do_action('Post to Facebook',sometext,
        callback.url('process_next','tweetprocessor',tweets=[sometext]))
