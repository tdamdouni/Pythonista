from urllib2 import urlopen
import csv
import json
import pprint
import nltk

# JSON reading
url_json = "http://wikilit.referata.com/" + \
			"wiki/Special:Ask/" + \
			"-5B-5BCategory:Publications-5D-5D/" + \
			"-3FHas-20author/-3FYear/" + \
			"-3FPublished-20in/-3FAbstract/-3FHas-20topic)/" + \
			"-3FHas-20domain/" + \
			"format%3D-20json"

# 'response' is a hash/dictionary
print 'Retrieving ', url_json
#response = json.load(urlopen(url_json))
#pprint.pprint(response.keys())


url = "http://wikilit.referata.com/" + \
		"wiki/Special:Ask/" + \
		"-5B-5BCategory:Publications-5D-5D/" + \
		"-3FHas-20author%3DAuthor(s)/-3FYear/" + \
		"-3FPublished-20in/-3FAbstract/-3FHas-20topic%3DTopic(s)/" + \
		"-3FHas-20domain%3DDomain(s)/" + \
		"format%3D-20csv/limit%3D-20100/offset%3D0"

# Get and read the web page
print '\nRetrieving ', url
#doc = urlopen(url).read()			# Object from urlopen has read method

# 'web' is a file-like handle
web = urlopen(url)

# 'lines' is an object that can be iterated over
lines = csv.reader(web, delimiter=',', quotechar='"')

header = []
papers = []
# Iterate over 'lines'
print '\nProcessing csv.reader'
for row in lines:
	# csv module lacks unicode support
	line = [unicode(cell, 'utf-8') for cell in row]
	if not header:
		header = line
		continue
	papers.append(dict(zip(header, line)))

# 'papers' is now a list of dictionaries
# get words from first abstract
#nltk.word_tokenize(papers[0]['Abstract'])

# convert each word to lowercase
print '\nConverting all words to lowercase'
#map(lambda word: word.lower(), papers[0]['Abstract'])

# now for all papers
for paper in papers:
	words = map(lambda word: word.lower(), nltk.word_tokenize(paper['Abstract']))
	paper['words'] = words 

# save papers to a JSON file
print '\nSaving papers to papers.json.'
json.dump(papers,open('papers.json','w'))
