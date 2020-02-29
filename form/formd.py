#!/usr/bin/env python
# encoding=utf8

# http://3e156c33bb09beb35fd0-19fc75fdc34cce7558ab01263b95946a.r86.cf1.rackcdn.com/formd.py

"""
Seth Brown
02-24-12
"""
from __future__ import print_function

from sys import stdin, stdout
import re
from collections import OrderedDict

class ForMd(object):
	"""Format mardown text"""
	def __init__(self, text):
		super(ForMd, self).__init__()
		self.text = text
		self.match_links = re.compile(r'(\[[^^]*?\])\s?(\[.*?\]|\(.*?\))',
		re.DOTALL | re.MULTILINE)
		self.match_refs = re.compile(r'(?<=\n)\[[^^]*?\]:\s?.*')
		self.data = []
		
	def _links(self, ):
		"""find Markdown links"""
		links = re.findall(self.match_links, self.text)
		for link in links:
			# remove newline breaks from urls spanning multi-lines
			parsed_link = [s.replace('\n','') for s in link]
			yield parsed_link
			
	def _refs(self):
		"""find Markdown references"""
		refs = re.findall(self.match_refs, self.text)
		refs.sort()
		refs = OrderedDict(i.split(":", 1) for i in refs)
		return refs
		
	def _format(self):
		"""process text"""
		links = (i for i in self._links())
		refs = self._refs()
		for n, link in enumerate(links):
			text, ref = link
			ref_num = ''.join(("[",str(n+1),"]: "))
			if ref in refs.keys():
				url = refs.get(ref).strip()
				formd_ref = ''.join((ref_num, url))
				formd_text = ''.join((text, ref_num))
				self.data.append([formd_text, formd_ref])
			elif text in refs.keys():
				url = refs.get(text).strip()
				formd_ref = ''.join((ref_num, url))
				formd_text = ''.join((text, ref_num))
				self.data.append([formd_text, formd_ref])
			elif ref not in refs.keys():
				parse_ref = ref.strip("()")
				formd_ref = ''.join((ref_num, parse_ref))
				formd_text = ''.join((text,ref_num))
				self.data.append([formd_text, formd_ref])
				
	def inline_md(self):
		"""generate inline markdown """
		self._format()
		text_link = iter([''.join((_[0].split("][",1)[0],
		"](", _[1].split(":",1)[1].strip(), ")")) for _ in self.data])
		formd_text = self.match_links.sub(lambda _: next(text_link), md)
		formd_md = self.match_refs.sub('', formd_text).strip()
		yield formd_md
		
	def ref_md(self):
		"""generate referenced markdown"""
		self._format()
		ref_nums = iter([_[0].rstrip(" :") for _ in self.data])
		formd_text = self.match_links.sub(lambda _: next(ref_nums), md)
		formd_refs = self.match_refs.sub('', formd_text).strip()
		references = (i[1] for i in self.data)
		formd_md = '\n'.join((formd_refs, '\n', '\n'.join(i for i in references)))
		yield formd_md
		
	def flip(self):
		"""convert markdown to the opposite style of the first text link"""
		first_match = re.search(self.match_links, self.text).group(0)
		if '(' and ')' in first_match:
			formd_md = self.ref_md()
		else:
			formd_md = self.inline_md()
		return formd_md
		
if __name__ == '__main__':
	import clipboard
	import console
	md = clipboard.get()
	if md:
		console.clear()
		text = ForMd(md)
		[clipboard.set(t) for t in text.flip()]
		final = clipboard.get()
		print(final)

