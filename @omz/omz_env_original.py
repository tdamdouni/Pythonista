# https://github.com/cclauss/Ten-lines-or-less/blob/master/omz_env.py

# coding: utf-8

# See: https://forum.omz-software.com/topic/2135/telling-if-i-m-pythonista-or-editorial-or-sublime-text-or-whatever

omz_env = None
try:
    import workflow
    omz_env = 'Editorial'
except ImportError:
    try:
        import scene
        omz_env = 'Pythonista'
    except ImportError:
        pass

if not omz_env:
    print('Sublime or other non-OMZ Software platform.')
else:
    print('Yeah!!')