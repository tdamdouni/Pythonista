# add-arguments-to-method-called-from-ui-scene-buttons

def show_view_A(sender):
    v = ui.View()
    v.background_color = â€˜whiteâ€™
    v.name = â€˜Aâ€™
    global location
    location = 1 # used in another method to grab a url
    sender.navigation_view.push_view(v)
    message = get_html(page_info,location_info)
    scrollview(v,message)

def show_view_B(sender):
    v = ui.View()
    v.background_color = â€˜whiteâ€™
    v.name = â€˜Bâ€™
    global location
    location = 2 # used in another method to grab a url
    sender.navigation_view.push_view(v)
    message = get_html(page_info,location_info)
    scrollview(v,message)
    
root_view = ui.View()
root_view.background_color = 'white'
root_view.name = 'Stuff'

A = ui.Button(title='A')
B = ui.Button(title='B')

A.action = show_view_A
B.action = show_view_B

root_view.add_subview(A)
root_view.add_subview(B)

# --------------------

import ui

page_info = None
location_info = None


def get_html(*args):
    pass


def scrollview(*args):
    pass


def show_view(sender):
    global location
    if sender.title == 'A':
        location = 1  # used in another method to grab a url
    elif sender.title == 'B':
        location = 2
    view = ui.View(name=sender.title, bg_color='white')
    sender.navigation_view.push_view(view)
    scrollview(view, get_html(page_info, location_info))


root_view = ui.View(name='Stuff', bg_color='white')
root_view.add_subview(ui.Button(title='A', action=show_view))
root_view.add_subview(ui.Button(title='B', action=show_view))

# --------------------

import ui

class MyClass(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_view()
        
    def make_view(self):
        A = ui.Button(title='A', action=self.show_view)
        A.AddledBadger = 'This is my A type personality'    # adding a attr to the btn at runtime
    
        B = ui.Button(title='B', action=self.show_view)
        B.x = A.width + 30
        B.AddledBadger = 'This is my B type personality'
        
        self.add_subview(A)
        self.add_subview(B)
        
        # you will notice your attr is print
        print(dir(A))
    
    def show_view(self, sender):
        print(sender.AddledBadger)
        return
        
        # if not all objects passed to this func may not have your new attr
        # you could do something like the below -
        if hasattr(sender, 'AddledBadger'):
            print('it has my custom attr')
        else:
            print('sender does not have my custom attr, i better do something else')
            
if __name__ == '__main__':
    f = (0, 0, 300, 400)
    v = MyClass(frame = f)
    v.present(style='sheet', animated=False)
# --------------------
