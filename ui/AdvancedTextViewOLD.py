import ui
class UndoStack(object):
    ''' class representing an action stack dor a textfield'''
    def __init__(self):
        from collections import deque
        self._undostack = deque()
        self._redostack = deque()
    def addAction(self,range, original, replacement):
        '''given range, and original text in that range, and replacement vale, either append to current entry, or pcreate new item on undo stack'''
        try:
            currentAction =self._undostack.pop()
            #two cases:  prepend/backspace, and postpend
            if range[1]==currentAction.replacementrange[0]:
              #  print 'prepend'
                #prepend
                currentAction.original=original+currentAction.original
                currentAction.replacement=replacement+currentAction.replacement
                currentAction.range[0]=range[0]
                currentAction.replacementrange[0]=range[0]               
                currentAction.replacementrange[1]=currentAction.replacementrange[0] + len(currentAction.replacement)
            elif range[0]==currentAction.replacementrange[1]:
             #   print 'append'
               #append, possibly highlighted afjacent tet and replaced
                currentAction.original = currentAction.original + original
                currentAction.replacement = currentAction.replacement + replacement
                currentAction.range[1]+=(range[1]-currentAction.replacementrange[1])
                currentAction.replacementrange[1]=currentAction.replacementrange[0] + len(currentAction.replacement)
            else:
              #  print 'new'
                self._undostack.append(currentAction)
                raise IndexError    #to add new entry
        except IndexError:
            # add new entry
            class undoaction(object):
                def __init__(self):
                    self.range=[0,0]
                    self.original=''
                    self.replacement=''
                    self.replacementrange=[0,0]
           # print 'new'
            currentAction = undoaction()
            currentAction.range=list(range)
            currentAction.original=original
            currentAction.replacement=replacement
            currentAction.replacementrange=list(range)
            currentAction.replacementrange[1]=currentAction.replacementrange[0] + len(currentAction.replacement)
        self._undostack.append(currentAction)
            
    def undo(self):
        '''pops undo action from undostack, and oushes to redo stack.  returns a range and text to replace in that range'''
        try:
            currentAction = self._undostack.pop()
            self._redostack.append(currentAction)
            return (tuple(currentAction.replacementrange), currentAction.original)
        except IndexError:
            return ((0,0), '')
    def redo(self):
        try:
            currentAction = self._redostack.pop()
            self._undostack.append(currentAction)
            return (tuple(currentAction.range), currentAction.replacement)
        except IndexError:
            return ((0,0), '')
            
class AdvancedTextView(ui.View):
    '''an advanced textview, which enables undo and redo capability.
    
    the basic model will be a view containing a textview.  we will masquerade the view to look like a textview, using properties and getters/ setters for textview specific properties.  then, we will intercept textview should change events.
    
what do we need to store?  range, original, replacement, and replacement range.
undo will set replacement range to original value.  redo sets range to replacement value.
replacement range is range[0],range[0]+len(replacement)

now, if range is adjacent to replacement range, i.e range[0]==replacementrange[1], then we expand replacement range, and append new text.  if not, the  we create a new undo entry.
    '''
    
    def __setattr__(self, name,value):
        '''masquerade as a textview.  all properties of the underlying textview are mirrored between this object and textview!'''
        if name not in ['frame','width','height','x','y','flex','hidden','transform']:
            if hasattr(self,'_tv'):
                if name in dir(self._tv):
                    object.__setattr__(self._tv,name,value)
        object.__setattr__(self,name,value)
    def __getattribute__(self,name):
        '''masquerade as textview... if we got here, lookup failed, so try _tv'''
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            if hasattr(self,'_tv') and name in dir(self._tv):
                return object.__getattribute__(self._tv,name)
            else:
                raise 
    def __init__(self, 
                 frame=(0, 0, 600, 400),
                 **kwargs):
        self._undo = UndoStack()
        self._tv = ui.TextView(frame=(0,0,self.width,self.height),bg_color=(1.0,1.0,1.0))
        self._tv.flex='WH'
        self.add_subview(self._tv)
        ui.View.__init__(self,**kwargs)
        #ui props
        self.frame=frame
        self._tv.delegate = self

    def textview_should_change(self, textview, range, replacement):
        #print range,replacement
        # print range
        original = textview.text[range[0]:range[1]]
        self._undo.addAction(range,original,replacement)
        return True
    def undoaction(self,sender):
        (range,replacement)=self._undo.undo()
        if range:
            try:
                self._tv.replace_range(range,replacement)
            except ValueError:
                self._undo = UndoStack()
    def redoaction(self,sender):
        (range,replacement)=self._undo.redo()
        if range:
            try:
                self._tv.replace_range(range,replacement)
            except  ValueError:
                self._undo = UndoStack()



if __name__=='__main__':
    v=AdvancedTextView()
    v.present('sheet')
    v.text='test'
