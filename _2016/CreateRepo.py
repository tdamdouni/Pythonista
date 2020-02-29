# coding: utf-8

# https://github.com/humberry/Github-Cheatsheet

from __future__ import print_function
import requests, json, dialogs

token = "InsertYourTokenHere"

fields=[{'type':'text', 'key':'repo_name', 'value':'', 'title':'Repository name:'}]
items = dialogs.form_dialog(title='CreateRepo', fields=fields, sections=None)
if items:
    repo_name = items.get('repo_name')
    if repo_name:
        url = 'https://api.github.com/user/repos'
        data = {"name": repo_name, "auto_init": True, "private": False}
        headers = {"Authorization": "token " + token}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code == 201:
            print('Success: Repo ' + repo_name + ' is created.')
        else:
            print('Error: ' + str(r))
    else:
        print('Error: No RepoName.')
