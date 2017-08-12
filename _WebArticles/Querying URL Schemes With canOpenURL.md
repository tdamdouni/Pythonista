# Querying URL Schemes With canOpenURL

_Captured: 2015-12-15 at 10:04 from [useyourloaf.com](http://useyourloaf.com/blog/querying-url-schemes-with-canopenurl.html?utm_source=tuicool&utm_medium=referral)_

Apple continues to put a high priority on protecting the privacy of a user so it should be no surprise that iOS 9 brings new security and privacy measures. One such measure is to prevent the abuse of canOpenURL to discover the Apps a user has installed.

### Querying a URL Scheme

It has long been possible to open an external application using the openURL: method. Typically you first query for the URL scheme of the application with canOpenURL: then you open it with openURL:. A typical Objective-C code snippet to test for a scheme:
    
    
    // Expects the URL of the scheme e.g. "fb://"
    - (BOOL)schemeAvailable:(NSString *)scheme {
      UIApplication *application = [UIApplication sharedApplication];
      NSURL *URL = [NSURL URLWithString:scheme];
      return [application canOpenURL:URL];
    }
    

Or if you prefer Swift maybe something like this:
    
    
    func schemeAvailable(scheme: String) -> Bool {
        if let url = NSURL.init(string: scheme) {
            return UIApplication.sharedApplication().canOpenURL(url)
        }
        return false
    }
    

To query for the Facebook and Twitter Apps:
    
    
    // Objective-C
    BOOL fbInstalled = [self schemeAvailable:@"fb://"];
    BOOL twInstalled = [self schemeAvailable:@"twitter://"];
    
    // Swift
    let fbInstalled = schemeAvailable("fb://")
    let twInstalled = schemeAvailable("twitter://")
    

This is useful but developers including Twitter and Facebook were using this mechanism to [discover the list of Apps](http://blogs.wsj.com/digits/2014/11/26/twitter-is-tracking-users-installed-apps-for-ad-targeting/) installed on a device so they can deliver "tailored content". Apple decided this is a privacy violation and so in iOS 9 restricted the querying of URL schemes. **If you build and link against the iOS 9 SDK you need to whitelist the schemes your app will query.** What is important to understand is that this policy can also impact older Apps that have not yet been rebuilt with the iOS 9 SDK. Let's take a look at two scenarios:

### An iOS 8 App Running on iOS 9

To simulate an iOS 8 App running on an iOS 9 device I built a test App with Xcode 6 using the iOS 8.4 SDK. I then run on an iOS 9 device that only has the Twitter App installed. As expected the query for the facebook scheme returned NO and the Twitter scheme YES. There is also a warning message in the device log for the failed query:
    
    
    CanOpen[2255:1002610] -canOpenURL: failed for URL:
     "fb://" - error: "(null)"
    

This is good, it means that _most_ Apps that rely on querying and opening schemes will continue to work unmodified on iOS 9. I say _most_ as there is an important limitation for Apps not linked against iOS 9. When you run such an App on iOS 9 there is a limit of 50 distinct schemes.

**If you exceed the limit of 50 distinct schemes canOpenURL will return NO. The count of distinct schemes your app can query is not reset even by restarting the device.**

To test this I queried for 100 different schemes to see what would happen:
    
    
    for (int scheme = 0; scheme < 100; scheme++) {
        [self schemeAvailable:[NSString stringWithFormat:@"%02d://",scheme]];
    }
    

For the first few queries the result is as expected indicating the scheme is not supported by any installed App:
    
    
    -canOpenURL: failed for URL: "00://" - error: "(null)"
    -canOpenURL: failed for URL: "01://" - error: "(null)"
    

Once we exceed 50 distinct schemes (including the already queried facebook and twitter schemes) the error message changes:
    
    
    -canOpenURL: failed for URL: "48://" - error:
     "This app has exceeded the number of allowed scheme queries"
    

At this point, it is not possible to query for new schemes. You can still query for the facebook and twitter schemes as they are part of the 50 allowed schemes but if you need to query for something else you are out of luck.

### App Linked with iOS 9

Switching to Xcode 7 to build and link my test code against the iOS 9 SDK changes things. The queries for the facebook and twitter schemes now fail with a permission error:
    
    
    -canOpenURL: failed for URL: "fb://" - error:
     "This app is not allowed to query for scheme fb"
    -canOpenURL: failed for URL: "twitter://" - error:
     "This app is not allowed to query for scheme twitter"
    

In iOS 9 you must whitelist any URL schemes your App wants to query in Info.plist under the LSApplicationQueriesSchemes key (an array of strings):

With the schemes included in Info.plist everything works as before. **When you link against iOS 9 you are not limited to 50 distinct schemes** you just need to declare what you need in Info.plist. There seems to be no limit for how many schemes you can include but I would expect questions from the App Store review team if they think you are abusing the mechanism.

Note that this mechanism only applies to canOpenURL and not openURL. You do _not_ need to have a scheme listed in Info.plist to be able to open it with openURL.

### Further Reading

  * [WWDC 2015 Session 703 Privacy and Your App](https://developer.apple.com/videos/wwdc/2015/?id=703)
