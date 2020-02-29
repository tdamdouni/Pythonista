from __future__ import print_function
# https://gist.github.com/dlo/4644960

import clipboard
import console
import requests
import json
import keychain
import webbrowser
from datetime import datetime

argument_index = 1

try:
    username = sys.argv[argument_index]
    argument_index += 1
except IndexError:
    username = "dlo"

default_extension = ".crash"

try:
    filename = sys.argv[argument_index]
    argument_index += 1
except IndexError:
    now = datetime.now()
    filename = "{}{}".format(now.strftime("%Y-%m-%d %H:%M:%S"), default_extension)
    content = clipboard.get()
    public = False
else:
    try:
        content = sys.argv[argument_index]
        argument_index += 1
    except IndexError:
        content = clipboard.get()

    # Gists created are private by default
    try:
        public = sys.argv[public_index] == "public"
    except:
        public = False

# Check if the user has already authenticated
access_token = keychain.get_password("GitHub", username)
if access_token is None:
    try:
        username, password = console.login_alert("GitHub Login")
    except KeyboardInterrupt:
        pass
    else:
        data = json.dumps({ "scopes": ["gist"], "note": "Pythonista"})
        console.show_activity()
        response = requests.post("https://api.github.com/authorizations", data=data, auth=(username, password))
        console.hide_activity()
        if response.status_code == 201:
            access_token = response.json['token']
            keychain.set_password("GitHub", username, access_token)
        else:
            console.alert("Invalid credentials. Exiting.")
            sys.exit(0)

data = json.dumps({"public": public, "files": {filename: {'content': content} }})
console.show_activity()
response = requests.post("https://api.github.com/gists?access_token={}".format(access_token), data=data)
console.hide_activity()
if response.status_code == 201:
    clipboard.set(response.json['html_url'])
    button_id = console.alert("Success", "Gist was successfully created.", "Open in Drafts")
    if button_id == 1:
        webbrowser.open("drafts://x-callback-url/create?text={}".format(response.json['html_url']))
else:
    console.alert("Couldn't create Gist.")
    print(response.content)
