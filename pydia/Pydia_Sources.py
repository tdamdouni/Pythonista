# coding: utf-8

# https://gist.github.com/bmw1821/bc2ccf257d60804be010

from __future__ import print_function
import os

class Source (object):

	def __init__(self, identifier, name, url, description, packages):
		self.identifier = identifier
		self.name = name
		self.url = url
		self.description = description
		self.packages = packages
		
def source_from_dict(source_dict, source_url):
	import Pydia_Package
	
	identifier = source_dict['identifier']
	
	name = source_dict['name']
	
	url = source_url
	if not url:
		url = source_dict['url']
		
	description = source_dict['description']
	
	raw_packages = source_dict['packages']
	
	packages = []
	
	for raw_package in raw_packages:
	
		package_identifier = raw_package['identifier']
		
		package_name = raw_package['name']
		
		package_author = raw_package['author']
		
		package_description = raw_package['description']
		
		package_version = raw_package['version']
		
		package_main_package_files = raw_package['main-package-files']
		
		package_install_script_url = raw_package.get('install-script-url', None)
		
		package_supporting_files = raw_package.get('supporting-files', [])
		
		package_dependencies = raw_package.get('dependencies', [])
		
		packages.append(Pydia_Package.Package(package_identifier, identifier, package_name, package_author, package_description, package_version, package_main_package_files, package_install_script_url, package_supporting_files, package_dependencies))
		
	packages = packages
	
	return Source(identifier, name, url, description, packages)
	
def source_from_json(json_file, source_url = None):
	import json
	
	return source_from_dict(json.load(json_file), source_url)
	
def add_source(source_url):
	import console
	import json
	import requests
	
	sources_list_dir = os.path.expanduser('~/Documents')  + '/site-packages/Pydia/Pydia User Info/Sources.json'
	
	sources = json.load(open(sources_list_dir))
	
	if source_url in sources.values():
		return False
		
	try:
		source_file_content = requests.request('GET', source_url).content
		source = source_from_dict(json.loads(source_file_content), source_url)
		sources[source.identifier] = source_url
		json.dump(sources, open(sources_list_dir, 'w'))
		return source
	except Exception as e:
		print(e)
		return None
		
def download_source_files():
	import json
	import requests
	import urllib
	import console
	
	pydia_dir = os.path.expanduser('~/Documents')  + '/site-packages/Pydia/'
	
	for file in os.listdir(pydia_dir + 'Pydia Sources'):
		try:
			os.remove(pydia_dir + 'Pydia Sources/' + file)
		except Exception as e:
			print(e)
			
	sources = json.load(open(pydia_dir + 'Pydia User Info/Sources.json'))
	
	source_URLs = [sources[identifier] for identifier in sources.keys()]
	
	#print 'Reloading sources...'
	
	for url in source_URLs:
		try:
		
			content = requests.request('GET', url).content
			
			source = json.loads(content)
			
			source['url'] = url
			
			source_identifier = urllib.quote(source['identifier'])
			
			file = open(pydia_dir + 'Pydia Sources/' + source_identifier + '.json', 'w')
			
			json.dump(source, file)
			
			console.set_color(0.0, 1.0, .09)
			#print 'Loaded source: \'%s\'' % source['name']
			console.set_color(0.0, 0.0, 0.0)
			
		except ValueError:
			console.set_color(1.0, .0, .0)
			#print 'Error: failed to load source at \'%s\'. Incorrect file format.' % url
			console.set_color(0.0, 0.0, 0.0)
		except:
			console.set_color(1.0, .0, .0)
			#print 'Error: failed to load source at \'%s\'' % url
			console.set_color(0.0, 0.0, 0.0)
			
def get_sources():
	import json
	
	sources_dir = os.path.expanduser('~/Documents')  + '/site-packages/Pydia/Pydia Sources/'
	
	source_files_paths = [sources_dir + file_name for file_name in os.listdir(sources_dir)]
	
	sources = []
	
	for file_path in source_files_paths:
		sources.append(source_from_json(open(file_path)))
		
	return sources
	
def get_source_for_identifier(identifier):

	for source in get_sources():
		if source.identifier == identifier:
			return source
			
	return None
	
def get_source_URLs():
	import json
	
	source_URLs_path = os.path.expanduser('~/Documents')  + '/site-packages/Pydia/Pydia User Info/Sources.json'
	
	source_URLs = json.load(open(source_URLs_path))
	
	return source_URLs
	
def get_unloaded_source_URLs():

	unloaded_source_URLs = []
	
	for identifier in get_source_URLs():
		url = get_source_URLs()[identifier]
		unloaded = True
		for source in get_sources():
			if source.url == url:
				unloaded = False
				break
		if unloaded:
			unloaded_source_URLs.append(url)
			
	return unloaded_source_URLs

