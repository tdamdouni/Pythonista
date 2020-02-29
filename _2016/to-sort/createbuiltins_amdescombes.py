# https://gist.github.com/amdescombes/30839ae0280a5077b8669757e5efa75d

"""
Creates python files for builtin modules in order to use them with PyCharm to get code completion and resolve all import issues
"""
from __future__ import print_function
import inspect
import sound
import _ui
import _scene2

def_fmt = '\n\n%sdef %s():\n%s    pass\n'
method_fmt = '\n%sdef %s(self):\n%s    pass\n'
cls_method_fmt = '\n%sdef %s(cls):\n%s    pass\n'
class_fmt = '\n\n%sclass %s:%s\n'
doc_fmt = '%s"""%s"""\n'


def handle_attribute(name, func, indent):
    if isinstance(func, int) or isinstance(func, float):
        return '\n%s%s = %s\n' % (indent, name, func)
    else:
        return '\n%s%s = "%s"\n' % (indent, name, func)


def get_info(modul, indentlevel=0, inclass=False):
    _f = []
    indent = '    ' * indentlevel
    for name, func in inspect.getmembers(modul):
        if callable(func):
            if name == '__getattribute__':
                continue
            isfunc = 'function' in str(func)
            if name == '__new__':
                _f.append(cls_method_fmt % (indent, name, indent))
            else:
                _f.append((def_fmt if isfunc else method_fmt if inclass else class_fmt) % (indent, name, indent))
            if not isfunc and not inclass:
                get_info(func, indentlevel + 1, True)
        else:
            if inclass and name == '__doc__':  # insert docstring
                _f.insert(0, doc_fmt % (indent, func))
            else:
                _f.append(handle_attribute(name, func, indent))
    return _f


def create_func(modul, modname, indentlevel=0, inclass=False):
    print("processing %s" % modname)
    _f = []
    indent = '    ' * indentlevel
    for name, func in inspect.getmembers(modul):
        if callable(func):
            if name == '__getattribute__':
                continue
            isfunc = 'function' in str(func)
            _f.append((def_fmt if isfunc else method_fmt if inclass else class_fmt) % (indent, name, indent))
            if not isfunc and not inclass:
                cls = get_info(func, indentlevel + 1, True)
                _f += cls
        else:
            if name == '__doc__':  # insert docstring
                _f.insert(0, doc_fmt % (indent, func))
            elif name not in ['__name__', '__package__']:
                _f.append(handle_attribute(name, func, indent))
    open(modname, 'w').write(''.join(_f))
    print("processed %s" % modname)


if __name__ == "__main__":
    create_func(sound, 'sound.py')
    create_func(_ui, '_ui.py')
    create_func(_scene2, '_scene2.py')
    print("done")
