# Sharing text with Drafts & Pythonista - Part 2

_Captured: 2015-11-07 at 00:46 from [mygeekdaddy.net](http://mygeekdaddy.net/2014/02/17/sharing-text-with-drafts-pythonista-part-2/)_

Sometimes when you come up with a solution, someone else has already found a more elegant solution. Case in point, my recent post on [sharing text between Drafts and Pythonista](http://mygeekdaddy.net/2014/02/16/getting-pythonista-to-return-text-back-to-drafts/). Shortly after sharing the post I got some feedback on the post and ultimately a tweet from the sensei of scripting himself:

> [@mygeekdaddy](https://twitter.com/mygeekdaddy) You can pass text back and forth without using the clipboard: <http://www.leancrew.com/all-this/2013/08/sorting-with-pythonista/>
> 
> -- Dr. Drang (@drdgrang) [February 16, 2014](https://twitter.com/drdrang/statuses/435082449417023488)

Digging into the link [@drdrang](https://twitter.com/drdrang) included in his tweet, I found it was a post he made about the same topic back in August. As I read through his post he noted that the origin of his solution actually came from [@hiilppp](https://twitter.com/hiilppp) and a [gist](https://gist.github.com/hiilppp/6139407) that hiilppp had posted a while back on GitHub.

As shown above, the script shows the basic syntax of using Pythonista's `&argv=[[draft]]` action to pass text from Drafts, then using `sys.argv` to read the text block from Drafts into the python script and then using a shortened x-callback-url to pass the modfied text back to Drafts. It's short, it's elegant and it gives me the big red button I wanted.

So does this invalidate my solution?

> Hell no! 

My original solution ultimately boiled down to what I've used in my scripting and what works for me. If I learn something new along the way, which I did in this case, I can take that little nugget and use it again down the road. Dr Drang is absolutely correct that the `sys.argv` method he and hiilppp shared is a cleaner way to manage text between Drafts and Pythonista. The comments

I received on the post tried to intimate that a solution that works, but is not the the _best_ solution available, should never be shared is just plain ridiculous. 
