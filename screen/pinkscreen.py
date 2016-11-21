# https://gist.github.com/lukaskollmer/26cdacbc2a29188b24d170a3a18f4d3c

from objc_util import *

UIColor = ObjCClass('UIColor')
UIViewController = ObjCClass('UIViewController')

@on_main_thread
def main():
	color = UIColor.colorWithHexString_('#FFC0CB')
	
	vc = UIViewController.new()
	vc.view().setBackgroundColor_(color)
	tabVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC.presentViewController_animated_completion_(vc, False, None)
	
if __name__ == '__main__':
	main()

