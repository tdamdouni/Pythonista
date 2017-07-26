# https://forum.omz-software.com/topic/3993/bug-in-editor-make_new_path-when-using-absolute-path

full_path = ... # Assuming you have a full path already

# Make sure that the file doesn't exist yet:
directory, filename = os.path.split(full_path)
suffix = 1
while os.path.exists(full_path):
	base_name, ext = os.path.splitext(filename)
	new_name = '%s_%i%s' % (base_name, suffix, ext)
	full_path = os.path.join(directory, new_name)
	suffix += 1
# Now we can safely call make_new_file:
editor.make_new_file(full_path)

