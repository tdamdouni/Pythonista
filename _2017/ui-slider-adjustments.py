# https://forum.omz-software.com/topic/4488/easy-add-images-or-change-colors-of-a-ui-slider

# ui.Slider is an UISlider
# we can set its images/colors via Objective-C
volume_slider = ui.Slider()
objc = ObjcInstance(volume_slider)
objc.minimumValueImage = ui.Image.named('iob:ios7_volume_low_32')
objc.maximumValueImage = ui.Image.named('iob:ios7_volume_high_32')
objc.thumbTintColor = ObjCClass('UIColor').color(red=1.0, green=0.0, blue=0.0, alpha=1.0)
