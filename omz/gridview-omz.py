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
