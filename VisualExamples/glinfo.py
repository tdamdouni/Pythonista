from visual import *
import sys, os, time

print("This test of OpenGL options is useful mainly on Windows.")
print()

def print_mtime(f):
    try:
        print("  %-30s %s" % (f, time.ctime(os.path.getmtime(f))))
    except:
        pass

tried = {}
paths = sys.path
try:
    windir = os.environ['windir']
    paths = paths + [os.path.join(windir,'system'),
                     os.path.join(windir,'system32')]
except:
    print('Windows directory not found.')

for dir in paths:
    for file in ['cvisual.dll', 'visual\\__init__.py', 'visual\\graph.py', 'opengl32.dll']:
        f = os.path.normcase(os.path.normpath(os.path.join(dir, file)))
        if f not in tried:
            tried[f] = print_mtime(f)

scene.title = "Renderer test"
scene.height = 2
scene.visible = 1
print(scene.info())
scene.visible = 0
