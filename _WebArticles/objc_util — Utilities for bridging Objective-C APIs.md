# objc_util — Utilities for bridging Objective-C APIs

_Captured: 2016-01-13 at 00:52 from [omz-software.com](http://omz-software.com/pythonista/docs/ios/objc_util.html)_


    UIPasteboard *pasteboard = [UIPasteboard generalPasteboard]
    [pasteboard setString:@"Hello Objective-C"];
    
    
    from objc_util import *
    UIPasteboard = ObjCClass('UIPasteboard')
    
    pasteboard = UIPasteboard.generalPasteboard()
    pasteboard.setString_('Hello Objective-C')
    

Note

As with [ctypes](http://omz-software.com/pythonista/docs/library/ctypes.html), there are lots of ways to crash Python using this module. When you call Objective-C methods, you have to be very careful to provide the correct parameter types.

## Example 1 - Setting the screen brightness

This simple example sets the screen brightness of your device:
    
    
    from objc_util import *
    
    # 'Import' an Objective-C class (generate a proxy for the class):
    UIScreen = ObjCClass('UIScreen')
    
    # Call a class method, this is equivalent to `[UIScreen mainScreen]` in Objective-C:
    screen = UIScreen.mainScreen()
    
    # `screen` is now an ObjCInstance that wraps an Objective-C object, and forwards messages to it.
    
    # The following call is equivalent to `[screen setBrightness:0.6]` (note the trailing underscore in the method name)
    screen.setBrightness_(0.6)
    

## Example 2 - Accessing the current song in Music/iPod app

This code snippet prints the currently-playing song in the console (note that this only works for the built-in Music app, not for third-party audio players):
    
    
    from objc_util import *
    
    MPMusicPlayerController = ObjCClass('MPMusicPlayerController')
    ipod_player = MPMusicPlayerController.iPodMusicPlayer()
    now_playing = ipod_player.nowPlayingItem()
    if now_playing:
        artist = now_playing.valueForProperty_('artist')
        title = now_playing.valueForProperty_('title')
        print 'Now playing: %s -- %s' % (artist, title)
    else:
        print 'No music playing'
    

### Creating New Objective-C Classes

For more advanced uses of Objective-C APIs, you sometimes need to create your own Objective-C classes at runtime. The main two scenarios when you'd want to do this are:

  * Implementing the commonly-used delegate pattern, i.e. providing a callback interface for a built-in Objective-C class.
  * Subclassing Objective-C classes that are intended to be subclassed for customization. One example would be subclassing UIView in order to override -drawRect:.

To accomplish this, the [objc_util](http://omz-software.com/pythonista/docs/ios/objc_util.html) module provides the [create_objc_class()](http://omz-software.com/pythonista/docs/ios/objc_util.html) function, which uses the Objective-C runtime to allocate and register a new class, and then wraps the class in an [ObjCClass](http://omz-software.com/pythonista/docs/ios/objc_util.html) object that you can use just like a built-in class in the examples above.

To create an Objective-C class using [create_objc_class()](http://omz-software.com/pythonista/docs/ios/objc_util.html), you need the following things:

**name** - the name of the class to create, as a string. This should only consist of letters, numbers, and underscore characters. It may not begin with a number. Please note that the name of the class that actually gets created may be different from this because a class with the name may already exist. If that's the case, a new name is chosen automatically, if the debug parameter is True (the default). If debug is False, the existing class will be returned, and all other parameters are ignored.

**superclass** - An ObjCClass object that determines the Objective-C class from which the new class inherits.

**methods** - A list of functions that are used to create the instance methods of the new class. To create an Objective-C method from a Python function, the Objective-C runtime needs additional metadata: the selector name, the type of the return value, and types for any arguments. As much as possible, [create_objc_class()](http://omz-software.com/pythonista/docs/ios/objc_util.html) will try to derive this metadata automatically, please see the the discussion under [create_objc_class()](http://omz-software.com/pythonista/docs/ios/objc_util.html) for details. Every Objective-C method needs at least two parameters that are hidden when calling it from Objective-C: _self is a pointer to the Objective-C object itself (note that this is not wrapped in an [ObjCInstance](http://omz-software.com/pythonista/docs/ios/objc_util.html) object, so you have to do this manually if needed), and _cmd, a pointer to the selector (usually not needed). The names of these two "hidden" parameters don't matter. Note that parameters are passed to Objective-C methods as "raw" pointers, not ObjCInstance objects, but you can convert object parameters easily by wrapping them manually, e.g. obj = ObjCInstance(_self).

**classmethods** (optional) - same as methods, but for class methods (rarely needed).

**protocols** (optional) - a list of strings that is used for hinting type encodings for methods. If you implement a delegate (or other) protocol, you should include the protocol's name (e.g. 'UITableViewDataSource') to make sure that the return and argument types for any methods can be inferred correctly.

Here is an example of creating a simple class that acts as the delegate for an MFMailComposeViewController (which is used to show the standard iOS Mail sheet). A delegate is required to use this class because it is otherwise impossible to get rid of the Mail sheet (the delegate is notified when the sheet has finished, and it's responsible for dismissing it).:
    
    
    # - (void)mailComposeController:(MFMailComposeViewController *)controller didFinishWithResult:(MFMailComposeResult)result error:(NSError *)error
    def mailComposeController_didFinishWithResult_error_(_self, _cmd, controller, result, error):
        print 'Mail composer finished'
        # Wrap the controller parameter in an `ObjCInstance`, so we can send messages:
        mail_vc = ObjCInstance(controller)
        # Set delegate to nil, and release its memory:
        mail_vc.setDelegate_(None)
        ObjCInstance(_self).release()
        # Dismiss the sheet:
        mail_vc.dismissViewControllerAnimated_completion_(True, None)
    
    methods = [mailComposeController_didFinishWithResult_error_]
    protocols = ['MFMailComposeViewControllerDelegate']
    MyMailComposeDelegate = create_objc_class('MyMailComposeDelegate', NSObject, methods=methods, protocols=protocols)
    
    @on_main_thread
    def show_mail_sheet():
        MFMailComposeViewController = ObjCClass('MFMailComposeViewController')
        mail_composer = MFMailComposeViewController.alloc().init().autorelease()
        # Use our new delegate class:
        delegate = MyMailComposeDelegate.alloc().init()
        mail_composer.setDelegate_(delegate)
        # Present the mail sheet:
        root_vc = UIApplication.sharedApplication().keyWindow().rootViewController()
        root_vc.presentViewController_animated_completion_(mail_composer, True, None)
    
    if __name__ == '__main__':
        show_mail_sheet()
    

## API Reference

### Classes

_class _objc_util.ObjCClass(_name_)
    

Wrapper for an Objective-C class with the given name; acts as a proxy for calling Objective-C class methods.

Method calls are converted to Objective-C messages on-the-fly - this is done by replacing underscores in the method name with colons in the selector name, and using the selector and arguments for a call to the low-level objc_msgSend() function in the Objective-C runtime.

For example, calling NSDictionary.dictionaryWithObject_forKey_(obj, key) (Python) is effectively translated to [NSDictionary dictionaryWithObject:obj forKey:key] (Objective-C). If a method call returns an Objective-C object, it is wrapped in an ObjCInstance, so calls can be chained ([ObjCInstance](http://omz-software.com/pythonista/docs/ios/objc_util.html) uses an equivalent proxy mechanism).

Some commonly used classes are module members (see list at the bottom), for others, you simply "import" it using the class name, e.g.:
    
    
    UIPasteboard = ObjCClass('UIPasteboard')
    

_class _objc_util.ObjCInstance(_ptr_)
    

Wrapper for a pointer to an Objective-C object; acts as a proxy for sending messages to the object.

Method calls are converted to Objective-C messages on-the-fly - this is done by replacing underscores in the method name with colons in the selector name, and using the selector and arguments for a call to the objc_msgSend() function in the Objective-C runtime. For example, calling obj.setFoo_withBar_(foo, bar) (Python) is effectively translated to [obj setFoo:foo withBar:bar] (Objective-C). If a method call returns an Objective-C object, it is also wrapped in an ObjCInstance, so calls can be chained.

If an instance wraps a common Objective-C collection type (NSArray, NSDictionary, NSSet), it behaves similar to a native Python collection in many ways. It can be iterated (for .. in), you can access items by key/index, using square bracket notation (some_dict['key'], some_array[3]...), etc.

_class _objc_util.ObjCBlock(_func_, _restype=None_, _argtypes=None_)
    

Warning

Block support is experimental. If you have the alternative of using an API that doesn't require blocks, it is strongly recommended that you do so.

[ObjCBlock](http://omz-software.com/pythonista/docs/ios/objc_util.html) can be used to pass blocks ("closures") to Objective-C methods. As mentioned above, this is experimental, and you should usually prefer to use APIs that don't require blocks, if possible. Some APIs absolutely require the use of blocks though. For blocks that don't have a return value and no arguments, you can pass a Python function, and it'll be converted to an [ObjCBlock](http://omz-software.com/pythonista/docs/ios/objc_util.html) automatically. In other cases, you need to specify the return and argumet types when creating the block explicitly.

Example of a block with arguments (used to sort an NSMutableArray with a custom comparison function):
    
    
    from objc_util import *
    cheeses = ns(['Camembert', 'Feta', 'Gorgonzola'])
    print cheeses
    
    def compare(_cmd, obj1_ptr, obj2_ptr):
        obj1 = ObjCInstance(obj1_ptr)
        obj2 = ObjCInstance(obj2_ptr)
        # Sort the strings by length:
        return cmp(obj1.length(), obj2.length())
    
    # Note: The first (hidden) argument `_cmd` is the block itself, so there are three arguments instead of two.
    compare_block = ObjCBlock(compare, restype=NSInteger, argtypes=[c_void_p, c_void_p, c_void_p])
    
    sorted_cheeses = cheeses.sortedArrayUsingComparator_(compare_block)
    print sorted_cheeses
    

### Functions

objc_util.create_objc_class(_name_, _superclass=NSObject_, _methods=_[], _classmethods=_[], _protocols=_[], _debug=True_)
    

  * The selector name is derived from the name of the function. The function name can optionally be prefixed by the Objective-C class name. For example, these two functions result in an equivalent selector name:
    
        def MyClass_doSomething_withObject_(_self, _cmd, foo, bar):
        pass
    
    def doSomething_withObject_(_self, _cmd, foo, bar):
        pass
    
    # The selector name for both of these functions would be 'doSomething:withObject:'.
    

  * To determine the return type and argument types, [create_objc_class()](http://omz-software.com/pythonista/docs/ios/objc_util.html) checks if the superclass has a method with the same selector. If that's the case, the types are inherited from the superclass's method. This strategy works for overriding a method in a subclass. If this fails, the protocols parameter is used. protocols is a list of strings, for example ['UIGestureRecognizerDelegate', 'UITableViewDataSource'] - these protocols are checked for methods with the same selector. This strategy works for example for implementing delegate protocols. Together, these strategies should determine the type information in most common cases. If they are not suitable in your case, you can set restype, argtypes, and encoding attributes on the function objects you pass.

Note

If you want to use an _existing_ Objective-C class, simply obtain a reference to it using ObjCClass(name). This function is for creating _new_ classes, e.g. to subclass an Objective-C class or implement a delegate protocol.

objc_util.ns(_obj_)
    

Convert common Python objects to their ObjC equivalents, i.e. str => NSString, int/float => NSNumber, list => NSMutableArray, dict => NSMutableDictionary, bytearray => NSData, set => NSMutableSet. Nested structures (list/dict/set) are supported. If an object is already an instance of [ObjCInstance](http://omz-software.com/pythonista/docs/ios/objc_util.html), it is left untouched.

If an Objective-C method expects an object as a parameter, the Python object parameter is automatically converted using this function, so you can e.g. pass Python strings to Objective-C methods that expect an NSString.

    

If the string contains a colon (':'), it is treated as a full URL and converted to an NSURL using +URLWithString:. Otherwise, a file URL is constructed using +fileURLWithPath:.

objc_util.on_main_thread(_func_)
    

Decorator function for calling another function on the UIKit main thread. A lot of Objective-C APIs (particularly in UIKit) require being called from the main thread. This is typically used to decorate another function, but it can also be used for dispatching a function call to the main thread ad-hoc, e.g. on_main_thread(my_function)(param1, param2)

Decorator example:
    
    
    from objc_util import *
    
    @on_main_thread
    def post_notification(name):
        NSNotificationCenter = ObjCClass('NSNotificationCenter')
        center = NSNotificationCenter.defaultCenter()
        center.postNotificationName_object_(name, None)
    
    # Every call of post_notification(...) will automagically happen on the main thread.
    

### Objective-C Classes/Structs

For convenience, a few commonly-used Objective-C classes and structs are made available as module-level objects, so they don't have to be wrapped explicitly. These are:

* objc_util.CGPoint
* class objc_util.CGSize
* class objc_util.CGVector
* class objc_util.CGRect
* class objc_util.CGAffineTransform
* class objc_util.UIEdgeInsets
* class objc_util.NSRange
* class objc_util.NSDictionary
* class objc_util.NSMutableDictionary
* class objc_util.NSArray
* class objc_util.NSMutableArray
* class objc_util.NSSet
* class objc_util.NSMutableSet
* class objc_util.NSString
* class objc_util.NSMutableString
* class objc_util.NSData
* class objc_util.NSMutableData
* class objc_util.NSNumber
* class objc_util.NSURL
* class objc_util.NSEnumerator
