# coding: utf-8

# https://gist.github.com/phillipsm/8afdcf295b90691810e5

# Python 3 version of Journalist's Resource Tip Sheet web scraping script

import requests, time
from bs4 import BeautifulSoup

# We've now imported the two packages that will do the heavy lifting
# for us, reqeusts and BeautifulSoup

# This is the URL that lists the current inmates
# Should this URL go away, and archive is available at
# http://perma.cc/2HZR-N38X
url_to_scrape = 'http://apps2.polkcountyiowa.gov/inmatesontheweb/'

# Tell the requests package to retreive the contents our page (it'll be
# grabbing what you see when you use the View Source feature in your browser)
r = requests.get(url_to_scrape)

# We now have the source HTML of the page. Let's ask BeaultifulSoup
# to parse it for us.
soup = BeautifulSoup(r.text, "html.parser")

# Down below we'll add our inmates to this list. For now,
# it's just a placeholder.
inmates_links = []

# Our source document puts each inmate in an HTML table row. Let's
# loop through all of those rows
for table_row in soup.select(".inmatesList tr"):

	# Each table row has a set of tabel cells, or tds. Let's
	# get all of those.
	table_cells = table_row.findAll('td')
	
	# Our table has one exception -- a row without any cells.
	# Let's handle that special case here by making sure we
	# have more than zero cells before processing the cells
	if len(table_cells) > 0:
	
		# By looking at our source (probably easiest in your browser), we can
		# see that the link is in the first td of each row. Let's extract the
		# value of that link here.
		#
		# Should this link pattern change, find an archive of an
		# example at http://perma.cc/RTU7-57DL
		relative_link_to_inmate_details = table_cells[0].find('a')['href']
		
		# The links to the inmates are relative (they look
		# like Details.aspx?bi=212840). We need to make them absolute links.
		# We do that by prepending our base URL (which conveniently is the same
		# one we used to get the list of inmates.)
		absolute_link_to_inmate_details = url_to_scrape + relative_link_to_inmate_details
		
		# We're done getting the link to the inmate details. Let's add it
		# to our list of inmates for later use
		inmates_links.append(absolute_link_to_inmate_details)
		
# Down below we'll add our inmates details to this list. For now,
# it's just a placeholder.
inmates = []

# Loop through the list of inmate links we built
# Since the inmate list is several hunderd links in total,
# we might want to slice just a few off for testing. Here, we start with five.
for inmate_link in inmates_links[:10]:

		# Once again we'll use requests to get the HTML of our link
		# and use beautiful soup to process it.
	r = requests.get(inmate_link)
	soup = BeautifulSoup(r.text, "html.parser")
	
	
	# We'll put the details we want to hang on to in this dictionary
	inmate_details = {}
	
	# Get all of our table rows in the inmateProfile table
	inmate_profile_rows = soup.select("#inmateProfile tr")
	
	# Inmate age
	# From looking at the HTML source (using View Source in our browser)
	# we see that age is in the first row and the first table cell (td)
	# We use the strip function to cleanup unwanted spaces
	inmate_details['age'] = inmate_profile_rows[0].findAll('td')[0].text.strip()
	
	# Inmate race
	# Race and naem are in our same inmateProfile table, we just find
	# the correct row
	inmate_details['race'] =  inmate_profile_rows[3].findAll('td')[0].text.strip()
	
	# Inmate sex
	inmate_details['sex'] =  inmate_profile_rows[4].findAll('td')[0].text.strip()
	
	
	# Get all of our table rows in the inmateNameDate table
	inmate_name_date_rows = soup.select("#inmateNameDate tr")
	
	# Inmate name
	inmate_details['name'] =  inmate_name_date_rows[1].findAll('td')[0].text.strip()
	
	# Inmate booking time
	inmate_details['booked_at'] = inmate_name_date_rows[2].findAll('td')[0].text.strip()
	
	
	# Get all of our table rows in the inmateNameDate table
	inmate_address_container = soup.select("#inmateAddress")
	
	inmate_details['city'] =  inmate_address_container[0].text.split('\n')[2].strip()
	
	
	# Now that we have all of the inmate details extracted and placed in a
	# dictionary, let's append that dictionary to our list
	inmates.append(inmate_details)
	
	
	# We don't want to overwhelm the Polk County site. Let's pause for one
	# second between each inmate request.
	time.sleep(1)
	
	
# We now have details (in our dictionary) for each inmate. Let's print those out.
for inmate in inmates:
	print('{0}, {1}'.format(inmate['name'], inmate['age']))
	print('{0} {1} from {2}'.format(inmate['race'], inmate['sex'], inmate['city']))
	print('Booked at {0}r'.format(inmate['booked_at']))
	print('')
	
	
# We might want to do more than just print out our numbers though. Maybe
# we want to see count up each inmate's city and print it out.s
inmate_cities =  {}

for inmate in inmates:

	# If we haven't seen the inmate's city already, add it to our
	# dictionary with the value of 1. Otherwise, just add 1.
	if inmate['city'] in inmate_cities:
		inmate_cities[inmate['city']] += 1
	else:
		inmate_cities[inmate['city']] = 1
		
print('Inmate city distribution')
print(inmate_cities)
print('')

# Or, each inmate's race
inmate_races =  {}

for inmate in inmates:
	if inmate['race'] in inmate_races:
		inmate_races[inmate['race']] += 1
	else:
		inmate_races[inmate['race']] = 1
		
print('Inmate race distribution')
print(inmate_races)

