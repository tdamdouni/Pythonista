# coding: utf-8

# https://gist.github.com/lukaskollmer/3a04ea02a410e26c9b2f6a74c2f214a8

import console
from objc_util import *

console.clear()

#importFramework('MediaPlayer')

MPMediaPickerController = ObjCClass('MPMediaPickerController')

def mediaPicker_didPickMediaItems_(_self, _cmd, _picker, _items):
	ObjCInstance(_picker).dismissViewControllerAnimated_completion_(True, None)
	print(ObjCInstance(_items))

def mediaPickerDidCancel_(_self, _cmd, _picker):
	ObjCInstance(_picker).dismissViewControllerAnimated_completion_(True, None)


@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	MediaPickerDelegate = create_objc_class('MediaPickerDelegate', methods=[mediaPicker_didPickMediaItems_, mediaPickerDidCancel_], protocols=['MPMediaPickerControllerDelegate'])
	mediaPicker = MPMediaPickerController.new()
	mediaPicker.setDelegate_(MediaPickerDelegate.new())
	
	tabVC.presentViewController_animated_completion_(mediaPicker, True, None)


if __name__ == '__main__':
	main()
