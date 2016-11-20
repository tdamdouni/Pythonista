# https://forum.omz-software.com/topic/3626/play-video-on-ios-quick-look/9

def download_file(url, tmpfile=None):
	if not tmpfile:
		local_filename = url.split('/')[-1]
	else:
		local_filename = tmpfile
		with open(local_filename, 'wb') as f:
			r = requests.get(url, stream=True)
			total_length = r.headers.get('content-length')
			if not total_length:
				print("Content mode...")
				f.write(r.content)
			else:
				print("Chunk mode...") # the below is used when getting that link
				dl = 0
				total_length = float(total_length)
				for chunk in r.iter_content(1024):
					dl += len(chunk)
					f.write(chunk)
	return local_filename

