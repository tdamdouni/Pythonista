# https://chihacknight.org/blog/2014/11/26/an-intro-to-web-scraping-with-python.html

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.akc.org/reg/dogreg_stats.cfm"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

table = soup.find_all('table')[1]
rows = table.find_all('tr')[2:]

data = {
    'breeds' : [],
    'rank2013' : [],
    'rank2012' : [],
    'rank2008' : [],
    'rank2003' : []
}

for row in rows:
	cols = row.find_all('td')
	data['breeds'].append( cols[0].get_text() )
	data['rank2013'].append( cols[1].get_text() )
	data['rank2012'].append( cols[2].get_text() )
	data['rank2008'].append( cols[3].get_text() )
	data['rank2003'].append( cols[4].get_text() )
	
dogData = pd.DataFrame( data )
dogData.to_csv("AKC_Dog_Registrations.csv")

