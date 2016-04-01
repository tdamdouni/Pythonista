# @ui update for version 1.6
# https://github.com/jsbain/uicomponents/blob/master/file_picker.py
# coding: utf-8
import dropdown, os, fnmatch
class FilteredFileDropdown(dropdown.DropdownView):
    def __init__(self,frame=(0,0,300,32),name='dropdown', filter='*',base=os.path.expanduser('~/Documents/Dropbox')):
        self.frame=frame
        self.filter=filter
        self.base=base
        super(type(self),self).__init__(frame=frame,name=name,items=self.path_generator)

        
    def path_generator(self):
        for filename in os.listdir(self.base):
                if self.abort():
                    return
                if fnmatch.fnmatch(filename,self.filter):
                    yield filename
if __name__=='__main__':
   d=FilteredFileDropdown(filter='*.py')
   d.present()