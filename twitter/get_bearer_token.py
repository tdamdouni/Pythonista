# https://github.com/taherh/twitter_application_auth/blob/master/get_bearer_token.py
# Copyright (c) 2013 Taher Haveliwala
#
# get_bearer_token.py
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, 
# this list of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
#
#
# Python example of Twitter API 1.1 Application-Only Authentication,
# as specified at:
#
#     https://dev.twitter.com/docs/auth/application-only-auth
#

import urllib2, base64, json

# NOTE: Put your consumer key & secret here
CONSUMER_KEY = b'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = b'YOUR_CONSUMER_SECRET'

#
# Step 1: Encode consumer key and secret
#

base64_consumer_key_secret = base64.b64encode(
    urllib2.quote(CONSUMER_KEY) + b':' + urllib2.quote(CONSUMER_SECRET))

#
# Step 2: Obtain a bearer token
#

# note: the following line won't verify server certificate; to do so you'll have to
#       use python3 and specify cafile & capauth
request = urllib2.Request("https://api.twitter.com/oauth2/token")
request.add_header('Authorization', b'Basic ' + base64_consumer_key_secret)
request.add_header("Content-Type", b'application/x-www-form-urlencoded;charset=UTF-8')
request.add_data(b'grant_type=client_credentials')

resp = urllib2.urlopen(request)
data = json.load(resp)
if data['token_type'] != 'bearer':
    throw("Bad token_type: " + data['token_type'])
access_token = data['access_token']

print("access_token: " + access_token)
print('')

#
# Step 3: Authenticate API requests with the bearer token
#

request = urllib2.Request(
        'https://api.twitter.com/1.1/statuses/user_timeline.json?count=3&screen_name=twitterapi'
    )
request.add_header('Authorization', b'Bearer ' + access_token)

resp = urllib2.urlopen(request)
data = json.load(resp)

print("Result:")
print(json.dumps(data, indent=4, separators=(',', ': ')))