# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

import spelling_mode

reload(spelling_mode)

def get_predefined_modes():
  
  modes = []
    
  mode = spelling_mode.spelling_mode()
  mode.control.name = u"Vor Rechtschreibreform"
  mode.control.comment = "Rechtschreibregeln wie sie vor der Reform am XXXXX gültig waren."
  mode.control.isImmutable = True
  mode.combination.switch_legacy_sz = True
  modes.append(mode)

  mode = spelling_mode.spelling_mode()
  mode.control.name = u"Aktuelle Rechtschreibung"
  mode.control.isImmutable = True
  mode.control.isReference = True
  modes.append(mode)

  return modes
  
def test():
  
  modes = get_predefined_modes()
        
if __name__ == '__main__':
  test()