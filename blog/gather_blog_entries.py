# [blog-entries-to-markdown](http://omz-forums.appspot.com/editorial/post/5307688003043328)
# Gather up an OrderedDict of blog entries, present as list, generate markdown from selected items

import bs4, collections, json, requests
url = 'https://www.ibm.com/developerworks/community/blogs/MartinPacker/?maxresults=500'
filename = 'Martin_Packer_blog.json'
print('=' * 56)
print('Downloading blog urls... This may take up to 60 seconds.')
soup = bs4.BeautifulSoup(requests.get(url).text)
entries = [x for x in soup.find_all('a', href=True, id=True) if '/entry/' in str(x)]
print('{} blog entries found.'.format(len(entries)))
entries_dict = collections.OrderedDict()
for entry in entries:
    entries_dict[entry.text.strip()] = entry['href'][:-8]  # '?lang=en'
with open(filename, 'w') as out_file:
    json.dump(entries_dict, out_file)
md_text = '\n'.join('1.  [{}]({})'.format(k, v) for k, v in entries_dict.iteritems())
with open(filename.replace('.json', '.md'), 'w') as out_file:
    out_file.write(md_text)
for key, value in entries_dict.iteritems():
    print('{}\n\t{}'.format(key, value))