# https://forum.omz-software.com/topic/3636/how-to-login-facebook-with-request-module-for-further-access/3

import requests
from urllib.parse import urlparse
import os
import pickle
import datetime

class MyLoginSession:
	"""
	a class which handles and saves login sessions. It also keeps track of proxy settings.
	It does also maintine a cache-file for restoring session data from earlier
	script executions.
	"""
	def __init__(self,
	loginUrl,
	loginData,
	loginTestUrl,
	loginTestString,
	sessionFileAppendix = '_session.dat',
	maxSessionTimeSeconds = 30 * 60,
	proxies = None,
	userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
	debug = True):
		"""
		save some information needed to login the session
		
		you'll have to provide 'loginTestString' which will be looked for in the
		responses html to make sure, you've properly been logged in
		
		'proxies' is of format { 'https' : 'https://user:pass@server:port', 'http' : ...
		'loginData' will be sent as post data (dictionary of id : value).
		'maxSessionTimeSeconds' will be used to determine when to re-login.
		"""
		urlData = urlparse(loginUrl)
		
		self.proxies = proxies
		self.loginData = loginData
		self.loginUrl = loginUrl
		self.loginTestUrl = loginTestUrl
		self.maxSessionTime = maxSessionTimeSeconds
		self.sessionFile = urlData.netloc + sessionFileAppendix
		self.userAgent = userAgent
		self.loginTestString = loginTestString
		self.debug = debug
		
		self.login()
		
	def modification_date(self, filename):
		"""
		return last file modification date as datetime object
		"""
		t = os.path.getmtime(filename)
		return datetime.datetime.fromtimestamp(t)
		
	def login(self, forceLogin = False):
		"""
		login to a session. Try to read last saved session from cache file. If this fails
		do proper login. If the last cache access was too old, also perform a proper login.
		Always updates session cache file.
		"""
		wasReadFromCache = False
		if self.debug:
			print('loading or generating session...')
		if os.path.exists(self.sessionFile) and not forceLogin:
			time = self.modification_date(self.sessionFile)
			
			# only load if file less than 30 minutes old
			lastModification = (datetime.datetime.now() - time).seconds
			if lastModification < self.maxSessionTime:
				with open(self.sessionFile, "rb") as f:
					self.session = pickle.load(f)
					wasReadFromCache = True
					if self.debug:
						print("loaded session from cache (last access %ds ago) "
						% lastModification)
		if not wasReadFromCache:
			self.session = requests.Session()
			self.session.headers.update({'user-agent' : self.userAgent})
			res = self.session.post(self.loginUrl, data = self.loginData, proxies = self.proxies)
			
			if self.debug:
				print('created new session with login' )
			self.saveSessionToCache()
			
		# test login
		res = self.session.get(self.loginTestUrl)
		if res.text.lower().find(self.loginTestString.lower()) < 0:
			raise Exception("could not log into provided site '%s'"
			" (did not find successful login string)"
			% self.loginUrl)
			
	def saveSessionToCache(self):
		"""
		save session to a cache file
		"""
		# always save (to update timeout)
		with open(self.sessionFile, "wb") as f:
			pickle.dump(self.session, f)
			if self.debug:
				print('updated session cache-file %s' % self.sessionFile)
				
	def retrieveContent(self, url, method = "get", postData = None):
		"""
		return the content of the url with respect to the session.
		
		If 'method' is not 'get', the url will be called with 'postData'
		as a post request.
		"""
		if method == 'get':
			res = self.session.get(url , proxies = self.proxies)
		else:
			res = self.session.get(url , data = postData, proxies = self.proxies)
			
		# the session has been updated on the server, so also update in cache
		self.saveSessionToCache()
		
		return res
		
if __name__ == "__main__":
	# proxies = {'https' : 'https://user:pass@server:port',
	#           'http' : 'http://user:pass@server:port'}
	
	loginData = {'user' : 'usr', 'password' :  'pwd'}
	
	loginUrl = 'https://...'
	loginTestUrl = 'https://...'
	successStr = 'Hello Tom'
	s = MyLoginSession(loginUrl, loginData, loginTestUrl, successStr,
	#proxies = proxies
	)
	
	res = s.retrieveContent('https://....')
	print(res.text)

