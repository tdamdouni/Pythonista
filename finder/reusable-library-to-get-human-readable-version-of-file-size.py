# coding: utf-8

def sizeof_fmt(self, num, suffix='B'):
	# copied from -
	# http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
	#for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

