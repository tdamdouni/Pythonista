# https://forum.omz-software.com/topic/3113/share-a-skeleton-for-making-and-testing-variable-height-cells-for-a-scrollview/23

import ui
from objc_util import *


class TableData(object):
    def __init__(self):
        self.data = [{'value': str(i), 'height': i+40} for i in range(10)]
    
    def tableview_number_of_rows(self, tableview, section):
        return len(self.data)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell()
        label = ui.Label()
        label.text = self.data[row]['value']
        label.number_of_lines = 0
        label_objc = ObjCInstance(label)
        UIViewAutoresizingNone = 0
        UIViewAutoresizingFlexibleLeftMargin = 1 << 0
        UIViewAutoresizingFlexibleWidth = 1 << 1
        UIViewAutoresizingFlexibleRightMargin = 1 << 2
        UIViewAutoresizingFlexibleTopMargin = 1 << 3
        UIViewAutoresizingFlexibleHeight = 1 << 4
        UIViewAutoresizingFlexibleBottomMargin = 1 << 5

        label_objc.autoresizeMask = UIViewAutoresizingFlexibleWidth + UIViewAutoresizingFlexibleTopMargin + UIViewAutoresizingFlexibleBottomMargin + UIViewAutoresizingFlexibleHeight
        label.height = self.data[row]['height']
        cell.content_view.add_subview(label)
        return cell


tv = ui.TableView()
tv.data_source = TableData()
tv_objc = ObjCInstance(tv)
tv_objc.rowHeight = -1.0 #UITableViewAutomaticDimension
tv_objc.estimatedRowHeight = 40.0
tv.present()
