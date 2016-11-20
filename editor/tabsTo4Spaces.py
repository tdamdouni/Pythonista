# replace ALL tab characters with four spaces

import editor, sys

theText = editor.get_text()
theCount = theText.count('\t')
if not theText.count('\t'):
    print('no tabs found.')
    sys.exit()
theLength = len(theText)
theText = theText.splitlines()
#theSelection = editor.get_selection()
for i in range(len(theText)):
    theText[i] = theText[i].replace('\t', '    ')
editor.replace_text(0, theLength, '\n'.join(theText))
#editor.set_selection(theSelection[0])
