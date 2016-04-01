# coding: utf-8
import ui, editor, console

class CommentView(ui.View):
    def __init__(self):
        console.hide_output()
        self.__make_self()
        self.__make_tvP()
        self.__make_bC()
        self.__make_biC()       
        self.did_load()
        self.layout()
        self.present('popover')

    def did_load(self):
        text = editor.get_text()
        selection = editor.get_line_selection()
        selected_text = text[selection[0]:selection[1]]
        is_comment = selected_text.strip().startswith('#')
        if is_comment:
            self.__bC.title = 'Uncomment'
            self.__tvP.text = selected_text.strip()[1:11] + '...'
            self.__tvP.text_color = 'black'
        else:
            self.__bC.title = 'Comment'
            self.__tvP.text = '#' + selected_text.strip()[0:10] + '...'
            self.__tvP.text_color = 'green'

    def layout(self):
        self.frame = (0,0, 320, 50)
        self.__tvP.frame = (10, 5, 200, 30)
        self.__bC.frame = (220, 10, 100, 30)
        self.__tvP.alpha = 0.0
        def f():
            self.__tvP.alpha = 1.0
        ui.animate(f, duration=1.0)

    def __make_self(self):
        self.CommentView_version = '2.0'
        self.CommentView_source_code = 'Original by @tony.'
        self.CommentView_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.name = ''

    def __make_tvP(self):
        self.__tvP = ui.TextView()
        self.__tvP.font = ('<system-bold>', 18)
        self.__tvP.background_color = '#f9f9f9'
        self.add_subview(self.__tvP)

    def __make_bC(self):
        self.__bC = ui.Button()
        self.__bC.action = self.__bCA
        self.add_subview(self.__bC)

    def __make_biC(self):
        self.__biC = ui.ButtonItem()
        self.__biC.title = 'Cancel'
        self.__biC.action = self.__biCA
        self.left_button_items = [self.__biC]

    def __bCA(self, sender):
        # from: pythonista/docs/editor --------------
        text = editor.get_text()
        selection = editor.get_line_selection()
        selected_text = text[selection[0]:selection[1]]
        is_comment = selected_text.strip().startswith('#')
        replacement = ''
        for line in selected_text.splitlines():
            if is_comment:
                if line.strip().startswith('#'):
                    replacement += line[line.find('#') + 1:] + '\n'
                else:
                    replacement += line + '\n'
            else:
                replacement += '#' + line + '\n'
        editor.replace_text(selection[0], selection[1], replacement)
        editor.set_selection(selection[0], selection[0] + len(replacement) - 1)
        # end -----------------------------------------
        self.close()

    def __biCA(self, sender):
        self.close()

if __name__ == "__main__":
    CommentView()