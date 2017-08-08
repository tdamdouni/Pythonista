# Automatic shortened URLs via Google

_Captured: 2015-09-26 at 02:39 from [www.leancrew.com](http://www.leancrew.com/all-this/2014/08/automatic-shortened-urls-via-google/)_

Back in the old days (that is, maybe three years ago), everyone on Twitter used some specialized URL shortening service, like [bit.ly](http://bit.ly) or [tr.im](http://tr.im), to keep their tweets under 140 characters. That became counterproductive when Twitter started its own shortening service and built an infrastructure around it. Nowadays, it's much better for your readers if you just paste in the full, true URL of the page you want to link to and let Twitter handle the shortening and the display.

Except…

Except when you want to include a link in a direct message. Twitter refuses most links in DMs because

  1. it doesn't want to pass along spam or phishing attacks in DMs; but
  2. it doesn't want to take responsibility for vetting the links before shortening them.

If you try to send a link via DM in the web interface, it responds with a terse "Your message can't be sent." In [Tweetbot](https://itunes.apple.com/us/app/tweetbot-3-for-twitter-iphone/id722294701?mt=8&uo=4&at=10l4Fv), you get a longer but no more satisfying explanation.

![Tweetbot DM error](https://farm6.staticflickr.com/5555/14810452035_dfd4490306_o.png)

> _By "later," I guess they mean "when Twitter changes its policy."_

Some links _are_ allowed in direct messages. I don't know all the possibilities, but I know you can include those from Google's [goo.gl](http://goo.gl/) service. I don't send a lot of direct messages, and those I send generally don't include links, but when I need to send links, goo.gl is what I use.

Yesterday I decided to automate the process of getting goo.gl-shortened links by using Google's [URL Shortener API](https://developers.google.com/url-shortener/). I signed up for an [API key](https://code.google.com/apis/console), but after some experimentation, I found that the key wasn't necessary. Maybe you need it if you want to track links, but I have no interest in that, especially for one-off links in direct messages.

I followed [Google's examples](https://developers.google.com/url-shortener/v1/getting_started#shorten) to learn how to shorten a URL from the command line using `[curl`](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/curl.1.html). Here's a long example, split up over three lines:
    
    
    curl  https://www.googleapis.com/urlshortener/v1/url \
     -H 'Content-Type: application/json' \
     -d '{"longUrl": "http://www.leancrew.com/all-this/2014/07/alfred/"}'

The `-d` argument is what's POSTed, and as you can see, it's in JSON format. The result is in JSON format, too:
    
    
    {
     "kind": "urlshortener#url",
     "id": "http://goo.gl/GZ5t0e",
     "longUrl": "http://www.leancrew.com/all-this/2014/07/alfred/"
    }

What I wanted to make was a [TextExpander](https://itunes.apple.com/us/app/textexpander-for-mac/id405274824?mt=12&uo=4&at=10l4Fv) snippet that would take the URL of the frontmost browser tab and return a shortened version of it. Here it is.

![TextExpander URL shortener](https://farm4.staticflickr.com/3874/14626003429_5068e17540_z.jpg)

> _It's an AppleScript snippet with an abbreviation of ;surl. The AppleScript content is this script:_
    
    
     1  tell application "System Events"
     2    set numSafari to count (every process whose name is "Safari")
     3    set numChrome to count (every process whose name is "Google Chrome")
     4  end tell
     5  set longURL to "none"
     6  
     7  if numSafari > 0 then
     8    tell application "Safari" to set longURL to URL of front document
     9  else
    10    if numChrome > 0 then
    11      tell application "Google Chrome" to set longURL to URL of active tab of front window
    12    end if
    13  end if
    14  
    15  set payload to "{\"longUrl\": \"" & longURL & "\"}"
    16  
    17  set cmd to "curl -s https://www.googleapis.com/urlshortener/v1/url -H 'Content-Type: application/json' -d '" & payload & "' | awk '/^ \"id\":/ {gsub(/\"|,/, \"\", $2); print $2}'"
    18  
    19  return do shell script cmd
    
    

Lines 1-13 are essentially the same as my `[;furl` snippet](http://www.leancrew.com/all-this/2010/10/textexpander-snippets-for-google-chrome/). They get the URL of the active browser tab, from Chrome if it's running or from Safari if it's running. Line 15 then constructs the JSON payload, and Line 17 builds a call to `curl` just like the example above. It also pipes the JSON output to an awk one-liner to extract just the shortened URL. There's a lot of backslash escaping of double quotation marks because AppleScript. Line 19 runs the command and returns the result.

(I decided to use awk here because the JSON returned by the API is pretty simple. If I were dealing with more complex output, I'd mimic what Greg Scown of Smile did in [this blog post](http://smilesoftware.com/blog/entry/currency-conversion-with-textexpander). He used a headless application called [JSON Helper](https://itunes.apple.com/us/app/json-helper-for-applescript/id453114608?mt=12&uo=4&at=10l4Fv) [free on the Mac App Store] to parse the longer JSON data returned from a currency conversion API call.)

I also made a similar snippet for shortening a URL on the clipboard. Its abbreviation is `;scurl` and its AppleScript content is this script:
    
    
    1  set longURL to the clipboard
    2  
    3  set payload to "{\"longUrl\": \"" & longURL & "\"}"
    4  
    5  set cmd to "curl -s https://www.googleapis.com/urlshortener/v1/url -H 'Content-Type: application/json' -d '" & payload & "' | awk '/^ \"id\":/ {gsub(/\"|,/, \"\", $2); print $2}'"
    6  
    7  return do shell script cmd
    
    

That takes care of OS X, how about iOS? There's no AppleScript on iOS, and TextExpander doesn't run scripts, so I went with a [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=10l4Fv) script that replaces a URL on the clipboard with a shortened version. Here's the script:
    
    
     1  import requests
     2  import json
     3  import clipboard
     4  
     5  # Build the request.
     6  shortener = "https://www.googleapis.com/urlshortener/v1/url"
     7  longURL = clipboard.get()
     8  headers = {'content-type': 'application/json'}
     9  payload = {'longUrl': longURL}
    10  
    11  # Get the shortened URL and put it on the clipboard.
    12  r = requests.post(shortener, headers=headers, data=json.dumps(payload))
    13  clipboard.set(r.json()['id'])
    
    

On iOS, I copy the URL I want to shorten, switch to Pythonista, run the script, then switch to Tweetbot to paste the shortened URL into a DM. There's probably a way to cut out a step or two by using an [x-callback URL](http://x-callback-url.com/), but I haven't messed around with that yet.

None of these scripts are forgiving. Inputs that aren't URLs will produce nasty output that isn't handled gracefully. Be aware of this if you want to adapt these scripts for your own use.
