#! python3
#combinePdfs.py - Combines all the PDFs in the specified directory into a single PDF named dest

# https://forum.omz-software.com/topic/3982/importing-my-py-file-causes-a-list-of-pdfs-in-my-working-directory-to-be-printed

import PyPDF2, os
ROOT = '/myrootfolder/'

#Get all the PDF filenames
def combinePdfs(dir,dest):
	if dir=='':
		dir=ROOT
	#print(dir)
	os.chdir(dir)
	pdfFiles = []
	for filename in os.listdir(dir):
		if filename.endswith('.pdf'):
			pdfFiles.append(filename)
	pdfFiles.sort()
	
	pdfWriter = PyPDF2.PdfFileWriter()
	
	# Loop through all the PDF files.
	for filename in pdfFiles:
		pdfFileObj = open(filename, 'rb')
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		
		# Loop through all the pages (except the first) and add them.
		for pageNum in range(1, pdfReader.numPages):
			pageObj = pdfReader.getPage(pageNum)
			pdfWriter.addPage(pageObj)
			
	# Save the resulting PDF to a file.
	if not(dest.endswith('.pdf')):
		dest+='.pdf'
	pdfOutput = open(dest, 'wb')
	pdfWriter.write(pdfOutput)
	pdfOutput.close()
	
def main():
	dest=input('input destination filename')
	dir=input('input directory where pdfs to be combined are stored - just hit enter for the default folder')
	if dir=='':
		dir=ROOT
	combinePdfs(dir,dest)
	
if __name__=='__main__':
	main()
# --------------------
import combinePdfs
import PyPDF2, os

ROOT = '/myrootfolder/'

def main():
	combinePdfs(ROOT,'test.pdf')
	
if __name__=='__main__':
	main()


