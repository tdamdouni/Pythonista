# coding: utf-8

'''
cloud.py

Vision:

- cloud.Import: to make the entry curve to using code hosted on GitHub much easier

Credits:

- cloud.Import: idea and first version by @guerito, future versions on @webmaster4o's GitHub

'''

import bs4, console, cStringIO, html2text, importlib, inspect, os, pickle, plistlib, requests, shutil, zipfile

DOCS_DIR = os.path.expanduser('~/Documents')
SITE_DIR = os.path.join(DOCS_DIR, 'site-packages')
CLOUD_PKL = os.path.join(SITE_DIR, 'cloud.pkl')
URL = 'http://forum.omz-software.com/topic/2775/cloud-import'

def load_index(url):
	'''Load from the cloud the plist that serves as an index for all modules. For now,
	"the cloud" is XML posted on the omz:software forums, but that will change soon.'''
	soup = bs4.BeautifulSoup(requests.get(url).text) # BeautifulSoup object for the forum post
	for code in soup.find_all('code', class_='xml'): # Find all code blocks with the class "xml"
		s = code.get_text() # Get text from the code
		if s.startswith('<?xml'): # Is the code block valid xml?
			return plistlib.readPlistFromString(s) # Load plist from code and return
			
# A dict of all modules
module_index = load_index(URL)

def read_dict_from_pickle(pickle_file_name):
	try:
		with open(CLOUD_PKL, 'r') as f: # If so, open it,
			return pickle.Unpickler(f).load() # And then unpickle it
	except IOError:
		return {}
		
def Import(sTarget):
	''' Load a module from the cloud into the normal namespace. Equivalent to
	"import <sTarget>" but it will download the module from the cloud.'''
	
	# URL for the requested module
	try:
		urlZ = module_index[sTarget]
	except KeyError:
		return None  # do we really want to fail silently here?
		
	# Pickled dictionary of modules. Pairs each module name with the number of commits at the time of last update.
	d = read_dict_from_pickle(CLOUD_PKL)
	s = html2text.html2text(requests.get(urlZ).text) # Load the text of the GitHub repo linked
	
	# The number of commits that have been made (occurs just before "commits" in the text of the page)
	i = s.find('commits')
	iNow = int(s[i - 4:i - 1])
	
	# Find the previous number of commits (if installed before) by checking the dictionary
	try:
		iOld = d[sTarget.split('.')[0]]
	except KeyError:
		iOld = -1 # Fallback to -1
		
	# Module needs to be updated if number of commits now is greater than the number of commits at time of download, or if the module does not exist
	
	# The module may have been deleted
	try:
		reload(__import__(sTarget))
		nonexistant=False
	except ImportError:
		nonexistant=True
		
	if iNow > iOld or nonexistant:
		console.hud_alert('updating ' + sTarget + ' ...')
		urlZ += '/archive/master.zip' # URL for downloading a zip of the repo
		# Download zipfile and extract
		content = requests.get(urlZ, stream=True).content
		# Load into a StringIO file-like object to avoid having to save locally
		with zipfile.ZipFile(cStringIO.StringIO(content)) as zip_file:
			for member in zip_file.namelist(): # Iterate through all files in zip
				l = member.split('/') # Split path to file
				# Just two levels deep into the zip, this is part of a moule
				if len(l) <= 2 and l[-1][-3:] == '.py': # It's a module, and it's a python source file
					# Extract the file and move it from the temp dir to site-packages
					zip_file.extract(member, DOCS_DIR)
					shutil.move(os.path.join(DOCS_DIR, member), os.path.join(SITE_DIR, l[-1]))
					
				elif l[1] == sTarget.split('.')[0] and l[-1] != '': # We're deeper into the module
					zip_file.extract(member, DOCS_DIR) # Extract to documents
					dest_path = os.path.join(SITE_DIR, l[-2]) # The path in which the package will live
					if not dest_path: # Make a folder for this module if it doesn't exist
						os.mkdir(dest_path)
					# Move the file to the site-packages folder
					shutil.move(os.path.join(DOCS_DIR, member), os.path.join(dest_path, l[-1]))
					
		shutil.rmtree(os.path.join(DOCS_DIR, l[0]))
	# Load the main module
	locals()[sTarget.split('.')[0]] = importlib.import_module(sTarget.split('.')[0]) # Load the top level module
	reload(locals()[sTarget.split('.')[0]]) # Reload the top-level module
	# Load a submodule
	if len(sTarget.split('.')) != 1: # A submodule was imported
		locals()[sTarget.split('.')[1]] = importlib.import_module(sTarget) # Load the submodule
		reload(locals()[sTarget.split('.')[1]]) # Reload the submodule
	# Load into the local namespace
	inspect.currentframe().f_back.f_globals[sTarget.split('.')[0]] = locals()[sTarget.split('.')[0]]
	
	# Set the current version
	d[sTarget.split('.')[0]] = iNow
	with open(CLOUD_PKL, 'w') as f:
		pickle.Pickler(f).dump(d)
		
if __name__ == "__main__":
	Import("Gestures")

