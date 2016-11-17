# coding: utf-8

# https://forum.omz-software.com/topic/2590/add-editor-buttons-changes-not-reflected/8

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
	
	print tabVC.navigationItem().rightBarButtonItems()
	
	rightItems.insert(-1,overviewItem)
	rightItems=ns(rightItems)
	rightItems.init()
	tabVC.navigationItem().set_rightBarButtonItems_(rightItems)
	print tabVC.navigationItem().rightBarButtonItems()
	
	#tabVC.persistentLeftBarButtonItems = [overviewItem]
	tabVC.reloadBarButtonItemsForSelectedTab()
	
if __name__ == '__main__':
	main()
	
# --------------------
	rightItems=list(tabVC.navigationItem().rightBarButtonItems())
	rightItems.insert(1,overviewItem)
	tabVC.navigationItem().rightBarButtonItems=rightItems
	
# --------------------

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
	
	print tabVC.navigationItem().rightBarButtonItems()
	print tabVC.toolbar().rightBarButtons()
	addButton(overviewItem)
	print tabVC.navigationItem().rightBarButtonItems()
	print tabVC.toolbar().rightBarButtons()
	
if __name__ == '__main__':
	main()
# --------------------
>>> tabVC.toolbar().rightBarButtons()[0].recursiveDescription()
<__NSCFString: <OMBarButton: 0x13fa71180; frame = (976 22; 40 40); layer = <CALayer: 0x13e5eefb0>>
	| <UIButton: 0x13faccfa0; frame = (0 0; 40 40); opaque = NO; layer = <CALayer: 0x13e5a0150>>
	|    | <UIImageView: 0x13f8b0960; frame = (8.5 8.5; 23 23); clipsToBounds = YES; opaque = NO; userInteractionEnabled = NO; layer = <CALayer: 0x13e5b8010>>>
>>> tabVC.toolbar().rightBarButtons()[3].recursiveDescription()
<__NSCFString: <OMBarButton: 0x13fca3f20; frame = (832 22; 40 40); layer = <CALayer: 0x13f956440>>
	| <UIButton: 0x13f9db140; frame = (0 0; 0 0); opaque = NO; layer = <CALayer: 0x13f9db3e0>>>
	
# --------------------

# coding: utf-8

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
	
# --------------------

