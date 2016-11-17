import urllib
import clipboard
import bs4
import webbrowser
import console

link = clipboard.get()

soup = bs4.BeautifulSoup(urllib.urlopen(link))
clipboard.set(soup.title.string +' '+ link)
text = clipboard.get()
console.clear()
print(text)

