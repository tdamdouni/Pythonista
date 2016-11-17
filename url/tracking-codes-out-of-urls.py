# Assumptions:
#
#   - used with Pythonista on iOS
#   - successful install of the Extraction module https://pypi.python.org/pypi/extraction
#     through pipista and yak shaving with shellista

# Initially based on http://blog.ouseful.info/2010/10/26/more-python-floundering-stripping-google-analytics-tracking-codes-out-of-urls/

import cgi, urllib, urlparse, webbrowser, sys, console, clipboard, requests, extraction

def choose_action(url):
	choice = console.alert('URL Cruft', '', 'Safari', 'Instapaper', 'More')
	if choice == 1:
		webbrowser.open("safari-" + url)
	elif choice == 2:
		webbrowser.open('i' + url)
	elif choice == 3:
		second_choice = console.alert("More",  '', 'Instapaper + Safari', 'Clipboard', 'Even More')
		if second_choice == 1:
			webbrowser.open("x-callback-instapaper://x-callback-url/add?url=" + url + "&x-success=" + url)
		elif second_choice == 2:
			clipboard.set(url)
		else:
			third_choice = console.alert("Even More", '', 'Delicious', 'Reading List')
			if third_choice == 1:
				clipboard.set(url)
				webbrowser.open("delicious://")
			elif third_choice == 2:
				webbrowser.add_to_reading_list(url)
				
argLen = len(sys.argv)

if argLen > 1:
	url = sys.argv[1]
else:
	url = clipboard.get()
	
p = urlparse.urlparse(url)
subdomain = p.hostname.split('.')[0]
if subdomain == 'm' or subdomain == 'mobile' or subdomain == 'on':
	html = requests.get(url).text
	extracted = extraction.Extractor().extract(html, source_url=url)
	
	urlLength = len(extracted.url)
	
	if urlLength > 1:
		url = extracted.url
		choose_action(url)
else:
	# p[4] contains query string arguments
	q = cgi.parse_qs(p[4])
	qt = {}
	
	stopkeys = [
	'email_blob',
	'mp_props',
	'_r', # New York Times
	'pagewanted', # New York Times
	'utm_source',
	'utm_medium',
	'utm_term',
	'utm_campaign',
	'mobify', # The New Yorker, after requesting the 'desktop' version
	'intcid',
	'cmp',
	'smid',
	'utm_cid',
	'utm_content',
	'fsrc',
	'src',
	'm'
	]
	for i in q:
		if i not in stopkeys:
			qt[i]=q[i][0]
			
	ptwo = urllib.urlencode(qt)
	ptwo = (p[0],p[1],p[2],p[3],ptwo,p[5])
	choose_action(urlparse.urlunparse(ptwo))

