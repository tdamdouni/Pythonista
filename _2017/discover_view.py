# https://github.com/cclauss/f1_hack/blob/master/discover_view.py#L24

# https://forum.omz-software.com/topic/4138/getting-notification-on-navigationview-go-back/4

import json
import ui

filename = 'current.json'


def data_path_to_str(data_path):  # ['a', 0, 'b'] --> [a][0][b]
    return f'[{"][".join(str(key) for key in data_path or [])}]'


def str_to_data_path(name=''):    # [a][0][b] --> ['a', 0, 'b']
    name = name.strip('[]').split('][')
    return [] if name == [''] else [int(s) if s.isdigit() else s for s in name]


class DiscoverView(ui.View):
    def __init__(self, data, name=''):
        self.name = name or 'API Discovery'
        self.data = data
        self.views = []
        self.add_subview(self.make_view([]))

    @property
    def curr_data_path(self):
        for i, view in enumerate(self.views):
            if view.on_screen:
                self.views = self.views[:i+1]  # trim the backed off views
                assert view is self.views[-1]
                return str_to_data_path(view.name)
        return []

    def data_at_data_path(self, data_path):
        data = self.data
        for key in data_path:
            data = data[key]
        return data

    def layout(self):
        if self.subviews:
            self.subviews[0].frame = self.bounds

    def make_dict_view(self, data, name):
        items = [f'{k} ({type(v).__name__}): {v}' for k, v in data.items()]
        lds = ui.ListDataSource(items)
        lds.font = ('<system-bold>', 10)
        return ui.TableView(data_source=lds, delegate=self, name=name,
                            row_height=20)

    def make_info_view(self, data, name):
        return ui.TextView(name=name, text=f'{type(data).__name__}: {data}')

    def make_list_view(self, data, name):
        items = [f'{i} {item} ({type(item).__name__})' for i, item
                 in enumerate(data)]
        lds = ui.ListDataSource(items)
        lds.font = ('<system-bold>', 10)
        return ui.TableView(data_source=lds, delegate=self, name=name,
                            row_height=20)

    def make_view(self, data_path):
        data = self.data_at_data_path(data_path)
        name = data_path_to_str(data_path)
        if isinstance(data, dict):
            return self.make_dict_view(data, name)
        elif isinstance(data, list):
            return self.make_list_view(data, name)
        else:
            return self.make_info_view(data, name)

    def tableview_did_select(self, tableview, section, row):
        key = tableview.data_source.items[row].split()[0]
        data_path = self.curr_data_path + [int(key) if key.isdigit() else key]
        view = self.make_view(data_path)
        self.views.append(view)
        tableview.navigation_view.push_view(view)

    def will_close(self):  # never gets called :-(
        print('will_close!!')


if __name__ == '__main__':
    print('=' * 23)
    try:
        with open(filename) as in_file:
            ui.NavigationView(DiscoverView(json.load(in_file))).present()
    except FileNotFoundError:
        exit("Please run 'f1_get.py' before running this script.")
