# https://github.com/cclauss/Pythonista_ui/blob/master/save_py_source.py

import datetime, os, zipfile

exts = 'py pyui'.split()
zip_file_name = 'aa_source_code_%Y_%m_%d_%H_%M_%S.zip'
zip_file_name = datetime.datetime.strftime(datetime.datetime.now(), zip_file_name)

def get_filenames(in_dir=None):
	def visit(_, dirname, names):
		for name in names:
			filename = os.path.join(dirname, name)
			if os.path.isfile(filename):
				filenames.append(filename)
				
	filenames = []
	os.path.walk(in_dir or os.curdir, visit, None)
	return filenames
	
filenames = get_filenames()
if exts:
	filenames = [fn for fn in filenames if os.path.splitext(fn)[1] in exts]
file_count = len(filenames)
print('{} files found.'.format(file_count))
if filenames:
	with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
		for i, filename in enumerate(filenames):
			zip_file.write(filename)
			if not i % 50:
				print('{} of {}: {}'.format(i, file_count, filename))
print('{}\n{} files copied into zip file: "{}".'.format('=' * 13, file_count, zip_file_name))

