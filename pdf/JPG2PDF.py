# coding: utf-8
# Images will be be insert in the order they were selected

import ui, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import *
from PIL import Image

pages = {'A0':A0, 'A1':A1, 'A2':A2, 'A3':A3, 'A4':A4, 'A5':A5, 'A6':A6, 'Letter':LETTER, 'Legal':LEGAL, 'ElevenSeventeen':ELEVENSEVENTEEN, 'B0':B0, 'B1':B1, 'B2':B2, 'B3':B3, 'B4':B4, 'B5':B5, 'B6':B6}

view = ui.load_view('JPG2PDF')
filename = view['textfield1']
bordersize_slider = view['slider1']
bordersize_label = view['label4']
pagesize = view['segmentedcontrol3']
orientation = view['segmentedcontrol1']
imageresize = view['segmentedcontrol2']
imagefiles = view['tableview1']
button = view['button1']
imagefiles.allows_multiple_selection = True
path = os.getcwd()
files = []
for entry in sorted(os.listdir(path)):
    if os.path.isfile(path + '/' + entry):
        if entry.find('.jpg') >= 0:
            files.append(entry)
lst = ui.ListDataSource(files)
imagefiles.data_source = lst
imagefiles.delegate = lst
imagefiles.editing = False
lst.delete_enabled = False
lst.font = ('Courier', 18)
### Preset
pagesize.selected_index = 4 #A4
orientation.selected_index = 1 #portrait
imageresize.selected_index = 1 #keep ratio
bordersize_slider.value = 0.1 #1cm
bordersize_label.text = '1.0cm'

def btn_GeneratePDF(sender):
    x = None 
    y = None 
    size = None
    if orientation.segments[orientation.selected_index] == 'landscape':
        size = landscape(pages[pagesize.segments[pagesize.selected_index]])
    else:
        size = pages[pagesize.segments[pagesize.selected_index]]
    c = canvas.Canvas(filename.text,pagesize=size)
    wpx, hpx = size # width and height in px
    i = []
    for row in imagefiles.selected_rows:
        i.append(row[1])
    slider_value = bordersize_slider.value * 10
    if slider_value > 0.0 and imageresize.segments[imageresize.selected_index] == 'whole page':
        x = y = slider_value * cm
        hpx = hpx - (2 * x)
        wpx = wpx - (2 * y)
        for selected in i:
            c.drawImage(files[selected], x, y, width=wpx, height=hpx)
            c.showPage()
    elif slider_value == 0.0 and imageresize.segments[imageresize.selected_index] == 'whole page':
        x = y = 0
        for selected in i:
            c.drawImage(files[selected], x, y, width=wpx, height=hpx)
            c.showPage()
    elif slider_value > 0.0 and imageresize.segments[imageresize.selected_index] == 'keep ratio':
        for selected in i:
            x = y = slider_value * cm
            wpx, hpx = size # width and height in px
            hpx = hpx - (2 * x)
            wpx = wpx - (2 * y)
            img_width, img_height = Image.open(files[selected]).size
            y_ratio = hpx / img_height
            x_ratio = wpx / img_width
            # 1.0 = okay, <1.0 = Image to big, >1.0 = Image to small
            if x_ratio == 1.0 and y_ratio == 1.0:
                pass #perfect size
            elif x_ratio == 1.0 and y_ratio > 1.0:
                y_offset = (hpx - img_height) / 2  #perfect width
                y += y_offset
                hpx = img_height
            elif x_ratio > 1.0 and y_ratio == 1.0:
                x_offset = (wpx - img_width) / 2  #perfect height
                x += x_offset
                wpx = img_width
            elif x_ratio > 1.0 and y_ratio > 1.0:
                y_offset = (hpx - img_height) / 2 #show image in original size
                y += y_offset
                x_offset = (wpx - img_width) / 2
                x += x_offset
                hpx = img_height
                wpx = img_width
            elif x_ratio >= 1.0 and y_ratio < 1.0:
                x_offset = (wpx - (img_width * y_ratio)) / 2
                x += x_offset
                hpx = img_height * y_ratio #shrink height
                wpx = img_width * y_ratio
            elif x_ratio < 1.0 and y_ratio >= 1.0:
                y_offset = (hpx - (img_height * x_ratio)) / 2
                y += y_offset
                hpx = img_height * x_ratio #shrink width
                wpx = img_width * x_ratio
            elif x_ratio < 1.0 and y_ratio < 1.0:
                if x_ratio < y_ratio: #which side?
                    y_offset = (hpx - (img_height * x_ratio)) / 2
                    y += y_offset
                    hpx = img_height * x_ratio #shrink width
                    wpx = img_width * x_ratio
                else:
                    x_offset = (wpx - (img_width * y_ratio)) / 2
                    x += x_offset
                    hpx = img_height * y_ratio #shrink height
                    wpx = img_width * y_ratio
            c.drawImage(files[selected], x, y, width=wpx, height=hpx)
            c.showPage()
    elif slider_value == 0.0 and imageresize.segments[imageresize.selected_index] == 'keep ratio':
        for selected in i:
            x = y = 0
            wpx, hpx = size # width and height in px
            img_width, img_height = Image.open(files[selected]).size
            y_ratio = hpx / img_height
            x_ratio = wpx / img_width
            # 1.0 = okay, <1.0 = Image to big, >1.0 = Image to small
            if x_ratio == 1.0 and y_ratio == 1.0:
                pass #perfect size
            elif x_ratio == 1.0 and y_ratio > 1.0:
                y = (hpx - img_height) / 2  #perfect width
                hpx = img_height
            elif x_ratio > 1.0 and y_ratio == 1.0:
                x = (wpx - img_width) / 2  #perfect height
                wpx = img_width
            elif x_ratio > 1.0 and y_ratio > 1.0:
                y = (hpx - img_height) / 2 #show image in original size
                x = (wpx - img_width) / 2
                hpx = img_height
                wpx = img_width
            elif x_ratio >= 1.0 and y_ratio < 1.0:
                x = (wpx - (img_width * y_ratio)) / 2
                hpx = img_height * y_ratio #shrink height
                wpx = img_width * y_ratio
            elif x_ratio < 1.0 and y_ratio >= 1.0:
                y = (hpx - (img_height * x_ratio)) / 2
                hpx = img_height * x_ratio #shrink width
                wpx = img_width * x_ratio
            elif x_ratio < 1.0 and y_ratio < 1.0:
                if x_ratio < y_ratio: #which side?
                    y = (hpx - (img_height * x_ratio)) / 2
                    hpx = img_height * x_ratio #shrink width
                    wpx = img_width * x_ratio
                else:
                    x = (wpx - (img_width * y_ratio)) / 2
                    hpx = img_height * y_ratio #shrink height
                    wpx = img_width * y_ratio
            c.drawImage(files[selected], x, y, width=wpx, height=hpx)
            c.showPage()
    c.save()
    view.close()

def sl_Bordersize(sender):
    val = round(sender.value,1)
    sender.value = val
    val = val * 10
    bordersize_label.text = str(val) + 'cm'

button.action = btn_GeneratePDF
bordersize_slider.action = sl_Bordersize
view.present('fullscreen')
