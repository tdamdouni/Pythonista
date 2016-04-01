# coding: utf-8

# https://gist.github.com/greinacker/063d38995f3ca228a130

import sys
import clipboard
import requests
import webbrowser

url = sys.argv[1]
redir_urls = []

resp = requests.get(url, allow_redirects = False)
while resp.status_code == 301 or resp.status_code == 302:
  new_url = resp.headers["location"]
  redir_urls.append(new_url)
  resp = requests.get(new_url, allow_redirects = False)

clipboard.set(",".join(redir_urls))
webbrowser.open("workflow://")
