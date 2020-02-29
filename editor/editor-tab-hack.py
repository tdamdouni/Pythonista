# coding: utf-8

# https://forum.omz-software.com/topic/2590/add-editor-buttons-changes-not-reflected/8

from __future__ import print_function
from objc_util import *

UIApplication = ObjCClass('UIApplication')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

@on_main_thread
def main():
	global tabVC,overviewItem
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	tabVC.tabCollectionView().collectionViewLayout().itemSize = CGSize(328,200)
	tabVC.tabCollectionView().contentInset = UIEdgeInsets(58,0,0,0)
	
	overviewItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('ShowTabs'), 0, tabVC, sel('showTabOverview:'))
	
	#Add the item
	rightItems=list(tabVC.navigationItem().rightBarButtonItems())
	
	print(tabVC.navigationItem().rightBarButtonItems())
	
	rightItems.insert(-1,overviewItem)
	rightItems=ns(rightItems)
	rightItems.init()
	tabVC.navigationItem().set_rightBarButtonItems_(rightItems)
	print(tabVC.navigationItem().rightBarButtonItems())
	
	#tabVC.persistentLeftBarButtonItems = [overviewItem]
	tabVC.reloadBarButtonItemsForSelectedTab()
	
if __name__ == '__main__':
	main()

