from __future__ import print_function
# https://gist.github.com/tlinnet/c1aaa1d4494548217b3ed91301f64eb2

from objc_util import *

#https://gist.github.com/rakhmad/23b3a13682ffe4c4ce64
#https://gist.github.com/omz/b39519b877c07dbc69f8
#http://stackoverflow.com/questions/2346893/tutorials-for-using-http-post-and-get-on-the-iphone-in-objective-c
#http://codewithchris.com/tutorial-how-to-use-ios-nsurlconnection-by-example/
#https://agilewarrior.wordpress.com/2012/02/01/how-to-make-http-request-from-iphone-and-parse-json-result/

# curl -X GET https://jsonplaceholder.typicode.com/posts/1
root1 = "http://www.stackoverflow.com"
root2 = "https://jsonplaceholder.typicode.com/posts/1"
root3 = "https://api.hotspotsystem.com/v2.0/locations/4/vouchers"
method = "GET"
sn_apikey = "secret"
#print("curl -X %s %s"%(method, root))

class Web(object):
    def __init__(self, root=None, method=None, headers=None):
        #NSMutableURLRequest* request = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:url]];
        self.request = ObjCClass('NSMutableURLRequest').alloc().initWithURL_(nsurl(root))
        #[request setHTTPMethod:@"POST"];
        self.request.setHTTPMethod_(method)

        # Make headers
        for key in headers:
            #[request setValue:@"es" forHTTPHeaderField:@"Accept-Language"];
            self.request.setValue_forHTTPHeaderField_(key, headers[key])

        # Make request
        #NSURLConnection * theConnection = [[NSURLConnection alloc] initWithRequest:imageRequest delegate:self];
        #self.conn = ObjCClass('NSURLConnection').alloc().initWithRequest_delegate_(self.request, self)
        self.conn = ObjCClass('NSURLConnection').alloc().initWithRequest_delegate_startImmediately_(self.request, self, True)

        #[connection autorelease];
        self.conn.autorelease()

        #- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data {[self.responseData appendData:data];}
        #self.data = self.conn.didReceiveData_()

    def get_conn(self):
        return self

# Try for root 2
headers = {}
A = Web(root=root2, method=method, headers=headers)
print(dir(A.get_conn().conn))

