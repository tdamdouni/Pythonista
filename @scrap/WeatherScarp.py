# https://forum.omz-software.com/topic/2366/what-do-i-look-for-when-wanting-to-scrape-a-certain-thing

# coding: utf-8

import bs4, requests

def get_beautiful_soup(url):
    return bs4.BeautifulSoup(requests.get(url).text)

soup = get_beautiful_soup('http://www.weatherbug.com')

print(soup.get_text())