from __future__ import print_function
import tarfile,sys

def untar(fname):
	if (fname.endswith("tar.gz")):
		tar = tarfile.open(fname)
		tar.extractall()
		tar.close()
		print("Extracted in Current Directory")
	else:
		print("Not a tar.gz file: '%s '" % sys.argv[0])
		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: '%s filename'" % sys.argv[0])
		sys.exit(0)
	untar(sys.argv[1])

