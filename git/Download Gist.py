import gistcheck
import clipboard
if __name__ == '__main__':
	if len(sys.argv) == 2:
		url = sys.argv[1]
	else:
		url = clipboard.get()
	gistcheck.download(url)
