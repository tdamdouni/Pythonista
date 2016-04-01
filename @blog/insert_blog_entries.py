# [blog-entries-to-markdown](http://omz-forums.appspot.com/editorial/post/5307688003043328)
# Gather up an OrderedDict of blog entries, present as list, generate markdown from selected items

import editor, json, ui
filename = 'Martin_Packer_blog.json'

with open(filename) as in_file:
    entries_dict = json.load(in_file)
#print('=' * 24)
#print('{} blog entries loaded.'.format(len(entries_dict)))

class BlogEntryView(ui.View):
    def __init__(self, entries_dict):
        self.entries_dict = entries_dict
        self.name = (__file__.rpartition('/')[2] or __file__)[:-3].replace('_', ' ').title()
        self.width = self.height = 632
        self.add_subview(self.make_table_view())
        self.present('sheet')

    def make_table_view(self):
        table_view = ui.TableView()
        table_view.data_source = ui.ListDataSource(sorted(entries_dict.keys()))
        table_view.data_source.font = ('Courier-Bold', 10)
        table_view.row_height = 16
        table_view.delegate = self
        table_view.frame = self.bounds
        return table_view

    def tableview_did_select(self, tableview, section, row):
        selected_text = tableview.data_source.items[row]
        markdown_text = '[{}]({})'.format(selected_text, self.entries_dict[selected_text])
        print(markdown_text)  # this line is just for debugging

        # to push markdown_text into the Editor, uncomment the next three lines
        #if markdown_text:
        #    selection = editor.get_selection()
        #    editor.replace_text(selection[0], selection[1], markdown_text + '\n')

        # to insert one link only, uncomment the next line
        #self.close()

BlogEntryView(entries_dict)