# http://musicdiver.com/wordpress/2017/02/ulam-zahlenspiralen/

#--------------------------------------------------------------------------
# Title      : Number Spirals Explorer
# Author     : Stefan Wolfrum (@metawops)
# Date       : June 2016
# Last Update: March 2017 (added Sharing Button for exporting a screenshot)
# Version    : 1.0
# License    : Creative Commons Attribution-ShareAlike 3.0 Germany License.
# LicenseLink: http://creativecommons.org/licenses/by-sa/3.0/de/
#--------------------------------------------------------------------------

import ui
import math
import webbrowser
import photos
import datetime
import console
from sympy.ntheory import isprime, sieve
from platform import machine

#--- NumberSpiralView class
class numberSpiralView (ui.View):

	def __init__(self):
		# This will also be called without arguments when the view is loaded from a UI file.
		# You don't have to call super. Note that this is called *before* the attributes
		# defined in the UI file are set. Implement `did_load` to customize a view after
		# it's been fully loaded from a UI file.
		self.transform = ui.Transform.translation(self.center[0], self.center[1])
		device = machine()
		if device == 'iPad6,7':    # iPad Pro 12.9"
			self.maxSpacing = 72.0
		elif (device == 'iPad6,4') or (device == 'iPad5,4'):  # iPad Pro 9.7" or iPad Air 2 9.7"
			self.maxSpacing = 51.0
		elif device == 'iPad5,1':  # iPad mini 4 7.9"
			self.maxSpacing = 51.0

		self.turns = 3.0  # initial number of turns of the spiral
		self.spacing = self.maxSpacing / self.turns
		self.maxTurns = 100.0
		self.drawAxis = False
		self.drawDots = True
		self.drawNumbers = True
		self.autoSpacing = True
		self.hilitePrimes = False
		self.drawSpiral = True
		self.primesOnly = False
		self.drawCurve = False
		self.curveParamA = 1.0
		self.curveParamB = 1.0
		self.curveParamC = 41.0
		self.maxA = self.maxB = self.maxC = 80.0
		self.spiralPath = ui.Path()
		self.axisPath = ui.Path()
		self.dotSize = 4.0
		self.numberOffsetX = 0.0
		self.numberOffsetY = 9.0
		self.primeDotColor = '#e00'
		self.numbersColor = '#000'
		self.curveColor = '#3af'
		self.curveDotsColor = (0.0, 0.0, 1.0, 0.5)
		self.spiralColor = '#999'
		self.dotsColor = '#666'
		self.backgroundColor = '#eee'
		#self.numberFont = ('<system>', 12)
		self.numberFont = ('HelveticaNeue-Light', 8)
			
	def setup(self):
		#print('setup()')
		self.listOfPrimes = [i for i in sieve.primerange(2,10000)]
		self.background_color = self.backgroundColor
		
	def did_load(self):
		# This will be called when a view has been fully loaded from a UI file.
		self.setup()
		
	def will_close(self):
		# This will be called when a presented view is about to be dismissed.
		# You might want to save data here.
		pass
	
	def draw(self):
		# This will be called whenever the view's content needs to be drawn.
		# You can use any of the ui module's drawing functions here to render
		# content into the view's visible rectangle.
		# Do not call this method directly, instead, if you need your view
		# to redraw its content, call set_needs_display().
		self.axisPath = ui.Path()
		self.spiralPath = ui.Path()
				
		(self.cx, self.cy) = self.bounds.center()
		
		if (self.drawAxis):
			ui.set_color('black')
			# x-Axis:
			self.axisPath.move_to(0, self.cy)
			self.axisPath.line_to(self.bounds[2], self.cy)
			# y-Axis:
			self.axisPath.move_to(self.cx, 0)
			self.axisPath.line_to(self.cx, self.bounds[3])
			
			#self.axisPath.move_to(cx+self.spacing*2.0*math.pi, 0)
			#self.axisPath.line_to(cx+self.spacing*2.0*math.pi, self.height)
			self.axisPath.stroke()
		
		if (self.drawSpiral):
			ui.set_color(self.spiralColor)
			t = 0.0
			max_t = self.turns * 2.0*math.pi
			t_step = 0.08  # t_step constant for now but should be dynamic!
			posx = posy = 0
			self.spiralPath.move_to(posx + self.cx, posy + self.cy)
			while (t < max_t-t_step):
				t = t + t_step
				posx = self.spacing * t * math.cos(t)
				posy = self.spacing * t * math.sin(t)
				self.spiralPath.line_to(posx + self.cx, -posy + self.cy)
			# finally make sure that the end of the path lies exactly on the x-Axis:
			finalx = self.spacing * max_t * math.cos(max_t)
			finaly = self.spacing * max_t * math.sin(max_t)
			self.spiralPath.line_to(finalx + self.cx, finaly + self.cy)
			self.spiralPath.stroke()
		
		if (self.drawDots):
			n = 0
			max_n = self.turns * self.turns
			while (n <= max_n):				
				(x, y) = coordsForNumber(n)
				dotx = self.cx + (x * self.spacing * 2*math.pi)
				doty = self.cy + (y * self.spacing * 2*math.pi)
							
				dotPath = ui.Path()
				if self.hilitePrimes:
					if (n in self.listOfPrimes):
						ui.set_color(self.primeDotColor)
						circlePath = ui.Path.oval(dotx-self.dotSize, doty-self.dotSize, 2*self.dotSize, 2*self.dotSize)
						circlePath.fill()
						if self.drawNumbers:
							ui.draw_string(str(n), (dotx+self.dotSize+self.numberOffsetX, doty-(self.dotSize+self.numberOffsetY)-self.numberFont[1]+10, 0, 0), self.numberFont, self.numbersColor)
					else:
						if not self.primesOnly:
							ui.set_color(self.dotsColor)
							circlePath = ui.Path.oval(dotx-self.dotSize, doty-self.dotSize, 2*self.dotSize, 2*self.dotSize)
							circlePath.fill()						
							if self.drawNumbers:
								ui.draw_string(str(n), (dotx+self.dotSize+self.numberOffsetX, doty-(self.dotSize+self.numberOffsetY)-self.numberFont[1]+10, 0, 0), self.numberFont, self.numbersColor)
				else:
					if not self.primesOnly:
						ui.set_color(self.dotsColor)
						#dotPath.add_arc(dotx, doty, self.dotSize, 0, 2*math.pi)
						#dotPath.fill()
						circlePath = ui.Path.oval(dotx-self.dotSize, doty-self.dotSize, 2*self.dotSize, 2*self.dotSize)
						circlePath.fill()
						if self.drawNumbers:
							ui.draw_string(str(n), (dotx+self.dotSize+self.numberOffsetX, doty-(self.dotSize+self.numberOffsetY)-self.numberFont[1]+10, 0, 0), self.numberFont, self.numbersColor)
				n = n + 1
				
		if self.drawCurve:
			curvePath = ui.Path()
			curvePath.line_width = 4.0
			curveDotsPath = ui.Path()
			primesCounter = 0
			# first point (n=0) requires a move_to:
			f_n = self.curveParamC  # a*0*0 + b*0 + c
			if (f_n in self.listOfPrimes):
				primesCounter = primesCounter + 1
			(x, y) = coordsForNumber(f_n)
			dotx = self.cx + (x * self.spacing * 2*math.pi)
			doty = self.cy + (y * self.spacing * 2*math.pi)
			curvePath.move_to(dotx, doty)
			t = 1
			max_t = self.turns * self.turns
			while (f_n < max_t):
				f_n = self.curveParamA*t*t + self.curveParamB*t + self.curveParamC
				if f_n < max_t:
					if (f_n in self.listOfPrimes):
						primesCounter = primesCounter + 1
					(x, y) = coordsForNumber(f_n)
					dotx = self.cx + (x * self.spacing * 2*math.pi)
					doty = self.cy + (y * self.spacing * 2*math.pi)
					ui.set_color(self.curveColor)
					curvePath.line_to(dotx, doty)
					#curvePath.stroke()
					#curveDotsPath = ui.Path()
					#ui.set_color(self.curveDotsColor)
					#curveDotsPath.add_arc(dotx, doty, self.dotSize+1, 0, 2*math.pi)
					#curveDotsPath.fill()
					t = t + 1.0
			curvePath.stroke()
			# number of dots under curve
			# number of primes under curve
			ui.draw_string("Number of dots   under curve: {:.0f}".format(t), (10, 10, 0, 0), ('Menlo-Regular', 10), self.dotsColor)
			ui.draw_string("Number of primes under curve: {:.0f}".format(primesCounter) + " ({:.1f}%)".format(primesCounter*100/t), (10, 24, 0, 0), ('Menlo-Regular', 10), self.primeDotColor)
			#self.superview['labelLongestPrimeStreak'].text = "{:.0f}".format(primesCounter)
	
	def layout(self):
		# This will be called when a view is resized. You should typically set the
		# frames of the view's subviews here, if your layout requirements cannot
		# be fulfilled with the standard auto-resizing (flex) attribute.
		device = machine()
		if self.width > self.height:
			self.scrOrientation = 'landscape'
			if device == 'iPad6,7':    # iPad Pro 12.9"
				self.maxSpacing = 72.0
			elif (device == 'iPad6,4') or (device == 'iPad5,4'):  # iPad Pro 9.7" oder iPad Air 2 9.7"
				self.maxSpacing = 51.0
			elif device == 'iPad5,1':  # iPad mini 4 7.9"
				self.maxSpacing = 51.0
		else:
			self.scrOrientation = 'portrait'
			if device == 'iPad6,7':    # iPad Pro 12.9"
				self.maxSpacing = 72.0
			elif (device == 'iPad6,4') or (device == 'iPad5,4'):  # iPad Pro 9.7" oder iPad Air 2 9.7"
				self.maxSpacing = 30.0
			elif device == 'iPad5,1':  # iPad mini 4 7.9"
				self.maxSpacing = 51.0
		self.spacing = (1.0/self.turns) * self.maxSpacing
		self.set_needs_display()

	def touch_began(self, touch):
		# Called when a touch begins.
		pass
	
	def touch_moved(self, touch):
		# Called when a touch moves.
		pass
	
	def touch_ended(self, touch):
		# Called when a touch ends.
		pass
	
	def keyboard_frame_will_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass
	
	def keyboard_frame_did_change(self, frame):
		# Called when the on-screen keyboard appears/disappears
		# Note: The frame is in screen coordinates.
		pass
