# Weather Underground in Pythonista

_Captured: 2015-12-11 at 00:51 from [leancrew.com](http://leancrew.com/all-this/2014/02/weather-underground-in-pythonista/)_

I woke up yesterday morning, checked the weather on my phone, and got a vague sense of dissatisfaction that's probably familiar to you. This weather app doesn't have Feature A; that app does, but it doesn't have Feature B; this other app has both, but they're inconveniently hidden behind a series of taps and swipes. What I want is a custom-built app that presents just the information I use in a format that's convenient to me. Last night I took the first step toward such an app by building a simple, locally hosted webapp in Pythonista.

Longtime readers may remember [my first attempt](http://www.leancrew.com/all-this/2011/04/weather-or-not/) at something like this, [a CGI script](https://github.com/drdrang/weathertext) built on the `[pywapi` library](https://code.google.com/p/python-weather-api/) that I access through Mobile Safari and a home screen button. It produces a page that looks like this:

![CGI weather](http://farm4.staticflickr.com/3729/12724092655_1f5da34152_z.jpg)

> _[CGI weather](http://www.flickr.com/photos/drdrang/12724092655/)_

Three years later, I still use it occasionally, but it has the distinct disadvantage of being hard-coded to the western suburbs of Chicago. This is fine most of the time, but is useless when I'm traveling.

The difference between now and three years ago is that now I have [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8&uo=4&at=10l4Fv) and its `[location` module](http://omz-software.com/pythonista/docs/ios/location.html). There are two ways to take advantage of this:

  1. Rewrite the CGI script to accept latitude and longitude as parameters and have it produce a page for that location. Use Pythonista to get the current location and open the location-encoded URL.
  2. Write the whole thing in Pythonista.

I chose the second because I thought a self-contained system would be more interesting to write.

The new script would need a radar map, which ruled out using `pywapi` and [Dark Sky](https://developer.forecast.io/docs/v2) (now Forecast) as the underlying API. That led me to the [Weather Underground API](http://www.wunderground.com/weather/api/), which offers both a simple calling convention and a rich set of data, including maps.

I will say, though, that although the Weather Underground API returns an abundant data set, it's very poorly organized. Numerical data sometimes comes in the form of a floating point number and other times as a Unicode string. The documentation is thin, so you need to run experiments to learn, for example, that actual temperature is a float but the "feels like" temperature is a string. Madness. Sunrise and sunset times are even worse; they're returned as two strings, one for the hour and another for the minute.

Anyway, here's my first pass at `WeatherUnderground.py`. It doesn't have any forecast information yet, and it's woefully short on error checking (by which I mean it has no error checking). Those will come later, as will a rewriting of the cruftier bits.
    
    
      1  #!/usr/bin/python
      2  
      3  import json
      4  import requests
      5  import time
      6  from datetime import datetime
      7  import location
      8  import webbrowser
      9  import BaseHTTPServer
     10  
     11  ########################## Functions ############################
     12  
     13  def wunder(lat, lon, wukey):
     14    "Return a dictionary of weather data for the given location."
     15    
     16    # URLs
     17    baseURL = 'http://api.wunderground.com/api/%s/' % wukey
     18    conditionURL = baseURL + 'conditions/q/%f,%f.json' % (lat, lon)
     19    astroURL = baseURL + 'astronomy/q/%f,%f.json' % (lat, lon)
     20    radarURL = baseURL + 'radar/image.png' \
     21                       + '?centerlat=%f&centerlon=%f' % (lat, lon - 1) \
     22                       + '&radius=100&width=480&height=360&timelabel=1' \
     23                       + '&timelabel.x=10&timelabel.y=350' \
     24                       + '&newmaps=1&noclutter=1'
     25  
     26    # Collect data.
     27    c = requests.get(conditionURL)
     28    current = c.json()['current_observation']
     29    a = requests.get(astroURL)
     30    astro = a.json()['moon_phase']
     31  
     32    # Turn sun rise and set times into datetimes.
     33    rise = '%s:%s' % (astro['sunrise']['hour'], astro['sunrise']['minute'])
     34    set = '%s:%s' % (astro['sunset']['hour'], astro['sunset']['minute'])
     35    sunrise = datetime.strptime(rise, '%H:%M')
     36    sunset = datetime.strptime(set, '%H:%M')
     37    
     38    # Mapping of pressure trend symbols to words.
     39    pstr = {'+': 'rising', '-': 'falling', '0': 'steady'}
     40  
     41    # Construct the dictionary and return it.
     42    wudata = {'pressure': float(current['pressure_in']),
     43              'ptrend': pstr[current['pressure_trend']],
     44              'temp': current['temp_f'],
     45              'desc': current['weather'],
     46              'wind_dir': current['wind_dir'],
     47              'wind': current['wind_mph'],
     48              'feel': float(current['feelslike_f']),
     49              'sunrise': sunrise,
     50              'sunset': sunset,
     51              'moon_pct': float(astro['percentIlluminated']),
     52              'moon_age': int(astro['ageOfMoon']),
     53              'radar': radarURL}
     54    return wudata
     55              
     56  
     57  def wuHTML(lat, lon, wukey):
     58    "Return HTML with WU data for given location."
     59    
     60    d = wunder(lat, lon, wukey)
     61  
     62    # Get data ready for presentation
     63    sunrise = d['sunrise'].strftime('%-I:%M %p').lower()
     64    sunset = d['sunset'].strftime('%-I:%M %p').lower()
     65    temp = '%.0f&deg;' % d['temp']
     66    pressure = 'Pressure: %.2f and %s' % (d['pressure'], d['ptrend'])
     67    wind = 'Wind: %s at %.0f mph' % (d['wind_dir'], d['wind'])
     68    feel = 'Feels like: %.0f&deg;' % d['feel']
     69    sun = 'Sunlight: %s to %s' % (sunrise, sunset)
     70    moon = 'Moon: %s%% at %s days' % (d['moon_pct'], d['moon_age'])
     71  
     72    # Assemble the HTML.
     73    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
     74    <html>
     75    <head>
     76    <meta name="viewport" content = "width = device-width" />
     77    <title>Weather</title>
     78    <style type="text/css">
     79      body { font-family: Helvetica; }
     80      h1 { font-size: 175%%;
     81        text-align: center;
     82        margin-bottom: 0; }
     83      h2 { font-size: 125%%;
     84        margin-top: 0;
     85        margin-bottom: 0; }
     86      #now { margin-left: 0; }
     87      #gust { padding-left: 2.75em; }
     88      div p { margin-top: .25em;
     89        margin-left: .25em; }
     90    </style>
     91    </head>
     92    <body onload="setTimeout(function() { window.top.scrollTo(0, 1) }, 100);">
     93    <h1>%s &bull; %s </h1>
     94  
     95    <p><img width="100%%" src="%s" /></p>
     96  
     97    <p id="now">%s<br />
     98    %s<br />
     99    %s<br />
    100    %s<br />
    101    %s<br /></p>
    102  
    103    </body>
    104    </html>''' % (temp, d['desc'], d['radar'], wind, feel, pressure, sun, moon)
    105  
    106    return html
    107  
    108  
    109  ######################### Main program ##########################
    110  
    111  # My Weather Underground key.
    112  wukey = 'xxxxxxxxxxxxx'
    113  
    114  # Get the GPS info.
    115  location.start_updates()
    116  time.sleep(2)
    117  loc = location.get_location()
    118  
    119  # Generate the HTML.
    120  html = wuHTML(loc['latitude'], loc['longitude'], wukey)
    121  
    122  # Create the request handler.
    123  class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    124    def do_GET(s):
    125      """Respond to a GET request."""
    126      s.send_response(200)
    127      s.send_header("Content-type", "text/html")
    128      s.end_headers()
    129      s.wfile.write(html)
    130  
    131  # Start the server and show the page.
    132  server = BaseHTTPServer.HTTPServer(('', 8888), MyHandler)
    133  webbrowser.open('http://localhost:8888')
    134  server.handle_request()
    
    

The `wunder` function makes two calls to Weather Underground and returns a dictionary with the data I want to present. Whatever conversions need to be made between strings, floats, and times are done here. I'll need to add one or two new calls to get forecast information, and I may need to restructure the dictionary.

The `wuHTML` function returns the HTML for the page being served. This is pretty crude code, written quickly to see if I could get something working. As I add more information, and maybe some interactivity, I'll have to move to a real templating system.

The main program starts with my Weather Underground API key. If you want to do something like this, you'll have to get your own. The key is free, but there are restrictions on how many API calls you can make. They're generous for personal use--10 calls per minute, up to 500 calls per day--but couldn't be used for a commercial product. That requires a paid account.

The script then gets the phone's location and feeds it to `wuHTML` to generate the page. At this point, I originally thought I could display the HTML using the `[webbrowser` module](http://omz-software.com/pythonista/docs/library/webbrowser.html), but that doesn't seem to be the case. In fact, I couldn't figure out any method to simply shoot the HTML to a browser. Either I'm using the wrong Google search terms or it really isn't allowed.

That led me to the `[BaseHTTPServer`](http://omz-software.com/pythonista/docs/library/basehttpserver.html) code. Lines 123-129 set up a handler class that serves the HTML in response to a `GET` request, and Lines 132 and 134 run the server. I have no previous experience with `BaseHTTPServer`, and I may be doing this part wrong. I have occasionally gotten "Address already in use" errors on Line 132, so I clearly don't have everything right yet.

Line 133 launches Pythonista's built-in browser to display the page, which looks like this:

![Weather Underground in Pythonista](http://farm4.staticflickr.com/3682/12721455433_87f51c0188_z.jpg)

As you can see, I stole most of the HTML from my old CGI script. I think I'll be dumping the moon information, and I'll definitely be adding wind gusts once I learn whether the WU API always includes a gust item in the returned JSON.

The radar map, by the way, isn't centered on my location. I've done that deliberately because I'm more interested in what's west of me than what's east of me. The positioning of the map is done in Line 21, where the center of the map is set one degree west of the current location. That's the kind of customization you can achieve when you write the code yourself.

I'm not sure how I'll handle the forecasts, but I'm leaning toward a detailed view of the remainder of today; morning, afternoon, and evening summaries for tomorrow; and maybe just high and low temperatures for the following day or two. There will be a lot of messing around as I learn what works and what doesn't, but I don't want to clutter ANIAT with every detail. At the moment, the code is in [a gist](https://gist.github.com/drdrang/9167711); as it grows, I think I'll move it to a proper GitHub repository.

This work is licensed under a [Creative Commons Attribution-Share Alike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).
