# coding: utf-8
import ui, console, editor, os, notification

class BaseMenu (ui.View):
    def __init__(self, directory):
        console.hide_output()
        self.__make_self(directory)
        self.__make_lds()
        self.__make_tv()
        self.__make_biB()
        self.__make_biE()
        self.layout()
        self.did_load() 
        self.present('popover')

    def did_load(self):
        if self.sDir == 'snippets': self.__biAE(object)

    def layout(self):
        self.width = 320
        self.height = len(self.lItems) * 50
        self.__tv.frame = (0, 0, 320, 600)
        self.__tv.row_height=50

    def __make_self(self, directory):
        self.BaseMenu_version = '3.0'
        self.BaseMenu_source_code = 'Original by @tony.'
        self.BaseMenu_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.sDir = directory
        self.name = self.sDir.title()
        self.sRow = ''
        self.lItems = list()
        self.bEdit = False
        self.make_list()

    def make_list(self):
        pass

    def __make_lds(self):
        self.__lds = ui.ListDataSource(self.lItems)
        self.__lds.action = self.__ldsA

    def __make_tv(self):
        self.__tv = ui.TableView()
        self.__tv.data_source = self.__lds
        self.__tv.delegate = self.__lds
        self.add_subview(self.__tv)

    def __make_biB(self):
        self.__biB = ui.ButtonItem()
        self.__biB.image = ui.Image.named('ionicons-ios7-arrow-back-32')
        self.__biB.action = self.__biAB
        self.left_button_items = [self.__biB]   

    def __make_biE(self):
        self.__biE = ui.ButtonItem()
        self.__biE.image = ui.Image.named('ionicons-ios7-play-outline-32')
        self.__biE.action = self.__biAE
        self.right_button_items = [self.__biE]  

    def __ldsA(self, sender):
        self.sRow = sender.items[sender.selected_row]['title']
        self.close()

    def __biAB(self, sender):
        self.sRow = '*back'
        self.close()

    def __biAE(self, sender):
        self.bEdit = not self.bEdit
        if self.bEdit:
            self.__biE.image = ui.Image.named('ionicons-ios7-compose-outline-32')
        else:
            self.__biE.image = ui.Image.named('ionicons-ios7-play-outline-32')

class Menu (BaseMenu):
    def did_load(self):
        self.left_button_items = []
        self.right_button_items = []

    def make_list(self):
        self.lItems = ({'title': 'Documents', 'image': 'ionicons-ios7-cloud-outline-32','accessory_type': 'disclosure_indicator'}), ({'title': 'Snippets',  'image': 'ionicons-ios7-pricetag-outline-32','accessory_type': 'disclosure_indicator'}), ({'title': 'Tools', 'image': 'ionicons-ios7-search-32', 'accessory_type': 'disclosure_indicator'}), ({'title': 'Projects', 'image': 'ionicons-ios7-star-outline-32', 'accessory_type': 'disclosure_indicator'})

class MenuLevel (BaseMenu):
    def make_list(self):
        self.lItems = list()
        for entry in os.listdir(os.path.expanduser('~/Documents/myProject/' + self.sDir + '/')):
            if os.path.splitext(entry)[1] == '.py':
                self.lItems.append({'title': os.path.splitext(entry)[0]})

class MenuController (object):
    def __init__(self):
        self.__make_self()
        self.__control_menu()

    def __make_self(self):
        self.MenuController_version = '3.0'
        self.MenuController_source_code = 'Original by @tony.'
        self.MenuController_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'

    def __control_menu(self):
        self.__m = Menu('Menu')
        self.__m.wait_modal()
        if self.__m.sRow != '':
            self.__ml = MenuLevel(self.__m.sRow.lower())
            self.__ml.wait_modal()
            if self.__ml.sRow == '*back':
                MenuController()
            else:
                pass
#               if False:
#                   if self.__ml.sRow != '':
#                       if self.__ml.bEdit:
#                           editor.open_file(self.__ml.sDir + '/' + self.__ml.sRow + '.py')
#                       else:
#                           execfile(os.path.expanduser('~/Documents/' + self.__ml.sDir + '/' + self.__ml.sRow + '.py'))
#               else:
#                   if self.__ml.sRow != '':
#                       if self.__ml.bEdit:
#                           target = self.__ml.sDir + '/' + self.__ml.sRow
#                       else:
#                           target = self.__ml.sDir + '/' + self.__ml.sRow + '?action=run'
#                       notification.schedule('', 0.1, '', 'pythonista://' + target)

if __name__ == "__main__":
    MenuController()