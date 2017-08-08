# Python, watermark a PDF

_Captured: 2016-02-05 at 01:34 from [wa5pb.freeshell.org](http://wa5pb.freeshell.org/motd/?p=769)_

This blog entry shows how to use Python and two third party modules (pyPdf and ReportLab) to watermark a PDF.
    
    
    _#This sample uses two third part modules for Python, 
    #pyPdf & ReportLab to achieve creating and placing 
    #watermark text at angle on an existing PDF file. 
    #This example was produced with Python 2.7 
    #See http://pybrary.net/pyPdf for more informaton about pyPdf. 
    #See http://www.reportlab.com for more information about ReportLab. 
    
    #Import the needed external modules and functions from pyPdf and reportlab._
    **from pyPdf import PdfFileWriter, PdfFileReader 
    from reportlab.pdfgen import canvas**
    
    _#Use reportlab to create a PDF that will be used 
    #as a watermark on another PDF._
    **c= canvas.Canvas("watermark.pdf") 
    c.setFont("Courier", 60)**
    _#This next setting with make the text of our 
    #watermark gray, nice touch for a watermark._
    **c.setFillGray(0.5,0.5)**
    _#Set up our watermark document. Our watermark 
    #will be rotated 45 degrees from the direction 
    #of our underlying document._
    **c.saveState() 
    c.translate(500,100) 
    c.rotate(45) 
    c.drawCentredString(0, 0, "A WATERMARK!") 
    c.drawCentredString(0, 300, "A WATERMARK!") 
    c.drawCentredString(0, 600, "A WATERMARK!") 
    c.restoreState() 
    c.save() **
    _
    #Read in the PDF that will have the PDF applied to it._
    **output = PdfFileWriter() 
    input1 = PdfFileReader(file("original_pdf.pdf", "rb"))** _
    
    #Just to demo this function from pyPdf. 
    #If the PDF has a title, this will print it out._
    **print "title = %s" % (input1.getDocumentInfo().title)**
    
    _#Open up the orgininal PDF._
    **page1 = input1.getPage(0)**
    
    _#Read in the file created above by ReportLab for our watermark._
    **watermark = PdfFileReader(file("watermark.pdf", "rb"))**
    _#Apply the watermark by merging the two PDF files._
    **page1.mergePage(watermark.getPage(0))**
    _#Send the resultant PDF to the output stream._
    **output.addPage(page1)**
    
    _#Just to demo this function from pyPdf. 
    #Return the number of pages in the watermarked PDF._
    **print "watermarked_pdf.pdf has %s pages." % input1.getNumPages()**
    
    _#write the output of our new, watermarked PDF._
    **outputStream = file("watermarked_pdf.pdf", "wb") 
    output.write(outputStream) 
    outputStream.close()**
