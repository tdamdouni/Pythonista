
"""Support for Acrobat Forms in ReportLab documents

This module is somewhat experimental at this time.

Includes basic support for
    textfields,
    select fields (drop down lists), and
    check buttons.

The public interface consists of functions at the moment.
At some later date these operations may be made into canvas
methods. (comments?)

The ...Absolute(...) functions position the fields with respect
to the absolute canvas coordinate space -- that is, they do not
respect any coordinate transforms in effect for the canvas.

The ...Relative(...) functions position the ONLY THE LOWER LEFT
CORNER of the field using the coordinate transform in effect for
the canvas.  THIS WILL ONLY WORK CORRECTLY FOR TRANSLATED COORDINATES
-- THE SHAPE, SIZE, FONTSIZE, AND ORIENTATION OF THE FIELD WILL NOT BE EFFECTED
BY SCALING, ROTATION, SKEWING OR OTHER NON-TRANSLATION COORDINATE
TRANSFORMS.

Please note that all field names (titles) in a given document must be unique.
Textfields and select fields only support the "base 14" canvas fonts
at this time.

See individual function docstrings below for more information.

The function test1(...) generates a simple test file.

THIS CONTRIBUTION WAS COMMISSIONED BY REPORTLAB USERS
WHO WISH TO REMAIN ANONYMOUS.
"""

### NOTE: MAKE THE STRING FORMATS DYNAMIC IN PATTERNS TO SUPPORT ENCRYPTION XXXX

import string
from reportlab.pdfbase.pdfdoc import PDFString, PDFStream, PDFDictionary, PDFName, PDFObject
from reportlab.lib.colors import obj_R_G_B

#==========================public interfaces

def textFieldAbsolute(canvas, title, x, y, width, height, value="", maxlen=1000000, multiline=0):
    """Place a text field on the current page
        with name title at ABSOLUTE position (x,y) with
        dimensions (width, height), using value as the default value and
        maxlen as the maximum permissible length.  If multiline is set make
        it a multiline field.
    """
    theform = getForm(canvas)
    return theform.textField(canvas, title, x, y, x+width, y+height, value, maxlen, multiline)

def textFieldRelative(canvas, title, xR, yR, width, height, value="", maxlen=1000000, multiline=0):
    "same as textFieldAbsolute except the x and y are relative to the canvas coordinate transform"
    (xA, yA) = canvas.absolutePosition(xR,yR)
    return textFieldAbsolute(canvas, title, xA, yA, width, height, value, maxlen, multiline)

def buttonFieldAbsolute(canvas, title, value, x, y):
    """Place a check button field on the current page
        with name title and default value value (one of "Yes" or "Off")
        at ABSOLUTE position (x,y).
    """
    theform = getForm(canvas)
    return theform.buttonField(canvas, title, value, x, y)

def buttonFieldRelative(canvas, title, value, xR, yR):
    "same as buttonFieldAbsolute except the x and y are relative to the canvas coordinate transform"
    (xA, yA) = canvas.absolutePosition(xR,yR)
    return buttonFieldAbsolute(canvas, title, value, xA, yA)

def selectFieldAbsolute(canvas, title, value, options, x, y, width, height):
    """Place a select field (drop down list) on the current page
        with name title and
        with options listed in the sequence options
        default value value (must be one of options)
        at ABSOLUTE position (x,y) with dimensions (width, height)."""
    theform = getForm(canvas)
    theform.selectField(canvas, title, value, options, x, y, x+width, y+height)

def selectFieldRelative(canvas, title, value, options, xR, yR, width, height):
    "same as textFieldAbsolute except the x and y are relative to the canvas coordinate transform"
    (xA, yA) = canvas.absolutePosition(xR,yR)
    return selectFieldAbsolute(canvas, title, value, options, xA, yA, width, height)

