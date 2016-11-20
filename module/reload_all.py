import os.path
import sys

DOCS = os.path.expanduser("~/Documents") + "/"

def main():
	for module in sys.modules.itervalues():
		try:
			if os.path.realpath(module.__file__).startswith(DOCS) and module.__name__ != "__main__":
				reload(module)
				#print("Reloaded: " + str(module))
		except AttributeError:
			pass
			
if __name__ == "__main__":
	main()

