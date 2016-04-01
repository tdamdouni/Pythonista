import os
import sys
import cmd
import contextlib

from ...tools.toolbox import bash

alias = ['shell']

def main(self, line):
    do_python(line)


def do_python(line):
    """Python shell"""
    args = bash(line)
    # Save the old path, in case user messes with it in shell

    with _save_context():
        sys.path.append(os.getcwd())

        if len(args) == 0:
            print 'Entering Python shell'
            p = PyShell()
            p.prompt = '>>> '
            p.cmdloop()
        else:
            # Run the program and pass any args.
            try:
                sys.argv = args[:]
                file_path = os.path.relpath(args[0])
                namespace = dict(locals(), **globals())
                namespace['__name__'] = '__main__'
                namespace['__file__'] = os.path.abspath(file_path)
                execfile(file_path, namespace, namespace)
            except:
                print 'Error: {0}'.format(sys.exc_value)

class PyShell(cmd.Cmd):
    def __init__(self):
        # super(PyShell, self).__init__()
        cmd.Cmd.__init__(self)
        self.did_quit = False
        self.exec_globals = globals()
        self.exec_locals = {}

    def do_quit(self, NoParams=None):
        """exit shell"""
        self.did_quit = True

    def emptyline(self):
        pass

    def precmd(self, line):
        if not line.startswith('quit'):
            if line:
                try:
                    exec (line, self.exec_globals, self.exec_locals)
                except SyntaxError as e:
                    print 'Syntax Error: {0}'.format(e)
                except ImportError as e:
                    print 'Import Error: {0}'.format(e)
                except NameError as e:
                    print 'Name Error: {0}'.format(e)
                except:
                    print 'Error: {0}'.format(sys.exc_value)
            return '\n'
        else:
            return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        return self.did_quit


@contextlib.contextmanager
def _save_context():
    sys._argv = sys.argv[:]
    sys._path = sys.path[:]
    yield
    sys.argv = sys._argv
    sys.path = sys._path
