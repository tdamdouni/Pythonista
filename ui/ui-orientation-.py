# https://forum.omz-software.com/topic/3115/ui-and-device-rotation-monitoring

#overwrite these methods in a ui.View
def layout(self):
	if self.width > self.height:
		self.scr_orientation = 'landscape'
	else:
		self.scr_orientation = 'portrait'
		
def draw(self):
    #display your landscape or portrait content


// Listen for device orientation changes:

[[NSNotificationCenter defaultCenter]
       addObserver:self
          selector:@selector(deviceOrientationDidChangeNotification:)
              name:UIDeviceOrientationDidChangeNotification
            object:nil];

// When notified, get the device orientation from UIDevice:

- (void)deviceOrientationDidChangeNotification:(NSNotification*)note
{
    UIDeviceOrientation orientation = [[UIDevice currentDevice] orientation];
    switch (orientation)
    {
        // etc...
    }
}

