# coding: utf-8

# https://gist.github.com/bmw1821/bc2ccf257d60804be010

from __future__ import print_function
import os
import PydiaKit

class Package (object):

	def __init__(self, identifier, source_identifier, name, author, description, version, main_package_files, install_script_url = None, supporting_files = [], dependencies = []):
		self.identifier = identifier
		self.source_identifier = source_identifier
		self.name = name
		self.author = author
		self.description = description
		self.version = version
		self.main_package_files = main_package_files
		self.install_script_url = install_script_url
		self.supporting_files = supporting_files
		self.dependencies = dependencies
		
	def get_dict(self):
		import json
		
		package_dict = {
		'identifier': self.identifier,
		'source-identifier': self.source_identifier,
		'name': self.name,
		'author': self.author,
		'description': self.description,
		'version': self.version,
		'main-package-files': self.main_package_files,
		'install-script-url': self.install_script_url,
		'supporting-files': self.supporting_files,
		'dependencies': self.dependencies
		}
		
		return package_dict
		
def get_packages():

	import Pydia_Sources
	
	packages = []
	
	for source in Pydia_Sources.get_sources():
		for package in source.packages:
			packages.append(package)
			
	return packages
	
def get_package_for_identifier(identifier):
	for package in get_packages():
		if package.identifier == identifier:
			return package
			
	return None
	
class PackageInstallOverwriteException (Exception):
	def __init__(self, files):
		super(PackageInstallOverwriteException, self).__init__()
		self.files = files
		
class PackageInstallMissingDependencyException (Exception):
	def __init__(self, identifiers):
		super(PackageInstallMissingDependencyException, self).__init__()
		self.identifiers = identifiers
		
def install_package(package, overwrite_files = False):
	import requests
	import shutil
	import json
	
	try:
	
		documents_dir = os.path.expanduser('~/Documents/')
		
		main_package_files = []
		
		supporting_files = []
		
		missing_dependencies = []
		for dependency_identifier in package.dependencies:
			dependency = get_package_for_identifier(dependency_identifier)
			if not dependency:
				dependency = get_installed_package_for_identifier(dependency_identifier)
			if not dependency:
				missing_dependencies.append(dependency_identifier)
				
		if len(missing_dependencies) > 0:
			raise PackageInstallMissingDependencyException(missing_dependencies)
			
		dependencies = []
		
		for dependency_identifier in package.dependencies:
			if not get_installed_package_for_identifier(dependency_identifier):
				dependencies.append(get_package_for_identifier(dependency_identifier))
				
		existing_files = []
		
		for dependency in dependencies:
			try:
				install_package(dependency, overwrite_files)
			except PackageInstallOverwriteException as e:
				existing_files += e.files
				
				
		for file in package.main_package_files:
			content = requests.request('GET', file['file-url']).content
			file_name = file['name']
			main_package_files.append((content, file_name))
			
		for supporting_file in package.supporting_files:
			content = requests.request('GET', supporting_file['file-url']).content
			file_name = supporting_file['name']
			supporting_files.append((content, PydiaKit.supporting_file_dir_for_identifier(package.identifier) + file_name))
			
		package_install_script_content = None
		if package.install_script_url:
			package_install_script_content = requests.request('GET', package.install_script_url).content
			
		for file in main_package_files:
			file_name = file[1]
			if os.path.exists(documents_dir + file_name):
				existing_files.append(file_name)
				
		if len(existing_files) == 0 or overwrite_files:
			for file in main_package_files:
				file_obj = open(documents_dir + file[1], 'w')
				file_obj.write(file[0])
		else:
			raise PackageInstallOverwriteException(existing_files)
			
		if os.path.exists(PydiaKit.supporting_file_dir_for_identifier(package.identifier)):
			shutil.rmtree(PydiaKit.supporting_file_dir_for_identifier(package.identifier))
		os.makedirs(PydiaKit.supporting_file_dir_for_identifier(package.identifier))
		
		for file in supporting_files:
			file_obj = open(file[1], 'w')
			file_obj.write(file[0])
			
		if package_install_script_content:
			exec package_install_script_content
			
		installed_packages_path = os.path.expanduser('~/Documents/site-packages/Pydia/Pydia User Info/Installed Packages.json')
		installed_packages = json.load(open(installed_packages_path))
		installed_packages[package.identifier] = package.get_dict()
		json.dump(installed_packages, open(installed_packages_path, 'w'))
		
		return True
	except PackageInstallOverwriteException as e:
		raise e
	except PackageInstallMissingDependencyException as e:
		raise e
	except Exception as e:
		return False
		
def uninstall_package(package_identifier):
	import json
	import shutil
	
	documents_dir =  os.path.expanduser('~/Documents/')
	
	installed_packages_path = documents_dir + 'site-packages/Pydia/Pydia User Info/Installed Packages.json'
	installed_packages = json.load(open(installed_packages_path))
	
	if get_installed_package_for_identifier(package_identifier):
	
		package = installed_packages[package_identifier]
		
		for file in package['main-package-files']:
			if os.path.exists(documents_dir + file['name']):
				os.remove(documents_dir + file['name'])
				
		if os.path.exists(documents_dir + 'site-packages/Pydia/Package Support/' + package_identifier):
			shutil.rmtree(documents_dir + 'site-packages/Pydia/Package Support/' + package_identifier)
			
		installed_packages.pop(package_identifier)
		json.dump(installed_packages, open(installed_packages_path, 'w'))
		
		return True
	else:
		return False
		
