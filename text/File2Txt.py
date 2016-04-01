# coding: utf-8

# https://github.com/HeyItsJono/Pythonista

# Converts any file to a .txt file in Pythonista.

import console, os, sys

if __name__ == '__main__':
    console.clear()
    filename = raw_input('Enter filename (Path Optional) \n')
    if not filename:
        sys.exit('No filename entered.')
    if filename.endswith('.txt'):
        sys.exit('Can not convert .txt to .txt.')
    try:
        with open(filename, 'r') as in_file:
            with open(os.path.splitext(filename)[0] + '.txt', 'w') as out_file:
                out_file.write(in_file.read())
    except IOError:
        console.hud_alert('File not found: ' + filename, icon = 'error')