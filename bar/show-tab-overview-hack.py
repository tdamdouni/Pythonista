# coding: utf-8

# runs once (not persistent)

# https://forum.omz-software.com/topic/2590/add-editor-buttons-changes-not-reflected/8

from objc_util import *

UIApplication = ObjCClass('UIApplication')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

@on_main_thread
def main():
	rootVC = UIApplication.sharedApplication().keyWindow().rootViewController()
	tabVC = rootVC.detailViewController()
	tabVC.tabCollectionView().collectionViewLayout().itemSize = CGSize(328,200)
	tabVC.tabCollectionView().contentInset = UIEdgeInsets(58,0,0,0)
	
	overviewItem = UIBarButtonItem.alloc().initWithImage_style_target_action_(UIImage.imageNamed_('ShowTabs'), 0, tabVC, sel('showTabOverview:'))
	rightItems=list(tabVC.navigationItem().rightBarButtonItems())
	rightItems.insert(1,overviewItem)
	tabVC.navigationItem().rightBarButtonItems=rightItems
	#tabVC.persistentLeftBarButtonItems = [overviewItem]
	
	
if __name__ == '__main__':
	main()

