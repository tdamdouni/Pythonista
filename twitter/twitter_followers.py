# coding: utf-8

# Copyright (c) 2016 Jesse Millar

import requests, clipboard, webbrowser

html = requests.get("http://www.twitter.com/tdamdouni").text

index = html.find("Followers</span>")
followers = html[index+82:index+85]

clipboard.set("@tdamdouni has " + followers + " Twitter followers.")

webbrowser.open("workflow://")

