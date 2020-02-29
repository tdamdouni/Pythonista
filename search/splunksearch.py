from __future__ import print_function
# https://gist.github.com/benbramley/777c0837106de67beb35
import urllib2
import urllib
from xml.dom import minidom
import re
import csv
import prettytable
import StringIO
import console

u='[SPLUNK USER HERE]'
p='[SPLUNK USER PASSWORD HERE]'
url='[SPLUNK MANAGEMENT URL HERE - e.g. https://splunkserver.com:8089]'

authservice='/services/auth/login'
searchservice='/services/search/jobs'

#Prompt for adhoc search
search = console.input_alert("enter search")

class SplunkSearch():

    def __init__(self):
    	print('initialised')


    def encodeUserData(self, user, password):
        return urllib.urlencode({'username':user, 'password':password})

    def executesearch(self, searchquery):
        req = urllib2.Request(url + authservice)
        creds = self.encodeUserData(u,p)
        res = urllib2.urlopen(req,creds)
        sessionxml = res.read()
        sessionkey = minidom.parseString(sessionxml).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue

        print("got session key: %s"  % sessionkey)

        if not searchquery.startswith('search'):
            searchquery = 'search ' + searchquery

        req = urllib2.Request(url + searchservice)
        req.add_header('Authorization', 'Splunk %s' % sessionkey)

        search=urllib.urlencode({'search': searchquery})
        res = urllib2.urlopen(req,search)
        searchxml = res.read()
        sid = minidom.parseString(searchxml).getElementsByTagName('sid')[0].childNodes[0].nodeValue

        print("got sid:  %s" % sid)

        searchservicesstatus = '/services/search/jobs/%s/' % sid
        req = urllib2.Request(url + searchservicesstatus)
        req.add_header('Authorization', 'Splunk %s' % sessionkey)

        isnotdone = True
        while isnotdone:
            res = urllib2.urlopen(req)
            searchstatus = res.read()
            isdonestatus = re.compile('isDone">(0|1)')
            isdonestatus = isdonestatus.search(searchstatus).groups()[0]
            if (isdonestatus == '1'):
                isnotdone = False

        print("got search status:  %s" % isdonestatus)

        searchserviceresults = '/services/search/jobs/%s/results?output_mode=csv&count=0' % sid
        req = urllib2.Request(url + searchserviceresults)
        req.add_header('Authorization', 'Splunk %s' % sessionkey)
        res = urllib2.urlopen(req)
        searchresults = res.read()
        results = StringIO.StringIO(searchresults)
        
        table = prettytable.from_csv(results)
        
        print(table)

s = SplunkSearch()
s.executesearch(search)