def test1():
    from reportlab.pdfgen import canvas
    fn = "formtest1.pdf"
    c = canvas.Canvas(fn)
    # first page
    c.setFont("Courier", 10)
    c.drawString(100, 500, "hello world")
    textFieldAbsolute(c, "fieldA", 100, 600, 100, 20, "default value")
    textFieldAbsolute(c, "fieldB", 100, 300, 100, 50, "another default value", multiline=1)
    selectFieldAbsolute(c, "fieldC", "France", ["Canada", "France", "China"], 100, 200, 100, 20)
    c.rect(100, 600, 100, 20)
    buttonFieldAbsolute(c, "field2", "Yes", 100, 700)
    c.rect(100, 700, 20, 20)
    buttonFieldAbsolute(c, "field3", "Off", 100, 800)
    c.rect(100, 800, 20, 20)
    # second page
    c.showPage()
    c.setFont("Helvetica", 7)
    c.translate(50, 20)
    c.drawString(100, 500, "hello world")
    textFieldRelative(c, "fieldA_1", 100, 600, 100, 20, "default value 2")
    c.setStrokeColorRGB(1,0,0)
    c.setFillColorRGB(0,1,0.5)
    textFieldRelative(c, "fieldB_1", 100, 300, 100, 50, "another default value 2", multiline=1)
    selectFieldRelative(c, "fieldC_1", "France 1", ["Canada 0", "France 1", "China 2"], 100, 200, 100, 20)
    c.rect(100, 600, 100, 20)
    buttonFieldRelative(c, "field2_1", "Yes", 100, 700)
    c.rect(100, 700, 20, 20)
    buttonFieldRelative(c, "field3_1", "Off", 100, 800)
    c.rect(100, 800, 20, 20)
    c.save()
    print("wrote", fn)

#==========================end of public interfaces

from reportlab.pdfbase.pdfpattern import PDFPattern

def getForm(canvas):
    "get form from canvas, create the form if needed"
    try:
        return canvas.AcroForm
    except AttributeError:
        theform = canvas.AcroForm = AcroForm()
        # install the form in the document
        d = canvas._doc
        cat = d._catalog
        cat.AcroForm = theform
        return theform

class AcroForm(PDFObject):
    def __init__(self):
        self.fields = []
    def textField(self, canvas, title, xmin, ymin, xmax, ymax, value="", maxlen=1000000, multiline=0):
        # determine the page ref
        doc = canvas._doc
        page = doc.thisPageRef()
        # determine text info
        R, G, B = obj_R_G_B(canvas._fillColorObj)
        #print "rgb", (R,G,B)
        font = canvas. _fontname
        fontsize = canvas. _fontsize
        field = TextField(title, value, xmin, ymin, xmax, ymax, page, maxlen,
                          font, fontsize, R, G, B, multiline)
        self.fields.append(field)
        canvas._addAnnotation(field)
    def selectField(self, canvas, title, value, options, xmin, ymin, xmax, ymax):
        # determine the page ref
        doc = canvas._doc
        page = doc.thisPageRef()
        # determine text info
        R, G, B = obj_R_G_B(canvas._fillColorObj)
        #print "rgb", (R,G,B)
        font = canvas. _fontname
        fontsize = canvas. _fontsize
        field = SelectField(title, value, options, xmin, ymin, xmax, ymax, page,
              font=font, fontsize=fontsize, R=R, G=G, B=B)
        self.fields.append(field)
        canvas._addAnnotation(field)
    def buttonField(self, canvas, title, value, xmin, ymin):
        # determine the page ref
        doc = canvas._doc
        page = doc.thisPageRef()
        field = ButtonField(title, value, xmin, ymin, page)
        self.fields.append(field)
        canvas._addAnnotation(field)
    def format(self, document):
        from reportlab.pdfbase.pdfdoc import PDFArray
        proxy = PDFPattern(FormPattern, Resources=GLOBALRESOURCES, fields=PDFArray(self.fields))
        return proxy.format(document)

FormPattern = [
'<<\r\n',
' /NeedAppearances true \r\n'
' /DA ', PDFString('/Helv 0 Tf 0 g '), '\r\n',
' /DR \r\n',
["Resources"],
' /Fields \r\n',
["fields"],
'>>'
]

def FormFontsDictionary():
    from reportlab.pdfbase.pdfdoc import PDFDictionary
    fontsdictionary = PDFDictionary()
    fontsdictionary.__RefOnly__ = 1
    for fullname, shortname in FORMFONTNAMES.items():
        fontsdictionary[shortname] = FormFont(fullname, shortname)
    fontsdictionary["ZaDb"] = ZADB
    return fontsdictionary

