from objc_util import *
import ctypes

AVAudioUnit=ObjCClass('AVAudioUnit')
AVAudioUnitComponent=ObjCClass('AVAudioUnitComponent')
AVAudioUnitComponentManager=ObjCClass('AVAudioUnitComponentManager')

#
# componentType,componentSubType,componentManufacturer is OSType
#
# ref:  developer.apple.com/reference/audiotoolbox/audiocomponentdescription
#
class AudioComponentDescription(ctypes.Structure):
    _fields_=[('componentType',ctypes.c_char_p),('componentSubType',ctypes.c_char_p),('componentManufacturer',ctypes.c_char_p),('componentFlags',ctypes.c_uint32),('componentFlagsMask',ctypes.c_uint32)]
    
anyEffect = AudioComponentDescription('aufx','dcmp','appl',0,0)
availableEffects = AVAudioUnitComponentManager.sharedAudioUnitComponentManager().componentsMatchingDescription_(anyEffect)