# end of Class NumberSpiralView

#--- TextField delegate
class CurveParamTextFieldDelegate (object):
	def textfield_should_begin_editing(self, textfield):
		return True
		
	def textfield_did_begin_editing(self, textfield):
		pass
		
	def textfield_did_end_editing(self, textfield):
		sv = textfield.superview
		spiralView = sv['spiralView']
		if textfield.name == 'textfieldA':
			val = int(textfield.text)
			sv['sliderA'].value = val/spiralView.maxA
			spiralView.curveParamA = val
			spiralView.set_needs_display()
		elif textfield.name == 'textfieldB':
			val = int(textfield.text)
			sv['sliderB'].value = val/spiralView.maxB
			spiralView.curveParamB = val
			spiralView.set_needs_display()
		elif textfield.name == 'textfieldC':
			val = int(textfield.text)
			sv['sliderC'].value = val/spiralView.maxC
			spiralView.curveParamC = val
			spiralView.set_needs_display()
												
	def textfield_should_return(self, textfield):
		textfield.end_editing()
		return True
		
	def textfield_should_change(self, textfield, range, replacement):
		return True
		
	def textfield_did_change(self, textfield):
		pass

#--- Utilities ----------------------------------------------

def coordsForNumber(n):
	r = theta = math.sqrt(n)
	x = r * math.cos(2*math.pi*theta)
	y = -r * math.sin(2*math.pi*theta)
	return (x, y)

