#!python3

# https://forum.omz-software.com/topic/3982/importing-my-py-file-causes-a-list-of-pdfs-in-my-working-directory-to-be-printed/2

# Hi @sobreacain Cool script! A few thoughts...

# dir() is a builtin function so I use dir_path to keep from clobbering it
# Use input(x).strip() and an or clause to get rid of leading and trailing whitespace and set a default if the user enters nothing
# Use the with open() syntax so that files are automatically closed and their file handles can be freed up.
# Under the wrench icon, use Check Style and Analyze (pyflakes) to catch other issues

# combinePdfs.py - Combines all the PDFs in the specified directory into a
#                  single PDF named dest

import os
import PyPDF2
ROOT = '/myrootfolder/'


def combinePdfs(dir_path, dest):
	"""Get all the PDF filenames"""
	dir_path = dir_path or ROOT
	if not dest.endswith('.pdf'):
		dest += '.pdf'
	# print(dir)
	os.chdir(dir_path)
	pdfFiles = sorted(fn for fn in os.listdir(dir_path) if fn.endswith('.pdf'))
	if not pdfFiles:
		exit('No .pdf files found in {}.'.format(dir_path))
	print('Processing {} .pdf files...'.format(len(pdfFiles)))
	pdfWriter = PyPDF2.PdfFileWriter()
	# Loop through all the PDF files.
	for filename in pdfFiles:
		with open(filename, 'rb') as in_file:
			pdfReader = PyPDF2.PdfFileReader(in_file)
			# Loop through all the pages (except the first) and add them.
			for pageNum in range(1, pdfReader.numPages):
				pdfWriter.addPage(pdfReader.getPage(pageNum))
	# Save the resulting PDF to a file.
	with open(dest, 'wb') as out_file:
		pdfWriter.write(out_file)
		
		
def main():
	dest = input('input destination filename').strip() or 'default.pdf'
	dir_path = input('input directory where pdfs to be combined are stored - '
	'just hit enter for the default folder').strip() or ROOT
	combinePdfs(dir_path, dest)
	
	
if __name__ == '__main__':
	main()

