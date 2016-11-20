# coding: utf-8

# https://gist.github.com/wcaleb/9fe0116169754763a3c2

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pandoc filter that grabs the BibTeX code block from each note file
# and then uses bibtexparser to add a "short title" entry in the "note" field,
# appending finished BibTeX entry to a bibliography file.

from pandocfilters import toJSONFilter, CodeBlock
# https://github.com/sciunto/python-bibtexparser
import bibtexparser

def bibtex(key, value, format, meta):
	if key != 'CodeBlock':
		return []
	else:
		format, s = value
		s = s.encode('utf-8')
		with open('/tmp/chunk.bib', 'w') as bibfile:
			bibfile.write(s)
		with open('/tmp/chunk.bib', 'r') as bibfile:
			bp = bibtexparser.load(bibfile)
			for record in bp.get_entry_list():
				longtitle = record['title']
				abbrtitle = longtitle.partition(':')[0]
				note = '    note = {' + abbrtitle + '},\n}'
		value[1] = s.rstrip('\}') + note.encode('utf-8')

if __name__ == "__main__":
	toJSONFilter(bibtex)