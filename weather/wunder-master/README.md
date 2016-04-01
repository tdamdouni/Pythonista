# Wunder #

Weather information via the [Weather Underground API][1]. Intended for use on an iPhone, but I'm sure the GPS stuff can be adapted to Android.

## CGI script ##

The CGI script, `wunder.py`, takes the latitude and longitude as parameters and generates a web page with

* A local radar image centered 1° west of the location. I'm used to weather coming from the west.
* The current conditions and today's sunrise and sunset.
* The forecast for the next twelve hours, given at three-hour intervals.
* Forecasts for the next two days, given at four-hour intervals.

<img width=300 src="http://leancrew.com/all-this/images2015/20150829-Weather%20page.png" alt="Weather page" title="Weather page" />

The script requires a [Weather Underground key][3] that's saved in the `wukey` variable on Line 187.

## HTML file ##

The HTML file, `wunderlocal.html`, uses the [iOS Geolocation class][2] to access the GPS data via JavaScript and uses the latitude and longitude to construct a URL that calls `wunder.py`.

Both the `wunder.py` and `wunderlocal.html` must be put on a server where they're accessible via a web browser. Depending on how your web server is configured, you may need to change the extension on `wunder.py` to make it executable. Whatever its name, you'll need to edit Line 11 of `wunderlocal.html` to set the `wURL` variable to the URL of the CGI script.

## Home screen buttons ##

To create a home screen button for a fixed location, just enter a URL of the form

    http://path/to/wunder.py?lat=yy.yyy&lon=-xx.xxx

where `yy.yyy` and `-xx.xxx` are the latitude and longitude of the location in decimal degrees. After the page loads, use the Share button and the <span class="menu">Add to Home Screen</span> command to create an icon on your home screen that opens Safari immediately to the weather page for that location.

Creating a home screen button that gives you the weather for your current location is a little trickier. First, comment out the `<script>` in Lines 17–19 of `wunderlocal.html`. Then uncomment the `<h1>` on Line 21. Then go to

    http://path/to/wunderlocal.html

in Safari. Because of the commenting/uncommenting, it won't show any weather data, but that's OK. Go ahead and use <span class="menu">Add to Home Screen</span> again to make an icon on your home screen linked to that URL.

Once you've made the home screen button, go back into `wunderlocal.html` and uncomment Lines 17–19 and comment out Line 21, putting the file back into its original state. Now when you tap the home screen button, it'll redirect you to a weather info page for your current location. You'll probably be asked for permission for the page to access your location.


[1]: http://www.wunderground.com/weather/api
[2]: https://developer.apple.com/library/safari/documentation/AppleApplications/Reference/SafariWebContent/GettingGeographicalLocations/GettingGeographicalLocations.html
[3]: http://www.wunderground.com/weather/api/d/login.html
