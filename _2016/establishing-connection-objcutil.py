from __future__ import print_function
# https://gist.github.com/tlinnet/92c0654081a6c49aa5b39a984018b253

# https://forum.omz-software.com/topic/3701/ipv6-in-pythonista-not-supplied/2

from objc_util import *

#https://gist.github.com/rakhmad/23b3a13682ffe4c4ce64
#https://gist.github.com/omz/b39519b877c07dbc69f8
#http://stackoverflow.com/questions/2346893/tutorials-for-using-http-post-and-get-on-the-iphone-in-objective-c
#http://codewithchris.com/tutorial-how-to-use-ios-nsurlconnection-by-example/

# curl -X GET https://jsonplaceholder.typicode.com/posts/1
root1 = "http://www.stackoverflow.com"
root2 = "https://jsonplaceholder.typicode.com/posts/1"
root3 = "https://api.hotspotsystem.com/v2.0/locations/4/vouchers"
method = "GET"
sn_apikey = "secret"
#print("curl -X %s %s"%(method, root))

def get(root=None, method=None, headers={}):
    #NSMutableURLRequest* request = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:url]];
    NSMutableURLRequest = ObjCClass('NSMutableURLRequest')
    request = NSMutableURLRequest.alloc().initWithURL_(nsurl(root))

    #[request setHTTPMethod:@"POST"];
    request.setHTTPMethod_(method)

    #[request setDelegate:self];
    #request.setDelegate(self)

    # Make header
    for key in headers:
        #[request setValue:@"es" forHTTPHeaderField:@"Accept-Language"];
        request.setValue_forHTTPHeaderField_(key, headers[key])

    # Make request
    #NSURLConnection * theConnection = [[NSURLConnection alloc] initWithRequest:imageRequest delegate:self];
    NSURLConnection = ObjCClass('NSURLConnection')
    theConnection = NSURLConnection.alloc().initWithRequest_delegate_(request, self)

    return "test"

# Try for root 1
headers = {"es":"Accept-Language"}
data = get(root=root1, method=method, headers=headers)

print(data)

