# coding: utf-8

import datetime, os, ui

def get_dir(path = os.path.expanduser('~')):
    dirs  = [] if path == os.path.expanduser('~') else ['..']
    files = []
    for entry in sorted(os.listdir(path)):
        if os.path.isdir(path + '/' + entry):
            dirs.append(entry)
        else:
            files.append(entry)
    dirs_and_files = ['/' + directory for directory in dirs]
    for file in files:
        full_pathname = path + '/' + file
        size = '{} Bytes'.format(os.path.getsize(full_pathname))
        date = datetime.datetime.fromtimestamp(os.path.getmtime(full_pathname))
        dirs_and_files.append('{:43} | {:20} | {}'.format(file, size, date))
    return dirs_and_files

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

class HexViewerView(ui.View):
    pos = -1
    searchstr = ''

    def __init__(self):
        self.name = self.path = os.getcwd()
        self.background_color = 'white'
        self.tableview1 = self.make_tableview1()
        self.lst = self.make_lst()
        self.present('fullscreen')

    def make_tableview1(self):
        tableview = ui.TableView()
        tableview.frame = self.frame
        tableview.x = tableview.y = 0
        tableview.flex = 'WH'
        tableview.row_height = 30
        tableview.background_color = '#DBDBDB'
        tableview.allows_selection = True
        self.add_subview(tableview)
        return tableview

    def make_lst(self):
        dirs_and_files = get_dir(self.path)
        lst = ui.ListDataSource(dirs_and_files)
        self.tableview1.data_source = lst
        self.tableview1.delegate = lst
        self.tableview1.editing = False
        lst.action = self.table_tapped
        lst.delete_enabled = False
        lst.font = ('Courier', 18)
        return lst

    def table_tapped(self, sender):
        rowtext = sender.items[sender.selected_row]
        filename_tapped = rowtext.partition('|')[0].strip()
        if filename_tapped[0] == '/':  # we have a directory
            if filename_tapped == '/..':  # move up one
                self.path = self.path.rpartition('/')[0]
            else:                         # move down one
                self.path = self.path + filename_tapped
            self.name = self.path
            self.lst = self.make_lst()
            self.tableview1.reload()
        else:
            self.hexview_a_file(filename_tapped)

    def make_textview1(self):
        textview = ui.TextView()
        textview.name = 'tv_data'
        textview.frame = self.frame
        textview.x = 6
        textview.y = 46
        textview.width = self.width - 12
        textview.height = self.height - 52
        textview.autoresizing = 'WHT'
        #textview.editable = False     #easy access no double tap needed
        textview.font = ('Courier', 15)
        self.add_subview(textview)
        return textview

    def make_textfield1(self):
        textfield = ui.TextField()
        textfield.name = 'tf_search_str'
        textfield.x = textfield.y = 6
        textfield.width = self.width - 161
        textfield.height = 32
        textfield.flex = 'WR'
        self.add_subview(textfield)
        return textfield

    def make_button1(self, title = 'Search'):
        button = ui.Button()
        button.name = 'btn_search'
        button.title = title
        button.x = self.width - 149
        button.y = 6
        button.width = 144
        button.height = 32
        button.flex = 'WL'
        button.border_width = 2
        button.corner_radius = 5
        button.action = self.button_action
        self.add_subview(button)
        return button

    def button_action(self, sender):
        tvd = self['tv_data']
        tfss = self['tf_search_str']
        if tfss.text != '':
            if tfss.text == HexViewerView.searchstr:
                #next hit
                HexViewerView.pos = tvd.text.find(HexViewerView.searchstr,HexViewerView.pos+1)
            else:
                #new search
                HexViewerView.searchstr = tfss.text
                HexViewerView.pos = tvd.text.find(HexViewerView.searchstr)
            if HexViewerView.pos >= 0:    #hit
                x = tvd.text.find('\n',HexViewerView.pos) - 79        #line start
                y = len(tvd.text) - len(tvd.text) % 80  #last line start
                if HexViewerView.pos < y:
                    sender.title = tvd.text[x:x+10]
                else:
                    sender.title = tvd.text[y:y+10]
                tvd.selected_range = (HexViewerView.pos, HexViewerView.pos+len(HexViewerView.searchstr))  # works only when textview is active!!!
            else:
                sender.title = 'Restart'
                HexViewerView.pos = -1
        else:
            sender.title = 'Search'
            HexViewerView.pos = -1

    def hexview_a_file(self, filename):
        self.tableview1.hidden = True
        self.textview1 = self.make_textview1()
        self.textfield1 = self.make_textfield1()
        self.button1 = self.make_button1()
        self.name = 'HexViewer: ' + filename
        full_pathname = self.path + '/' + filename
        self.textview1.text = hex_view(full_pathname)

HexViewerView()
