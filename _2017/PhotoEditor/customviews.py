import ui
from objc_util import *


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
        self.ui_img = CI2UIImage(self.ci_img, self._ctx)        
        self.ui_img.drawInRect_(self.rect)


class DisplayHistogram(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CIContext = ObjCClass('CIContext')
        self._ctx = CIContext.contextWithOptions_(None)
        CIFilter = ObjCClass('CIFilter')
        self._CIAreaHistogram = CIFilter.filterWithName_('CIAreaHistogram')
        self._CIHistogramDisplayFilter = CIFilter.filterWithName_('CIHistogramDisplayFilter')
        ci_img = ObjCClass('CIImage').imageWithContentsOfURL_(nsurl('20160730_152103.jpg'))
        self.ci_img = ci_img
        
    def draw(self):
        histogram_img = self.CIImage2CIHistogram()
        ui_img = CI2UIImage(histogram_img, self._ctx) 
        ui_img.drawInRect_(CGRect((0.0, 0.0), (256, 100)))
        
    def CIImage2CIHistogram(self):
        CIVector = ObjCClass('CIVector')
        c.CGAffineTransformMakeScale.argtypes = [c_double, c_double]
        c.CGAffineTransformMakeScale.restype = CGAffineTransform
        transform = c.CGAffineTransformMakeScale(c_double(0.1), c_double(0.1))
        scaled_img = self.ci_img.imageByApplyingTransform_(transform)
        self._CIAreaHistogram.setDefaults()
        self._CIAreaHistogram.setValue_forKey_(scaled_img, 'inputImage')
        self._CIAreaHistogram.setValue_forKey_(256, 'inputCount')
        vec = CIVector.vectorWithCGRect_(scaled_img.extent())
        self._CIAreaHistogram.setValue_forKey_(vec, 'inputExtent')
        self._CIAreaHistogram.setValue_forKey_(25.0, 'inputScale')
        area_img = self._CIAreaHistogram.valueForKey_('outputImage')
        self._CIHistogramDisplayFilter.setDefaults()
        self._CIHistogramDisplayFilter.setValue_forKey_(100.0, 'inputHeight')
        self._CIHistogramDisplayFilter.setValue_forKey_(1.0, 'inputHighLimit')
        self._CIHistogramDisplayFilter.setValue_forKey_(area_img, 'inputImage')
        histogram_img = self._CIHistogramDisplayFilter.valueForKey_('outputImage')
        return histogram_img
        

class FiltersView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.name is not None:
            title_label = ui.Label(text=self.name,
                                   frame=(10, 0, 275, 25),
                                   alignment=ui.ALIGN_CENTER,
                                   font =('<system-bold>', 18))
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
        SLIDER_TITLE_OFFSET = 25
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
            
class SaveDialog(ui.View):
    def __init__(self, initial_width, initial_height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initial_width = initial_width
        self._initial_height = initial_height
        self.frame = (10, 100, 275, 250)
        self.background_color = 'white'
        self.img_width = ui.TextField(frame=(10, 30, 100, 25),
                                      keyboard_type=ui.KEYBOARD_DECIMAL_PAD,
                                      text=str(initial_width),
                                      action=self.update_height)
        self.add_subview(self.img_width)
        width_label = ui.Label(frame=(10, 5, 150, 25), text='Image Width')
        self.add_subview(width_label)
        self.img_height = ui.TextField(frame=(150, 30, 100, 25),
                                       keyboard_type=ui.KEYBOARD_DECIMAL_PAD,
                                       text=str(initial_height),
                                       action=self.update_width)
        self.add_subview(self.img_height)
        height_label = ui.Label(frame=(150, 5, 150, 25), text='Image Height')
        self.add_subview(height_label)
        aspect_ratio = self._initial_width / self._initial_height
        self.aspect = ui.TextField(frame=(70, 100, 150, 25),
                                   text=str(aspect_ratio),
                                   keyboard_type=ui.KEYBOARD_DECIMAL_PAD,
                                   alignment=ui.ALIGN_CENTER,
                                   action=self.updatefrom_aspectratio)
        self.add_subview(self.aspect)
        aspect_label = ui.Label(frame=(70, 75, 150, 25), 
                                text='Aspect',
                                alignment=ui.ALIGN_CENTER)
        self.add_subview(aspect_label)
        self.save_button = ui.Button(frame=(175, 150, 50, 25), 
                                     title='Save',
                                     action=self.save)
        self.add_subview(self.save_button)
        self.cancel_button = ui.Button(frame=(30, 150, 50, 25), 
                                     title='Cancel',
                                     action=self.cancel)
        self.add_subview(self.cancel_button)

    def update_height(self, sender):
        self.img_height.text = '{:.0f}'.format(float(sender.text) /
                                   float(self.aspect.text))
    def update_width(self, sender):
        self.img_width.text = '{:.0f}'.format(float(sender.text) *
                                   float(self.aspect.text))
                                   
    def updatefrom_aspectratio(self, sender):
        self.img_height.text = '{:.0f}'.format(float(self.img_width.text) /
                                   float(sender.text))
                      
    def save(self, sender):
         self.scale = float(self.img_width.text) / self._initial_width
         self.aspect_ratio = float(self.aspect.text)
         self.close()
         
    def cancel(self, sender):
         pass
        
        


def CI2UIImage(ci_img, ctx):
    cg_img = ctx.createCGImage_fromRect_(ci_img, ci_img.extent())
    ui_img = UIImage.imageWithCGImage_scale_orientation_(cg_img, 1.0, 0)
    c.CGImageRelease.argtypes = [c_void_p]
    c.CGImageRelease.restype = None
    c.CGImageRelease(cg_img)
    return ui_img
