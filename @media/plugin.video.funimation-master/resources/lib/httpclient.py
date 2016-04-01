# -*- coding: utf-8 -*-
import os
import json
import urllib2
import cookielib
from urllib import urlencode

__all__ = ['HTTPClient']


class HTTPClient(object):

    def __init__(self, base_url='', cookiefile=None, headers=None):
        super(HTTPClient, self).__init__()
        self.base_url = base_url
        self.cookiefile = cookiefile
        self._cookiejar = cookielib.LWPCookieJar(self.cookiefile)

        try:
            if self.cookiefile is not None:
                if not os.path.exists(os.path.dirname(self.cookiefile)):
                    os.makedirs(os.path.dirname(self.cookiefile))
                else:
                    self._cookiejar.load()
        except IOError:
            # files doesn't exist yet
            pass

        cookie_handler = urllib2.HTTPCookieProcessor(self._cookiejar)
        self.opener = urllib2.build_opener(cookie_handler)

        if headers is not None:
            self.opener.addheaders = headers

    def get(self, url, query=None):
        if query is not None:
            if isinstance(query, dict):
                q = dict((k, v) for k, v in query.iteritems() if v is not None)
                url = url + '?' + urlencode(q)
            else:
                url = url + '?' + query
        return self._request(self._build_request(url))

    def post(self, url, data):
        return self._request(self._build_request(url, data))

    def get_cookie(self, name):
        for x in self._cookiejar:
            if x.name == name:
                return x
        return None

    def save_cookies(self):
        self._cookiejar.save()

    def _request(self, request):
        content = self.opener.open(request)
        if self.cookiefile:
            self.save_cookies()

        if content.info()['content-type'] == 'application/json':
            content = json.load(content, 'utf-8')
        else:
            content = content.read()

        return content

    def _build_request(self, url, data=None):
        url = self.base_url + url
        if data is not None:
            if isinstance(data, dict):
                req = urllib2.Request(url, json.dumps(data),
                                      {'Content-Type': 'application/json'})
            else:
                req = urllib2.Request(url, data)
        else:
            req = urllib2.Request(url)

        return req
