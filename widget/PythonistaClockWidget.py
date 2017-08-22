# coding: utf-8
import ui, speech, console
svgInHtml='''
<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 400 400" width="400" height="400" version="1.0">
  <defs>
    <linearGradient id="a" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#777799"/>
      <stop offset="100%" style="stop-color:#ffffff"/>
    </linearGradient>
    <linearGradient id="b" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="25%" style="stop-color:#b6b6cc"/>
      <stop offset="40%" style="stop-color:#515177"/>
      <stop offset="48%" style="stop-color:#ffffff"/>
      <stop offset="56%" style="stop-color:#ffffff"/>
      <stop offset="75%" style="stop-color:#8b8baa"/>
      <stop offset="98%" style="stop-color:#efeff4"/>
      <stop offset="100%" style="stop-color:#fbfbfc"/>
    </linearGradient>
    <linearGradient id="c" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="100%" style="stop-color:#777799"/>
    </linearGradient>
    <radialGradient id="d" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:#ffffff"/>
      <stop offset="40%" style="stop-color:#ffffff"/>
      <stop offset="70%" style="stop-color:#e6e6ee"/>
      <stop offset="92%" style="stop-color:#b6b6cc"/>
      <stop offset="100%" style="stop-color:#636388"/>
    </radialGradient>
    <radialGradient id="e" cx="50%" cy="150%" r="200%" fx="50%" fy="150%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0"/>
      <stop offset="59%" style="stop-color:#ffffff;stop-opacity:0"/>
      <stop offset="60%" style="stop-color:#ffffff;stop-opacity:0.6"/>
      <stop offset="70%" style="stop-color:#ffffff;stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0.0"/>
    </radialGradient>
  </defs>
  <g transform="translate(200 200)">
    <circle cx="0" cy="0" r="200" fill="#cecedd"/>
    <circle cx="0" cy="0" r="196" stroke="url(#a)" stroke-width="5" fill="url(#b)"/>
    <circle cx="0" cy="0" r="170" stroke="url(#c)" stroke-width="4" fill="url(#d)"/>
    <circle cx="0" cy="0" r="172" stroke="#ffffff" stroke-width="0.5" fill="none"/>
    <circle cx="0" cy="0" r="193.5" stroke="#ffffff" stroke-width="0.5" fill="none"/>
    <g id="O">
      <polygon points="4,155 4,130 -4,130 -4,155" style="fill:#777799;stroke:#313155;stroke-width:1"/>
      <polygon points="4,-155 4,-130 -4,-130 -4,-155" style="fill:#777799;stroke:#313155;stroke-width:1"/>
    </g>
    <g transform="rotate(30)"><use xlink:href="#O"/></g>
    <g transform="rotate(60)"><use xlink:href="#O"/></g>
    <g transform="rotate(90)"><use xlink:href="#O"/></g>
    <g transform="rotate(120)"><use xlink:href="#O"/></g>
    <g transform="rotate(150)"><use xlink:href="#O"/></g>
    <polygon id="h" points="6,-80 6,18 -6,18 -6,-80" style="fill:#232344">
      <animateTransform id="ht" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="86400s" repeatCount="indefinite"/>
    </polygon>
    <polygon id="m" points="3.5,-140 3.5,23 -3.5,23 -3.5,-140" style="fill:#232344">
      <animateTransform id="mt" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="3600s" repeatCount="indefinite"/>
    </polygon>
    <polygon id="s" points="2,-143 2,25 -2,25 -2,-143" style="fill:#232344">
      <animateTransform id="st" attributeType="xml" attributeName="transform" type="rotate" from="000" to="000" begin="0" dur="60s" repeatCount="indefinite"/>
    </polygon>
    <circle cx="0" cy="0" r="163" fill="url(#e)"/>
  </g>
  <script type="text/javascript"><![CDATA[
    var d = new Date();
    var s = d.getSeconds();
    var m = d.getMinutes() + s/60;
    var h = (d.getHours() % 12) + m/60 + s/3600;
    document.getElementById('st').setAttribute('from',s*6);
    document.getElementById('mt').setAttribute('from',m*6);
    document.getElementById('ht').setAttribute('from',h*30);
    document.getElementById('st').setAttribute('to',360+s*6);
    document.getElementById('mt').setAttribute('to',360+m*6);
    document.getElementById('ht').setAttribute('to',360+h*30);
  ]]></script>
</svg>
'''
announce1 = "The current local time"
announce2 =  "is"

numbersZeroToTwenty = 'zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty'.split(',')

thirty = "thirty"
forty = "forty"
fifty = "fifty"
am = "A.M"
pm = "P.M"
ampm = ""
oclock = "oclock"
# Turn off tracing when not required for simple debug/trace
traceFlag = True

