# @ui
# https://gist.github.com/jsbain/fcadaffff4be09c4ec78
import ui
class TabbedView(ui.View):
    def __init__(self,tablist=[], frame=(0,0)+ui.get_screen_size()):
        '''takes an iterable of Views, using the view name as the tab selector.  
        empty views sre just given generic names'''
        self.tabcounter=0    #unique counter, for name disambiguation
        self.buttonheight=30 #height of buttonbar
        #setup button bar
        self.tabbuttons=ui.SegmentedControl(frame=(0,0,self.width, self.buttonheight))
        self.tabbuttons.action=self.tab_action
        self.tabbuttons.flex='W'
        self.tabbuttons.segments=[]
        self.add_subview(self.tabbuttons)

        for tab in tablist:
            self.addtab(tab)
    def tab_action(self,sender):
        if sender.selected_index >= 0:
            tabname=sender.segments[sender.selected_index]
            self[tabname].bring_to_front()
    def focus_tab_by_index(self,index):
        self.tabbuttons.selected_index=index
        self.tab_action(self.tabbuttons)
    
    def focus_tab_by_name(self,tabname):
        self.tabbuttons.selected_index=self.tabbuttons.segments.index(tabname)
        self.tab_action(self.tabbuttons)

    def addtab(self,tab):
            if not tab.name:
                tab.name='tab{}'.format(self.tabcounter)
            if tab.name in self.tabbuttons.segments:
                #append unique counter to name
                tab.name+=str(self.tabcounter)
            self.tabcounter+=1
            self.tabbuttons.segments+=(tab.name,) 
            tab.frame=(0,self.buttonheight,self.width,self.height-self.buttonheight)
            tab.flex='WH'
            self.add_subview(tab)
            self.focus_tab_by_name(tab.name)

    def removetab(self,tabname):
        self.tabbuttons.segments=[x for x in self.tabbuttons.segments if x != tabname]
        self.remove_subview(tabname)
        # if tab was top tab, think about updating selected tab to whatever is on top 
        
    def layout(self):
        pass   # maybe set tabbuttons size
        
if __name__=='__main__':
    v=TabbedView()
    v.addtab(ui.View(name='red',bg_color='red'))
    v.addtab(ui.View(bg_color='blue'))
    v.addtab(ui.View(name='green',bg_color='green'))
    v.addtab(ui.View(name='green',bg_color='green'))
    v.present()