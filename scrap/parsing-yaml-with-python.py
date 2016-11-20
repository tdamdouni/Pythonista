# coding: utf-8

# Captured from: _https://forum.omz-software.com/topic/2216/parsing-yaml-with-python/6_

# yaml
---
title: "Mary had a little lamb"
link: http://google.com
---

###==============================

#coding: utf-8
import console
import yaml
import editor

from StringIO import StringIO
text = StringIO(editor.get_text())

doc = list(yaml.load_all(text))

tweet_link = doc["link"]
tweet_title = doc["title"]


console.hud_alert(tweet_link)

###==============================

my_dict = yaml.load(editor.get_text())

###==============================

#coding: utf-8
import yaml
import editor
import clipboard

m = yaml.load(editor.get_text().replace('-', ''))

tweet = m['title']

if "link" in m:
	tweet = tweet + ' ' + m['link']
	
clipboard.set(tweet)

###==============================

yaml_text = editor.get_text().rpartition('---')[0]
yaml_dict = yaml.load(yaml_text.partition('---')[2] or yaml_text)

###==============================

yaml_dict = yaml.load(editor.get_text().partition('---')[2].partition('---')[0])

