# coding: utf-8

# https://github.com/coomlata1/pythonista-scripts

'''
#---Script: GetPyuiAttribs.py
#---Author: coomlata1
#---Created: 02/19/2017
#---Last Modified: 02/27/2017

#---Purpose: This Pythonista script allows the selection of a 
    pyui file from any folder in the Pythonista documents 
    directory. Once selected, the script mines the attributes 
    of the view and subview objects in the file and converts 
    them to text that can be modified slightly and entered as 
    code into the associated py file. This makes for an 
    easier coding transistion for scripts that use a pyui 
    file to be merged into a single py file. The attributes 
    are displayed in the console and written to the clipboard 
    for easy copying to the py script.

#---Contributions: The idea for this script came from a 
    thread on the Pythonista forum here:
    'https://forum.omz-software.com/topic/989/any-ui-module-tutorials-out-there/6'

    Inspiration also came from the script GUI_Helper.py. 
    Thanks to @nekotaroneko for GUI_Helper.py available here:
    'https://github.com/nekotaroneko/GUI_Helper'
    
    The excellent file-picker code used in this script and in 
    Gui_Helper.py comes from the script 'File Picker.py' by
    @omz at 'https://gist.github.com/e3433ebba20c92b63111'
''' 
from __future__ import print_function
import json, pprint, clipboard, os

