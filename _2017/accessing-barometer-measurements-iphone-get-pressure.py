# https://forum.omz-software.com/topic/3078/accessing-barometer-measurements/14

from objc_util import ObjCInstance, ObjCClass, ObjCBlock, c_void_p

pressure = None

def get_pressure():

  def handler(_cmd, _data, _error):
    global pressure
    pressure = ObjCInstance(_data).pressure()

  handler_block = ObjCBlock(handler, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])

  CMAltimeter = ObjCClass('CMAltimeter')
  NSOperationQueue = ObjCClass('NSOperationQueue')
  if not CMAltimeter.isRelativeAltitudeAvailable():
    print('This device has no barometer.')
    return
  altimeter = CMAltimeter.new()
  main_q = NSOperationQueue.mainQueue()
  altimeter.startRelativeAltitudeUpdatesToQueue_withHandler_(main_q, handler_block)
  #print('Started altitude updates.')
  try:
    while pressure is None:
      pass
  finally:
    altimeter.stopRelativeAltitudeUpdates()
    #print('Updates stopped.')
    return pressure

if __name__ == '__main__':
  print(get_pressure())