def get_installed_packages():
	import json
	
	documents_dir = os.path.expanduser('~/Documents/')
	installed_packages_path = documents_dir + 'site-packages/Pydia/Pydia User Info/Installed Packages.json'
	raw_installed_packages = json.load(open(installed_packages_path))
	packages = []
	
	for package_identifier in raw_installed_packages:
	
		raw_package = raw_installed_packages[package_identifier]
		
		package_identifier = raw_package['identifier']
		
		package_source_identifier = raw_package['source-identifier']
		
		package_name = raw_package['name']
		
		package_author = raw_package['author']
		
		package_description = raw_package['description']
		
		package_version = raw_package['version']
		
		package_main_package_files = raw_package['main-package-files']
		
		package_install_script_url = raw_package.get('install-script-url', None)
		
		package_supporting_files = raw_package.get('supporting-files', [])
		
		package_dependencies = raw_package.get('dependencies', [])
		
		packages.append(Package(package_identifier, package_source_identifier, package_name, package_author, package_description, package_version, package_main_package_files, package_install_script_url, package_supporting_files, package_dependencies))
		
	return packages
	
def package_is_installed(package):
	for _package in get_packages():
		if _package.identifier == package.identifier:
			if _package.version == package.version:
				return True
	return False
	
def get_package_updates():
	import json
	
	documents_dir =  os.path.expanduser('~/Documents/')
	installed_packages_path = documents_dir + 'site-packages/Pydia/Pydia User Info/Installed Packages.json'
	installed_packages = json.load(open(installed_packages_path))
	
	updates = []
	
	for installed_package_identifier in installed_packages:
		for available_package in get_packages():
			if installed_package_identifier == available_package.identifier:
				if installed_packages[installed_package_identifier]['version'] < available_package.version:
					updates.append(available_package)
					break
					
	return updates
	
def update_available_for_package(package):

	for update in get_package_updates():
		if package.identifier == update.identifier:
			return update
			
	return None
	
def get_installed_package_for_identifier(identifier):

	for package in get_installed_packages():
		if package.identifier == identifier:
			return package
			
	return None
	
def update_package(package_identifier, overwrite_files = False):
	import requests
	import shutil
	import json
	
	installed_package = get_installed_package_for_identifier(package_identifier)
	update = update_available_for_package(installed_package)
	if not update:
		return None
		
	try:
	
		documents_dir = os.path.expanduser('~/Documents/')
		
		main_package_files = []
		
		supporting_files = []
		
		uninstalled_dependencies = [dependency for dependency in update.dependencies if not get_installed_package_for_identifier(dependency)]
		
		missing_dependencies = []
		for dependency_identifier in uninstalled_dependencies:
			dependency = get_package_for_identifier(dependency_identifier)
			if not dependency:
				dependency = get_installed_package_for_identifier(dependency_identifier)
			if not dependency:
				missing_dependencies.append(dependency_identifier)
				
		if len(missing_dependencies) > 0:
			raise PackageInstallMissingDependencyException(missing_dependencies)
			
		dependencies = []
		
		for dependency_identifier in uninstalled_dependencies:
			if not get_installed_package_for_identifier(dependency_identifier):
				dependencies.append(get_package_for_identifier(dependency_identifier))
				
		existing_files = []
		
		for dependency in dependencies:
			try:
				install_package(dependency, overwrite_files)
			except PackageInstallOverwriteException as e:
				dependency_existing_files += e.files
				
		for file in update.main_package_files:
			content = requests.request('GET', file['file-url']).content
			file_name = file['name']
			main_package_files.append((content, file_name))
			
		for supporting_file in update.supporting_files:
			content = requests.request('GET', supporting_file['file-url']).content
			file_name = supporting_file['name']
			supporting_files.append((content, PydiaKit.supporting_file_dir_for_identifier(update.identifier) + file_name))
			
		package_install_script_content = None
		if update.install_script_url:
			package_install_script_content = requests.request('GET', update.install_script_url).content
			
		installed_files = []
		
		for file in get_installed_package_for_identifier(package_identifier).main_package_files:
			file_name = file['name']
			installed_files.append(file_name)
			
		for file in main_package_files:
			file_name = file[1]
			if os.path.exists(documents_dir + file_name) and not file_name in installed_files:
				existing_files.append(file_name)
				
		if len(existing_files) == 0 or overwrite_files:
			if not uninstall_package(installed_package.identifier):
				return None
			for file in main_package_files:
				file_obj = open(documents_dir + file[1], 'w')
				file_obj.write(file[0])
		else:
			raise PackageInstallOverwriteException(existing_files)
		if os.path.exists(PydiaKit.supporting_file_dir_for_identifier(update.identifier)):
			shutil.rmtree(PydiaKit.supporting_file_dir_for_identifier(update.identifier))
		os.makedirs(PydiaKit.supporting_file_dir_for_identifier(update.identifier))
		
		for file in supporting_files:
			file_obj = open(file[1], 'w')
			file_obj.write(file[0])
			
		if package_install_script_content:
			exec package_install_script_content
			
		installed_packages_path = os.path.expanduser('~/Documents/site-packages/Pydia/Pydia User Info/Installed Packages.json')
		installed_packages = json.load(open(installed_packages_path))
		installed_packages[update.identifier] = update.get_dict()
		json.dump(installed_packages, open(installed_packages_path, 'w'))
		
		return update
	except PackageInstallOverwriteException as e:
		raise e
	except PackageInstallMissingDependencyException as e:
		raise e
	except Exception as e:
		print(e)
		return None
		
def get_packages_for_search_text(search_text):

	search_text = search_text.lower()
	
	results = []
	
	for package in get_packages():
		include_package = True
		for key_word in search_text.split(' '):
			include_package = include_package and (key_word in package.name.lower() or key_word in package.description.lower())
		if include_package:
			results.append(package)
			
	return results
	
def packages_dependant_on(package_identifier):
	dependant_packages = []
	for package in get_installed_packages():
		if package_identifier in package.dependencies:
			dependant_packages.append(package)
	return dependant_packages

