from __future__ import print_function
# @parse @xmlrpc
# http://www.leancrew.com/all-this/2013/01/local-archive-of-wordpress-posts/
# https://gist.github.com/danielpunkass/9c55e99af283ec0e24ec
#!/usr/bin/python
import sys
import xmlrpclib

postLimit = 1000

if (len(sys.argv) < 4):
	print("Usage: %s <blogAPIURL> <username> <password>" % sys.argv[0])
	print("E.g.: %s http://example.com/xmlrpc.php daniel 1234" % sys.argv[0])
	sys.exit(0)

blogServer = xmlrpclib.Server(sys.argv[1])

# All posts from 0 to postLimit, excluding all fields except 'link'
allPosts = blogServer.wp.getPosts(1, sys.argv[2], sys.argv[3], {"offset" : 0, "number": postLimit}, ['link'])

allLinks = [x['link'] for x in allPosts]

print("\n".join(allLinks))