# pythonista Forum Web Scarping Text
# coding: utf-8
import bs4, requests
import webbrowser
import console

def get_beautiful_soup(url):
    return bs4.BeautifulSoup(requests.get(url).text)
a = raw_input('url to check. url structure (http://www.url.com or net or gov or org)     ')
console.clear()
soup = get_beautiful_soup(a)
webbrowser.open('http://amdouni.com')

print(soup.prettify())