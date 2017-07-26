#!/usr/bin/env python

# https://forum.omz-software.com/topic/3966/adding-a-page-header-to-pdf-output/5

import PyPDF2

pdfs_dir = '../../../Documents/'
bg_filename = pdfs_dir + 'Client_Name_Header_Footer.pdf'
fg_filename = pdfs_dir + 'Client_Report.pdf'

with open(bg_filename, 'rb') as bg_file, open(fg_filename, 'rb') as fg_file:
	bg_page = PyPDF2.PdfFileReader(bg_file).getPage(0)
	pdf_out = PyPDF2.PdfFileWriter()
	for page in PyPDF2.PdfFileReader(fg_file).pages:
		if page.extractText():  # Do not copy pages that have no text
			page.mergePage(bg_page)
			pdf_out.addPage(page)
	if pdf_out.getNumPages():
		with open('New.pdf', 'wb') as out_file:
			# Caution: All three files MUST be open when write() is called
			pdf_out.write(out_file)