speechDelay = 0.05
locale = "en-US"
#==============================================================================
class ClockGadget:
	def __init__(self):
		view = ui.load_view()
		
		# Set announce duration to a default of once per every 15 minutes.
		#view['rootview']['announceFreqTextfield'].text = '15'
		#view['rootview']['announceFreqSlider'].value = .25 # every 1/4 hour.
		
		# cache away the current location (if location services on for Pythonista)
		self.locationString = self.createCurrentLocationString()
		
		if traceFlag: print 'location string in __init__ is ->>' + self.locationString
		
		webview = view['rootview']['webview']

		# Place the analog clock in a location that is sensible for a "gadget"
		# and disable touch or multitouch gestures to prevent unwannted resizing
		# or movement to the underlying clock itself which has no need to do so.
		webview.height = 20
		webview.width = 10
		webview.frame= 15,25,120,125
		webview.multitouch_enabled = False
		webview.touch_enabled = False
		if traceFlag: print 'Presenting view now.'
		view.present('sidebar')
		if traceFlag: print 'Loading html with embedded svg now.'
		webview.load_html(svgInHtml)
#==============================================================================
	def speaknowButtonTapped(self, sender):
		if sender.name == 'speakTimeButton':
			# Get the say seconds preference
			isSaySeconds = sender.superview['speakSecondsSwitch'].value
			if traceFlag: print 'isSaySeconds current value now->>' + str(isSaySeconds)
			
			timeMessage = self.getCurrentLocalTimeAnnouncement(isSaySeconds)
			if traceFlag: print 'Time message to announce ->>' + timeMessage
			speech.say(timeMessage,locale, speechDelay)
#=============================================================================
	def switchTapped(self,sender):
		if sender.name == 'speakSecondsSwitch':
			if traceFlag: print "speakSecondsSwitch tapped...current value is ->>" + str(sender.value)
#==============================================================================
	def createCurrentLocationString(self):
		import location
		location.start_updates()
		coordinates = location.get_location()
		addressDictionaries = location.reverse_geocode(coordinates)
		mycity = addressDictionaries[0]['City']
		mycountry = addressDictionaries[0]['Country']
		
		# if we can't get city and country not much point to continue
		if mycountry == None or mycity == None:
			return ""
		
		locationString = "in " + mycity + " " + mycountry
		location.stop_updates()
		
		if traceFlag: print 'Returning location string ->>' + locationString
		return locationString
#==============================================================================
	def getCurrentLocalTimeAnnouncement(self, isSaySeconds):
		from datetime import datetime
		
		##todo maybe get time and pass in from another function since calc twice?
		now = datetime.now().time()
		nowHour = now.hour
		nowMinutes = now.minute
		nowSeconds = now.second

		# Get the current local hour
		hourString = self.getCurrentHourString(nowHour)
		if traceFlag: print "hourString is -->" + hourString

		# Get the local current minute
		minuteString = self.getCurrentMinutesString(nowMinutes)
		if traceFlag: print 'minuteString is ->>' + minuteString
		
		# If it is right on the hour, add "o'clock"; if not, bad English grammar to use it in this context.
		if nowMinutes == 0:
			hourString = hourString + " " + oclock

		# If minutes less than 10 US english adds ' oh'begore saying minutes, eg. 'Two oh one'for 2:01, but make sure not to append 'owe' if its right on the hour. That is, when 'oclock' never 'owe' preventing 'nine oclock owe p.m.' phrases.
		if nowMinutes > 0 and nowMinutes < 10:
			minuteString = "owe " + minuteString # Use 'owe' which is real word not to confuse speech synth.

		# Not using 24 hour system but instead a 12 hour one which uses a.m and p.m
		ampm = am if nowHour < 12 else pm

		announcement = ""
		seconds = "seconds"
		
		if isSaySeconds:
			# English grammar, if seconds is 1, agrrement rules say use singular.
			if nowSeconds == 1: seconds = "second"
			
			announcement =  announce1 + " " + self.locationString + " " +announce2 + " " + hourString + " " + minuteString + " " + ampm + " " + str(nowSeconds) + " " + seconds + " "
		else:
			announcement =  announce1 + " " + self.locationString + " " + announce2 + " "  + hourString + " " + minuteString + " " + ampm
		if traceFlag: print announcement
		return announcement
#==============================================================================
	def getCurrentHourString(self, nowHour):
		if traceFlag: print "nowHour parameter to function ->>" + str(nowHour)
		hourString = ""
	
		assert -1 < nowHour < 24, 'Error: Invalid hour {}.'.format(nowHour)
		if traceFlag: print "Hour string to return ->>" + hourString
		return numbersZeroToTwenty[nowHour % 12 or 12]
