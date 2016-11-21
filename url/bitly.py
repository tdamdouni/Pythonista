import requests
import keychain

def shorten_url(long_url):
	USER = ''
	API_KEY = keychain.get_password('bitly', USER)
	
	bitly_url = 'http://api.bit.ly/v3/shorten'
	
	s = requests.Session()
	payload = {'login': USER, 'APIKEY': API_KEY, 'URI': long_url}
	short_url = s.get(bitly_url, params = payload).json['data']['url']
	
	return short_url

