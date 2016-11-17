# coding: utf-8

# https://forum.omz-software.com/topic/2535/fixing-the-caret-color-in-the-console-prompt

from objc_util import *
#Thanks to @JonB, he posted similar code a while back
def filter_subviews_by_class(view,objcclasstext=None):
	matching_svs=[]
	sv=view.subviews()
	if sv is None:
		return matching_svs
	for v in sv:
		if objcclasstext and objcclasstext in v._get_objc_classname():
			matching_svs.append(v)
		matching_svs.extend(
		filter_subviews_by_class(v,objcclasstext))
	return matching_svs
	
w=ObjCClass('UIApplication').sharedApplication().keyWindow()
main_view=w.rootViewController().view()
console_prompt=filter_subviews_by_class(main_view,'PA2PromptTextField')[0]
console_prompt.tintColor=ObjCClass('UIColor').colorWithRed_green_blue_alpha_(0.47, 0.67, 0.71, 1.0)