#--- Slider change ---------------------------------------

def sliderAchanged(sender):
	spiralView = v['spiralView']
	spiralView.curveParamA = int(sender.value * spiralView.maxA)
	v['textfieldA'].text = "{:.0f}".format(spiralView.curveParamA)
	spiralView.set_needs_display()	
	
def sliderBchanged(sender):
	spiralView = v['spiralView']
	spiralView.curveParamB = int(sender.value * spiralView.maxB)
	v['textfieldB'].text = "{:.0f}".format(spiralView.curveParamB)
	spiralView.set_needs_display()	
	
def sliderCchanged(sender):
	spiralView = v['spiralView']
	spiralView.curveParamC = int(sender.value * spiralView.maxC)
	v['textfieldC'].text = "{:.0f}".format(spiralView.curveParamC)
	spiralView.set_needs_display()	
		
def sliderSpacingChanged(sender):
	spiralView = v['spiralView']
	spiralView.spacing = sender.value * spiralView.maxSpacing
	v['labelSpacing'].text = "{:.1f}".format(spiralView.spacing)
	spiralView.set_needs_display()
	
def sliderTurnsChanged(sender):
	spiralView = v['spiralView']
	spiralView.turns = int(sender.value * spiralView.maxTurns)
	if spiralView.turns == 0:
		spiralView.turns = 1
	v['labelTurns'].text = "{:.0f}".format(spiralView.turns)
	if v['switchAutoSpacing'].value:
		spiralView.spacing = (1.0/spiralView.turns) * spiralView.maxSpacing
		v['labelSpacing'].text = "{:.1f}".format(spiralView.spacing)
	spiralView.set_needs_display()
	
