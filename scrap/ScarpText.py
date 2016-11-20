# http://omz-forums.appspot.com/pythonista/post/5903606662299648
# coding: utf-8
import bs4, requests

def get_beautiful_soup(url):
    return bs4.BeautifulSoup(requests.get(url).text)

soup = get_beautiful_soup('http://omz-forums.appspot.com/pythonista')
print(soup.prettify())
# See: http://www.crummy.com/software/BeautifulSoup/bs4/doc for all the things you can do with the soup.