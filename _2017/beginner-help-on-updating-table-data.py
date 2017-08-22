# https://forum.omz-software.com/topic/4249/beginner-help-on-updating-table-data/4

# 3 col list sorting

import ui
from operator import itemgetter

sdata = [('Bob','Dylan',58),('Eric','Clapton', 56),('Elvis','Presley',48),('Michael', 'Jackson', 60),('Al', 'Stewart',54),('Boz', 'Scaggs',64)]

ditemsa = []
ditemsb = []
ditemsc = []

for x in range(len(sdata)):
    ditemsa.append(sdata[x][0])
    ditemsb.append(sdata[x][1])
    ditemsc.append(sdata[x][2])

def sortaction(self, opt=0):
    global sdata
    sdata = sorted(sdata,key=itemgetter(opt))
    ditemsa = []
    ditemsb = []
    ditemsc = []
    for x in range(len(sdata)):
        ditemsa.append(sdata[x][0])
        ditemsb.append(sdata[x][1])
        ditemsc.append(sdata[x][2])
    print(sdata)

    ####
    # how toupdate data_source display
    # after pressing sort
    ####
    
    tbv1.data_source.items=ditemsa
    tbv2.data_source.items=ditemsb
    tbv3.data_source.items=ditemsc

def bt1_action(self):
    sortaction(self, 0)

def bt2_action(self):
    sortaction(self,1)

def bt3_action(self):
    sortaction(self,2)

class MyView(ui.View):

    def __init__(self, name='MyView', bg_color='lightyellow', frame=(0,0,360,660)):
        self.name = name
        self.bg_color = bg_color
        self.add_subview(self.make_table_view('tbv1', (0, 50, 100,600), 'green',ditemsa))
        self.add_subview(self.make_table_view('tbv2', (105, 50, 100,600), 'blue', ditemsb))
        self.add_subview(self.make_table_view('tbv3', (210, 50, 100,600), 'red',ditemsc))
        self.add_subview(self.make_btn_view('bt1','FName', (0,0, 100,40),'palegreen', action=bt1_action))
        self.add_subview(self.make_btn_view('bt2','LName', (105,0, 100,40),'skyblue', action=bt2_action))
        self.add_subview(self.make_btn_view('bt3','Age', (210,0, 100,40),'pink', action=bt3_action))
        self.present()


    def make_table_view(self, name, frame, col, dsrc):
        table_view = ui.TableView(name=name, frame=frame)
        table_view.row_height = 25
        data_source = ui.ListDataSource(dsrc)
        data_source.name = dsrc
        data_source.text_color=col
        data_source.font=('Avenir Next Condensed',14)
        table_view.data_source = data_source
        return table_view
        
    def make_btn_view(self, name, title, frame, col, action):
        btn_view = ui.Button(name=name, frame=frame, bg_color=col)
        btn_view.title=title
        btn_view.tint_color=0
        btn_view.action = action
        return btn_view

MyView()
# --------------------
def sortaction(self, opt=0):
    global sdata
    print(self)
    sdata = sorted(sdata,key=itemgetter(opt))
    ditemsa = []
    ditemsb = []
    ditemsc = []
    for x in range(len(sdata)):
        ditemsa.append(sdata[x][0])
        ditemsb.append(sdata[x][1])
        ditemsc.append(sdata[x][2])
    print(sdata)
    
    ####
    # how toupdate data_source display
    # after pressing sort
    ####
    
    sv=self.superview
    sv['tbv1'].data_source.items=ditemsa
    sv['tbv2'].data_source.items=ditemsb
    sv['tbv3'].data_source.items=ditemsc
