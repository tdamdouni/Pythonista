import dropdown, os, fnmatch
class FilteredDirDropdown(dropdown.DropdownView):
    def __init__(self,frame=(0,0,300,32),name='dropdown', filter='*',base=os.path.expanduser('~/Documents')):
        self.frame=frame
        self.filter=filter
        self.base=base
        super(type(self),self).__init__(frame=frame,name=name,items=self.path_generator)

        
    def path_generator(self):
        for rootpath,dirs,_ in os.walk(self.base):
            for d in dirs:
                if self.abort():
                    return
                if fnmatch.fnmatch(d,self.filter):
                    yield os.path.relpath(rootpath,self.base)


