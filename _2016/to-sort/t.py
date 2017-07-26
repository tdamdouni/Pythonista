# https://forum.omz-software.com/topic/3400/share-a-unique-set-of-attrs-from-the-combination-of-all-ui-elements/2

import ui, pprint

items = [
    ui.View, ui.Button, ui.ButtonItem, ui.ImageView, ui.Label, ui.NavigationView, ui.ScrollView, ui.SegmentedControl, ui.Slider, ui.Switch, ui.TableView, ui.TextField, ui.TextView,
    ui.WebView, ui.DatePicker, ui.ActivityIndicator, ui.TableViewCell
    ]

def show():
    iitems = enumerate(items)
    for x in iitems:
        print(x)

def all():
    for a in items:
        pp.pprint((a,dir(a)))
        
def one(i):
    a = items[i]
    pp.pprint((a,dir(a)))
    
pp = pprint.PrettyPrinter(indent=3, width=46)


ins='show() displays the ui elements,\nall() prints all attrs of all ui elements,\none(i) prints attrs of element i where i is the elem number (as shown by show())'
print()
show()
print()
print(ins)
