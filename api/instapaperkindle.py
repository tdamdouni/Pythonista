#!/usr/local/bin/python

import requests
import re
import keychain

mypass = keychain.get_password('instapaper', 'n8henrie@gmail.com')

s = requests.Session()
login_url = 'http://www.instapaper.com/user/login'


payload = {'username': 'n8henrie@gmail.com', 'password': mypass}
s.post(login_url, data=payload)

user_url = 'http://www.instapaper.com/user'
send_url = 'http://www.instapaper.com/user/kindle_send_now'

get_form_key = s.get(user_url).content
form_key = re.search(r'<input type="hidden" id="form_key_send_now" name="form_key" value="([a-zA-Z0-9]+)"/>', get_form_key).group(1)

send_params = {'form_key': form_key}
s.post(send_url, data=send_params)