#==============================================================================
	def getCurrentMinutesString(self, nowMinutes):
		minuteString = ""

		# Handles minutes between 1 and 20
		if nowMinutes > 0 and nowMinutes < 21:
			minuteString = numbersZeroToTwenty[nowMinutes]

		# Handles minutes between 21 and 29
		if nowMinutes > 20 and nowMinutes < 30:
			if nowMinutes == 21:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[1]
			elif nowMinutes == 22:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[2]
			elif nowMinutes == 23:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[3]
			elif nowMinutes == 24:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[4]
			elif nowMinutes == 25:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[5]
			elif nowMinutes == 26:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[6]
			elif nowMinutes == 27:
				minuteString = numbersZeroToTwenty[20] + " " + numbersZeroToTwenty[7]
			elif nowMinutes == 28:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[8]
			elif nowMinutes == 29:
				minuteString = numbersZeroToTwenty[20] + " " + numbersOneToTwenty[9]

		# Handle 30 minutes
		if nowMinutes == 30:
			minuteString = thirty

		# Handles minutes between 31 and 39
		if nowMinutes > 30 and nowMinutes < 40:
			if nowMinutes == 31:
				minuteString = thirty + " " + numbersZeroToTwenty[1]
			elif nowMinutes == 32:
				minuteString = thirty + " " + numbersZeroToTwenty[2]
			elif nowMinutes == 33:
				minuteString = thirty + " " + numbersZeroToTwenty[3]
			elif nowMinutes == 34:
				minuteString = thirty + " " + numbersZeroToTwenty[4]
			elif nowMinutes == 35:
				minuteString = thirty + " " + numbersZeroToTwenty[5]
			elif nowMinutes == 36:
				minuteString = thirty + " " + numbersZeroToTwenty[6]
			elif nowMinutes == 37:
				minuteString = thirty + " " + numbersZeroToTwenty[7]
			elif nowMinutes == 38:
				minuteString = thirty + " " + numbersZeroToTwenty[8]
			elif nowMinutes == 39:
				minuteString = thirty + " " + numbersZeroToTwenty[9]

		# Handles 40 minutes
		if nowMinutes == 40:
			minuteString = forty

		if nowMinutes > 40 and nowMinutes < 50:
			if nowMinutes == 41:
				minuteString = forty + " " + numbersZeroToTwenty[1]
			elif nowMinutes == 42:
				minuteString = forty + " " + numbersZeroToTwenty[2]
			elif nowMinutes == 43:
				minuteString = forty + " " + numbersZeroToTwenty[3]
			elif nowMinutes == 44:
				minuteString = forty + " " + numbersZeroToTwenty[4]
			elif nowMinutes == 45:
				minuteString = forty + " " + numbersZeroToTwenty[5]
			elif nowMinutes == 46:
				minuteString = forty + " " + numbersZeroToTwenty[6]
			elif nowMinutes == 47:
				minuteString = forty + " " + numbersZeroToTwenty[7]
			elif nowMinutes == 48:
				minuteString = forty + " " + numbersZeroToTwenty[8]
			elif nowMinutes == 49:
				minuteString = forty + " " + numbersZeroToTwenty[9]

		# Handle 50 minutes
		if nowMinutes == 50:
			minuteString = fifty

		# Handle minutes between 51 and 59
		if nowMinutes > 50 and nowMinutes < 60:
			if nowMinutes == 51:
				minuteString = fifty + " " + numbersZeroToTwenty[1]
			elif nowMinutes == 52:
				minuteString = fifty + " " + numbersZeroToTwenty[2]
			elif nowMinutes == 53:
				minuteString = fifty + " " + numbersZeroToTwenty[3]
			elif nowMinutes == 54:
				minuteString = fifty + " " + numbersZeroToTwenty[4]
			elif nowMinutes == 55:
				minuteString = fifty + " " + numbersZeroToTwenty[5]
			elif nowMinutes == 56:
				minuteString = fifty + " " + numbersZeroToTwenty[6]
			elif nowMinutes == 57:
				minuteString = fifty + " " + numbersZeroToTwenty[7]
			elif nowMinutes == 58:
				minuteString = fifty + " " + numbersZeroToTwenty[8]
			elif nowMinutes == 59:
				minuteString = fifty + " " + numbersZeroToTwenty[9]

		if traceFlag: print "Minute string to return ->>" + minuteString
		return minuteString
#==============================================================================
if traceFlag: console.clear()
ClockGadget()
