# coding: utf-8

# https://forum.omz-software.com/topic/2794/old-bugs/21

from __future__ import print_function
import twitter
account = twitter.get_all_accounts()[0]
def perform_search():
    data = twitter.search(account, 'Privacy OR Apple from:RepTedLieu',
                          parameters={'result_type': 'mixed'})
    for status in data['statuses']:
        print('> user: ', status['user']['screen_name'])
        print(status['text'])
        print("________________________>")

perform_search()