def FormResources():
    return PDFPattern(FormResourcesDictionaryPattern,
                      Encoding=ENCODING, Font=GLOBALFONTSDICTIONARY)

ZaDbPattern = [
' <<'
' /BaseFont'
'    /ZapfDingbats'
' /Name'
'    /ZaDb'
' /Subtype'
'    /Type1'
' /Type'
'    /Font'
'>>']


FormResourcesDictionaryPattern = [
'<<',
' /Encoding ',
["Encoding"], '\r\n',
' /Font ',
["Font"], '\r\n',
'>>'
]

FORMFONTNAMES = {
    "Helvetica": "Helv",
    "Helvetica-Bold": "HeBo",
    'Courier': "Cour",
    'Courier-Bold': "CoBo",
    'Courier-Oblique': "CoOb",
    'Courier-BoldOblique': "CoBO",
    'Helvetica-Oblique': "HeOb",
    'Helvetica-BoldOblique': "HeBO",
    'Times-Roman': "Time",
    'Times-Bold': "TiBo",
    'Times-Italic': "TiIt",
    'Times-BoldItalic': "TiBI",
    }

EncodingPattern = [
'<<',
' /PDFDocEncoding ',
["PDFDocEncoding"], '\r\n',
'>>',
]

PDFDocEncodingPattern = [
'<<'
' /Differences'
'    ['
' 24'
' /breve'
' /caron'
' /circumflex'
' /dotaccent'
' /hungarumlaut'
' /ogonek'
' /ring'
' /tilde'
' 39'
' /quotesingle'
' 96'
' /grave'
' 128'
' /bullet'
' /dagger'
' /daggerdbl'
' /ellipsis'
' /emdash'
' /endash'
' /florin'
' /fraction'
' /guilsinglleft'
' /guilsinglright'
' /minus'
' /perthousand'
' /quotedblbase'
' /quotedblleft'
' /quotedblright'
' /quoteleft'
' /quoteright'
' /quotesinglbase'
' /trademark'
' /fi'
' /fl'
' /Lslash'
' /OE'
' /Scaron'
' /Ydieresis'
' /Zcaron'
' /dotlessi'
' /lslash'
' /oe'
' /scaron'
' /zcaron'
' 160'
' /Euro'
' 164'
' /currency'
' 166'
' /brokenbar'
' 168'
' /dieresis'
' /copyright'
' /ordfeminine'
' 172'
' /logicalnot'
' /.notdef'
' /registered'
' /macron'
' /degree'
' /plusminus'
' /twosuperior'
' /threesuperior'
' /acute'
' /mu'
' 183'
' /periodcentered'
' /cedilla'
' /onesuperior'
' /ordmasculine'
' 188'
' /onequarter'
' /onehalf'
' /threequarters'
' 192'
' /Agrave'
' /Aacute'
' /Acircumflex'
' /Atilde'
' /Adieresis'
' /Aring'
' /AE'
' /Ccedilla'
' /Egrave'
' /Eacute'
' /Ecircumflex'
' /Edieresis'
' /Igrave'
' /Iacute'
' /Icircumflex'
' /Idieresis'
' /Eth'
' /Ntilde'
' /Ograve'
' /Oacute'
' /Ocircumflex'
' /Otilde'
' /Odieresis'
' /multiply'
' /Oslash'
' /Ugrave'
' /Uacute'
' /Ucircumflex'
' /Udieresis'
' /Yacute'
' /Thorn'
' /germandbls'
' /agrave'
' /aacute'
' /acircumflex'
' /atilde'
' /adieresis'
' /aring'
' /ae'
' /ccedilla'
' /egrave'
' /eacute'
' /ecircumflex'
' /edieresis'
' /igrave'
' /iacute'
' /icircumflex'
' /idieresis'
' /eth'
' /ntilde'
' /ograve'
' /oacute'
' /ocircumflex'
' /otilde'
' /odieresis'
' /divide'
' /oslash'
' /ugrave'
' /uacute'
' /ucircumflex'
' /udieresis'
' /yacute'
' /thorn'
' /ydieresis'
'    ]'
' /Type'
' /Encoding'
'>>']

