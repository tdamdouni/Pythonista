import editor
import console
import os
import re
import sys
import codecs
import workflow
from StringIO import StringIO

# Set CSS theme
theme = editor.get_theme()
workflow.set_variable('CSS', workflow.get_variable('CSS Dark' if theme == 'Dark' else 'CSS Light'))

# Set Variables
p = editor.get_path()
console.clear()
term = workflow.get_variable('Search Term')
pattern = re.compile(re.escape(term), flags=re.IGNORECASE)
term_array = term.split()
for i in range(len(term_array)):
		term_array[i] = re.escape(term_array[i])
from urllib import quote
dir = os.path.split(p)[0]
valid_extensions = set(['.txt', '.md', '.markd', '.text', '.mdown', '.taskpaper'])
html = StringIO()
filename_match = 0
content_match = 0
match_count = 0

# Iterate over fienames against search terms and output if match found

for w in os.walk(dir):
	dir_path = w[0]
	filenames = w[2]
	match_check = 0
	for name in filenames:
			filename_match = 0
			full_path = os.path.join(dir_path, name)
			ext = os.path.splitext(full_path)[1]
			if ext.lower() not in valid_extensions:
					continue

			x = 0

			try:
					for n in range(len(term_array)):
							if re.search(term_array[n].lower(), name.lower()):
									x += 1
			except UnicodeDecodeError, e:
					pass

			if x == len(term_array):
					match_count += 1
					filename_match += 1
					match_check += 1
					root, rel_path = editor.to_relative_path(full_path)
					ed_url = 'editorial://open/' + quote(rel_path.encode('utf-8')) + '?root=' + root
					html.write('<h2><a href="' + ed_url + '">' + name + '</a></h2>')

			found_snippets = []
			i = 0
			try:
					with codecs.open(full_path, 'r', 'utf-8') as f:
						if term in f.read():
							for line in f:
								for match in re.finditer(pattern, line):
									start = max(0, match.start(0) - 100)
									end = min(len(line)-1, match.end(0) + 100)
									snippet = (line[start:match.start(0)],
															match.group(0),
															line[match.end(0):end],
															match.start(0) + i,
															match.end(0) + i)
									found_snippets.append(snippet)
									match_count += 1
									i += len(line)
			except UnicodeDecodeError, e:
					pass


			if len(found_snippets) > 0:
					match_count += 1
					root, rel_path = editor.to_relative_path(full_path)
					if filename_match == 0:
							ed_url = 'editorial://open/' + quote(rel_path.encode('utf-8')) + '?root=' + root
							html.write('<h2><a href="' + ed_url + '">' + name + '</a></h2>')
					for snippet in found_snippets:
							start = snippet[3]
							end = snippet[4]
							select_url = 'editorial://open/' + quote(rel_path.encode('utf-8')) + '?root=' + root
							select_url += '&selection=' + str(start) + '-' + str(end)
							html.write('<a class="result-box" href="' + select_url + '">' + snippet[0] + '<span class="highlight">' + snippet[1] + '</span>' + snippet[2] + '</a>')

if match_count == 0:
	html.write('<p>No matches found.</p>')

workflow.set_output(html.getvalue())





#           html.write('<h2><a href="' + ed_url + '">' + name + '</a></h2>')
# Output no match found
#if match_count == 0:
#   html.write('<p>No matches found.</p>' + 'term var = ' + str(term_array) )
#workflow.set_output(html.getvalue())
