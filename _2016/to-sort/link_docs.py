'''
link_docs doc_A_file_or_url doc_B_file_or_url
Automatically generate hyperlinks from doc A to doc B

'''
import requests
import bs4
import io
import re
import sys

def links_for_terms(url):
	'''
	Given the URL of an HTML document,
	find things that look like defined terms with
	IDs; return those terms with links to them, like
	
	{'cow': 'http://mypage.html#cow',
	'fish': 'http://mypage.html#fish'}
	'''
	response = requests.get(url)
	text = response.content.decode(response.encoding)
	soup = bs4.BeautifulSoup(text)
	result = {}
	for tag in soup.findAll('a'):
		if 0 < len(tag.text.split()) < 5:
			result[tag.text.lower()] = '%s%s' % (url, tag['href'])
	return result
	
# Things that appear to be ``dt``s in definition lists.
# The ``dt`` value goes in ``\1``, the ``dd`` in ``\2``.
dt_pattern = re.compile('^(\w+.*?)(\n  \w)', re.DOTALL)

not_indented = re.compile(r'^\S')
indented_two = re.compile(r'  \S')

def hyperlinked_rst(rst_filename, url):
	'''
	Finds defined terms in definition lists
	in ``rst_filename``, finds corresponding
	linkable anchors in ``url``, returns version
	of rst with added hyperlinks
	'''
	
	links = links_for_terms(url)
	
	with open(rst_filename, 'r') as infile:
		raw_content = infile.read()
		cooked_content = []
		new_links = set()
		for raw_line in raw_content.splitlines():
			if 'ackage' in raw_line:
				#import ipdb; ipdb.set_trace()
				pass
			line = raw_line.rstrip()
			if (indented_two.search(line)
			and cooked_content
			and not_indented.search(cooked_content[-1])
			and not cooked_content[-1].endswith('_')
			):
				core_term = cooked_content[-1].strip().lower()
				for term in (core_term, core_term[:-1],
				'%ss' % core_term):
					if term in links:
						new_links.add('.. _`%s`: %s' % (cooked_content[-1],
						links[term.lower()]))
						cooked_content[-1] = '`%s`_' % cooked_content[-1]
			cooked_content.append(raw_line)
		new_content = '%s\n\n%s' % ('\n'.join(cooked_content),
		'\n\n'.join(new_links))
		return new_content
		
if __name__ == '__main__':
	print(hyperlinked_rst(*sys.argv[1:3]))

