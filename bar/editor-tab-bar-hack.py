# coding: utf-8

# https://forum.omz-software.com/topic/2590/add-editor-buttons-changes-not-reflected/8

from __future__ import print_function
from objc_util import *

UIApplication = ObjCClass('UIApplication')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
tabVC = rootVC.detailViewController()

def addButton(buttonitem):
	global OMbuttonitem
	#Add to main thing
	rightItems=list(tabVC.navigationItem().rightBarButtonItems())
	rightItems.append(buttonitem)
	rightItems=ns(rightItems)
	tabVC.navigationItem().set_rightBarButtonItems_(rightItems)
	#Add to toolbar
	OMbuttonitem=ObjCClass('OMBarButton').alloc().initWithBarButtonItem_(buttonitem)
	OMbuttonitem.setFrame_(CGRect(CGPoint(832,22),CGSize(40,40)))
	rightItems=list(tabVC.toolbar().rightBarButtons())
	rightItems.append(OMbuttonitem)
	rightItems=ns(rightItems)
	tabVC.toolbar().setRightBarButtons_(rightItems)
	
def reset():
	tabVC.reloadBarButtonItemsForSelectedTab()
	tabVC.toolbar().reloadRightBarButtonItems()
	
@on_main_thread
def main():
	tabVC.tabCollectionView().collectionViewLayout().itemSize = CGSize(328,200)
	tabVC.tabCollectionView().contentInset = UIEdgeInsets(58,0,0,0)
	overviewItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('ShowTabs'), 0, tabVC, sel('showTabOverview:'))
	
	print(tabVC.navigationItem().rightBarButtonItems())
	print(tabVC.toolbar().rightBarButtons())
	addButton(overviewItem)
	print(tabVC.navigationItem().rightBarButtonItems())
	print(tabVC.toolbar().rightBarButtons())
	
if __name__ == '__main__':
	main()