```python# --------------------
birth_years# --------------------
ditemc# --------------------
from operator import itemgetter
import ui

musicians = [('Bob', 'Dylan', 58), ('Eric', 'Clapton', 56),
             ('Elvis', 'Presley', 48), ('Michael', 'Jackson', 60),
             ('Al', 'Stewart', 54), ('Boz', 'Scaggs', 64)]

first_names = [musician[0] for musician in musicians]
last_names = [musician[1] for musician in musicians]
birth_years = [musician[2] for musician in musicians]


def button_action(sender):
    opt = int(sender.name.split('_')[-1])
    global musicians
    musicians = sorted(musicians, key=itemgetter(opt))
    first_names = [musician[0] for musician in musicians]
    last_names = [musician[1] for musician in musicians]
    birth_years = [musician[2] for musician in musicians]
    print(musicians)

    ####
    # how toupdate data_source display
    # after pressing sort
    ####

    sender.superview['first_names'].data_source.items = first_names
    sender.superview['last_names'].data_source.items = last_names
    sender.superview['birth_years'].data_source.items = birth_years


class MyView(ui.View):

    def __init__(self, name='MyView', bg_color='lightyellow',
                 frame=(0, 0, 360, 660)):
        self.name = name
        self.bg_color = bg_color
        self.add_subview(self.make_table_view('first_names', (0, 50, 100, 600),
                                              'green', first_names))
        self.add_subview(self.make_table_view('last_names', (105, 50, 100, 600),
                                              'blue', last_names))
        self.add_subview(self.make_table_view('birth_years', (210, 50, 100, 600),
                                              'red', birth_years))
        self.add_subview(ui.Button(name='button_0', frame=(0, 0, 100, 40),
                                   title='FName', bg_color='palegreen',
                                   action=button_action))
        self.add_subview(ui.Button(name='button_1', frame=(105, 0, 100, 40),
                                   title='LName', bg_color='skyblue',
                                   action=button_action))
        self.add_subview(ui.Button(name='button_2', frame=(210, 0, 100, 40),
                                   title='BirthYear', bg_color='pink',
                                   action=button_action))
        self.present()

    def make_table_view(self, name, frame, col, dsrc):
        table_view = ui.TableView(name=name, frame=frame)
        table_view.row_height = 25
        data_source = ui.ListDataSource(dsrc)
        data_source.name = dsrc
        data_source.text_color = col
        data_source.font = ('Avenir Next Condensed', 14)
        table_view.data_source = data_source
        return table_view


MyView()
# --------------------
# 3 col list sorting

import ui
from operator import itemgetter

class MyView(ui.View):
    def bt1_action(self, sender):
        self.sortaction(0)
    
    def bt2_action(self, sender):
        self.sortaction(1)
   
    def bt3_action(self, sender):
        self.sortaction(2)
       
    def sortaction(self, opt=0):
        self.sdata = sorted(self.sdata,key=itemgetter(opt))  
        self.tbv1.data_source.items=[f for f,l,a in self.sdata]
        self.tbv2.data_source.items=[l for f,l,a in self.sdata]
        self.tbv3.data_source.items=[a for f,l,a in self.sdata]     

    def __init__(self, name='MyView', bg_color='lightyellow', frame=(0,0,360,660)):
        self.name = name
        self.bg_color = bg_color        
        self.sdata = [('Bob','Dylan',58),('Eric','Clapton', 56),
                    ('Elvis','Presley',48),('Michael', 'Jackson', 60),
                    ('Al', 'Stewart',54),('Boz', 'Scaggs',64)]  
        self.sdata = sorted(self.sdata,key=itemgetter(0))       
        self.tbv1 =self.make_table_view('tbv1', (0, 50, 100,600), 'green',
                    [f for f,l,a in self.sdata])
        self.tbv2 =self.make_table_view('tbv2', (105, 50, 100,600), 'blue', 
                [l for f,l,a in self.sdata])
        self.tbv3 = self.make_table_view('tbv3', (210, 50, 100,600), 'red',
                [a for f,l,a in self.sdata])
        
        self.add_subview(self.tbv1)
        self.add_subview(self.tbv2)
        self.add_subview(self.tbv3)
        self.add_subview(self.make_btn_view('bt1','FName', (0,0, 100,40),'palegreen',
            action=self.bt1_action))
        self.add_subview(self.make_btn_view('bt2','LName', (105,0, 100,40),'skyblue', 
            action=self.bt2_action))
        self.add_subview(self.make_btn_view('bt3','Age', (210,0, 100,40),'pink',
            action=self.bt3_action))
        self.present()


    def make_table_view(self, name, frame, col, dsrc):
        table_view = ui.TableView(name=name, frame=frame)
        table_view.row_height = 25
        data_source = ui.ListDataSource(dsrc)
        data_source.name = dsrc
        data_source.text_color=col
        data_source.font=('Avenir Next Condensed',14)
        table_view.data_source = data_source
        return table_view
        
    def make_btn_view(self, name, title, frame, col, action):
        btn_view = ui.Button(name=name, frame=frame, bg_color=col)
        btn_view.title=title
        btn_view.tint_color=0
        btn_view.action = action
        return btn_view

MyView()
# --------------------
