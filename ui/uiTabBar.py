from __future__ import print_function
# https://forum.omz-software.com/topic/2310/share-code-tabbar

# coding: utf-8

from objc_util import *
import ctypes
import weakref
import ui

_tab_bar_delegate_cache = weakref.WeakValueDictionary()
_retain_me = None ## stops from crashing

try:
    BLMTabBarDelegate = ObjCClass('BLMTabBarDelegate')
except ValueError:
    @ctypes.CFUNCTYPE(None, c_void_p, c_void_p, c_void_p, c_void_p)
    def tabBar_didSelectItem_(self, cmd, tab_bar, tab_bar_item):
        tab_bar = _tab_bar_delegate_cache[self].tab_bar_ref()
        if tab_bar:
            tab_bar._notify_did_select_item()
    
    _retain_me = tabBar_didSelectItem_ ## stop garbage collection 
    NSObject = ObjCClass('NSObject')
    class_ptr = c.objc_allocateClassPair(NSObject.ptr, 'BLMTabBarDelegate', 0)
    selector = sel('tabBar:didSelectItem:')
    c.class_addMethod(class_ptr, selector, tabBar_didSelectItem_, 'v0@0:0@0@0')
    c.objc_registerClassPair(class_ptr)
    BLMTabBarDelegate = ObjCClass('BLMTabBarDelegate')

UITabBar     = ObjCClass('UITabBar')
UITabBarItem = ObjCClass('UITabBarItem')

class TabBar (ui.View):
    @on_main_thread
    def __init__(self, *args, **kwargs):
        super(TabBar, self).__init__(*args, **kwargs)
        frame = CGRect(CGPoint(0, 0), CGSize(self.width, self.height))
        self.tab_bar = UITabBar.alloc().initWithFrame_(frame).autorelease()
        flex_width, flex_height = (1<<1), (1<<4)
        self.tab_bar.setAutoresizingMask_(flex_width|flex_height)
        self_objc = ObjCInstance(self)
        self_objc.addSubview_(self.tab_bar)
        self.item_changed_action = None
        self.tab_bar_delegate = BLMTabBarDelegate.new().autorelease()
        self.tab_bar.setDelegate_(self.tab_bar_delegate)
        self.tab_bar_delegate.tab_bar_ref = weakref.ref(self)
        _tab_bar_delegate_cache[self.tab_bar_delegate.ptr] = self.tab_bar_delegate
    
        
    @property
    @on_main_thread
    def items(self):
        return self.tab_bar.items()
    
    @items.setter
    @on_main_thread
    def items(self, items):
        self.tab_bar.setItems_animated_(items, True)
        
    @property
    @on_main_thread
    def selected_item(self):
        return self.tab_bar.selectedItem()
    
    @property
    @on_main_thread
    def delegate(self):
        return self.delegate()
    
    @delegate.setter
    @on_main_thread
    def delegate(self, delegate):
        self.tab_bar.setDelegate_(delegate)
        
    def _notify_did_select_item(self):
        if callable(self.item_changed_action):
            self.item_changed_action(self)
    


tab_bar_item_1 = UITabBarItem.alloc().initWithTabBarSystemItem_tag_(0,0).autorelease()

tab_bar_item_2 = UITabBarItem.alloc().initWithTabBarSystemItem_tag_(1,1).autorelease()

def tab_bar_item_changed(sender):
    print(sender.selected_item.description())

root = ui.View(frame=(0,0,500,500))
tab_bar = TabBar(frame=(0,451,500,49))
tab_bar.items = [tab_bar_item_1, tab_bar_item_2]
tab_bar.item_changed_action = tab_bar_item_changed
root.add_subview(tab_bar)
root.present('sheet')