# http://stackoverflow.com/questions/12737740/python-requests-and-persistent-sessions

if __name__ == "__main__":
	# proxies = {'https' : 'https://user:pass@server:port',
	#           'http' : 'http://user:pass@server:port'}
	
	loginData = {'user' : 'usr',
	'password' :  'pwd'}
	
	loginUrl = 'https://...'
	loginTestUrl = 'https://...'
	successStr = 'Hello Tom'
	s = MyLoginSession(loginUrl, loginData, loginTestUrl, successStr,
	#proxies = proxies
	)
	
	res = s.retrieveContent('https://....')
	print(res.text)