def FormFont(BaseFont, Name):
    from reportlab.pdfbase.pdfdoc import PDFName
    return PDFPattern(FormFontPattern, BaseFont=PDFName(BaseFont), Name=PDFName(Name), Encoding=PDFDOCENC)

FormFontPattern = [
'<<',
' /BaseFont ',
["BaseFont"], '\r\n',
' /Encoding ',
["Encoding"], '\r\n',
' /Name ',
["Name"], '\r\n',
' /Subtype '
' /Type1 '
' /Type '
' /Font '
'>>' ]

def resetPdfForm():
    global PDFDOCENC,ENCODING,GLOBALFONTSDICTIONARY,GLOBALRESOURCES,ZADB
    PDFDOCENC = PDFPattern(PDFDocEncodingPattern)
    ENCODING = PDFPattern(EncodingPattern, PDFDocEncoding=PDFDOCENC)
    ZADB = PDFPattern(ZaDbPattern)
    GLOBALFONTSDICTIONARY = FormFontsDictionary()
    GLOBALRESOURCES = FormResources()
from reportlab.rl_config import register_reset
register_reset(resetPdfForm)
resetPdfForm()

def TextField(title, value, xmin, ymin, xmax, ymax, page,
              maxlen=1000000, font="Helvetica-Bold", fontsize=9, R=0, G=0, B=0.627, multiline=0):
    from reportlab.pdfbase.pdfdoc import PDFString, PDFName
    Flags = 0
    if multiline:
        Flags = Flags | (1<<12) # bit 13 is at position 12 :)
    fontname = FORMFONTNAMES[font]
    return PDFPattern(TextFieldPattern,
                      value=PDFString(value), maxlen=maxlen, page=page,
                      title=PDFString(title),
                      xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax,
                      fontname=PDFName(fontname), fontsize=fontsize, R=R, G=G, B=B, Flags=Flags)


TextFieldPattern = [
'<<'
' /DA'
' (', ["fontname"],' ',["fontsize"],' Tf ',["R"],' ',["G"],' ',["B"],' rg)'
' /DV ',
["value"], '\r\n',
' /F 4 /FT /Tx'
'/MK << /BC [ 0 0 0 ] >>'
' /MaxLen ',
["maxlen"], '\r\n',
' /P ',
["page"], '\r\n',
' /Rect '
'    [', ["xmin"], " ", ["ymin"], " ", ["xmax"], " ", ["ymax"], ' ]'
'/Subtype /Widget'
' /T ',
["title"], '\r\n',
' /Type'
'    /Annot'
' /V ',
["value"], '\r\n',
' /Ff ',
["Flags"],'\r\n',
'>>']

def SelectField(title, value, options, xmin, ymin, xmax, ymax, page,
              font="Helvetica-Bold", fontsize=9, R=0, G=0, B=0.627):
    #print "ARGS", (title, value, options, xmin, ymin, xmax, ymax, page, font, fontsize, R, G, B)
    from reportlab.pdfbase.pdfdoc import PDFString, PDFName, PDFArray
    if value not in options:
        raise ValueError("value %s must be one of options %s" % (repr(value), repr(options)))
    fontname = FORMFONTNAMES[font]
    optionstrings = list(map(PDFString, options))
    optionarray = PDFArray(optionstrings)
    return PDFPattern(SelectFieldPattern,
                      Options=optionarray,
                      Selected=PDFString(value), Page=page,
                      Name=PDFString(title),
                      xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax,
                      fontname=PDFName(fontname), fontsize=fontsize, R=R, G=G, B=B)

