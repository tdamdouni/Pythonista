from __future__ import print_function
# https://gist.github.com/Cethric/83a4b2ccf25798d5e074

# coding: utf-8
import ui
from objc_util import *
import ctypes

AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureVideoDataOutput = ObjCClass('AVCaptureVideoDataOutput')
AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
AVCaptureStillImageOutput = ObjCClass('AVCaptureStillImageOutput')
AVCaptureConnection = ObjCClass('AVCaptureConnection')
UIImage = ObjCClass('UIImage')

kCGBitmapAlphaInfoMask = 0x1F
kCGBitmapFloatComponents = 1 << 8
kCGBitmapByteOrderMask = 0x7000
kCGBitmapByteOrderDefault = 0 << 12
kCGBitmapByteOrder16Little = 1 << 12
kCGBitmapByteOrder32Little = 2 << 12
kCGBitmapByteOrder16Big = 3 << 12
kCGBitmapByteOrder32Big = 4 << 12

kCGImageAlphaNone = 0
kCGImageAlphaPremultipliedLast = 1
kCGImageAlphaPremultipliedFirst = 2
kCGImageAlphaLast = 3
kCGImageAlphaFirst = 4
kCGImageAlphaNoneSkipLast = 5
kCGImageAlphaNoneSkipFirst = 6
kCGImageAlphaOnly = 7


class CMTime(ctypes.Structure):
    _fields_ = [
                ('CMTimeValue', ctypes.c_int64),
                ('CMTimeScale', ctypes.c_int32),
                ('CMTimeEpoch', ctypes.c_int64),
                ('CMTimeFlags', ctypes.c_uint32),
                ]
                
def CMTimeMake(value, scale):
    cm = CMTime()
    cm.CMTimeScale = scale
    cm.CMTimeValue = value
    return cm

def dispatch_queue_create(name, parent):
    func = c.dispatch_queue_create
    func.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(name, parent))
    
def dispatch_release(queue_obj):
    raise RuntimeError('This is not the method you are looking for')
    func = c.dispatch_release
    func.argtyps = [ctypes.c_void_p]
    func.restype = None
    return func(ObjCInstance(queue_obj).ptr)
    
def CMSampleBufferGetImageBuffer(buffer):
    func = c.CMSampleBufferGetImageBuffer
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(buffer))
    
def CVPixelBufferLockBaseAddress(imagebuffer, param_0):
    func = c.CVPixelBufferLockBaseAddress
    func.argtypes = [ctypes.c_void_p, ctypes.c_int]
    func.restype = None
    return func(ObjCInstance(imagebuffer).ptr, param_0)

def CVPixelBufferUnlockBaseAddress(imagebuffer, param_0):
    func = c.CVPixelBufferUnlockBaseAddress
    func.argtypes = [ctypes.c_void_p, ctypes.c_int]
    func.restype = None
    return func(ObjCInstance(imagebuffer).ptr, param_0)
    
def CVPixelBufferGetBaseAddress(imagebuffer):
    func = c.CVPixelBufferGetBaseAddress
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_void_p
    return func(ObjCInstance(imagebuffer).ptr)

def CVPixelBufferGetBytesPerRow(imagebuffer):
    func = c.CVPixelBufferGetBytesPerRow
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_int
    return func(ObjCInstance(imagebuffer).ptr)

def CVPixelBufferGetWidth(imagebuffer):
    func = c.CVPixelBufferGetWidth
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_int
    return func(ObjCInstance(imagebuffer).ptr)
    
def CVPixelBufferGetHeight(imagebuffer):
    func = c.CVPixelBufferGetHeight
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_int
    return func(ObjCInstance(imagebuffer).ptr)
    
def CGColorSpaceCreateDeviceRGB():
    func = c.CGColorSpaceCreateDeviceRGB
    func.argtypes = None
    func.restype = ctypes.c_void_p
    return ObjCInstance(func())
    
def CGBitmapContextCreate(baseAddress, width, height, param_0, bytesPerRow, colorSpace, flags):
    func = c.CGBitmapContextCreate
    func.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int32]
    func.restype = ctypes.c_void_p
    result = func(baseAddress, width, height, param_0, bytesPerRow, ObjCInstance(colorSpace).ptr, flags)
    if result is not None:
        return ObjCInstance(result)
    else:
        raise RuntimeError('Failed to create context')
        
def CGContextRelease(context):
    func = c.CGContextRelease
    func.argtypes = [ctypes.c_void_p]
    func.restype = None
    return func(ObjCInstance(context).ptr)
    
def CGColorSpaceRelease(colorSpace):
    func = c.CGColorSpaceRelease
    func.argtypes = [ctypes.c_void_p]
    func.restype = None
    return func(ObjCInstance(colorSpace))
        
