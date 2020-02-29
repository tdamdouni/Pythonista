# coding: utf-8

from __future__ import print_function
import datetime, os, ui, shutil, console, sys, clipboard, requests, zipfile, zlib, tarfile, photos, editor, time, struct, Image

def get_dir(path = os.path.expanduser('~')):
    dirs  = [] if path == os.path.expanduser('~') else ['..']
    files = []
    for entry in sorted(os.listdir(path)):
        if os.path.isdir(path + '/' + entry):
            dirs.append(entry)
        else:
            files.append(entry)
    dirs_and_files = []
    for directory in dirs:
        dic = {'accessory_type':'none'}
        dic.setdefault('title', '/' + directory)
        dirs_and_files.append(dic)
    if path != os.path.expanduser('~'):
        for file in files:
            full_pathname = path + '/' + file 
            dic = {'accessory_type':'detail_button'}
            dic.setdefault('title', file)
            dic.setdefault('size', os.path.getsize(full_pathname))
            dic.setdefault('date', datetime.datetime.fromtimestamp(os.path.getmtime(full_pathname)))
            dirs_and_files.append(dic)
    return dirs_and_files

def get_dirs(path = os.path.expanduser('~')):
    dir = [] if path == os.path.expanduser('~') else ['..']
    for entry in sorted(os.listdir(path)):
        if os.path.isdir(path + '/' + entry):
            dir.append(entry)
    dirs = ['/' + directory for directory in dir]
    return dirs

def get_imgs(path):
    files = []
    types = ['.jpg', '.png', '.gif', '.bmp', '.tif']
    i = 0
    for entry in sorted(os.listdir(path)):
        if os.path.isfile(path + '/' + entry):
            ext = entry[len(entry)-4:]
            for t in types:
              if ext == t or ext == t.upper():
                files.append(entry)
                i += 1
    sorted(files)
    return files

def hex_view(filepath):
    return_value = ''
    try:
        with open(filepath,'rb') as in_file:
            for line in range(0, os.path.getsize(filepath), 16):
                h = s = ''
                for c in in_file.read(16):
                    i = ord(c)
                    h += '{:02X} '.format(i)
                    s += c if 31 < i < 127 else '.'
                return_value += '0x{:08X} | {:48}| {:8}\n'.format(line, h, s)
    except Exception as e:
        return 'Error!\nFile = {}\nError = {}'.format(filepath, e)
    return return_value

class MyImageView(ui.View):
    def __init__(self,path,file,imgs,index):
        self.color = 'white'
        self.x_off = 0
        self.y_off = 0
        self.scr_height = None 
        self.scr_width = None 
        self.img = ui.Image.named(path + '/' + file)
        self.scr_cor = 2.0
        self.ratio = 1.0
        self.path = path
        self.file = file
        self.imgs = imgs
        self.index = index
        self.len_imgs = len(imgs)
        if self.img != None:
            self.img_width, self.img_height = self.img.size
            self.name = self.file + ' (' + str(self.img_width) + ',' + str(self.img_height) + ')'
        else:
            self.touch_began(None)

    def draw(self):
        self.scr_height = self.height
        self.scr_width = self.width
        path = ui.Path.rect(0, 0, self.scr_width, self.scr_height)
        ui.set_color(self.color)
        path.fill()
        self.img.draw(self.x_off,self.y_off,self.img_width*self.ratio/self.scr_cor,self.img_height*self.ratio/self.scr_cor)

    def touch_began(self, touch):
        self.index += 1
        if self.index < self.len_imgs:
            self.img = ui.Image.named(self.path + '/' + self.imgs[self.index])
        else:
            self.index = 0
            self.img = ui.Image.named(self.path + '/' + self.imgs[self.index])
        if self.img != None:
            self.img_width, self.img_height = self.img.size
            self.name = self.imgs[self.index] + ' (' + str(self.img_width) + ',' + str(self.img_height) + ')'
            self.layout()
            self.set_needs_display()
        else:
            self.touch_began(None)
        #self.close()

    def layout(self):
        scr_height_real = self.height * self.scr_cor
        scr_width_real = self.width * self.scr_cor
        y_ratio = scr_height_real / self.img_height
        x_ratio = scr_width_real / self.img_width
        # 1.0 = okay, <1.0 = Image to small, >1.0 = Image to big
        if x_ratio == 1.0 and y_ratio == 1.0:
            self.ratio = 1.0 #perfect size
        elif x_ratio == 1.0 and y_ratio > 1.0:
            self.ratio = 1.0 #perfect width
        elif x_ratio > 1.0 and y_ratio == 1.0:
            self.ratio = 1.0 #perfect height
        elif x_ratio > 1.0 and y_ratio > 1.0:
            self.ratio = 1.0 #show image in original size
        elif x_ratio >= 1.0 and y_ratio < 1.0:
            self.ratio = y_ratio #shrink height
        elif x_ratio < 1.0 and y_ratio >= 1.0:
            self.ratio = x_ratio #shrink width
        elif x_ratio < 1.0 and y_ratio < 1.0:
            if x_ratio < y_ratio: #which side?
                self.ratio = x_ratio
            else:
                self.ratio = y_ratio
        else:
            print('This should never happen. :(')

