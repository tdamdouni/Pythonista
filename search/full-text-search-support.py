# https://forum.omz-software.com/topic/3252/need-full-text-search-support/7

# coding: utf-8

import ui,os,editor

#
flist = []
#
ds = ui.ListDataSource([])
#
TotalFiles = 0

#
def Search(sender):
	sKey = sender.text.lstrip().encode('utf-8')
	sResult = FileSearch(flist,sKey)
	ResultCnt = len(sResult)
	sender.superview['info'].text = '(%d/%d)' % (ResultCnt,TotalFiles)
	ds.items = sResult
	
#
def Search2nd(sender):
	sKey = sender.superview['sInfo'].text.lstrip().encode('utf-8')
	tfile = []
	for i in ds.items:
		tfile.append('.'+i['title'])
	sResult = FileSearch(tfile,sKey)
	ResultCnt = len(sResult)
	sender.superview['info'].text = '(%d/%d)' % (ResultCnt,TotalFiles)
	ds.items = sResult
	
def dsSelect(sender):
	selectCnt = sender.selected_row
	sfile = '.'+ds.items[selectCnt]['title']
	#
	editor.open_file(sfile,1)
	
#
def GetFiles(rootDir):
	for lists in os.listdir(rootDir):
		path = os.path.join(rootDir, lists)
		flist.append(path)
		if os.path.isdir(path): GetFiles(path)
		
def FileSearch(flist,skey):
	olist = []
	fexttype = ['py','txt','md','sql','js','html','htm','css']
	skey = skey.lower()
	for i in flist:
		if i.lower().find(skey) > -1:
			olist.append({'title':i[1:],'accessory_type':'none'})
		else:
			fext = i.split('.')[-1].lower()
			for j in fexttype:
				if j == fext:
					with open(i,'r') as fp:
						for line in fp:
							if line.lower().find(skey) > -1:
								olist.append({'title':i[1:],'accessory_type':'detail_button'})
								break
	return olist
	
	
#
v = ui.load_view()

#
v['sInfo'].action = Search

#
doc_path = os.path.expanduser('~/Documents')
os.chdir(doc_path)

#
GetFiles('.')
TotalFiles = len(flist)

ds.action = dsSelect
v['tableview1'].data_source = ds
v['tableview1'].delegate = ds
v.present('popover') #, title_bar_color='white', title_color=0.3)

# --------------------


[
  {
    "selected" : false,
    "frame" : "{{0, 0}, {410, 615}}",
    "class" : "View",
    "nodes" : [
      {
        "selected" : false,
        "frame" : "{{6, 10}, {231, 28}}",
        "class" : "TextField",
        "nodes" : [

        ],
        "attributes" : {
          "uuid" : "7A865866-A098-4A9D-8340-60FA6C66C016",
          "corner_radius" : 0,
          "frame" : "{{105, 292}, {200, 32}}",
          "border_color" : "RGBA(0.000000,0.000000,1.000000,1.000000)",
          "border_width" : 1,
          "alignment" : "left",
          "autocorrection_type" : "default",
          "font_name" : "<System>",
          "spellchecking_type" : "default",
          "class" : "TextField",
          "name" : "sInfo",
          "font_size" : 17
        }
      },
      {
        "selected" : false,
        "frame" : "{{3, 42}, {401, 567}}",
        "class" : "TableView",
        "nodes" : [

        ],
        "attributes" : {
          "flex" : "WH",
          "data_source_items" : "",
          "data_source_delete_enabled" : false,
          "frame" : "{{105, 208}, {200, 200}}",
          "uuid" : "80A0C61C-7E81-4D08-A044-14F51827780A",
          "data_source_number_of_lines" : 1,
          "class" : "TableView",
          "data_source_font_size" : 16,
          "background_color" : "RGBA(1.0, 1.0, 1.0, 1.0)",
          "name" : "tableview1",
          "row_height" : 32
        }
      },
      {
        "selected" : false,
        "frame" : "{{299, 6}, {105, 32}}",
        "class" : "Label",
        "nodes" : [

        ],
        "attributes" : {
          "font_size" : 18,
          "frame" : "{{130, 292}, {150, 32}}",
          "uuid" : "65227454-EAE5-46F6-BC2B-C83584F78C31",
          "text" : "",
          "alignment" : "left",
          "class" : "Label",
          "name" : "info",
          "font_name" : "<System>"
        }
      },
      {
        "selected" : false,
        "frame" : "{{245, 10}, {46, 28}}",
        "class" : "Button",
        "nodes" : [

        ],
        "attributes" : {
          "border_width" : 1,
          "action" : "Search2nd",
          "frame" : "{{165, 292}, {80, 32}}",
          "title" : "2nd",
          "class" : "Button",
          "font_bold" : true,
          "uuid" : "A874A7F3-61BA-4FF1-9BD9-4C0AF81A117A",
          "corner_radius" : 0,
          "font_size" : 15,
          "name" : "button1"
        }
      }
    ],
    "attributes" : {
      "enabled" : true,
      "background_color" : "RGBA(1.000000,1.000000,1.000000,1.000000)",
      "tint_color" : "RGBA(0.000000,0.478000,1.000000,1.000000)",
      "border_color" : "RGBA(0.000000,0.000000,0.000000,1.000000)",
      "flex" : ""
    }
  }
]

# --------------------