SelectFieldPattern = [
'<< % a select list\r\n'
' /DA ',
' (', ["fontname"],' ',["fontsize"],' Tf ',["R"],' ',["G"],' ',["B"],' rg)\r\n',
#'    (/Helv 12 Tf 0 g)\r\n',
' /DV ',
["Selected"],'\r\n',
' /F ',
'    4\r\n',
' /FT ',
'    /Ch\r\n',
' /MK ',
'    <<',
'    /BC',
'        [',
'            0',
'            0',
'            0',
'        ]',
'    /BG',
'        [',
'            1',
'            1',
'            1',
'        ]',
'    >>\r\n',
' /Opt ',
["Options"],'\r\n',
' /P ',
["Page"],'\r\n',
'/Rect',
'    [',["xmin"], " ", ["ymin"], " ", ["xmax"], " ", ["ymax"],
'    ] \r\n',
'/Subtype',
'    /Widget\r\n',
' /T ',
["Name"],'\r\n',
' /Type ',
'    /Annot',
' /V ',
["Selected"],'\r\n',
'>>']

def ButtonField(title, value, xmin, ymin, page):
    if value not in ("Yes", "Off"):
        raise ValueError("button value must be 'Yes' or 'Off': "+repr(value))
    (dx, dy) = (16.77036, 14.90698)
    return PDFPattern(ButtonFieldPattern,
                      Name=PDFString(title),
                      xmin=xmin, ymin=ymin, xmax=xmin+dx, ymax=ymin+dy,
                      Hide=HIDE,
                      APDOff=APDOFF,
                      APDYes=APDYES,
                      APNYes=APNYES,
                      Value=PDFName(value),
                      Page=page)

ButtonFieldPattern = ['<< ',
'/AA',
'    <<',
'    /D ',
["Hide"],'\r\n',
#'        %(imported.18.0)s',
'    >> ',
'/AP ',
'    <<',
'    /D',
'        <<',
'        /Off ',
#'            %(imported.40.0)s',
["APDOff"], '\r\n',
'        /Yes ',
#'            %(imported.39.0)s',
["APDYes"], '\r\n',
'        >>', '\r\n',
'    /N',
'        << ',
'        /Yes ',
#'            %(imported.38.0)s',
["APNYes"],  '\r\n',
'        >>',
'    >>\r\n',
' /AS ',
["Value"], '\r\n',
' /DA ',
PDFString('/ZaDb 0 Tf 0 g'), '\r\n',
'/DV ',
["Value"], '\r\n',
'/F ',
'    4 ',
'/FT ',
'    /Btn ',
'/H ',
'    /T ',
'/MK ',
'    <<',
'    /AC (\\376\\377)',
#PDFString('\376\377'),
'    /CA ',
PDFString('4'),
'    /RC ',
PDFString('\376\377'),
'    >> ','\r\n',
'/P ',
["Page"], '\r\n',
'/Rect',
'    [',["xmin"], " ", ["ymin"], " ", ["xmax"], " ", ["ymax"],
'    ] ','\r\n',
'/Subtype',
'    /Widget ',
'/T ',
["Name"], '\r\n',
'/Type',
'    /Annot ',
'/V ',
["Value"], '\r\n',
' >>']

HIDE = PDFPattern([
'<< '
'/S '
' /Hide '
'>>'])

def buttonStreamDictionary():
    "everything except the length for the button appearance streams"
    result = PDFDictionary()
    result["SubType"] = "/Form"
    result["BBox"] = "[0 0 16.77036 14.90698]"
    font = PDFDictionary()
    font["ZaDb"] = ZADB
    resources = PDFDictionary()
    resources["ProcSet"] = "[ /PDF /Text ]"
    resources["Font"] = font
    result["Resources"] = resources
    return result

def ButtonStream(content):
    dict = buttonStreamDictionary()
    result = PDFStream(dict, content)
    result.filters = []
    return result

APDOFF = ButtonStream('0.749 g 0 0 16.7704 14.907 re f\r\n')
APDYES = ButtonStream(
'0.749 g 0 0 16.7704 14.907 re f q 1 1 14.7704 12.907 re W '+
'n BT /ZaDb 11.3086 Tf 0 g  1 0 0 1 3.6017 3.3881 Tm (4) Tj ET\r\n')
APNYES = ButtonStream(
'q 1 1 14.7704 12.907 re W n BT /ZaDb 11.3086 Tf 0 g  1 0 0 1 3.6017 3.3881 Tm (4) Tj ET Q\r\n')


#==== script interpretation

if __name__=="__main__":
    test1()
