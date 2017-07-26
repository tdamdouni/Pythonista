# https://gist.github.com/paultopia/db6b6c785614ab8af2e1a6b9b25c66fd

from requests import get
from shutil import copyfileobj
from hashlib import sha256
import gzip
testhtml = "http://paul-gowder.com/curve/index.html"
testbinary = "http://paul-gowder.com/penguin-square.jpg"

# fetch and save to file

def fetch_and_save(url, name):
	file = get(url, stream=True)
	with open(name, 'wb') as out:
		copyfileobj(file.raw, out)
		
def hashfile(file):
	with open(file, "rb") as infile:
		f = infile.read()
	hash = sha256()
	hash.update(f)
	return hash.hexdigest()
	
def fetch_and_hash(url):
	file = get(url, stream=True)
	f = file.raw.read()
	hash = sha256()
	hash.update(f)
	return hash.hexdigest()
	
# the file saving method just saves binary files to disk.
# sometimes they're gzipped, no less.
# here's a function to get strings out of them.
# try to get string out of binary file as if it's not gzipped
# if it turns out to be gzipped it will throw a unicode error,
# then unzip itg. Tested on gzipped html and works.

def open_binary_string_file(filename):
	try:
		with open(filename, "rb") as f:
			bytes = f.read()
			return bytes.decode()
	except UnicodeDecodeError:
		with gzip.open(filename, "rb") as f:
			bytes = f.read()
			return bytes.decode()
			
# fetcher will need to distinguish between originally string-like
# files (.csv, .txt .html .html) and originally binary files
# and save that to the json/database/whev
# -- or some other reproducible way of getting human-readable pdf etc. out.


# CONFIRMED: fetch_and_hash produces same hash as hashfile on fetch_and_save for html file
# print(fetch_and_hash(testhtml))
# fetch_and_save(testhtml, "mypage.html")
# print(hashfile("mypage.html"))

# ALSO CONFIRMED: fetch and hash produces same hash as hashfile on fetch and save for jpg file
#print(fetch_and_hash(testbinary))
#fetch_and_save(testbinary, "mybin.jpg")
#print(hashfile("mybin.jpg"))

# ALSO: jpg file as saved seems to just be user-viewable. Will test on a pdf too; it might be that for binary files I don't have to worry about breaking out of compression for some reason.

