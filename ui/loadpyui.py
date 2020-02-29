'''loadpyui
custom version of load_pyui, which reads json pyui and returns a view.
notable differences with ui.load_view version:
    - although not currently implemented, this could support late binding of actions/delegates from instance objects.  
    - any attribute in a view can be set in a hand edited json pyui file, whereas ui.load_view only allows certain attributes to be set
    - not all attributes settable in the pyui editor are aupported, aee below
    
in general the pyui is a json representation of a view:
    actually, an array of dicts defining views.  only the first entry is populated.  
    keys are: class, frame, attributes, and nodes(aka subviews).  by instantiating the class, setting the frame, walking through attributes, one can create the top view.  then, by recursively building nodes and adding them as subviews, we can create the entire view heirarchy. the main difficulty is handling all of the special cases, where the pyui attributes do not match names or type expexted in the python object.  for instance fonts, actions, colors, and several other cases.  i probably have not found all of the quirks yet.
    
    currently, the following are unsupported (and quite possibly more):
         tableview datasource
         actions that dont appear in globals, or inside a custom class.  todo would be to allow some syntax that allows you to specify a root controller, or, to traverse globals using obj.method type indexing.
         textfield border_style (not sure this maps to)
         
         
'''
from __future__ import print_function


import json,ui,ast,re

def loadpyui(filename,verbose=False):
    '''load a pyui file, and return a view'''
    with open(filename) as f:
        v=json.load(f)[0]
    return build_view(v,verbose)
    
class IgnoreVal(object):
    '''dummy class to return nothing '''
    pass
    
def build_view(view_dict,verbose=False ):
    '''build a view given a dict'''
    #each view has class, frame, attributes, nodes

    # first:  instantiate the view
    if str(view_dict['class'] ) in ui.__dict__:
        v=eval(view_dict['class'],ui.__dict__)()
    elif str(view_dict['class'] in globals()):
        v=eval(view_dict['class'],globals())    #not tested!
    # next, set frame
    v.frame=parse_frame(view_dict['frame'])
    #handle attributes
    a= view_dict['attributes'] 
    for key,val in a.items():
        for regexp,handler in special_handlers.items():
            val = handler(str(val)) if re.match(regexp,key) else val
        try:
            if not isinstance(val,IgnoreVal):
                v.__setattr__(str(key),val)
        except AttributeError:
            if verbose:
                print(key, val ,'was not set ', end=' ')
                if 'name' in a:
                    print('for ',a['name'])
                else:
                    print('for root')

    #handle some other special cases for pyui quirks
    if 'font' in dir(v):
        v.font=get_font(a) 
    if 'numberOfLines' in a:
        v.number_of_lines=a.get('numberOfLines')
    if 'content_size' in dir(v):
        v.content_size=(a.get('content_width',0),a.get('content_height',0))
    if 'action' in dir(v) and 'action' in a:
        bind_action(v,a['action'])

    #now, populate subviews
    for n in view_dict['nodes']:
        sv=build_view(n,verbose)
        v.add_subview(sv)
    return v
    
def parse_color(c):
    '''strip RGBA and return the color tuple.
'''
    return ast.literal_eval(c.replace('RGBA','') )
def parse_frame(framestr):
    '''convert {{x,y},{w,h}} string to (x,y,w,h) tuple '''
    frame=framestr.replace('{', '').replace('}', '')
    return ast.literal_eval(frame)
def parse_alignment(a):
    '''handle alignment attribute.  TODO: handle all valid types'''
    if a=='left':
        return ui.ALIGN_LEFT
    elif a=='right':
        return ui.ALIGN_RIGHT
    elif a=='center':
        return ui.ALIGN_CENTER
    else:        #fixme... handle all types. 
        print('unhandled alignment',a)
        return ui.ALIGN_LEFT
def parse_segments(seg):
    '''segmentview.segments convert 'Hello|World' to ['Hello','World']'''
    return seg.split('|')
    
def ignore(val):
    '''dont populate this attribute'''
    return IgnoreVal()
    
def get_font(attribs):
    '''get populated font name font attributes'''
    font_size=attribs.get('font_size',12)
    font_name=attribs.get('font_name', '<system>')
    font_bold=attribs.get('font_bold',False)

    if font_bold:
        font_name=font_name.split('>')
        font_name[0]+='Bold'
        font_name='>'.join(font_name)
    return (font_name,font_size)
def bind_action(v,action):
    '''set v.action to methodname contain in action.  check instance methods of custom class, for actions of this.action style, and globals() for everythin else.
    TODO:  allow fully qualified methods from within modules  '''
    if 'action' not in dir(v):
        return
    
    if action.startswith('this'):
        action=action.split('this.')[1]
        if action in dir(v):
            v.action= v.__getattribute__(action)
    elif action in globals():
            v.action= globals()[action]
    else:
        print('Warning: could not bind action', action, 'in ', v.name)

#handle keys which match the regexp keys below, replace value with function called on value   
special_handlers={'.*color':parse_color,
                  'alignment':parse_alignment,
                  'segments':parse_segments,
                  'uuid':ignore,
                  'enabled':ignore,
                  'font_.*':ignore,
                  'numberOfLines':ignore,
                  'content_[height|width]':ignore,
                  'action':ignore}

if __name__=='__main__':
    v=loadpyui('sample.pyui',verbose=True)
    v.present('sheet')

