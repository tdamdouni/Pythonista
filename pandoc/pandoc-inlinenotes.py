# coding: utf-8

# https://gist.github.com/wcaleb/17ca606788f9b4b9a36b

#!/usr/bin/env python

from pandocfilters import toJSONFilter, RawInline, Space, Str, walk

"""
Pandoc filter for Markdown that converts most endnotes into
Pandoc's inline notes. If input notes had multiple paragraphs,
the paragraphs are joined by a space. But if an input note
had any blocks other than paragraphs, the note is left as is.
"""

def query(k, v, f, meta):
	global inlines
	if k == 'BlockQuote':
		inlines.append(v)
	elif isinstance(v, list):
		if inlines and k == 'Para':
			inlines.append(Space())
		inlines.extend(v)
	return v
	
def inlinenotes(k, v, f, meta):
	global inlines
	inlines = []
	if k == 'Note' and f == 'markdown':
		walk(v, query, f, meta)
		if all(isinstance(x, dict) for x in inlines):
			return [RawInline('html', '^[')] + inlines + [Str(']')]
			
if __name__ == "__main__":
	toJSONFilter(inlinenotes)

