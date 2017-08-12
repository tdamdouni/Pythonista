# Weather or not

_Captured: 2015-12-28 at 14:07 from [www.leancrew.com](http://www.leancrew.com/all-this/2011/04/weather-or-not/)_

Ben Brooks spent all day [publishing](http://brooksreview.net/2011/04/weather/) [posts](http://brooksreview.net/2011/04/seasonality/) on [iOS weather apps](http://brooksreview.net/2011/04/weather-follow-up/), and after reviewing over a dozen apps, he still didn't find an unambiguous winner.

I feel his pain. I've tried a handful of weather apps--nothing that Ben didn't cover today--and have kept switching back and forth because none of them have been satisfying. While reading Ben's posts, I decided that most of the time all I really wanted in a weather app is what I have on my Mac desktop via [NerdTool](http://mutablecode.com/apps/nerdtool): a short text description of the [current conditions and forecasts](http://www.leancrew.com/all-this/2011/03/nerdtool-picts-and-buddhism/) for today and tomorrow and [a radar image of the Chicago area](http://www.leancrew.com/all-this/2011/03/desktop-radar-image-via-nerdtool/).

I decided to try a simple CGI script that uses the same [pywapi Python library](http://code.google.com/p/python-weather-api/) used by [my weathertext script](https://github.com/drdrang/weathertext). In addition to the text, it grabs the radar image I use on my Desktop. The script is saved as `weather.cgi` in the `[weathertext` repository](https://github.com/drdrang/weathertext), and you can see it in action by pointing Mobile Safari to <http://leancrew.com/cgi-bin/weather.cgi>.

![Composite of weather.cgi page](http://www.leancrew.com/all-this/images2011/weather-cgi.png)

> _Composite of weather.cgi page_

**Update 4/27/11**  
I should mention that I made [a weather webapp](http://www.leancrew.com/all-this/2008/05/better-weather-forecasts-for-the-iphone/) a few years ago and abandoned it. That one worked by screen-scraping brief forecasts from a National Weather Service page. It wasn't as concise and didn't include as much information as this project. Also, because didn't use an API, it'll break if the design of the source page changes significantly. Surprisingly, [it still works](http://www.leancrew.com/cgi-bin/nws-naperville.cgi).

The best thing about `weather.cgi` is its speed. Because there's only one image--and it's a static image--the page loads much more quickly than any of the apps I've used.

Obviously, this is not a complete substitute for a real weather app because it's limited to a single location. But it's the location I spend the most time checking, so it may work better than a real app when I'm around home. I've put a link to it on my home screen so I can test it for a week or so.

**Update 4/28/11**  
Young Mr. Brooks has [forked](https://github.com/benbrooks/weathertext/blob/master/weather.cgi) my repository, changed the location to Seattle, and restyled the output by fiddling with the embedded CSS. You can [see it here](http://b3nbrooks.com/cgi-bin/weather.cgi).

I think I'll steal his idea of making the current temperature more prominent (and getting rid of the word "temperature"--what else would it be?), but I won't be changing the font to Thornburi. Verdana maybe, but not Thornburi. And my old eyes could use a bit more contrast than he gives.
