# coding: utf-8
import ui, editor, console

class ReplaceView(ui.View):
    def __init__(self):
        console.hide_output()
        self.__make_self()
        self.__make_tfF()
        self.__make_tfR()
        self.__make_bR()
        self.__make_biC()
        self.did_load()
        self.layout()
        self.present('popover')

    def __make_self(self):
        self.ReplaceView_version = '2.0'
        self.ReplaceView_source_code = 'Original by @tony.'
        self.ReplaceView_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.name = ''

    def did_load(self):
        if len(self.__tfF.text) > 0: 
            self.__tfF.enabled = False
            self.__tfF.text_color = 'grey'

    def layout(self):
        self.frame = (0,0, 320, 50)
        self.__tfF.frame = (10, 10, 100, 30)
        self.__tfR.frame = (120, 10, 100, 30)
        self.__bR.frame = (220, 10, 100, 30)
        self.__tfR.alpha = 0.0
        def f():
            self.__tfR.alpha = 1.0
        ui.animate(f, 1)

    def __make_tfF(self):
        self.__tfF = ui.TextField()
        self.__tfF.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
        self.__tfF.text = editor.get_text()[editor.get_selection()[0]:editor.get_selection()[1]]
        self.add_subview(self.__tfF)

    def __make_tfR(self):
        self.__tfR = ui.TextField()
        self.__tfR.text_color = 'red'
        self.__tfR.autocapitalization_type = ui.AUTOCAPITALIZE_NONE
        self.__tfR.text = self.__tfF.text
        self.add_subview(self.__tfR)

    def __make_bR(self):
        self.__bR = ui.Button()
        self.__bR.title = 'Replace'
        self.__bR.action = self.__bRA
        self.add_subview(self.__bR)

    def __make_biC(self):
        self.__biC = ui.ButtonItem()
        self.__biC.title = 'Cancel'
        self.__biC.action = self.__biCA
        self.left_button_items = [self.__biC]

    def __bRA(self, sender):
        if len(editor.get_text()) != 0: 
            editor.replace_text(0, len(editor.get_text()), editor.get_text().replace(self.__tfF.text, self.__tfR.text))
        self.close()

    def __biCA(self, sender):
        self.close()

if __name__ == "__main__":
    ReplaceView()