# Settings dialog sliders

def sliderSettingsDotSizeChanged(sender):
	spiralView = v['spiralView']
	spiralView.dotSize = int(sender.value * 9.0 + 1.0)
	sender.superview['labelDotSize'].text = "{:.0f}".format(spiralView.dotSize)
	spiralView.set_needs_display()

def sliderSettingsFontSizeChanged(sender):
	spiralView = v['spiralView']
	spiralView.numberFont = ('HelveticaNeue-Light', sender.value * 23.0 + 8.0)
	# Achtung! offset auch anpassen, proportional ... wie?
	sender.superview['labelFontSize'].text = "{:.0f}".format(spiralView.numberFont[1])
	spiralView.set_needs_display()
	
#--- Switch change --------------------------------------

def switchAutoSpacingChanged(sender):
	v['sliderSpacing'].hidden = sender.value
	spiralView = v['spiralView']
	if sender.value:
		spiralView.spacing = (1.0/spiralView.turns) * spiralView.maxSpacing
	else:
		v['sliderSpacing'].value = spiralView.spacing/spiralView.maxSpacing
	v['labelSpacing'].text = "{:.1f}".format(spiralView.spacing)
	spiralView.set_needs_display()	

def switchDrawAxisChanged(sender):
	spiralView = v['spiralView']
	spiralView.drawAxis = sender.value
	spiralView.set_needs_display()

def switchDrawDotsChanged(sender):
	spiralView = v['spiralView']
	spiralView.drawDots = sender.value
	v['labelDrawNumbers'].hidden = not sender.value
	v['switchDrawNumbers'].hidden = not sender.value
	v['labelHilitePrimes'].hidden = not sender.value
	v['switchHilitePrimes'].hidden = not sender.value
	if sender.value:  # es wurde EINgeschaltet
		# wenn HilitePrimes aus ist, darf PrimesOnly nicht sichtbar gemacht werden
		if spiralView.hilitePrimes:
			v['labelPrimesOnly'].hidden = not sender.value   # False
			v['switchPrimesOnly'].hidden = not sender.value  # False
	else:  # es wurde AUSgeschaltet
		# dann muss PrimesOnly immer auch ausgeblendet werden
		v['labelPrimesOnly'].hidden = not sender.value   # False
		v['switchPrimesOnly'].hidden = not sender.value  # False		
			
	spiralView.set_needs_display()

def switchDrawNumbersChanged(sender):
	spiralView = v['spiralView']
	spiralView.drawNumbers = sender.value
	spiralView.set_needs_display()

def switchHilitePrimesChanged(sender):
	spiralView = v['spiralView']
	spiralView.hilitePrimes = sender.value
	v['labelPrimesOnly'].hidden = not sender.value
	v['switchPrimesOnly'].hidden = not sender.value
	if not spiralView.hilitePrimes:
		spiralView.primesOnly = False
		v['switchPrimesOnly'].value = False
	spiralView.set_needs_display()

def switchDrawSpiralChanged(sender):
	spiralView = v['spiralView']
	spiralView.drawSpiral = sender.value
	spiralView.set_needs_display()
	
def switchPrimesOnlyChanged(sender):
	spiralView = v['spiralView']
	spiralView.primesOnly = sender.value
	spiralView.set_needs_display()

def switchDrawCurveChanged(sender):
	spiralView = v['spiralView']
	spiralView.drawCurve = sender.value
	toggleCurveGUI(not spiralView.drawCurve)
	spiralView.set_needs_display()

#--- Buttons ----------------------------------------------
		
def buttonMetawopsTapped(sender):
	webbrowser.open("safari-http://twitter.com/metawops")
	
# Show the settings dialog
def settingsButtonTapped(sender):
	settingsView = ui.load_view('NumberSpiralsSettings.pyui')
	spiralView = v['spiralView']
	settingsView['sliderDotSize'].value = (spiralView.dotSize-1.0)/9.0
	settingsView['labelDotSize'].text = "{:.0f}".format(spiralView.dotSize)
	settingsView['sliderFontSize'].value = (spiralView.numberFont[1]-8.0)/23.0
	settingsView['labelFontSize'].text = "{:.0f}".format(spiralView.numberFont[1])
	settingsView.present('sheet')

