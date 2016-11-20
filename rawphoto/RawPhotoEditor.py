# https://github.com/philiplessner/PhotoEditor

import photos
import ui
import console
from objc_util import *
from toolz import assoc_in, get_in, merge


class RawPhotoEditor(ui.View):
	def __init__(self):
		self.frame = (0, 0, 1280, 1024)
		self.name = ' RAW Photo Editor'
		self.background_color = (0.2, 0.2, 0.2, 1.0)
		button_tint_color = (0.0, 0.5, 0.75, 1.0)
		self.left_button_items = [ui.ButtonItem(title='  Open     ',
		tint_color= button_tint_color,
		action=self.open_image),
		ui.ButtonItem(title='Save     ',
		tint_color=button_tint_color,
		action=self.save_image),
		ui.ButtonItem(title='Exit',
		tint_color=button_tint_color,
		action=self.exit_photoeditor)]
		
		self._CIVector = ObjCClass('CIVector')
		
		# Views for displaying Image
		self.sv = ui.ScrollView(frame=(10, 20, 640, 427))
		self.sv.content_size = (1500, 1000)
		self.ci_view = DisplayCIImage(frame=(0, 0, 1500, 1000))
		self.sv.add_subview(self.ci_view)
		# View for displaing histogram
		self.histogram_view = DisplayHistogram(frame=(200, 525, 300, 150))
		self.histogram_view.border_width = 1
		self.histogram_view.border_color = 'black'
		
		
		# Views for displaying filters
		self.filters_sv = ui.ScrollView(frame=(700, 25, 350, 660))
		self.filters_sv.content_size = (350, 3000)
		self.filters_sv.paging_enabled = True
		self.add_subview(self.filters_sv)
		self.display_rawfilters()
		self.display_adjustfilters()
		# Label it
		filters_label = ui.Label(text='Filters',
		frame=(800, 0, 75, 25),
		text_color='white',
		font =('<system-bold>', 18))
		self.add_subview(filters_label)
		
		enlarge_button = ui.Button(frame=(100, 450, 100, 25),
		title='Enlarge',
		font=('<system-bold>', 18),
		tint_color=button_tint_color,
		action=self.enlarge_image)
		shrink_button = ui.Button(frame=(225, 450, 100, 25),
		title='Shrink',
		font=('<system-bold>', 18),
		tint_color=button_tint_color,
		action=self.shrink_image)
		fit_button = ui.Button(frame=(350, 450, 100, 25),
		title='Fit',
		font=('<system-bold>', 18),
		tint_color=button_tint_color,
		action=self.fit_image)
		original_button = ui.Button(frame=(475, 450, 100, 25),
		title='Original Size',
		font=('<system-bold>', 18),
		tint_color=button_tint_color,
		action=self.original_image)
		
		self.add_subview(self.sv)
		self.add_subview(self.histogram_view)
		self.add_subview(enlarge_button)
		self.add_subview(shrink_button)
		self.add_subview(fit_button)
		self.add_subview(original_button)
		
		self.present('fullscreen', title_bar_color=(0.2, 0.2, 0.2, 1.0), orientations=['landscape'], title_color='white')
		
	def display_rawfilters(self):
		SLIDER_X = 10
		TOP_SLIDER_Y = 15
		SLIDER_Y_SPACING = 60
		SLIDER_WIDTH = 275
		SLIDER_HEIGHT = 55
		
		self._CIHighlightShadowAdjust_raw = ObjCClass('CIFilter').filterWithName_('CIHighlightShadowAdjust')
		self.rawfilter_view = FiltersView(name='RAW', frame=(0, 0, 300, 650), background_color=(0.75, 0.75, 0.75, 1.0))
		self.filters_sv.add_subview(self.rawfilter_view)
		
		temperature_view = SliderWithValueLabel('Temperature', {'m': 5000.0, 'b': 3000.0}, self.raw_temperature, '{:.0f}', frame=(SLIDER_X, TOP_SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(temperature_view)
		tint_view = SliderWithValueLabel('Tint', {'m': 300.0, 'b': -150.0}, self.raw_tint, '{:.0f}', frame=(SLIDER_X, TOP_SLIDER_Y + SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(tint_view)
		ev_view = SliderWithValueLabel('Exposure', {'m': 6.0, 'b': -3.0}, self.raw_ev, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 2 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(ev_view)
		highlight_view = SliderWithValueLabel('Highlights', {'m': 1.0, 'b': 0.0}, self.raw_highlight, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 3 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(highlight_view)
		shadow_view = SliderWithValueLabel('Shadows', {'m': 2.0, 'b': -1.0}, self.raw_shadow, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 4 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(shadow_view)
		colornoise_view = SliderWithValueLabel('Color Noise', {'m': 1.0, 'b': 0.0}, self.raw_colornoise, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 5 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(colornoise_view)
		luminancenoise_view = SliderWithValueLabel('Luminance Noise', {'m': 1.0, 'b': 0.0}, self.raw_luminancenoise, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 6 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.rawfilter_view.add_subview(luminancenoise_view)
		
	def display_adjustfilters(self):
		SLIDER_X = 10
		TOP_SLIDER_Y = 15
		SLIDER_Y_SPACING = 60
		SLIDER_WIDTH = 275
		SLIDER_HEIGHT = 55
		
		# Set up filters
		CIFilter = ObjCClass('CIFilter')
		self.CIHighlightShadowAdjust = CIFilter.filterWithName_('CIHighlightShadowAdjust')
		self.CIColorControls = CIFilter.filterWithName_('CIColorControls')
		self.CIExposureAdjust = CIFilter.filterWithName_('CIExposureAdjust')
		self.CIVibrance = CIFilter.filterWithName_('CIVibrance')
		self.CIToneCurve = CIFilter.filterWithName_('CIToneCurve')
		
		self.adjustfilters_view = FiltersView(name='Adjustments',
		frame=(0, 700, 300, 650),
		background_color=(0.75, 0.75, 0.75, 1.0))
		self.filters_sv.add_subview(self.adjustfilters_view)
		
		exposure_view = SliderWithValueLabel('Exposure', {'m': 12.0, 'b': -6.0}, self.adjust_exposure, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(exposure_view)
		brightness_view = SliderWithValueLabel('Brightness', {'m': 1.0, 'b': -0.5}, self.adjust_brightness, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(brightness_view)
		contrast_view = SliderWithValueLabel('Contrast', {'m': 1.5, 'b': 0.0}, self.adjust_contrast, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 2 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(contrast_view)
		highlight_view = SliderWithValueLabel('Highlights', {'m': 1.0, 'b': 0.0}, self.adjust_highlights, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 3 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(highlight_view)
		shadow_view = SliderWithValueLabel('Shadows', {'m': 2.0, 'b': -1.0}, self.adjust_shadows, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 4 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(shadow_view)
		saturation_view = SliderWithValueLabel('Saturation', {'m': 2.0, 'b': 0.0}, self.adjust_saturation, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 5 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(saturation_view)
		vibrance_view = SliderWithValueLabel('Vibrance', {'m': 2.0, 'b': -1.0}, self.adjust_vibrance, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 6 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(vibrance_view)
		self.adjustfilters_view.add_subview(saturation_view)
		midtonecontrast_view = SliderWithValueLabel('Midtone Contrast', {'m': 0.5, 'b': 0.0}, self.adjust_midtonecontrast, '{:.2f}', frame=(SLIDER_X, TOP_SLIDER_Y + 7 * SLIDER_Y_SPACING, SLIDER_WIDTH, SLIDER_HEIGHT))
		self.adjustfilters_view.add_subview(midtonecontrast_view)
		
	@ui.in_background
	def raw_ev(self, sender):
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputEV'], sender.value))
		self.update_image()
		
	@ui.in_background
	def raw_temperature(self, sender):
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputNeutralTemperature'], sender.value))
		self.update_image()
		
	@ui.in_background
	def raw_tint(self, sender):
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputNeutralTint'], sender.value))
		self.update_image()
		
	@ui.in_background
	def raw_highlight(self, sender):
		highlight = sender.value
		self._CIHighlightShadowAdjust_raw.setValue_forKey_(highlight, 'inputHighlightAmount')
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputLinearSpaceFilter'], self._CIHighlightShadowAdjust_raw))
		self.update_image()
		
	@ui.in_background
	def raw_shadow(self, sender):
		shadow = sender.value
		self._CIHighlightShadowAdjust_raw.setValue_forKey_(shadow, 'inputShadowAmount')
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputLinearSpaceFilter'], self._CIHighlightShadowAdjust_raw))
		self.update_image()
		
	@ui.in_background
	def raw_colornoise(self, sender):
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputColorNoiseReductionAmount'], sender.value))
		self.update_image()
		
	@ui.in_background
	def raw_luminancenoise(self, sender):
		self._state_history.append(assoc_in(self._state_history[-1], ['rawfilter', 'inputLuminanceNoiseReductionAmount'], sender.value))
		self.update_image()
		
	@ui.in_background
	def adjust_exposure(self, sender):
		self.CIExposureAdjust = self.CIExposureAdjust.copy()
		self.CIExposureAdjust.setValue_forKey_(sender.value, 'inputEV')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIExposureAdjust'], self.CIExposureAdjust))
		self.update_image()
		
	@ui.in_background
	def adjust_brightness(self, sender):
		self.CIColorControls = self.CIColorControls.copy()
		self.CIColorControls.setValue_forKey_(sender.value, 'inputBrightness')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIColorControls'], self.CIColorControls))
		self.update_image()
		
	@ui.in_background
	def adjust_contrast(self, sender):
		self.CIColorControls = self.CIColorControls.copy()
		self.CIColorControls.setValue_forKey_(sender.value, 'inputContrast')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIColorControls'], self.CIColorControls))
		self.update_image()
		
	@ui.in_background
	def adjust_highlights(self, sender):
		self.CIHighlightShadowAdjust = self.CIHighlightShadowAdjust.copy()
		self.CIHighlightShadowAdjust.setValue_forKey_(sender.value, 'inputHighlightAmount')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIHighlightShadowAdjust'], self.CIHighlightShadowAdjust))
		self.update_image()
		
	@ui.in_background
	def adjust_shadows(self, sender):
		self.CIHighlightShadowAdjust = self.CIHighlightShadowAdjust.copy()
		self.CIHighlightShadowAdjust.setValue_forKey_(sender.value, 'inputShadowAmount')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIHighlightShadowAdjust'], self.CIHighlightShadowAdjust))
		self.update_image()
		
	@ui.in_background
	def adjust_saturation(self, sender):
		self.CIColorControls = self.CIColorControls.copy()
		self.CIColorControls.setValue_forKey_(sender.value, 'inputSaturation')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIColorControls'], self.CIColorControls))
		self.update_image()
		
	@ui.in_background
	def adjust_vibrance(self, sender):
		self.CIVibrance = self.CIVibrance.copy()
		self.CIVibrance.setValue_forKey_(sender.value, 'inputAmount')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIVibrance'], self.CIVibrance))
		self.update_image()
		
	@ui.in_background
	def adjust_midtonecontrast(self, sender):
		self.CIToneCurve = self.CIToneCurve.copy()
		self.CIToneCurve.setValue_forKey_(self._CIVector.vectorWithX_Y_(0.25, 0.25 * (1.0 - sender.value)), 'inputPoint1')
		self.CIToneCurve.setValue_forKey_(self._CIVector.vectorWithX_Y_(0.75, 0.75 * (1.0 + sender.value)), 'inputPoint3')
		self._state_history.append(assoc_in(self._state_history[-1], ['CIToneCurve'], self.CIToneCurve))
		self.update_image()
		
	def open_image(self, sender):
		rawdata, uti = pickphoto2data()
		if rawdata is None:
			return
		self._rawfilter = init_rawfilter(rawdata, uti)
		if self._rawfilter.valueForKey_('inputBoostShadowAmount') is None:
			self.error_alert('File Error', 'Not a RAW File or Unsupported RAW Type')
			return
			
		rawfilter = {'rawfilter': {'inputEV': self._rawfilter.valueForKey_('inputEV'), 'inputBoostShadowAmount': self._rawfilter.valueForKey_('inputBoostShadowAmount'), 'inputNeutralTemperature': self._rawfilter.valueForKey_('inputNeutralTemperature'), 'inputNeutralTint': self._rawfilter.valueForKey_('inputNeutralTint'),
		'inputColorNoiseReductionAmount': self._rawfilter.valueForKey_('inputColorNoiseReductionAmount'), 'inputLuminanceNoiseReductionAmount': self._rawfilter.valueForKey_('inputLuminanceNoiseReductionAmount'), 'inputLinearSpaceFilter': self._CIHighlightShadowAdjust_raw}}
		
		self._CIHighlightShadowAdjust_raw.setDefaults()
		self.CIHighlightShadowAdjust.setDefaults()
		self.CIColorControls.setDefaults()
		self.CIExposureAdjust.setDefaults()
		self.CIVibrance.setDefaults()
		self.CIToneCurve.setDefaults()
		adjustfilters = {
		'CIHighlightShadowAdjust': self.CIHighlightShadowAdjust, 'CIColorControls': self.CIColorControls,
		'CIExposureAdjust': self.CIExposureAdjust,
		'CIVibrance': self.CIVibrance,
		'CIToneCurve': self.CIToneCurve
		}
		
		self._initial_state = merge(rawfilter, adjustfilters)
		self._state_history = [self._initial_state]
		
		# Initialize sliders and slider value labels
		self.rawfilter_view['Temperature'].initialize(get_in(['rawfilter', 'inputNeutralTemperature'], self._initial_state).floatValue())
		self.rawfilter_view['Tint'].initialize(get_in(['rawfilter', 'inputNeutralTint'], self._initial_state).floatValue())
		self.rawfilter_view['Exposure'].initialize(get_in(['rawfilter', 'inputEV'], self._initial_state).floatValue())
		self.rawfilter_view['Color Noise'].initialize(get_in(['rawfilter', 'inputColorNoiseReductionAmount'], self._initial_state).floatValue())
		self.rawfilter_view['Luminance Noise'].initialize(get_in(['rawfilter', 'inputLuminanceNoiseReductionAmount'], self._initial_state).floatValue())
		self.rawfilter_view['Highlights'].initialize(1.0)
		self.rawfilter_view['Shadows'].initialize(0.0)
		
		self.adjustfilters_view['Exposure'].initialize(get_in(['CIExposureAdjust'], self._initial_state).valueForKey_('inputEV').floatValue())
		self.adjustfilters_view['Brightness'].initialize(get_in(['CIColorControls'], self._initial_state).valueForKey_('inputBrightness').floatValue())
		self.adjustfilters_view['Contrast'].initialize(get_in(['CIColorControls'], self._initial_state).valueForKey_('inputContrast').floatValue())
		self.adjustfilters_view['Highlights'].initialize(get_in(['CIHighlightShadowAdjust'], self._initial_state).valueForKey_('inputHighlightAmount').floatValue())
		self.adjustfilters_view['Shadows'].initialize(get_in(['CIHighlightShadowAdjust'], self._initial_state).valueForKey_('inputShadowAmount').floatValue())
		self.adjustfilters_view['Saturation'].initialize(get_in(['CIColorControls'], self._initial_state).valueForKey_('inputSaturation').floatValue())
		self.adjustfilters_view['Vibrance'].initialize(get_in(['CIVibrance'], self._initial_state).valueForKey_('inputAmount').floatValue())
		self.adjustfilters_view['Midtone Contrast'].initialize(0.0)
		
		
		ci_img = self._rawfilter.valueForKey_('outputImage')
		self.ci_view.ci_img = ci_img
		self.ci_view.width = self.ci_view.ci_img.extent().size.width
		self.ci_view.height = self.ci_view.ci_img.extent().size.height
		self.ci_view.x = 0.0
		self.ci_view.y = 0.0
		self.sv.content_size = (self.ci_view.ci_img.extent().size.width, self.ci_view.ci_img.extent().size.height)
		self.ci_view.rect = CGRect((0.0, 0.0), (640, 427))
		self.ci_view.set_needs_display()
		
		self.histogram_view.ci_img = ci_img
		self.histogram_view.set_needs_display()
		
	def update_image(self):
		self._rawfilter = update_rawfilter(self._rawfilter, self._state_history[-1]['rawfilter'])
		ci_img = self._rawfilter.valueForKey_('outputImage')
		for k, v in self._state_history[-1].items():
			if k != 'rawfilter':
				v.setValue_forKey_(ci_img, 'inputImage')
				ci_img = v.valueForKey_('outputImage')
		self.ci_view.ci_img = ci_img
		self.ci_view.set_needs_display()
		#self.histogram_view.ci_img = self.ci_view.ci_img
		#self.histogram_view.set_needs_display()
		
	def save_image(self, sender):
		c.UIImageWriteToSavedPhotosAlbum.argtypes =[c_void_p, c_void_p, c_void_p, c_void_p]
		c.UIImageWriteToSavedPhotosAlbum.restype = None
		c.UIImageWriteToSavedPhotosAlbum(self.ci_view.ui_img, None, None, None)
		
	def exit_photoeditor(self, sender):
		self.close()
		
	def enlarge_image(self, sender):
		new_width = self.ci_view.rect.size.width * 1.5
		new_height = self.ci_view.rect.size.height * 1.5
		if (new_width <= self.ci_view.ci_img.extent().size.width) and (new_height <= self.ci_view.ci_img.extent().size.height):
			self.ci_view.rect = CGRect((0.0, 0.0), (new_width, new_height))
			self.ci_view.set_needs_display()
			
	def shrink_image(self, sender):
		new_width = self.ci_view.rect.size.width / 1.5
		new_height = self.ci_view.rect.size.height / 1.5
		self.ci_view.rect = CGRect((0.0, 0.0), (new_width, new_height))
		self.ci_view.set_needs_display()
		
	def fit_image(self, sender):
		self.ci_view.rect = CGRect((0.0, 0.0), (640, 427))
		self.sv.content_offset = (0, 0)
		self.ci_view.set_needs_display()
		
	def original_image(self, sender):
		self.ci_view.rect = CGRect((0.0, 0.0), (self.ci_view.ci_img.extent().size.width, self.ci_view.ci_img.extent().size.height))
		self.ci_view.set_needs_display()
		
	@ui.in_background
	def error_alert(self, title, msg):
		val = console.alert(title, msg, 'OK', hide_cancel_button=True)
		return val
		
		
class DisplayCIImage(ui.View):
	'''
	Display a CIImage as a UIImage
	class has two properties that need to be set each time a UIImage is drawn
	ci_img: the CIImage to display (initially set to photosplash.png)
	rect: a CGRect that is the size of the UIImage to display (initially
	set to ((0.0, 0.0), (640, 427)) )
	In addition, when a new image is loaded, frame.height and frame.width should be set to the original size of the image
	'''
	def __init__(self, *args, **kwargs):
		'''
		Set a (reusable) drawing context and provide default values for the image and image size
		'''
		super().__init__(*args, **kwargs)
		CIContext = ObjCClass('CIContext')
		self._ctx = CIContext.contextWithOptions_(None)
		ci_img = ObjCClass('CIImage').imageWithContentsOfURL_(nsurl('photosplash.png'))
		self.rect = CGRect((0.0, 0.0), (640, 427))
		self.ci_img = ci_img
		
	def draw(self):
		'''
		Redraw the UIImage by calling the method set_needs_display on the
		instance of the class
		'''
		cg_img = self._ctx.createCGImage_fromRect_(self.ci_img,
		self.ci_img.extent())
		self.ui_img = UIImage.imageWithCGImage_scale_orientation_(cg_img, 1.0, 0)
		c.CGImageRelease.argtypes = [c_void_p]
		c.CGImageRelease.restype = None
		c.CGImageRelease(cg_img)
		self.ui_img.drawInRect_(self.rect)
		
		
class DisplayHistogram(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		CIContext = ObjCClass('CIContext')
		self._ctx = CIContext.contextWithOptions_(None)
		#self.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
		self.CIVector = ObjCClass('CIVector')
		CIFilter = ObjCClass('CIFilter')
		self.CIAreaHistogram = CIFilter.filterWithName_('CIAreaHistogram')
		self.CIHistogramDisplayFilter = CIFilter.filterWithName_('CIHistogramDisplayFilter')
		ci_img = ObjCClass('CIImage').imageWithContentsOfURL_(nsurl('20160730_152103.jpg'))
		self.ci_img = ci_img
		
	def draw(self):
		c.CGAffineTransformMakeScale.argtypes = [c_double, c_double]
		c.CGAffineTransformMakeScale.restype = CGAffineTransform
		transform = c.CGAffineTransformMakeScale(c_double(0.1), c_double(0.1))
		self.scaled_img = self.ci_img.imageByApplyingTransform_(transform)
		self.CIAreaHistogram.setDefaults()
#        self.CIAreaHistogram.setValue_forKey_(self.ci_img, 'inputImage')
		self.CIAreaHistogram.setValue_forKey_(self.scaled_img, 'inputImage')
		self.CIAreaHistogram.setValue_forKey_(256, 'inputCount')
		vec = self.CIVector.vectorWithCGRect_(self.scaled_img.extent())
		self.CIAreaHistogram.setValue_forKey_(vec, 'inputExtent')
		self.CIAreaHistogram.setValue_forKey_(25.0, 'inputScale')
		self.area_img = self.CIAreaHistogram.valueForKey_('outputImage')
		self.CIHistogramDisplayFilter.setDefaults()
		self.CIHistogramDisplayFilter.setValue_forKey_(100.0, 'inputHeight')
		self.CIHistogramDisplayFilter.setValue_forKey_(1.0, 'inputHighLimit')
		self.CIHistogramDisplayFilter.setValue_forKey_(self.area_img, 'inputImage')
		self.disp_img = self.CIHistogramDisplayFilter.valueForKey_('outputImage')
		cg_img = self._ctx.createCGImage_fromRect_(self.disp_img,
		self.disp_img.extent())
		self.ui_img = UIImage.imageWithCGImage_scale_orientation_(cg_img, 1.0, 0)
		c.CGImageRelease.argtypes = [c_void_p]
		c.CGImageRelease.restype = None
		c.CGImageRelease(cg_img)
		self.ui_img.drawInRect_(CGRect((0.0, 0.0), (256, 100)))
		
		
class FiltersView(ui.View):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.name is not None:
			title_label = ui.Label(text=self.name,
			frame=(150, 0, 100, 25))
			self.add_subview(title_label)
			
			
class SliderWithValueLabel(ui.View):
	def __init__(self, slider_name, convert, action, valuefmt, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._m = convert['m']
		self._b = convert['b']
		self._valuefmt = valuefmt
		self.changed = action
		self.name = slider_name
		SLIDER_WIDTH = 200
		SLIDER_HEIGHT = 30
		SLIDER_TITLE_OFFSET = 20
		SLIDER_TITLE_WIDTH = 200
		SLIDER_TITLE_HEIGHT = 25
		SLIDER_VALUE_OFFSET = 10
		SLIDER_VALUE_HEIGHT = 25
		SLIDER_VALUE_WIDTH = 50
		self.border_width = 0
		self.border_color = 'black'
		self._slider = ui.Slider(frame=(0, SLIDER_TITLE_OFFSET, SLIDER_WIDTH, SLIDER_HEIGHT))
		self._slider.continuous = False
		self._slider.value = 0.5
		self._slider.action = self.update
		slider_title = ui.Label(frame=(0, 0, SLIDER_TITLE_WIDTH, SLIDER_TITLE_HEIGHT))
		slider_title.text = slider_name
		slider_title.text_color = 'black'
		self._slider_valuelabel = ui.Label(frame=(SLIDER_WIDTH + SLIDER_VALUE_OFFSET, SLIDER_TITLE_OFFSET, SLIDER_VALUE_WIDTH, SLIDER_VALUE_HEIGHT))
		self._slider_valuelabel.text = str(0.5)
		self._slider_valuelabel.border_width = 1
		self._slider_valuelabel.border_color = 'black'
		self._slider_valuelabel.alignment = ui.ALIGN_CENTER
		self.add_subview(self._slider)
		self.add_subview(slider_title)
		self.add_subview(self._slider_valuelabel)
		
	def initialize(self, value):
		self.value = value
		self._slider_valuelabel.text = self._valuefmt.format(self.value)
		self._slider.value = (value - self._b) / self._m
		
	def update(self, sender):
		self.value = self._m * sender.value + self._b
		self._slider_valuelabel.text = self._valuefmt.format(self.value)
		if self.changed and callable(self.changed):
			self.changed(self)
			
			
def pickphoto2data():
	all = photos.get_assets()
	asset = photos.pick_asset(all)
	if asset is not None:
		bobj = asset.get_image_data(original=True)
		rawdata = bobj.getvalue()
		return rawdata, bobj.uti
	return None, None
	
	
def load_ci_image(img_data):
	ci_img = ObjCClass('CIImage').imageWithData_(img_data)
	return ci_img
	
	
def raw2ci_img(imgdata, uti, d):
	CIFilter = ObjCClass('CIFilter')
	rawfilter = CIFilter.filterWithImageData_options_(ns(imgdata), {'kCGImageSourceTypeIdentifierHint': uti})
	rawfilter.setDefaults()
	for k, v in d.items():
		rawfilter.setValue_forKey_(v, k)
	ci_img = rawfilter.valueForKey_('outputImage')
	return ci_img
	
	
def init_rawfilter(imgdata, uti):
	CIFilter = ObjCClass('CIFilter')
	rawfilter = CIFilter.filterWithImageData_options_(ns(imgdata), {'kCGImageSourceTypeIdentifierHint': uti})
	rawfilter.setDefaults()
	return ObjCInstance(rawfilter)
	
	
def update_rawfilter(rawfilter, d):
	for k, v in d.items():
		rawfilter.setValue_forKey_(v, k)
	return rawfilter
	
	
def update_ciimg(ci_img, filter_state):
	filter = filter_state['filter']
	filter.setValue_forKey_(ci_img, 'inputImage')
	for k, v in filter_state.items():
		if k != 'filter':
			filter.setValue_forKey_(v, k)
	return filter.valueForKey_('outputImage')
	
	
if __name__ == '__main__':
	rpe = RawPhotoEditor()

