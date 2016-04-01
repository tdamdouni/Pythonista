# coding: utf-8
import ui, console

class WebBrowser(ui.View):
    def __init__(self):
        self.__make_self()
        self.__make_wvB()
        self.__make_bB()
        self.__make_bF()
        self.__make_bR()
        self.did_load()
        self.layout()
        self.present('panel')

    def did_load(self):
        pass

    def layout(self):
        self.__wvB.frame = (0, 0, self.width, self.height - 50)
        self.__bB.frame = (10, self.__wvB.height, 50, 50)
        self.__bF.frame = (60, self.__wvB.height, 50, 50)
        self.__bR.frame = (self.__wvB.width - 70, self.__wvB.height, 50, 50)

    def __make_self(self):
        self.WebBrowser_version = '2.0'
        self.WebBrowser_source_code = 'Original by @tony.'
        self.WebBrowser_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.name = 'Browser'
        self.server = None

    def __make_wvB(self):
        self.__wvB = ui.WebView()
        self.add_subview(self.__wvB)

    def __make_bB(self):
        self.__bB = ui.Button()
        self.__bB.image = ui.Image.named('ionicons-ios7-arrow-left-32')
        self.__bB.action = self.__bBA
        self.add_subview(self.__bB)

    def __make_bF(self):
        self.__bF = ui.Button()
        self.__bF.image = ui.Image.named('ionicons-ios7-arrow-right-32')
        self.__bF.action = self.__bFA
        self.add_subview(self.__bF)

    def __make_bR(self):
        self.__bR = ui.Button()
        self.__bR.image = ui.Image.named('ionicons-ios7-reload-32')
        self.__bR.action = self.__bBA
        self.add_subview(self.__bR)

    def __bBA(self, sender):
        self.__wvB.go_back()

    def __bFA(self, sender):
        self.__wvB.go_forward()

    def __bRA(self, sender):
        self.__wvB.reload()

    def open(self, strURL):
        self.__wvB.load_url(strURL)

    def will_close(self):
        if self.server is not None:
            self.server.shutdown()
        console.hide_output()

if __name__ == "__main__":
    WebBrowser()