# file_picker code
def file_picker(title=None, root_dir=None, multiple=False,
        select_dirs=False, file_pattern=None, show_size=True):
  import ui
  from objc_util import ObjCInstance, ObjCClass
  from operator import attrgetter
  import functools
  import ftplib, re

  class TreeNode (object):
    def __init__(self):
      self.expanded = False
      self.children = None
      self.leaf = True
      self.title = ''
      self.subtitle = ''
      self.icon_name = None
      self.level = 0
      self.enabled = True

    def expand_children(self):
      self.expanded = True
      self.children = []

    def collapse_children(self):
      self.expanded = False

    def __repr__(self):
      return '<TreeNode: "%s"%s>' % (self.title, ' (expanded)' if self.expanded else '')

  class FileTreeNode (TreeNode):
    def __init__(self, path, show_size=True, select_dirs=True,
    file_pattern=None):
      TreeNode.__init__(self)
      self.path = path
      self.title = os.path.split(path)[1]
      self.select_dirs = select_dirs
      self.file_pattern = file_pattern
      is_dir = os.path.isdir(path)
      self.leaf = not is_dir
      ext = os.path.splitext(path)[1].lower()
      if is_dir:
        self.icon_name = 'Folder'
      elif ext == '.py':
        self.icon_name = 'FilePY'
      elif ext == '.pyui':
        self.icon_name = 'FileUI'
      elif ext in ('.png', '.jpg', '.jpeg', '.gif'):
        self.icon_name = 'FileImage'
      else:
        self.icon_name = 'FileOther'
      self.show_size = show_size
      if not is_dir and show_size:
        self.subtitle = human_size((os.stat(self.path).st_size))
      if is_dir and not select_dirs:
        self.enabled = False
      elif not is_dir:
        filename = os.path.split(path)[1]
        self.enabled = not file_pattern or re.match(file_pattern, filename)

    @property
    def cmp_title(self):
      return self.title.lower()

    def expand_children(self):
      if self.children is not None:
        self.expanded = True
        return
      files = os.listdir(self.path)
      children = []
      for i,filename in enumerate(files):
        if filename.startswith('.'):
          continue

        full_path = os.path.join(self.path, filename)
        node = FileTreeNode(full_path, self.show_size, self.select_dirs, self.file_pattern)
        node.level = self.level + 1
        children.append(node)

      self.expanded = True
      self.children = sorted(children, key=attrgetter('leaf', 'cmp_title'))

  class TreeDialogController (object):
    def __init__(self, root_node, allow_multi=False, async_mode=False):
      self.async_mode = async_mode
      self.allow_multi = allow_multi
      self.selected_entries = None
      self.table_view = ui.TableView()
      self.table_view.frame = (0, 0, 500, 500)
      self.table_view.data_source = self
      self.table_view.delegate = self
      self.table_view.flex = 'WH'
      self.table_view.allows_multiple_selection = True
      self.table_view.tint_color = 'gray'
      self.view = ui.View(frame=self.table_view.frame)
      self.view.add_subview(self.table_view)
      self.view.name = root_node.title
      self.busy_view = ui.View(frame=self.view.bounds, flex='WH', background_color=(0, 0, 0, 0.35))
      hud = ui.View(frame=(self.view.center.x - 50, self.view.center.y - 50, 100, 100))
      hud.background_color = (0, 0, 0, 0.7)
      hud.corner_radius = 8.0
      hud.flex = 'TLRB'
      spinner = ui.ActivityIndicator()
      spinner.style = ui.ACTIVITY_INDICATOR_STYLE_WHITE_LARGE
      spinner.center = (50, 50)
      spinner.start_animating()
      hud.add_subview(spinner)
      self.busy_view.add_subview(hud)
      self.busy_view.alpha = 0.0
      self.view.add_subview(self.busy_view)
      self.done_btn = ui.ButtonItem(title='Done', action=self.done_action)
      self.root_btn = ui.ButtonItem(title='Root', action=self.root_btn_action)
      self.mobile_btn = ui.ButtonItem(title='Mobile', action=self.mobile_btn_action)
      if self.allow_multi:
        self.view.right_button_items = [self.done_btn, self.mobile_btn, self.root_btn]
      self.done_btn.enabled = False
      self.root_node = root_node
      self.entries = []
      self.flat_entries = []
      if self.async_mode:
        self.set_busy(True)
        t = threading.Thread(target=self.expand_root)
        t.start()
      else:
        self.expand_root()

    def expand_root(self):
      self.root_node.expand_children()
      self.set_busy(False)
      self.entries = self.root_node.children
      self.flat_entries = self.entries
      self.table_view.reload()

    def flatten_entries(self, entries, dest=None):
      if dest is None:
        dest = []
      for entry in entries:
        dest.append(entry)
        if not entry.leaf and entry.expanded:
          self.flatten_entries(entry.children, dest)
      return dest

    def rebuild_flat_entries(self):
      self.flat_entries = self.flatten_entries(self.entries)

    def tableview_number_of_rows(self, tv, section):
      return len(self.flat_entries)

    def tableview_cell_for_row(self, tv, section, row):
      cell = ui.TableViewCell()
      entry = self.flat_entries[row]
      level = entry.level - 1
      image_view = ui.ImageView(frame=(44 + 20*level, 5, 34, 34))
      label_x = 44+34+8+20*level
      label_w = cell.content_view.bounds.w - label_x - 8
      if entry.subtitle:
        label_frame = (label_x, 0, label_w, 26)
        sub_label = ui.Label(frame=(label_x, 26, label_w, 14))
        sub_label.font = ('<System>', 12)
        sub_label.text = entry.subtitle
        sub_label.text_color = '#999'
        cell.content_view.add_subview(sub_label)
      else:
        label_frame = (label_x, 0, label_w, 44)
      label = ui.Label(frame=label_frame)
      if entry.subtitle:
        label.font = ('<System>', 15)
      else:
        label.font = ('<System>', 18)
      label.text = entry.title
      label.flex = 'W'
      cell.content_view.add_subview(label)
      if entry.leaf and not entry.enabled:
        label.text_color = '#999'
      cell.content_view.add_subview(image_view)
      if not entry.leaf:
        has_children = entry.expanded
        btn = ui.Button(image=ui.Image.named('CollapseFolder' if has_children else 'ExpandFolder'))
        btn.frame = (20*level, 0, 44, 44)
        btn.action = self.expand_dir_action
        cell.content_view.add_subview(btn)
      if entry.icon_name:
        image_view.image = ui.Image.named(entry.icon_name)
      else:
        image_view.image = None
      cell.selectable = entry.enabled
      return cell

    def row_for_view(self, sender):
      '''Helper to find the row index for an 'expand' button'''
      cell = ObjCInstance(sender)
      while not cell.isKindOfClass_(ObjCClass('UITableViewCell')):
        cell = cell.superview()
      return ObjCInstance(self.table_view).indexPathForCell_(cell).row()

    def expand_dir_action(self, sender):
      '''Invoked by 'expand' button'''
      row = self.row_for_view(sender)
      entry = self.flat_entries[row]
      if entry.expanded:
        sender.image = ui.Image.named('ExpandFolder')
      else:
        sender.image = ui.Image.named('CollapseFolder')
      self.toggle_dir(row)
      self.update_done_btn()

    def toggle_dir(self, row):
      '''Expand or collapse a folder node'''
      entry = self.flat_entries[row]
      if entry.expanded:
        entry.collapse_children()
        old_len = len(self.flat_entries)
        self.rebuild_flat_entries()
        num_deleted = old_len - len(self.flat_entries)
        deleted_rows = range(row + 1, row + num_deleted + 1)
        self.table_view.delete_rows(deleted_rows)
      else:
        if self.async_mode:
          self.set_busy(True)
          expand = functools.partial(self.do_expand, entry, row)
          t = threading.Thread(target=expand)
          t.start()
        else:
          self.do_expand(entry, row)

    def do_expand(self, entry, row):
      '''Actual folder expansion (called on background thread if async_mode is enabled)'''
      entry.expand_children()
      self.set_busy(False)
      old_len = len(self.flat_entries)
      self.rebuild_flat_entries()
      num_inserted = len(self.flat_entries) - old_len
      inserted_rows = range(row + 1, row + num_inserted + 1)
      self.table_view.insert_rows(inserted_rows)

    def tableview_did_select(self, tv, section, row):
      self.update_done_btn()

    def tableview_did_deselect(self, tv, section, row):
      self.update_done_btn()

    def update_done_btn(self):
      '''Deactivate the done button when nothing is selected'''
      selected = [self.flat_entries[i[1]] for i in self.table_view.selected_rows if self.flat_entries[i[1]].enabled]
      if selected and not self.allow_multi:
        self.done_action(None)
      else:
        self.done_btn.enabled = len(selected) > 0

    def set_busy(self, flag):
      '''Show/hide spinner overlay'''
      def anim():
        self.busy_view.alpha = 1.0 if flag else 0.0
      ui.animate(anim)

    def done_action(self, sender):
      self.selected_entries = [self.flat_entries[i[1]] for i in self.table_view.selected_rows if self.flat_entries[i[1]].enabled]
      self.view.close()

    def root_btn_action(self, sender):
      root_node = FileTreeNode('/', True, True, r'^.+$')
      self.root_node = root_node
      self.expand_root()

    def mobile_btn_action(self, sender):
      root_node = FileTreeNode('/var/mobile', True, True, r'^.+$')
      self.root_node = root_node
      self.expand_root()

  if root_dir is None:
    root_dir = os.path.expanduser('~/Documents')
  if title is None:
    title = os.path.split(root_dir)[1]
  root_node = FileTreeNode(root_dir, show_size, select_dirs, file_pattern)
  root_node.title = title or ''
  picker = TreeDialogController(root_node, allow_multi=multiple)

  picker.view.present('sheet')
  picker.view.wait_modal()
  if picker.selected_entries is None:
    return None
  paths = [e.path for e in picker.selected_entries]
  if multiple:
    return paths
  else:
    return paths[0]

