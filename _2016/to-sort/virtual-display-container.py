from __future__ import print_function
# https://forum.omz-software.com/topic/1934/virtual-display-container/9

import ui
import math

class GridView (ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.visible_range = []
        self.visible_views = {}
        self.items = []
        self.reusable_cells = []
        self.item_size = (120, 120)
        self.scrollview = ui.ScrollView(frame=self.bounds, flex='WH')
        self.scrollview.content_size = (0, 2000)
        self.scrollview.delegate = self
        self.data_source = None
        self.add_subview(self.scrollview)
    
    def reload(self):
        self.visible_range = []
        for v in self.visible_views.values():
            self.scrollview.remove_subview(v)
        self.visible_views = {}
        w, h = self.bounds[2:]
        items_per_row = int(w / self.item_size[0])
        num_rows = math.ceil(len(self.items) / float(items_per_row))
        self.scrollview.content_size = (0, num_rows * self.item_size[1])
        self.scrollview_did_scroll(self.scrollview)
        
    def layout(self):
        self.reload()
    
    def frame_for_item(self, item_index):
        w, h = self.bounds[2:]
        items_per_row = int(w / self.item_size[0])
        row = item_index / items_per_row
        col = item_index % items_per_row
        x_spacing = (w - (items_per_row * self.item_size[0])) / (items_per_row-1)
        return (col*(self.item_size[0] + x_spacing), row*self.item_size[1], self.item_size[0], self.item_size[1])
    
    def create_or_reuse_cell(self):
        if self.reusable_cells:
            cell = self.reusable_cells[0]
            del self.reusable_cells[0]
            return cell
        if self.data_source:
            return self.data_source.gridview_create_cell(self)
        else:
            return ui.View(bg_color='gray')
        
    def configure_cell(self, cell_view, item):
        if self.data_source:
            self.data_source.gridview_configure_cell(self, cell_view, item)
        
    def scrollview_did_scroll(self, scrollview):
        y = scrollview.content_offset[1]
        w, h = self.bounds[2:]
        items_per_row = int(w / self.item_size[0])
        first_visible_row = max(0, int(y / self.item_size[1]))
        num_visible_rows = int(h / self.item_size[1]) + 2
        range_start = first_visible_row * items_per_row
        range_end = min(len(self.items), range_start + num_visible_rows * items_per_row)
        visible_range = range(range_start, range_end)
        if visible_range != self.visible_range:
            self.visible_range = visible_range
            # Remove views that are no longer visible:
            for i in self.visible_views.keys():
                if i not in visible_range:
                    cell = self.visible_views[i]
                    self.reusable_cells.append(cell)
                    self.scrollview.remove_subview(cell)
                    del self.visible_views[i]
            # Add views that are not visible yet:
            for i in visible_range:
                if i not in self.visible_views:
                    cell_frame = self.frame_for_item(i)
                    view = self.create_or_reuse_cell()
                    view.frame = cell_frame
                    self.configure_cell(view, self.items[i])
                    self.scrollview.add_subview(view)
                    self.visible_views[i] = view


class GridViewDemoController (object):
    def __init__(self):
        from random import randint
        # Generate a large number of random colors:
        colors = ['#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255)) for i in xrange(9999)]
        self.gridview = GridView(frame=(0, 0, 500, 500), background_color='white', name='GridView Demo')
        self.gridview.item_size = (100, 120)
        self.gridview.data_source = self
        self.gridview.items = colors
    
    # Data source methods:
    def gridview_create_cell(self, gridview):
        # This is called when a new cell is needed.
        # When the grid view is scrolled, cells that become invisible are reused,
        # so this doesn't get called too often.
        cell = ui.View(frame=(0, 0, 100, 100))
        swatch = ui.View(frame=(10, 10, 80, 60), name='swatch', flex='wh')
        swatch.corner_radius = 4
        cell.add_subview(swatch)
        label = ui.Label(frame=(10, 80, 80, 15), name='label', flex='wt')
        label.font = ('<System>', 13)
        label.alignment = ui.ALIGN_CENTER
        label.text_color = '#333333'
        cell.add_subview(label)
        return cell
    
    def gridview_configure_cell(self, gridview, cell, item):
        # Note: The cell may be a new one (created by gridview_create_cell),
        # or an existing cell that is reused after it was scrolled out of the visible area.
        # This method should configure the cell to display the given item (which can be
        # any kind of object; in this demo, all items are strings).
        cell['label'].text = item
        cell['swatch'].background_color = item

demo = GridViewDemoController()
demo.gridview.present('sheet')
# --------------------

import ui


class VirtualScroll(ui.View):
    def __init__(self,frame, width , height, items_per_line , num_items):
        self.frame = frame
        
        # make the scroll view
        scroll = ui.ScrollView()
        scroll.frame = frame
        scroll.content_size = (self.width, height * num_items)
        print(scroll.content_size)
        
        self.add_subview(scroll)
        

if __name__ == '__main__':
    frame = (0,0,540,576)
    v = ui.View()
    # 1000000 items
    vs = VirtualScroll(frame , 270, 675, 2, 1000000)
    v.add_subview(vs)
    v.present('sheet')
# --------------------
class GridView (ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
# --------------------
# code from @omz
import ui

class test(ui.View):
    def __init__(self, frame, item_size):
        self.frame = frame
        self.item_size = item_size
        
    def frame_for_item(self, item_index):
        w, h = self.bounds[2:]
        items_per_row = int(w / self.item_size[0])
        row = item_index / items_per_row
        col = item_index % items_per_row
        x_spacing = (w - (items_per_row * self.item_size[0])) / (items_per_row-1)
        return (col*(self.item_size[0] + x_spacing), row*self.item_size[1], self.item_size[0], self.item_size[1])
    
    
if __name__ == '__main__':
    frame = (0,0,540,576)
    item_size = (120,120)
    x = test(frame, item_size)
    for i in range(0,101):
        print(x.frame_for_item(i))
# --------------------
# code from @omz
import ui

        
def frame_for_item(frame, item_size, item_index):
    w, h = frame[2:]
    items_per_row = int(w / item_size[0])
    row = item_index / items_per_row
    col = item_index % items_per_row 
    x_spacing = (w - (items_per_row * item_size[0])) / (items_per_row-1)
    return (col*(item_size[0] + x_spacing), row*item_size[1], item_size[0], item_size[1])
    
    
if __name__ == '__main__':
    frame = (0,0,540,576 - 44)
    item_size = (120,120)
    for i in range(0,101):
        print(frame_for_item(frame, item_size , i ))
# --------------------
#@omz code
import ui
import console
import math
import Image
_cells_created =[]
_cells_deleted = []

# do color example if true, otherwise use
# PosterCell as the cell. 
_DO_COLOR = True

# the cell size used for both examples 
_cell_size = (64 * 2, 64 * .8)

# if 0, is calculated, > 0 overrides the calc
# a bug i need to fix in func frame_for_item, divide by zero error if _cells_per_row == 1. 
# i probably introduced the bug :(
_cells_per_row = 3

# the number of cells to create for the poster demo
# can be a big number, just dont want to crash 
# anyones device. 
_num_data_items_postercell_demo = 2000

class PosterCell(ui.View):
    def __init__(self, item_size , item_index = -1):
        self.frame = (0,0,item_size[0], item_size[1])
        
        self.iv = ui.ImageView()
        self.iv.frame = self.frame
        self.add_subview(self.iv)
        self.item_index = item_index
    
        self.index_label = ui.Label(frame = (0,0, self.width, 14))
        self.index_label.text_color = 'orchid'
        self.index_label.font = ('<system-bold>',18)
        self.add_subview(self.index_label)
        
        self.btn = ui.Button(frame = self.frame)
        self.add_subview(self.btn)
        
        
        
        #for debugging
        _cells_created.append(item_index)
        
    # i assume its smarter to wait for the call 
    # to configure cell before loading an image
    def load_data(self, gridview, cell, item):
        if not self.iv.image:
            self.iv.image = ui.Image.named('ionicons-checkmark-circled-32')
        self.index_label.text = str(self.item_index)
        
    def cell_action_callback(self, func):
        self.btn.action = func
        
    def __del__(self):
        #for debugging
        _cells_deleted.append(self.item_index)
        
        
class GridView (ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.visible_range = []
        self.visible_views = {}
        self.items = []
        self.reusable_cells = []
        self.item_size = 0 # (120, 120)
        self.scrollview = ui.ScrollView(frame=self.bounds, flex='WH')
        self.scrollview.content_size = (0, 2000)
        self.scrollview.delegate = self
        self.data_source = None
        self.add_subview(self.scrollview)
        self.cells_per_row = 0

    def reload(self):
        self.visible_range = []
        for v in self.visible_views.values():
            self.scrollview.remove_subview(v)
            self.visible_views = {}
        w, h = self.bounds[2:]
        #items_per_row = int(w / self.item_size[0])
        items_per_row = self.xcells_per_row()
        num_rows = math.ceil(len(self.items) / float(items_per_row))
        self.scrollview.content_size = (0, num_rows *self.item_size[1])
        self.scrollview_did_scroll(self.scrollview)
        print('reload')
        
    def xcells_per_row(self):
        if self.cells_per_row:
            return self.cells_per_row
            
        w, h = self.bounds[2:]
        return int(w / self.item_size[0])
        
    def layout(self):
        self.reload()

    def frame_for_item(self, item_index):
        w, h = self.bounds[2:]
        #items_per_row = int(w / self.item_size[0])
        items_per_row = self.xcells_per_row()
        row = item_index / items_per_row
        col = item_index % items_per_row
        x_spacing = (w - (items_per_row * self.item_size[0])) / (items_per_row-1)
        return (col*(self.item_size[0] + x_spacing), row*self.item_size[1], self.item_size[0], self.item_size[1])

    def create_or_reuse_cell(self, item_index):
        if self.reusable_cells:
            cell = self.reusable_cells[0]
            del self.reusable_cells[0]
            return cell
            
        if self.data_source:
            return self.data_source.gridview_create_cell(self, item_index)
        else:
            return ui.View(bg_color='gray')

    def configure_cell(self, cell_view, item):
        if self.data_source:
            self.data_source.gridview_configure_cell(self, cell_view, item)

    def scrollview_did_scroll(self, scrollview):
        y = scrollview.content_offset[1]
        w, h = self.bounds[2:]
        items_per_row = self.xcells_per_row()
        #items_per_row = int(w / self.item_size[0])
        first_visible_row = max(0, int(y / self.item_size[1]))
        num_visible_rows = int(h / self.item_size[1]) + 2
        range_start = first_visible_row * items_per_row
        range_end = min(len(self.items), range_start + num_visible_rows * items_per_row)
        visible_range = range(range_start, range_end)
        if visible_range != self.visible_range:
            self.visible_range = visible_range
            # Remove views that are no longer visible:
            for i in self.visible_views.keys():
                if i not in visible_range:
                    cell = self.visible_views[i]
                    self.reusable_cells.append(cell)
                    self.scrollview.remove_subview(cell)
                    # added this call and check. i think
                    # its correct. if i didnt do it, the
                    # __del__ method in PosterCell class
                    # not being called
                    if hasattr(self.visible_views[i], '__del__'):
                        self.visible_views[i].__del__()
                    del self.visible_views[i]
                    
            # Add views that are not visible yet:
            for i in visible_range:
                if i not in self.visible_views:
                    cell_frame = self.frame_for_item(i)
                    # i am doing this wrong. i is not the
                    # index item being created. need to 
                    # fugure out the real index number
                    view = self.create_or_reuse_cell(i)
                    view.frame = cell_frame
                    self.configure_cell(view, self.items[i])
                    self.scrollview.add_subview(view)
                    self.visible_views[i] = view
    
    def cell_callback(self, sender):
        #sure, my thought needed here
        print('cell called us back')
        
    # not working ??
    def __del__(self):
        print('exiting')
        


class GridViewDemoController (object):
    def __init__(self):
        if _DO_COLOR:
            from random import randint
            # Generate a large number of random colors:
            colors = ['#%02x%02x%02x' % (randint(0, 255), randint(0, 255), randint(0, 255)) for i in xrange(2000)]
        
            self.gridview = GridView( frame=(0, 0, 500, 500), background_color='white', name='GridView Demo Color')
        
        #self.gridview.item_size = (100, 120)
        
            self.gridview.item_size = _cell_size
            self.gridview.data_source = self
            self.gridview.items = colors
            
            self.gridview.cells_per_row = _cells_per_row
        else:
            self.gridview = GridView( frame=(0, 0, 500, 500), background_color='white', name='GridView Demo Poster')
            self.gridview.cells_per_row = _cells_per_row
            self.gridview.item_size = _cell_size
            self.gridview.data_source = self
            self.gridview.items = range(_num_data_items_postercell_demo)
            

    # Data source methods:
    def gridview_create_cell(self, gridview, item_index):
        
        # This is called when a new cell is needed.
        # When the grid view is scrolled, cells that become invisible are reused,
        # so this doesn't get called too often.
         
        if _DO_COLOR:
            cell = ui.View(frame=(0, 0, 100, 100))
            swatch = ui.View(frame=(10, 10, 80, 60), name='swatch', flex='wh')
            swatch.corner_radius = 4
            cell.add_subview(swatch)
            label = ui.Label(frame=(10, 80, 80, 15), name='label', flex='wt')
            label.font = ('<System>', 13)
            label.alignment = ui.ALIGN_CENTER
            label.text_color = '#333333'
            cell.add_subview(label)
            #added a btn
            btn = ui.Button(frame = cell.frame, name = 'btn')
            cell.add_subview(btn)
            return cell
        else:
            return PosterCell(_cell_size, item_index)

    def gridview_configure_cell(self, gridview, cell, item):
        # Note: The cell may be a new one (created by gridview_create_cell),
        # or an existing cell that is reused after it was scrolled out of the visible area.
        # This method should configure the cell to display the given item (which can be any kind of object; in this demo, all items are strings).
        
        if _DO_COLOR:
            cell['label'].text = item
            cell['swatch'].background_color = item
            cell['btn'].action = gridview.cell_callback
        else:
            # load a picture or whatever needs to happen
            cell.load_data(gridview, cell, item)
            # set a callback function in the cell to callback the gridview
            cell.cell_action_callback(gridview.cell_callback)

demo = GridViewDemoController()
demo.gridview.present('sheet')
# --------------------
#@omz code, and mangled by @Phuket2, sorry!
import ui
import math

_num_infocells = 2000

# cap the number of items that _reusable_cells list holds
_reusable_cells_cap = 30

# the cell size
_cell_size = (135, 96)

# if 0, is calculated, > 0 overrides the calc
# a bug i need to fix in func frame_for_item, divide by zero error if _cells_per_row == 1. 
# i probably introduced the bug :(
_cells_per_row = 0

    
class InfoCell(ui.View):
    def __init__(self, item_size , item_index):
        
        self.frame = (0,0,item_size[0], item_size[1])
        self.index = item_index

        index_lb = ui.Label(name = 'index_lb', frame = (0,0,self.width, self.height *.75))
        index_lb.font = ('<system-bold>', 36)
        index_lb.alignment = ui.ALIGN_CENTER
        index_lb.border_width = .5
        self.add_subview(index_lb)
        
        info_lb = ui.Label(name = 'info_lb', frame = (0,index_lb.height, self.width, self.height - index_lb.height ))
        
        index_lb.font = ('<system-bold>', 22)
        info_lb.alignment = ui.ALIGN_CENTER
        info_lb.background_color = 'orchid'
        self.add_subview(info_lb)
        
        btn = ui.Button(name = 'btn', frame = self.frame)
        btn.action = self.cell_action_callback
        self.add_subview(btn)
        
        
    def load_data(self, gridview, cell, item):
        self['index_lb'].text = str(item)
    
    def set_info_label(self, text):
        self['info_lb'].text = text
        if text == 'Created':
            self['info_lb'].background_color = 'red'
        else:
            self['info_lb'].background_color = 'orange'
        
            
        
    def cell_action_callback(self, func):
        self['btn'].action = func
        
    def __del__(self):
        pass
        
class GridView (ui.View):
    def __init__(self, item_size, cells_per_row = None ,  *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.visible_range = []
        self.visible_views = {}
        self.items = []
        self.reusable_cells = []
        self.item_size = item_size
        self.item_h , self.item_w = item_size
        self.scrollview = ui.ScrollView(frame=self.bounds, flex='WH')
        self.scrollview.content_size = (0, 2000)
        self.scrollview.delegate = self
        self.data_source = None
        self.add_subview(self.scrollview)
        
        #used to aviod redundant calls from reload function.
        self.screen_size = (0,0)
    
        
    
    def reload(self):
        
        # aviod double call at launch. overhead
        # can be small, but if loading pics etc.
        # better to aviod it. 
        if self.screen_size == ui.get_screen_size() :
            return
            
        self.visible_range = []
        for v in self.visible_views.values():
            self.scrollview.remove_subview(v)
            self.visible_views = {}
        w, h = self.bounds[2:]
        #items_per_row = int(w / self.item_size[0])
        items_per_row = self.xcells_per_row()
        num_rows = math.ceil(len(self.items) / float(items_per_row))
        self.scrollview.content_size = (0, num_rows *self.item_size[1])
        self.scrollview_did_scroll(self.scrollview)
        self.screen_size = ui.get_screen_size()
        
        #self.cell_buffer[0] 
        self.num_rows = num_rows
        print('reload')
    
        
    def xcells_per_row(self):
        if self.cells_per_row:
            return self.cells_per_row
            
        w, h = self.bounds[2:]
        return int(w / self.item_size[0])
        
    def layout(self):
        self.reload()

    def frame_for_item(self, item_index):
        w, h = self.bounds[2:]
        #items_per_row = int(w / self.item_size[0])
        items_per_row = self.xcells_per_row()
        row = item_index / items_per_row
        col = item_index % items_per_row
        x_spacing = (w - (items_per_row * self.item_size[0])) / (items_per_row-1)
        return (col*(self.item_size[0] + x_spacing), row*self.item_size[1], self.item_size[0], self.item_size[1])
        
    
    def create_or_reuse_cell(self, item_index):
        
        # @Phuket2
        # trying to change the buffering system
        # assuming that resuable_cells is 
        # calculated well
        
        # using a sledge hammer here! i can see when 
        # scrolling around fast some intresting results. not sure its good ir right through
        
        # maybe rather than deleting the first entries in the list, 
        # i could iterate over the list
        # and delete elements that are furthest away
        # from the currently visible row, fwd and backwards. just a thought.
        # its very difficult for me to predict the correct approach.
        # size of buffer, speed of alogorithm to
        # etc... 
        
        # cap the buffered items  
        buf_size = _reusable_cells_cap
        
        # hmmm, i am not really sure all the clean 
        # up of objects are being handled correctly 
        # here
        num_buf_items = len(self.reusable_cells)
        if num_buf_items > buf_size:
            del self.reusable_cells[:num_buf_items -buf_size]
        
        
        self.name = str (len(self.reusable_cells))
        for cell in self.reusable_cells:
            if cell.index == item_index:
                cell.set_info_label('reused')
                return cell
        
        # @Phuket2
        # i commented out the below code    
        '''
        if self.reusable_cells:
            cell = self.reusable_cells[0]
            del self.reusable_cells[0]
            return cell
        '''
            
        if self.data_source:
            return self.data_source.gridview_create_cell(self, item_index)
            
        else:
            return ui.View(bg_color='gray')

    def configure_cell(self, cell_view, item):
        if self.data_source:
            self.data_source.gridview_configure_cell(self, cell_view, item)

    def scrollview_did_scroll(self, scrollview):
        y = scrollview.content_offset[1]
        w, h = self.bounds[2:]
        items_per_row = self.xcells_per_row()
        #items_per_row = int(w / self.item_size[0])
        first_visible_row = max(0, int(y / self.item_size[1]))
        # @Phuket2
        # pretty sure the + 2 below is the 'read ahead' buffer of rows. 
        # will play with this value later
        num_visible_rows = int(h / self.item_size[1]) + 2
        range_start = first_visible_row * items_per_row
        range_end = min(len(self.items), range_start + num_visible_rows * items_per_row)
        visible_range = range(range_start, range_end)
        if visible_range != self.visible_range:
            self.visible_range = visible_range
            # Remove views that are no longer visible:
            for i in self.visible_views.keys():
                if i not in visible_range:
                    cell = self.visible_views[i]
                    self.reusable_cells.append(cell)
                    self.scrollview.remove_subview(cell)
                    # @Phuket2
                    # added this call and check. i think
                    # its correct. if i didnt do it, the
                    # __del__ method in PosterCell class
                    # not being called
                    if hasattr(self.visible_views[i], '__del__'):
                        self.visible_views[i].__del__()
                        
                    del self.visible_views[i]
                    
            # Add views that are not visible yet:
            for i in visible_range:
                if i not in self.visible_views:
                    cell_frame = self.frame_for_item(i)
                    view = self.create_or_reuse_cell(i)
                    view.frame = cell_frame
                    self.configure_cell(view, self.items[i])
                    self.scrollview.add_subview(view)
                    self.visible_views[i] = view
                
    def cell_callback(self, sender):
        # @Phuket2
        #sure, more thought needed here
        print('cell called us back')
        
    # @Phuket2  
    # not sure why its not working ??
    # seems to never be called
    def __del__(self):
        print('exiting')
        


class GridViewDemoController (object):
    def __init__(self):
        
        self.gridview = GridView( _cell_size,_cells_per_row,  frame=(0, 0, 500, 500), background_color='white', name='GridView Demo Poster')
        
        
        
        self.gridview.cells_per_row = _cells_per_row
        self.gridview.item_size = _cell_size
        self.gridview.data_source = self
        self.gridview.items =range( _num_infocells)
        
        
    # Data source methods:
    def gridview_create_cell(self, gridview, item_index):
        
        # This is called when a new cell is needed.
        # When the grid view is scrolled, cells that become invisible are reused,
        # so this doesn't get called too often.
        
        cell =  InfoCell(_cell_size, item_index )
        cell.set_info_label('Created')
        return cell
        
    def gridview_configure_cell(self, gridview, cell, item):
        # Note: The cell may be a new one (created by gridview_create_cell),
        # or an existing cell that is reused after it was scrolled out of the visible area.
        # This method should configure the cell to display the given item (which can be any kind of object; in this demo, all items are strings).
        
        cell.load_data(gridview, cell, item)
        cell.cell_action_callback(gridview.cell_callback)
        
_hide_tb = False  
demo = GridViewDemoController()
demo.gridview.present('sheet', hide_title_bar = _hide_tb )
# --------------------