# tapping the save icon saves the view's content as a PNG file to the current dir
def saveButtonTapped(sender):
	view = v['spiralView']
	img = snapshot(view)
	ui_image_to_file(img, 'NumberSpiralScreenshot.png')
	add_to_album('NumberSpiralScreenshot.png', 'Number Spirals')
	if (console.alert('Image saved', 'The image was saved to the Photos album "Number Spirals".', 'Photos')) == 1:
		# lauch Photos, go to album "Number Spirals" and show the saved (last) photo
		webbrowser.open('photos-redirect://')
	return


def snapshot(obj):
	with ui.ImageContext(obj.width, obj.height) as ctx:
		obj.draw_snapshot()
		return ctx.get_image()

def ui_image_to_file(img, filename):
	# write ui-Image, img to file "filename"
	if not type(img) is ui.Image:
		print('expected {} but received {}. File not written.'.format(ui.Image, type(img)))
		return False
	bytes = img.to_png()
	with open(filename, 'wb') as file:
		file.write(bytes)

def add_to_album(image_path, album_name):
	# KUDOS to Ole Zorn here!
	# Source: https://forum.omz-software.com/topic/3889/adding-an-image-to-my-own-album-in-photos-how/2
	# Find the album or create it:
	try:
		album = [a for a in photos.get_albums() if a.title == album_name][0]
	except IndexError:
		album = photos.create_album(album_name)
	# Add the file as an asset to the library:
	asset = photos.create_image_asset(image_path)
	# Workaround a possible timestamp bug:
	asset.creation_date = datetime.datetime.now()
	# Add the asset to the album:
	album.add_assets([asset])

#--- GUI helpers

def toggleCurveGUI(hideBool):
	v['labelA'].hidden = hideBool
	v['labelB'].hidden = hideBool
	v['labelC'].hidden = hideBool
	v['sliderA'].hidden = hideBool
	v['sliderB'].hidden = hideBool
	v['sliderC'].hidden = hideBool
	v['textfieldA'].hidden = hideBool
	v['textfieldB'].hidden = hideBool
	v['textfieldC'].hidden = hideBool
	

#--- MAIN

if (machine()[:3] == 'iPa'):
	v = ui.load_view('NumberSpirals.pyui')
	spiralView = v['spiralView']
	v['sliderSpacing'].value = (spiralView.spacing)/spiralView.maxSpacing
	v['labelSpacing'].text = "{:.1f}".format(spiralView.spacing)
	v['sliderTurns'].value = (spiralView.turns)/spiralView.maxTurns
	v['labelTurns'].text = "{:.0f}".format(spiralView.turns)
	v['switchAutoSpacing'].value = spiralView.autoSpacing
	v['sliderSpacing'].hidden = spiralView.autoSpacing
	v['switchDrawAxis'].value = spiralView.drawAxis
	v['switchDrawDots'].value = spiralView.drawDots
	v['switchDrawNumbers'].value = spiralView.drawNumbers
	v['switchHilitePrimes'].value = spiralView.hilitePrimes
	v['switchDrawSpiral'].value = spiralView.drawSpiral
	v['switchPrimesOnly'].value = spiralView.primesOnly
	if (not spiralView.primesOnly):
		v['labelPrimesOnly'].hidden = True
		v['switchPrimesOnly'].hidden = True
	v['switchDrawCurve'].value = spiralView.drawCurve
	if (not spiralView.drawCurve):
		toggleCurveGUI(True)
	
	v['textfieldA'].delegate = CurveParamTextFieldDelegate()
	v['textfieldB'].delegate = CurveParamTextFieldDelegate()
	v['textfieldC'].delegate = CurveParamTextFieldDelegate()

	v['sliderA'].value = spiralView.curveParamA / spiralView.maxA
	v['textfieldA'].text = "{:.0f}".format(spiralView.curveParamA)
	v['sliderB'].value = spiralView.curveParamB / spiralView.maxB
	v['textfieldB'].text = "{:.0f}".format(spiralView.curveParamB)
	v['sliderC'].value = spiralView.curveParamC / spiralView.maxC
	v['textfieldC'].text = "{:.0f}".format(spiralView.curveParamC)
			
	v.present('full_screen')
else:
	print('Sorry, Number Spiral Explorer is iPad-only.')