def human_size(size_bytes, no_suffixs=False):
  '''Helper function for formatting human-readable file sizes'''
  if size_bytes == 1:
    return "1 byte"
  suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]
  num = float(size_bytes)
  for suffix, precision in suffixes_table:
    if num < 1024.0:
      break
    num /= 1024.0
  if precision == 0:
    formatted_size = "%d" % num
  else:
    formatted_size = str(round(num, ndigits=precision))
  if not no_suffixs:
    return "%s %s" % (formatted_size, suffix)
  else:
    return formatted_size

def to_abs_path(*value):
  #import os
  
  abs_path = os.path.join(os.path.expanduser('~'),'Documents')
  for _value in value:
    abs_path = os.path.join(abs_path,_value)
  return abs_path

def add_custom_class(pyui_path, class_name):
  with open(pyui_path, 'r') as f:
    root_list = json.loads(f.read())
    root_view_dict = root_list[0]
    #print root_view_dict
    root_view_dict['attributes']['custom_class'] = class_name
    root_view_str = '[' + json.dumps(root_view_dict) + ']'

  with open(pyui_path, 'w') as f:
    f.write(root_view_str)
# End of file_picker code

def get_attribs(pyui_file):
  attribs = []

  with open(pyui_file) as in_file:
    r = json.load(in_file)
  
  # Debug
  #pprint.pprint(r)
  #print len(r[0])
  #print r[0]['class']
  #print r[0]['frame']
  #print r[0]['attributes']
  #print len(r[0]['nodes'])
  #print len(r[0]['nodes'][1])
  #print len(r[0]['nodes'][0]['attributes'])

  # Get class & frame attributes for the top level view
  attrib = r[0]['class']
  attrib = 'ui.{}()'.format(attrib)
  #print '{} = {}'.format('class', attrib)
  attribs.append('{} = {}'.format('class', attrib))
    
  attrib = r[0]['frame']
  attrib = attrib.replace('{', '').replace('}', '')
  attrib = '({})'.format(attrib)
  #print '{} = {}'.format('frame', attrib)
  attribs.append('{} = {}'.format('frame', attrib))
    
  # Get balance of top level view attributes & convert them to a format suited to code in a py file when necessary
  for s in r[0]['attributes']:
    attrib =  r[0]['attributes'][s]
    # Add parenthesis for some text based attributes
    if s in ('flex', 'title', 'name', 'text', 'font_name'):
      attrib = "'{}'".format(attrib)
    # Colors
    if 'color' in s:
      attrib = attrib.replace('RGBA', '')
    # Images
    if s == 'image_name':
      attrib = "ui.Image.named('{}')".format(attrib)
    #print '{} = {}'.format(s, attrib)
    attribs.append('{} = {}'.format(s, attrib))
  #print '\n'
  attribs.append('\n')
  
  nodes = r[0]['nodes']

  # Loop through all subviews and get their attributes. First the class & frame...
  for i in range(len(nodes)):
    attrib = nodes[i]['class']
    attrib = 'ui.{}()'.format(attrib)
    #print '{} = {}'.format('class', attrib)
    attribs.append('{} = {}'.format('class', attrib))
    
    attrib =  nodes[i]['frame']
    attrib = attrib.replace('{', '').replace('}', '')
    attrib = '({})'.format(attrib)
    #print '{} = {}'.format('frame', attrib)
    attribs.append('{} = {}'.format('frame', attrib))
    
    # Now get the balance of subview attributes & convert to a format suited to code in a py file when necessary
    for s in nodes[i]['attributes']:
      # Filter out the redundant & unwanted attributes
      if not s in ('frame', 'class', 'uuid'):
        attrib = nodes[i]['attributes'][s]
        # Add parenthesis for some text based attributes
        if s in ('flex', 'title', 'name', 'text', 'font_name'):
          attrib = "'{}'".format(attrib)
        # Segmented controls
        if s == 'segments':
          attrib = attrib.replace('|', ', ')
          attrib = "'{}'".format(attrib)
        # Text alignment
        if s == 'alignment':
          attrib = 'ui.ALIGN_{}'.format(attrib.upper())
        # Images
        if s == 'image_name':
          attrib = "ui.Image.named('{}')".format(attrib)
        # Colors
        if 'color' in s:
          attrib = attrib.replace('RGBA', '')
        # Datasource in TableViews class
        if s == 'data_source_items':
          the_items = []
          attrib = attrib.replace('\n', ',')
          items = attrib.split(',')
          for w in range(len(items)):
             the_items.append('{}'.format(items[w].strip()))  
          attrib = '{}'.format(the_items)
        #print '{} = {}'.format(s, attrib)
        attribs.append('{} = {}'.format(s, attrib))
    #print '\n'
    attribs.append('\n')
  
  # Convert list to text
  attribs = '\n'.join(attribs)
  return attribs

def main():
  pyui_path = file_picker('Select pyui file', multiple = False, select_dirs = False, file_pattern = r'^.+.pyui$')

  if not pyui_path:
    console.hud_alert('No Pyui File Selected', 'error')
    exit()
  
  # Get attributes of selected pyui file
  attribs = get_attribs(pyui_path)
  
  # Clear clipboard, then copy attributes to it
  clipboard.set('')
  clipboard.set(attribs)
  
  print(attribs)
  console.hud_alert('Attributes Successfully Copied to Clipboard', 'success', 2)
if __name__ == '__main__':
  main()