def CGBitmapContextCreateImage(context):
    func = c.CGBitmapContextCreateImage
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(ObjCInstance(context).ptr))
    
def CGImageRelease(image):
    func = c.CGImageRelease
    func.argtypes = [ctypes.c_void_p]
    func.restype = None
    return func(ObjCInstance(image).ptr)
    
def UIImageFromSampleBuffer(buffer):
    imagebuffer =  CMSampleBufferGetImageBuffer(buffer)
    CVPixelBufferLockBaseAddress(imagebuffer, 0)
    baseAddress = CVPixelBufferGetBaseAddress(imagebuffer)
    width = CVPixelBufferGetWidth(imagebuffer)
    height = CVPixelBufferGetHeight(imagebuffer)
    colorSpace = CGColorSpaceCreateDeviceRGB()
    flags = kCGBitmapByteOrderDefault | kCGImageAlphaNoneSkipFirst
    context = CGBitmapContextCreate(baseAddress, width / 4, height / 4, 8, 4 * width, colorSpace, flags)
    quartzImage = CGBitmapContextCreateImage(context)
    CVPixelBufferUnlockBaseAddress(imagebuffer, 0)
    CGContextRelease(context)
    CGColorSpaceRelease(colorSpace)
    image = UIImage.imageWithCGImage_(quartzImage)
    CGImageRelease(quartzImage)
    return image
    
def UIImagePNGRepresentation(image):
    func = c.UIImagePNGRepresentation
    func.argtypes = [ctypes.c_void_p]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(ObjCInstance(image).ptr))
    
def UIImageJPEGRepresentation(image, scale=32):
    func = c.UIImageJPEGRepresentation
    func.argtypes = [ctypes.c_void_p, ctypes.c_float]
    func.restype = ctypes.c_void_p
    return ObjCInstance(func(ObjCInstance(image).ptr, scale))
    
    
view = None

@on_main_thread
def change_image(image):
    if view is not None:
        ObjCInstance(view['imageview1']).setImage_(ObjCInstance(image))
        # view['imageview1'].image = ui.Image.named('test.png')

def captureOutput_didOutputSampleBuffer_fromConnection_(_cmd, _self, _output, _buffer, _connection):
    buffer = ObjCInstance(_buffer)
    image = UIImageFromSampleBuffer(buffer)
    imageRep = UIImagePNGRepresentation(image)
    imageRep = UIImageJPEGRepresentation(image)
    imageRep.writeToFile_atomically_('test.png', True)
    imageRep.writeToFile_atomically_('test.jpg', True)
    change_image(image)

delegate_call = create_objc_class('delegate_call', protocols=['AVCaptureVideoDataOutputSampleBufferDelegate'], methods=[captureOutput_didOutputSampleBuffer_fromConnection_])
    
class CameraView(ui.View):
    @on_main_thread
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        
        self.inputDevice = AVCaptureDevice.devices()[0]
        self.captureInput = AVCaptureDeviceInput.deviceInputWithDevice_error_(self.inputDevice, None)

        if not self.captureInput:
            print('Failed to create device')
            exit()
    
        self.captureOutput = AVCaptureVideoDataOutput.alloc().init()
        self.captureSession = AVCaptureSession.alloc().init()
        self.captureSession.setSessionPreset_('AVCaptureSessionPresetHigh')
        
        if self.captureSession.canAddInput_(self.captureInput):
            self.captureSession.addInput_(self.captureInput)
    
        if self.captureSession.canAddOutput_(self.captureOutput):
            self.captureSession.addOutput_(self.captureOutput)
        
        print('setup')
        
        self.captureVideoPreviewLayer = AVCaptureVideoPreviewLayer.layerWithSession_(self.captureSession)
        
        queue_test = dispatch_queue_create('imageDispatch', None)
        
        print('callback')
        self.captureOutput.setMinFrameDuration_(CMTimeMake(1, 2), argtypes=[CMTime], restype=None)
        callback = delegate_call.alloc().init()
        self.captureOutput.setSampleBufferDelegate_queue_(callback, queue_test)
        
    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        self.set_layer()
    
    @on_main_thread
    def set_layer(self):
        v = ObjCInstance(self)
        self.captureVideoPreviewLayer.setFrame_(v.bounds())
        self.captureVideoPreviewLayer.setVideoGravity_('AVLayerVideoGravityResizeAspectFill')
        v.layer().addSublayer_(self.captureVideoPreviewLayer)
        
        self.captureSession.startRunning()
    
    @on_main_thread
    def will_close(self):
        self.captureSession.stopRunning()
        

class CustomView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.frame = (0,0, 800,600)
        
    def did_load(self):
        self['camera'].set_layer()
        self['imageview1'].image = ui.Image.named('test:Numbers')
        
    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        
    def will_close(self):
        self['camera'].will_close()
        

view = ui.load_view('ImageView')
view.present()