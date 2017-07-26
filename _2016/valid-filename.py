# https://forum.omz-software.com/topic/3332/sync-files-with-dropbox/9

def valid_filename_for_upload(filename):
	return not any(filename == STATE_FILE,     # Synchronator state file
	filename.startswith('.'),   # hidden file
	filename.startswith('@'),   # temporary file
	filename.endswith('~'),     # temporary file
	filename.endswith('.pyc'),  # generated Python file
	filename.endswith('.pyo'))  # generated Python file

