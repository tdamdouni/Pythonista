# https://forum.omz-software.com/topic/3618/querying-returned-nserror

err_ptr = c_void_p()
device_input = ObjCClass('AVCaptureDeviceInput').deviceInputWithDevice_error_(input_device, byref(err_ptr))
if err_ptr:
    err = ObjCInstance(err)
    print(err)
