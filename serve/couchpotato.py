from __future__ import print_function
import requests
import console
import sys
import urllib
import webbrowser


## This script lets you add a movie to CouchPotato from LaunchCenterPro
# When you search for a movie, LCP will open with the results of that search.
# Pick a movie from that list, this script will add it and return to LCP if successful. 

# To search for a movie:
# couchpotato.py?argv=search&argv=searchterm
# Does a search with CP API, generates LCP [list] url and opens it
# Replace searchterm with a (partial) movie title

# To add a movie:
# couchpotato.py?argv=add&argv=movietitle&argv=imdb_id
# Adds a movie to CP. Searching for a movie will automatically generate a LCP list containing these URLs.
# Replace movietitle with a movie title. Has to be a title that came from a CP search (see above)
# Replace imdb_id with a valid imdb_id for the movie.

# CHANGE THESE VARIABLES TO YOUR OWN SETTINGS
api_key = 'YOUR_API_CODE'
base_url = 'http://www.couchpotatoserver.com'
# /CHANGE THESE


### STOP EDITING HERE, PROGRAM BELOW ###

# Constants
ADD = "add"
SEARCH = "search"

class CouchPotato():	
	def __init__(self, api_key, base_url):
		self.api_key = api_key
		self.base_url = base_url
	
	def get_api_url(self, api_method):
		return "{base_url}/api/{api_key}/{api_method}/".format(base_url=self.base_url, api_key=self.api_key, api_method=api_method)
	
	def do_api_call(self, url, params):
		api_call = requests.request('GET', url, params=params)
		if api_call.status_code > 300 or api_call.status_code < 200:
			print("API call failed, status code: {status_code}".format(status_code=api_call.status_code))
		return api_call

	def search(self, query):
		search_url = self.get_api_url('movie.search')
		search_params = {'q': query}
		return self.do_api_call(search_url, search_params)
	
	def add(self, title, imdb_id):
		add_url = self.get_api_url('movie.add')
		add_params = {
			'name': title,
			'identifier': imdb_id
		}
		
		return self.do_api_call(add_url, add_params)
		
	def generate_neat_name(self, movie_dict):
		return "{title} ({year})".format(title=movie_dict.get("original_title"), year=movie_dict.get("year"))


class LaunchCenterPro():
	def generate_menu(self, menu_title, menu_items):
		# Expects a string (menu_title) and a list consisting of tuples (menu_items).
		# Format for the tuples: 'menu item name', 'url'
		# The first 8 items will be shown
		menu_urls = list()
		for menu_item in menu_items[0:8]:
			formatted_menu_item = "{menu_item_name}={menu_item_url}".format(menu_item_name=menu_item[0], menu_item_url=menu_item[1])
			menu_urls.append(formatted_menu_item)
		encoded_menu_url = urllib.quote("launchpro://?url=[List:{menu_title}|{formatted_movie_urls}]".format(menu_title=menu_title, formatted_movie_urls="|".join(menu_urls)))
		
		return "launchpro://?url={encoded_menu_url}".format(encoded_menu_url=encoded_menu_url)
	
	def generate_confirm_message(self, message):
		# A kind of hacky way to create a confirm dialog
		ok_button = ("", ""),
		return self.generate_menu(message, ok_button)
	
	def return_to_lcp(self):
		webbrowser.open("launchpro://")

		
class PythonistaHelper():
	def current_script(self):
		return sys.argv[0].rsplit('/', 1)[-1]

	def generate_run_url(self, *args, **kwargs):
		# Use kwarg "argv_list" to add argv URL parameters
		run_url = "pythonista://{current_script}?action=run".format(current_script=self.current_script())
		
		if "argv_list" in kwargs:
			argv_list = kwargs.get("argv_list")
			argv_list = [urllib.quote(argv) for argv in argv_list]
			argv_joined = "&argv=".join(argv_list)
			run_url = "{run_url}&argv={argvs}".format(run_url=run_url, argvs=argv_joined)
		return run_url

def search_movie(query):
	cp = CouchPotato(api_key, base_url);
	search_results = cp.search(query)

	if search_results:
		json_response = search_results.json()
		if "movies" in json_response:
			movies = list()
			helper = PythonistaHelper()
			lcp = LaunchCenterPro()
			
			for movie in json_response["movies"][0:8]:
				movie_menu_item = cp.generate_neat_name(movie)
				argv_list = (ADD, movie.get("original_title"), movie.get("imdb"))
				movie_menu_url = helper.generate_run_url(argv_list=argv_list)
				movie_tuple = movie_menu_item, movie_menu_url
				movies.append(movie_tuple)
			
			lcp_url = lcp.generate_menu("What movie do you want to add to CouchPotato?", movies)
			webbrowser.open(lcp_url)
			
def add_movie(name, imdb_id):
	cp = CouchPotato(api_key, base_url);
	add_result = cp.add(name, imdb_id).json()
	if "success" in add_result and add_result.get('success') == True:
		lcp = LaunchCenterPro()
		confirm_url = lcp.generate_confirm_message("Movie added!")
		webbrowser.open(confirm_url)
	else:
		print(add_result)
		raise Exception("Failed to add movie!")


# The actual kickoff of the script
if len(sys.argv) > 2:
	# At least 3 argv's given
	if sys.argv[1] == ADD:
		add_movie(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == SEARCH:
		search_movie(sys.argv[2])
	else:
		raise Exception("Called the script without valid argv's!")
else:
	raise Exception("No sys.argv's given!")