# https://gist.github.com/anonymous/c811a4e77f3f0a2eb575aa0e52dfa7e7

# https://forum.omz-software.com/topic/3821/google-cloud-python-libraries

from oauth2client import _helpers, _pure_python_crypt

def get_google_events(calendar_events):
	g = conf['google']
	
	with open(g['json_file'], 'r') as file_obj:
		client_credentials = json.load(file_obj)
	private_key_pkcs8_pem = client_credentials['private_key']
	signer = _pure_python_crypt.RsaSigner.from_string(private_key_pkcs8_pem)
	
	header = {'typ': 'JWT', 'alg': 'RS256'}
	now = int(time.time())
	payload = {
		'aud': 'https://www.googleapis.com/oauth2/v4/token',
		'scope': g['scopes'],
		'iat': now,
		'exp': now + 3600, # 1 hour in seconds
		'iss': g['email_address']
	}
	segments = [
		_helpers._urlsafe_b64encode(_helpers._json_encode(header)),
		_helpers._urlsafe_b64encode(_helpers._json_encode(payload)),
	]
	signing_input = b'.'.join(segments)
	signature = signer.sign(signing_input)
	segments.append(_helpers._urlsafe_b64encode(signature))
	claim = b'.'.join(segments)
	
	post_data = {
		'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer',
		'assertion':claim
	}
	req = requests.post('https://www.googleapis.com/oauth2/v4/token', post_data)
	resp = req.json()
	access_token = resp['access_token']
	auth_header = {
		'Authorization':'Bearer ' + access_token
	}
	calendar_url = 'https://www.googleapis.com/calendar/v3/calendars/mikael.honkala@gmail.com/events'
	
	hel_time = datetime.datetime.now(tz)
	start_time = hel_time.strftime('%Y-%m-%dT00:00:00+02')
	
	get_data = {
		'maxResults':100,
		'orderBy':'startTime',
		'singleEvents':'true',
		'timeMin':start_time
	}
	req = requests.get(calendar_url, params = get_data, headers = auth_header)
	#req = requests.get(calendar_list_url, headers = auth_header)
	resp = req.json()
	
	for item in resp['items']:
		start_time_item = item['start']
		start_time = parse_google_event_datetime(item['start'])
		end_time = parse_google_event_datetime(item['end'])
		event = {
			'summary': item.get('summary', ''),
			'location': item.get('location', ''),
			'start_time': start_time,
			'end_time': end_time
		}
		add_event(calendar_events, event)
	
	#return req.text
	#return json.dumps(resp['items'])
	#return str(req.status_code)
	
def parse_google_event_datetime(datetime_item):
	if datetime_item.get('date', False):
		datetime_text = datetime_item['date'] +  'T00:00:00'
	else:
		datetime_text = datetime_item['dateTime'][:19]
	datetime_object = datetime.datetime.strptime(datetime_text, '%Y-%m-%dT%H:%M:%S')
	datetime_object = datetime_object.replace(tzinfo = tz)
	return datetime_object
