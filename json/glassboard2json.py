#!/usr/bin/env python

"""
This script converts a Glassboard HTML archive to JSON.

Usage:
python glassboard2json.py glassboard_export/index.html -o output_file.json

Requirement: BeautifulSoup4 (bs4)

Notes: Nested replies are not fully supported, all posts that belong to a thread are exported as a flat list.
Attachments/images are not supported at all.

The output has the following structure:

{
  "threads": [
    [
      {
        "username": "Board Owner",
        "date": "2012-10-18 01:25:00",
        "text": "Board created for Board Owner"
      }
    ],
    [
      {
        "username": "Board Owner",
        "date": "2012-10-18 01:30:00",
        "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt."
      },
      {
        "username": "User 1",
        "date": "2012-10-18 01:32:00",
        "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt."
      }
    ]
  ]
  "users": [
    "Board Owner",
    "User 1"
  ],
  "title": "Board Title"
}
"""
from __future__ import print_function

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path', help='The index.html file from the Glassboard export')
	parser.add_argument('-o', '--output', help='The output file (default: stdout)')
	args = parser.parse_args()
	
	input_path = args.input_path
	output_path = args.output
	from bs4 import BeautifulSoup
	import re
	from datetime import datetime
	import json
	with open(input_path, 'r') as f:
		html_doc = f.read()
		# Workaround:
		# Glassboard doesn't escape "<title>" tags in posts correctly, which causes bs4 (and Safari) to choke.
		# I'd guess that there are some other cases that the Glassboard exporter doesn't handle correctly.
		html_doc = html_doc.replace('<title>', '&lt;title&gt;')
	soup = BeautifulSoup(html_doc)
	posts = soup.find_all('div', attrs={'class': re.compile('(status|comment)Div')})
	board_title_element = soup.find('span', attrs={'class': 'boardTitle'})
	board_title = board_title_element.get_text()
	current_thread = []
	all_threads = []
	all_users = set()
	for post in posts:
		post_class = post.attrs['class'][0]
		text = post.get_text().strip()
		lines = text.splitlines()
		post_text = '\n'.join(lines[1:])
		metadata = lines[0]
		match = re.search('(.*?)((January|February|March|April|May|June|July|August|September|October|November|December).*)', metadata)
		username = match.group(1).strip()
		all_users.add(username)
		date_string = match.group(2)
		dt = datetime.strptime(date_string, '%B %d, %Y - %I:%M %p GMT')
		if post_class == 'statusDiv':
			if current_thread:
				all_threads.append(current_thread)
			current_thread = [{'username': username, 'date': dt.isoformat(' '), 'text': post_text}]
		else:
			current_thread.append({'username': username, 'date': dt.isoformat(' '), 'text': post_text})
	if current_thread:
		all_threads.append(current_thread)
		
	output = {'title': board_title, 'threads': all_threads, 'users': list(all_users)}
	if output_path:
		with open(output_path, 'w') as f:
			json.dump(output, f, indent=2)
	else:
		print(json.dumps(output, indent=2))
		
if __name__ == '__main__':
	main()

