# http://omz-forums.appspot.com/pythonista/post/5253563362050048
# coding: utf-8
import bs4, requests

def get_beautiful_soup(url):
    return bs4.BeautifulSoup(requests.get(url).text)

soup = get_beautiful_soup('http://amdouni.com')

print(soup.prettify())

links = []
for anchor in soup.find_all('a'):  # tags like: <a href='http...'
    try:
        link = anchor['href']
        if link.startswith('http'):
            links.append(link)
    except KeyError:
        pass
print('\n'.join(sorted(set(links))))

print('=' * 40)  # print the text of the body of the webpage without all  the html junk
print(soup.body.get_text())  # get the body of the soup, and then get only the text of that
print('=' * 40)  # contains lots of blank lines... let's get rid of the blank lines
for line in soup.body.get_text().splitlines():
    if line.strip():
        print(line)
print('=' * 40)  # another way to write the three previous lines uses a list comprehension and str.join()
print('\n'.join([x for x in soup.body.get_text().splitlines() if x.strip()]))
print('=' * 40)  # contains lots of lines that have indentation... left justify all lines
for line in soup.body.get_text().splitlines():
    if line.strip():
        print(line.lstrip())
print('=' * 40)  # rewritten using a list comprehension and str.join()
print('\n'.join([x.lstrip() for x in soup.body.get_text().splitlines() if x.strip()]))