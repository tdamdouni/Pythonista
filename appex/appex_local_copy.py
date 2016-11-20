# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/appex_local_copy.py

# Make a local copy of the text file passed in via a share sheet.

# See: https://forum.omz-software.com/topic/2637/is-it-possible-to-read-a-file-say-txt-file-from-other-app

import appex, datetime

def main():
	if appex.is_running_extension():
		attachments = appex.get_attachments()
		assert attachments and attachments[0].rstrip(), "Ain't gots no text!!"
		file_name = 'from Goodreader_{:%Y_%m_%d_%H_%M_%S}.txt'.format(datetime.datetime.now())
		with open(file_name, 'w') as out_file:
			out_file.write(attachments[0])
		print('{} bytes written to {}.'.format(len(attachments[0]), file_name))
		
if __name__ == '__main__':
	main()

