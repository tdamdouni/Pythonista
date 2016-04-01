# coding: utf-8
import ui, io, os
from PIL import Image as ImageP

class MultiBrowser (ui.View):
    def __init__(self):
        self.__make_self()
        self.__make_wv1()
        self.__make_wv2()
        self.__make_wv3()
        self.__make_bRA()
        self.__make_bB()
        self.__make_bF2()
        self.__make_bF3()
        self.did_load()
        self.layout()
        self.__bRAA(object)
        self.present('panel')

    def did_load(self):
        pass

    def layout(self):
        self.wv_1.frame = (self.wv_1.x, 10, 498, 284)
        self.wv_2.frame = (520, 10, 495, 651)
        self.wv_3.frame = (10, 309, 495, 352)
        self.__bRA.frame = (981, 668, 32, 32)
        self.__bB.frame = (930, 668, 32, 32)
        self.__bF2.frame = (520, 668, 32, 32)
        self.__bF3.frame = (10, 668, 32, 32)
        if self.__bF3.hidden == True:
            self.__bF2.x = 10
            self.wv_2.frame = (10, 10, 1005, 651)
        if self.__bF2.hidden == True:
            self.wv_3.frame = (10, 10, 1005, 651)

    def __make_self(self):
        self.MultiBrowser_version = '3.0'
        self.MultiBrowser_source_code = 'Original by @tony.'
        self.MultiBrowser_permissions = 'Permission to use/subclass/redistribute, but NOT to modify code.'
        self.name = 'MultiBrowser'
        self.url_1 = 'http://youtu.be/4BbjSXZnjBo'
        self.url_2 = 'http://omz-forums.appspot.com/pythonista'
        self.url_3 = 'http://omz-forums.appspot.com/pythonista'
        self.__sJsW = "var metas = document.getElementsByTagName('meta');var i; for (i=0; i<metas.length; i++) {if (metas[i].name == 'viewport'){metas[i].content = 'width=device-width';}}"
        self.threshold_1 = 0
        self.threshold_2 = 0
        self.threshold_3 = 0
        self.javascript_1 = ''
        self.javascript_2 = self.__sJsW + ''
        self.javascript_3 = self.__sJsW + ''
        self.count_1 = 0
        self.count_2 = 0
        self.count_3 = 0
        self.__ipR = None

    def __make_wv1(self):
        self.wv_1 = ui.WebView()
        self.wv_1.delegate = self.delegate_1()
        self.wv_1.x = 10
        self.add_subview(self.wv_1)

    def __make_wv2(self):
        self.wv_2 = ui.WebView()
        self.wv_2.delegate = self.delegate_2()
        self.add_subview(self.wv_2)

    def __make_wv3(self):
        self.wv_3 = ui.WebView()
        self.wv_3.delegate = self.delegate_3()
        self.add_subview(self.wv_3)

    def __make_bRA(self):
        self.__bRA = ui.Button()
        self.__bRA.image = ui.Image.named('ionicons-ios7-reload-32')
        self.__bRA.action = self.__bRAA
        self.add_subview(self.__bRA)

    def __make_bB(self):
        self.__bB = ui.Button()
        self.__bB.image = ui.Image.named('ionicons-ios7-arrow-left-32')
        self.__bB.action = self.__bBA
        self.__bB.hidden = True
        self.add_subview(self.__bB)

    def __make_bF2(self):
        self.__bF2 = ui.Button()
        self.__bF2.image = ui.Image.named('ionicons-arrow-expand-32')
        self.__bF2.action = self.__bF2A
        self.add_subview(self.__bF2)

    def __make_bF3(self):
        self.__bF3 = ui.Button()
        self.__bF3.image = ui.Image.named('ionicons-arrow-expand-32')
        self.__bF3.action = self.__bF3A
        self.add_subview(self.__bF3)

    class delegate_1 (object):
        def webview_did_finish_load(self, webview): 
            self = webview.superview
            if self.count_1 == self.threshold_1:
                webview.evaluate_javascript(self.javascript_1)
            self.count_1 += 1

    class delegate_2 (object):
        def webview_did_finish_load(self, webview):
            self = webview.superview
            if self.count_2 == self.threshold_2:
                webview.evaluate_javascript(self.javascript_2)
            self.count_2 += 1

    class delegate_3 (object):
        def webview_did_finish_load(self, webview):
            self = webview.superview
            if self.count_3 == self.threshold_3:
                webview.evaluate_javascript(self.javascript_3)
            self.count_3 += 1

    def __bR1A(self, sender):
        if self.count_1 == 0:
            self.wv_1.load_url(self.url_1)

    def __bR2A(self, sender):
        self.count_2 = 0
        self.wv_2.load_url(self.url_2)  

    def __bR3A(self, sender):
        self.count_3 = 0
        self.wv_3.load_url(self.url_3)

    def __bRAA(self, sender):
        ui.cancel_delays()
        self.__iQ = 5
        self.__ipR = ImageP.open('ionicons-ios7-reload-32')
        self.__bRA.image = ui.Image.named('ionicons-load-d-32')
        self.__bF2.enabled = False 
        self.__bF3.enabled = False 
        self.__bR1A(object)
        self.__bR2A(object)
        self.__bR3A(object)
        ui.delay(self.__AutoRefresh,3)

    def __bBA(self, sender):
        self.wv_2.go_back()
        self.wv_3.go_back()

    def __bF2A(self, sender):
        self.wv_2.bring_to_front()
        if self.wv_2.width < 1000:
            ui.cancel_delays()
            if getattr(self, 'bD3', None) is not None: self.bD3.hidden = True
            self.__bB.hidden = False
            self.__bF2.image = ui.Image.named('ionicons-arrow-shrink-32')
            self.__bF3.hidden = True 
            self.__bF2.x = 10
            self.wv_2.width = 1005
            self.wv_2.height = 651
        else:
            if getattr(self, 'bD3', None) is not None: self.bD3.hidden = False
            self.__bB.hidden = True
            self.__bF2.image = ui.Image.named('ionicons-arrow-expand-32')
            self.__bF2.x = 520
            self.__bF3.hidden = False 
            self.wv_2.width = 495
            self.wv_2.height = 651
            self.__bRAA(object)
        self.wv_2.evaluate_javascript(self.javascript_2)

    def __bF3A(self, sender):
        self.wv_3.bring_to_front()
        if self.wv_3.width < 1000:
            ui.cancel_delays()
            if getattr(self, 'bD3', None) is not None: self.bD3.hidden = True
            self.__bB.hidden = False
            self.__bF3.image = ui.Image.named('ionicons-arrow-shrink-32')
            self.__bF2.hidden = True 
            self.wv_3.width = 1005
            self.wv_3.height = 651
        else:
            if getattr(self, 'bD3', None) is not None: self.bD3.hidden = False
            self.__bB.hidden = True
            self.__bF3.image = ui.Image.named('ionicons-arrow-expand-32')
            self.__bF2.hidden = False 
            self.wv_3.width = 495
            self.wv_3.height = 352
            self.__bRAA(object)
        self.wv_3.evaluate_javascript(self.javascript_3)

    def __AutoRefresh(self):
        if self.__iQ ==  5:
            self.__iQ = 1
            self.__bF2.enabled = True
            self.__bF3.enabled = True
            with io.BytesIO() as bIO:
                self.__ipR.save(bIO, self.__ipR.format)
                self.__bRA.image = ui.Image.from_data(bIO.getvalue())
            ui.delay(self.__AutoRefresh, 57)
        else:
            with io.BytesIO() as bIO:
                l_ipR = self.__ipR.rotate(-90 * self.__iQ)
                l_ipR.save(bIO, self.__ipR.format)
                if self.__iQ == 4:
                    self.__bRAA(object)
                else:
                    self.__bRA.image = ui.Image.from_data(bIO.getvalue())
                    self.__iQ += 1
                    ui.delay(self.__AutoRefresh, 60)

    @ui.in_background
    def will_close(self):
        ui.cancel_delays()
        self.wv_1.stop()
        self.wv_2.stop()
        self.wv_3.stop()

class MyMultiBrowser (MultiBrowser):
    def did_load(self):
        self.__make_self()

    def __make_self(self):
        self.name = 'My Multi'
        self.url_2 = 'http://www.engadget.com'
        self.threshold_2 = 2
        self.javascript_2 += "window.scrollTo(0,document.getElementById('header-social-icons').offsetTop + 20);"

if __name__ == "__main__":
    MyMultiBrowser()