class PhoneManager(object):
    pos = -1
    searchstr = ''

    def __init__(self):
        self.temp = None
        self.elements = []
        self.view = ui.load_view('PhoneManager')
        self.root = os.path.expanduser('~')
        self.rootlen = len(self.root)
        self.path = os.getcwd()
        self.path_po = self.path
        self.view.name = self.path[self.rootlen:]
        self.make_tableview('tableview1', 0, 50, 320, 454)
        self.tableview1 = self.view['tableview1']
        self.tableview1.flex = 'WH'
        self.lst = self.make_lst()
        self.lst_po = self.lst
        self.filename = ''
        self.files = []
        self.set_button_actions()
        self.view.present('full_screen')

    def set_button_actions(self):               # assumes that ALL buttons have an action method 
        for subview in self.view['scrollview1'].subviews:      # with EXACTLY the same name as the button name
            if isinstance(subview, ui.Button):  # `self.view['btn_Help'].action = self.btn_Help`
                subview.action = getattr(self, subview.name)
                
    def btn_Select(self, sender):
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.name = self.path_po[self.rootlen:]
        self.make_textfield('tf_filter', '*.jpg', 6, 6, 308, 32)
        self.make_segcontr('sc_select', ['All/None', 'Filter', '*.py*'], 6, 46, 308, 64)
        self.make_button('button1', 'Okay', 6, 118, 150, 100, action=self.btn_Select_Okay)
        self.make_button('button2', 'Cancel', 164, 118, 150, 100, action=self.btn_Cancel)

    def btn_Select_Okay(self, sender):
        def search_table(search_str):
          length = len(self.view['tableview1'].data_source.items)
          r = []
          for i in range(1, length):
            if search_str != '.*':
              pos = self.view['tableview1'].data_source.items[i]['title'].rfind(search_str)
              if pos > -1:
                t = tuple([0, i])
                r.append(t)
            else:
              t = tuple([0, i])
              r.append(t)
            self.view['tableview1'].selected_rows = r
              
        rows = self.view['tableview1'].selected_rows
        select = self.view['sc_select'].selected_index
        search_str = ''
        if select == 0:
            if rows == []:
              search_str = '.*'
              search_table(search_str)
            else:
              self.view['tableview1'].selected_rows = []
              self.view['tableview1'].reload_data()
        elif select == 2:
            search_str = '.py'
            search_table(search_str)
        else:
            ext = self.view['tf_filter'].text
            pos = ext.find('*.')
            if pos == 0:
              search_str = ext[pos+1:]
              search_table(search_str)
        self.remove_view_po()
                
    def btn_HTMLview(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          row = self.view['tableview1'].selected_row[1]
          self.view_po = ui.View()
          self.view_po.name = self.view['tableview1'].data_source.items[row]['title']
          wv = ui.WebView()
          wv.width = self.view_po.width
          wv.height = self.view_po.height
          wv.flex = 'WH'
          self.view_po.add_subview(wv)
          self.view_po.present('full_screen')
          wv.load_url(self.path + '/' + self.filename)
          wv.scales_page_to_fit = True
        else:
          self.btn_Help(None,message='Please select one file.',name='Error')

    def btn_Edit(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          row = self.view['tableview1'].selected_row[1]
          filename = self.view['tableview1'].data_source.items[row]['title']
          editor.open_file(self.path + '/' + filename)
          self.view.close()
        else:
          self.btn_Help(None,message='Please select one file.',name='Error')

    def btn_PicView(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          row = self.view['tableview1'].selected_row[1]
          filename = self.view['tableview1'].data_source.items[row]['title']
          imgs = get_imgs(self.path)
          index = imgs.index(filename)
          self.view_po = MyImageView(self.path,filename,imgs,index)
          self.view_po.present('full_screen')
        else:
          self.btn_Help(None,message='Please select start file.',name='Error')

    @ui.in_background
    def btn_GetPic(self, sender):
        bytestring = photos.pick_image(raw_data=True)
        png = bytearray.fromhex('89504E47')
        jpg = bytearray.fromhex('FFD8FF')
        gif = bytearray.fromhex('474946')
        bmp = bytearray.fromhex('424D')
        tif = bytearray.fromhex('49492A')
        ext = ''
        if bytestring[0:4] == png:
          ext = '.png'
        elif bytestring[0:3] == jpg:
          ext = '.jpg'
        elif bytestring[0:3] == gif:
          ext = '.gif'
        elif bytestring[0:2] == bmp:
          ext = '.bmp'
        elif bytestring[0:3] == tif:
          ext = '.tif'
        else:
          self.btn_Help(None,message="Unknown image type! (Only png, jpg, gif, bmp and tif are supported)",name='Error')
          return
        size = len(bytestring)
        for i in xrange(sys.maxint):
          filename = 'image{}'.format(str(i).zfill(3)) + ext
          if not os.path.exists(filename):
            file = open(self.path + '/' + filename, 'wb')
            file.write(bytestring)
            break
        self.make_lst()
        self.view['tableview1'].reload_data()
        console.hud_alert(filename + ' / ' + str(size / 1024) + ' kB', duration = 3.0)

    def btn_Help(self, sender, message='', name='Help'):
        if message == '':
            message = 'Scroll buttons to the left for all commands.\nRemoveDir deletes everthing in the current dir (files and subdirs).\nExtract always creates a subdir with the archivename.\nPicView now browses png, jpg, gif, bmp and tif.\nMove and Rename are changing the directory path/name when no file is selected!!!\nMultiselect for move, copy, delete and compress.\nUse at your own risk.'
        self.temp = self.view.name
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.view.name = name
        self.make_textview('textview', message, 6, 6, self.view.width - 12, 150, edit=False)
        self.view['textview'].flex = 'WR'
        self.make_button('button', 'Cancel', 6, 160, self.view.width - 12, self.view.height - 160, action=self.btn_Cancel)
        self.view['button'].flex = 'WRH'

    def make_view_browse(self):
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.name = self.path_po[self.rootlen:]
        self.make_tableview('tableview2', 6, 6, self.view.width - 12, self.view.height - 68)
        self.view['tableview2'].flex = 'WH'
        self.make_button('button1', 'Okay', 6, self.view.height - 56, 150, 50, action=self.btn_Move_Okay)
        self.view['button1'].flex = 'RT'
        self.make_button('button2', 'Cancel', self.view.width - 156, self.view.height - 56, 150, 50, action=self.btn_Cancel)
        self.view['button2'].flex = 'LT'

    def btn_Move(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows > 0:
          self.files = []
          for row in self.view['tableview1'].selected_rows:
            self.files.append(self.view['tableview1'].data_source.items[row[1]]['title'])
        self.make_view_browse()
        self.path_po = self.path
        self.make_lst_po()
        self.view['tableview2'].reload()

    def btn_Move_Okay(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        try:
            if sel_rows == 0:
                shutil.move(self.path,self.path_po)
                self.path = self.path_po
                self.make_lst()
                self.view['tableview1'].reload_data()
                self.remove_view_po()
            else:
                for filename in self.files:
                  if not os.path.isfile(self.path_po + '/' + filename): # file  doesn't exist
                    shutil.move(self.path + '/' + filename,self.path_po + '/' + filename)
                    self.make_lst()
                    self.view['tableview1'].reload_data()
                    self.remove_view_po()
                  else: # file exist
                    self.remove_view_po()
                    self.btn_Help(None,message='File: ' + filename + ' already exists in the destination directory.',name='Error')
        except Exception as e: # move error
            self.remove_view_po()
            self.btn_Help(None,message=str(e),name='Error')

    def make_lst_po(self):
        dirs = get_dirs(self.path_po)
        lst = ui.ListDataSource(dirs)
        self.view['tableview2'].data_source = lst
        self.view['tableview2'].delegate = lst
        self.view['tableview2'].editing = False
        lst.action = self.table_tapped_po
        lst.delete_enabled = False
        lst.font = ('Courier', 18)
        return lst

    def table_tapped_po(self, sender):
        dirname_tapped = sender.items[sender.selected_row]
        if dirname_tapped[0] == '/':  # we have a directory
            if dirname_tapped == '/..':  # move up one
                self.path_po = self.path_po.rpartition('/')[0]
            else:                         # move down one
                self.path_po = self.path_po + dirname_tapped
            self.view.name = self.path_po[self.rootlen:]
            self.lst_po = self.make_lst_po()
            self.view['tableview2'].reload()

    @ui.in_background
    def btn_OpenIn(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          row = self.view['tableview1'].selected_row[1]
          filename = self.view['tableview1'].data_source.items[row]['title']
          file = self.path + '/' + filename
          console.open_in(file)
        else:
          self.btn_Help(None,message='Please select one file.',name='Error')

    def btn_Download(self, sender):
        url = clipboard.get()
        pos = url.find('://') # ftp://, http://, https:// >> 3-5
        if pos < 3 or pos > 5:
            url = 'http://www.'
            filename = ''
        else:
            pos = url.rfind('/') + 1
            filename = url[pos:]
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.make_label('label1', 'Download:', 6, 6, 308, 32)
        self.make_textfield('textfield1', url, 6, 46, 308, 32)
        self.make_label('label3', 'Filename:', 6, 94, 308, 32)
        self.make_textfield('textfield2', filename, 6, 134, 308, 32)
        self.make_button('button1', 'Okay', 6, 182, 150, 100, action=self.btn_Download_Okay)
        self.make_button('button2', 'Cancel', 164, 182, 150, 100, action=self.btn_Cancel) #94

    def btn_Download_Okay(self, sender):
        url = self.view['textfield1'].text
        pos = url.find('://') # ftp://, http://, https:// >> 3-5
        if pos > 2 and pos < 6:
            if self.view['textfield2'].text == '':
                pos = url.rfind('/') + 1
                filename = url[pos:]
            else:
                filename = self.view['textfield2'].text
            try:
                dl = requests.get(url, stream=True)
                with open(self.path + '/' + filename, 'wb') as f:
                    for chunk in dl.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                self.make_lst()
                self.view['tableview1'].reload_data()
                self.remove_view_po()
            except Exception as e:
                self.remove_view_po()
                self.btn_Help(None,message=str(e),name='Error')
        else:
            self.remove_view_po()
            self.btn_Help(None,message='Please start url with ftp://, http:// or https://.',name='Error')

    def btn_Compress(self, sender):
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.name = self.path_po[self.rootlen:]
        self.make_textfield('tf_name', 'Archivename', 6, 6, 308, 32)
        self.make_segcontr('sc_compression', ['.zip', '.tar', '.tar.gz', '.tar.bz2'], 6, 46, 308, 64)
        self.make_segcontr('sc_range', ['Selected', 'All', '*.py*'], 6, 118, 308, 64)
        self.make_button('button1', 'Okay', 6, 190, 150, 100, action=self.btn_Compress_Okay)
        self.make_button('button2', 'Cancel', 164, 190, 150, 100, action=self.btn_Cancel)

    def btn_Compress_Okay(self, sender):
        def tar_compress(archive_name, compression, filter=False, files=[]):
            if compression == 'tar':
                archive_name += '.tar'
                mode = 'w'
            elif compression == 'gztar':
                archive_name += '.tar.gz'
                mode = 'w:gz'
            elif compression == 'bztar':
                archive_name += '.tar.bz2'
                mode = 'w:bz2'
            tar = tarfile.open(archive_name, mode)
            if filter:
                for file in files:
                    tar.add(self.path + '/' + file,arcname=file)
            else:
                tar.add(self.path + '/' + self.filename,arcname=files[0])
            tar.close()
            
        sel_rows = len(self.view['tableview1'].selected_rows)
        files = []
        if sel_rows > 0:
          #self.files = []
          for row in self.view['tableview1'].selected_rows:
            files.append(self.view['tableview1'].data_source.items[row[1]]['title'])
        comp = self.view['sc_compression'].selected_index
        compression = ''
        mode = ''
        rang = self.view['sc_range'].selected_index
        archive_name = self.path + '/' + self.view['tf_name'].text # no extension
        if comp == 0:
            compression = 'zip'
        elif comp == 1:
            compression = 'tar'
        elif comp == 2:
            compression = 'gztar'
        else:
            compression = 'bztar'
        if rang == 0 and sel_rows == 1: # selected file
            if compression == 'zip':
                zf = zipfile.ZipFile(archive_name + '.zip', mode='w')
                zf.write(self.path + '/' + files[0], os.path.basename(self.path + '/' + files[0]), compress_type=zipfile.ZIP_DEFLATED)
                zf.close()
            else:
                tar_compress(archive_name, compression, filter=False, files=files)
        else:
            if rang == 1: # all files
                files = self.get_files()
            elif rang == 2: # only python files (*.py*)
                files = self.get_files(filter=True)
            if compression == 'zip':
                zf = zipfile.ZipFile(archive_name + '.zip', mode='w')
                for file in files:
                    zf.write(self.path + '/' + file, os.path.basename(self.path + '/' + file), compress_type=zipfile.ZIP_DEFLATED)
                zf.close()
            else:
                tar_compress(archive_name, compression, filter=True, files=files)
        self.make_lst()
        self.view['tableview1'].reload_data()
        self.remove_view_po()

    def get_files(self,filter=False):
        files = []
        for entry in sorted(os.listdir(self.path)):
            if os.path.isfile(self.path + '/' + entry):
                if filter:
                    if entry.find('.py') >= 0: # has to be fixed with re
                        files.append(entry)
                else:
                    files.append(entry)
        return files

    def btn_Extract(self, sender):
      sel_rows = len(self.view['tableview1'].selected_rows)
      if sel_rows == 1:
        pos = self.filename.rfind('.')
        ext = self.filename[pos+1:]
        dir_name = ''
        if ext == 'zip' or ext == 'tar':
            dir_name = self.filename[:pos]
            os.mkdir(self.path + '/' + dir_name)
            if ext == 'zip':
                file = open(self.path + '/' + self.filename, 'rb')
                z = zipfile.ZipFile(file)
                z.extractall(self.path + '/' + dir_name)
                file.close()
            elif ext == 'tar':
                tar = tarfile.open(self.path + '/' + self.filename)
                tar.extractall(self.path + '/' + dir_name)
                tar.close()
        elif ext == 'gz' or ext == 'bz2':
            dir_name = self.filename[:pos-4]
            os.mkdir(self.path + '/' + dir_name)
            tar = tarfile.open(self.path + '/' + self.filename)
            tar.extractall(self.path + '/' + dir_name)
            tar.close()
        else:
          self.btn_Help(None,message='Unsupported compression type.',name='Error')
        self.make_lst()
        self.view['tableview1'].reload_data()
      else:
        self.btn_Help(None,message='Please select one file.',name='Error')

    def btn_HexView(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          row = self.view['tableview1'].selected_row[1]
          filename = self.view['tableview1'].data_source.items[row]['title']
          self.hexview_a_file(filename)
        else:
          self.btn_Help(None,message='Please select one file.',name='Error')

    def btn_RemoveDir(self, sender):
        pos = self.path.rfind('/')
        dir = self.path[pos:]
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.make_label('label1', 'Remove Dir:', 6, 6, 308, 32)
        self.make_textfield('textfield1', dir, 6, 46, 308, 32)
        self.make_button('button1', 'Okay', 6, 94, 150, 100, action=self.btn_RemoveDir_Okay)
        self.make_button('button2', 'Cancel', 164, 94, 150, 100, action=self.btn_Cancel)

    def btn_RemoveDir_Okay(self, sender):
        shutil.rmtree(self.path)
        pos = self.path.rfind('/')
        dir = self.path[:pos]
        self.path = dir
        self.view.name = self.path[self.rootlen:]
        self.make_lst()
        self.view['tableview1'].reload_data()
        self.remove_view_po()

    def btn_MakeDir(self, sender):
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.make_label('label1', 'Make Dir:', 6, 6, 308, 32)
        self.make_textfield('textfield1', '', 6, 46, 308, 32)
        self.make_button('button1', 'Okay', 6, 94, 150, 100, action=self.btn_MakeDir_Okay)
        self.make_button('button2', 'Cancel', 164, 94, 150, 100, action=self.btn_Cancel)

    def btn_MakeDir_Okay(self, sender):
        os.mkdir(self.path + '/' + self.view['textfield1'].text)
        self.make_lst()
        self.view['tableview1'].reload_data()
        self.remove_view_po()

    def btn_Delete(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows > 0:
          self.files = []
          for row in self.view['tableview1'].selected_rows:
            self.files.append(self.view['tableview1'].data_source.items[row[1]]['title'])
          self.view['scrollview1'].hidden = True 
          self.view['tableview1'].hidden = True
          self.make_label('label1', 'Delete:', 6, 6, 308, 32)
          if sel_rows == 1:
            self.make_textfield('textfield1', self.filename, 6, 46, 308, 32)
          else:
            self.make_textfield('textfield1', str(sel_rows) + ' files?', 6, 46, 308, 32)
          self.make_button('button1', 'Okay', 6, 94, 150, 100, action=self.btn_Delete_Okay)
          self.make_button('button2', 'Cancel', 164, 94, 150, 100, action=self.btn_Cancel)
        else:
          self.btn_Help(None,message='Please select a file.',name='Error')

    def btn_Delete_Okay(self, sender):
        for filename in self.files:
          os.remove(self.path + '/' + filename)
        self.make_lst()
        self.view['tableview1'].reload_data()
        self.remove_view_po()

    def btn_Copy(self, sender):
        #copy+rename in current dir // copy several files in other dir
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows > 0:
          if sel_rows == 1:
            row = self.view['tableview1'].selected_row[1]
            filename = self.view['tableview1'].data_source.items[row]['title']
            self.view['scrollview1'].hidden = True 
            self.view['tableview1'].hidden = True
            self.make_label('label1', 'Make copy of:', 6, 6, 308, 32)
            self.make_label('label2', self.filename, 6, 46, 308, 32, color='lightgrey', border=0.5, radius=5)
            self.make_label('label3', 'New Name:', 6, 94, 308, 32)
            self.make_textfield('textfield1', self.filename, 6, 134, 308, 32)
            self.make_button('button1', 'Okay', 6, 182, 150, 100, action=self.btn_Copy_Okay)
            self.make_button('button2', 'Cancel', 164, 182, 150, 100, action=self.btn_Cancel)
          else:
            self.files = []
            for row in self.view['tableview1'].selected_rows:
              self.files.append(self.view['tableview1'].data_source.items[row[1]]['title'])
            self.view['scrollview1'].hidden = True 
            self.view['tableview1'].hidden = True
            self.name = self.path_po[self.rootlen:]
            self.make_tableview('tableview2', 6, 6, self.view.width - 12, self.view.height - 68)
            self.view['tableview2'].flex = 'WH'
            self.make_button('button1', 'Okay', 6, self.view.height - 56, 150, 50, action=self.btn_Copy_Okay)
            self.view['button1'].flex = 'RT'
            self.make_button('button2', 'Cancel', self.view.width - 156, self.view.height - 56, 150, 50, action=self.btn_Cancel)
            self.view['button2'].flex = 'LT'
            self.path_po = self.path
            self.make_lst_po()
            self.view['tableview2'].reload()
        else:
          self.btn_Help(None,message='Please select a file.',name='Error')

    def btn_Copy_Okay(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows == 1:
          if self.filename != self.view['textfield1'].text:
            shutil.copyfile(self.path + '/' + self.filename, self.path + '/' + self.view['textfield1'].text)
            self.make_lst()
            self.view['tableview1'].reload_data()
          self.remove_view_po()
        else:
          error = False 
          for filename in self.files:
            if not os.path.isfile(self.path_po + '/' + filename): # file  doesn't exist
              shutil.copyfile(self.path + '/' + filename,self.path_po + '/' + filename)
            else:
              error = True
          self.make_lst()
          self.view['tableview1'].reload_data()
          self.remove_view_po()
          if error:
            self.btn_Help(None,message='Some or all files already exists in the destination directory.',name='Error')

    def btn_Rename(self, sender):
        sel_rows = len(self.view['tableview1'].selected_rows)
        if sel_rows < 2:
          if sel_rows > 0:
            row = self.view['tableview1'].selected_row[1]
            self.filename = self.view['tableview1'].data_source.items[row]['title']
          self.view['scrollview1'].hidden = True 
          self.view['tableview1'].hidden = True
          self.make_label('label1', 'Old Name:', 6, 6, 308, 32)
          self.make_label('label2', self.filename, 6, 46, 308, 32, color='lightgrey', border=0.5, radius=5)
          self.make_label('label3', 'New Name:', 6, 94, 308, 32)
          self.make_textfield('textfield1', self.filename, 6, 134, 308, 32)
          self.make_button('button1', 'Okay', 6, 182, 150, 100, action=self.btn_Rename_Okay)
          self.make_button('button2', 'Cancel', 164, 182, 150, 100, action=self.btn_Cancel)
        else:
          self.btn_Help(None,message='Please select one item to rename a file or no item to rename the current directory.',name='Error')

    def btn_Rename_Okay(self, sender):
        if self.filename == '':  #rename directory
            pos = self.path.rfind('/')
            dir = self.path[:pos + 1] + self.view['textfield1'].text
            os.rename(self.path + '/', dir + '/')
            self.path = dir
            self.view.name = dir[self.rootlen:]
        else:
            os.rename(self.path + '/' + self.filename, self.path + '/' + self.view['textfield1'].text)
        self.make_lst()
        self.view['tableview1'].reload_data()
        self.remove_view_po()

    def btn_Cancel(self, sender):
        self.remove_view_po()

    def make_label(self, name, text, x, y, width, height, color=None, border=None, radius=None):
        label = ui.Label()
        label.name = name
        label.text = text
        label.frame = (x, y, width, height)
        if color != None:
          label.border_color = color
          label.border_width = border
          label.corner_radius = radius
        self.view.add_subview(label)
        self.elements.append(name)

    def make_textfield(self, name, text, x, y, width, height):
        textfield = ui.TextField()
        textfield.name = name
        textfield.text = text
        textfield.frame = (x, y, width, height)
        textfield.clear_button_mode = 'always'
        self.view.add_subview(textfield)
        self.elements.append(name)

    def make_button(self, name, title, x, y, width, height, action, color='blue', border=0.7, radius=5):
        button = ui.Button()
        button.name = name 
        button.title = title
        button.frame = (x, y, width, height)
        button.border_color = color
        button.border_width = border
        button.corner_radius = radius
        button.action = action
        self.view.add_subview(button)
        self.elements.append(name)

    def make_segcontr(self, name, segments, x, y, width, height):
        segcontr = ui.SegmentedControl()
        segcontr.name = name
        segcontr.segments = segments
        segcontr.selected_index = 0
        segcontr.frame = (x, y, width, height)
        self.view.add_subview(segcontr)
        self.elements.append(name)

    def make_textview(self, name, text, x, y, width, height, edit=True, color=None, border=None, radius=None):
        textview = ui.TextView()
        textview.name = name
        textview.text = text
        textview.frame = (x, y, width, height)
        if color != None:
            textview.border_color = color
            textview.border_width = border
            textview.corner_radius = radius
        if edit == False:
            textview.font = ('Courier', 11)
            textview.editable = False 
        self.view.add_subview(textview)
        self.elements.append(name)

    def remove_view_po(self):
        for element in self.elements:
          self.view.remove_subview(self.view[element])
        self.elements = []
        self.view['scrollview1'].hidden = False 
        self.view['tableview1'].hidden = False 
        if self.temp != None:
          self.view.name = self.temp
          self.temp = None

    def make_tableview(self, name, x, y, width, height):
        tableview = ui.TableView()
        tableview.name = name
        tableview.frame = (x, y, width, height)
        tableview.border_width = 1
        tableview.border_color = 'blue'
        tableview.corner_radius = 5
        tableview.row_height = 40
        tableview.bg_color = 'black'
        tableview.background_color = 'white'
        tableview.allows_selection = True
        tableview.allows_multiple_selection = True
        self.view.add_subview(tableview)
        if name != 'tableview1':  #files view
            self.elements.append(name)

    def make_lst(self):
        dirs_and_files = get_dir(self.path)
        lst = ui.ListDataSource(dirs_and_files)
        lst.accessory_action = self.fileinfo
        self.tableview1.data_source = lst
        self.tableview1.delegate = lst
        self.tableview1.editing = False
        lst.action = self.table_tapped
        lst.delete_enabled = False
        lst.font = ('Courier', 18)
        return lst

    def table_tapped(self, sender):
        filename_tapped = sender.items[sender.selected_row]['title']
        #print filename_tapped
        if filename_tapped[0] == '/':  # we have a directory
            if filename_tapped == '/..':  # move up one
                self.path = self.path.rpartition('/')[0]
            else:                         # move down one
                self.path = self.path + filename_tapped
            self.view.name = self.path[self.rootlen:]
            self.lst = self.make_lst()
            self.tableview1.reload()
            self.filename = ''
        else:
            self.filename = filename_tapped

    def btn_Search(self, sender):
        tvd = self.view['tv_data']
        tfss = self.view['tf_search']
        if tfss.text != '':
            if tfss.text == PhoneManager.searchstr:
                #next hit
                PhoneManager.pos = tvd.text.find(PhoneManager.searchstr,PhoneManager.pos+1)
            else:
                #new search
                PhoneManager.searchstr = tfss.text
                PhoneManager.pos = tvd.text.find(PhoneManager.searchstr)
            if PhoneManager.pos >= 0:    #hit
                x = tvd.text.find('\n',PhoneManager.pos) - 79        #line start
                y = len(tvd.text) - len(tvd.text) % 80  #last line start
                if PhoneManager.pos < y:
                    sender.title = tvd.text[x:x+10]
                else:
                    sender.title = tvd.text[y:y+10]
                tvd.selected_range = (PhoneManager.pos, PhoneManager.pos+len(PhoneManager.searchstr))  # works only when textview is active!!!
            else:
                sender.title = 'Restart'
                PhoneManager.pos = -1
        else:
            sender.title = 'Search'
            PhoneManager.pos = -1

    def hexview_a_file(self, filename):
        self.view['scrollview1'].hidden = True 
        self.view['tableview1'].hidden = True
        self.view.name = filename
        self.make_button('btn_close', 'X', 6, 6, 32, 32, self.btn_Cancel)
        self.make_textfield('tf_search', '', 44, 6, self.view.width - 156, 32)
        self.view['tf_search'].flex = 'W'
        self.make_button('btn_search', 'Search', self.view.width - 106, 6, 100, 32, self.btn_Search)
        self.view['btn_search'].flex = 'L'
        full_pathname = self.path + '/' + filename
        self.make_textview('tv_data', hex_view(full_pathname), 6, 46, self.view.width - 12, self.view.height - 50, edit=False, color='lightgrey', border=0.5, radius=5)
        self.view['tv_data'].flex = 'WH'

    @ui.in_background
    def fileinfo(self, sender):
        til = sender.items[sender.tapped_accessory_row]['title']
        siz = sender.items[sender.tapped_accessory_row]['size']
        dat = sender.items[sender.tapped_accessory_row]['date']
        title = til
        msg = str(siz) + ' Bytes'
        msg += '\n' + str(dat)
        console.alert(title, msg)

PhoneManager()
