#coding: utf-8

import string

import spelling_mode

reload(spelling_mode)

from spelling_mode import *

global default_mode

def set_default_mode(mymode):
  global default_mode
  default_mode = mymode
  
def get_default_mode():
  global default_mode
  return default_mode

      
def capitalize(l, c=C_NONE):
  if default_mode.switch_capitalization_all_capital or(c & default_mode.bitswitch_capitalization):
    if l == 'ü':
      return 'Ü'
    elif l == 'ä':
      return 'Ä'
    elif l == 'ö':
      return 'Ö'
    elif l == 'š':
      return 'Š'
    elif l == 'č':
      return 'Č'
    elif l == 'ā':
      return 'Ā'
    elif l == 'ė':
      return 'Ė'
    elif l == 'ī':
      return 'Ī'
    elif l == 'ō':
      return 'Ō'
    elif l == 'ū':
      return 'Ū'
    elif l == 'ß':
      if default_mode.switch_capitalization_expand_sz:
        return 'SS'
      else:
        return 'ß'
    else:
      return string.upper(l)
  else:
    return l
    
def space(c=C_NONE):
  if default_mode.switch_layout_word_separation:
    return " "
  else:
    return ""

def fs():
  if default_mode.switch_punctuation_full_stop:
    return "."
  else:
    return ""
          
def para():
  if default_mode.switch_layout_paragraph_separation:
    return "\n"
  else:
    return space()          

def double_consonant(l):
  if default_mode.switch_simplification_double_consonants:
    return capitalize(l) 
  else:
    return capitalize(l+l)

def comma_sc():
  if default_mode.switch_punctuation_comma_sub_clause:
    return ","
  else:
    return ""

def colon():
  if default_mode.switch_punctuation_colon:
    return ":"
  else:
    return ""
  
def dot_abbr():
  if default_mode.switch_punctuation_dot_abbr:
    return "."
  else:
    return ""

def elongation(l, c, m):
  if default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_NONE:
    return l(c)
  elif default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_E or (default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_DEFAULT and m == ELONGATION_MODE_E):
    return l(c) + capitalize("e")
  elif default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_H or (default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_DEFAULT and m == ELONGATION_MODE_H):
    return l(c) + capitalize("h")
  elif default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_MACRON or (default_mode.segmented_control_harmonization_elongation == ELONGATION_MODE_DEFAULT and m == ELONGATION_MODE_MACRON):
    if (l == a):
      return capitalize("ā")
    elif (l == e):
      return capitalize("ė")
    elif (l == i):
      return capitalize("ī")
    elif (l == o):
      return capitalize("ō")
    elif (l == u):
      return capitalize("ū")
    else:
      return l(c) + l()
      
  else: 
    return l(c) + l()

# ōūāī

def a(c=C_NONE):
  return capitalize("a", c)

def aa(c=C_NONE):
  return elongation(a, c, ELONGATION_MODE_DOUBLE)

def ah(c=C_NONE):
  return elongation(a, c, ELONGATION_MODE_H)

def au(c=C_NONE):
  return capitalize("a", c) + capitalize("u")

def auml(c=C_NONE):
  if default_mode.switch_simplification_expand_umlaut:
    return capitalize("a", c) + capitalize("e")
  else:
    return capitalize("ä", c)
  
def aumlu(c=C_NONE):
  if default_mode.switch_simplification_aumlu_oi:
    return o(c) + i()
  else:
    return capitalize("ä", c) + u()
  
def b(c=C_NONE):
  return capitalize("b", c)

def bb():
  return double_consonant("b")
      
def c(c=C_NONE, m=C_K):
  if default_mode.switch_simplification_c_kz:
    if m == C_K:
      return k(c)
    elif m == C_S:
      return s(c)
    elif m == C_TSCH:
      return tsch(c)
    else:
      return z(c)
  else:
    return capitalize("c", c)

def ch(c=C_NONE, m=0):
  if default_mode.switch_simplification_ch_sch and m == CH_GREEK:
    return sch(c)
  elif default_mode.switch_simplification_ch_ck and m == CH_CK:
    return capitalize("c", c) + k()
  elif default_mode.switch_simplification_ch_k and m == CH_K:
    return k(c)
  else:
    return capitalize("c", c) + capitalize("h")

def ck(c=C_NONE):
  if default_mode.switch_simplification_ck_kk:
    return double_consonant("k")
  else:
    return capitalize("c", c) + k()

def d(c=C_NONE, m=VOICEFULL):
  if default_mode.switch_simplification_d_t and m == VOICELESS:
    return t(c)
  else:
    return capitalize("d", c)

def e(c=C_NONE, m=0):
  if default_mode.switch_harmonization_homophony_elongated_vowels and (m == ACTUALLY_ELONGATED):
    return eh(c)
  else:
    return capitalize("e", c)

def eh(c=C_NONE):
  return elongation(e, c, ELONGATION_MODE_H)

def ei(c=C_NONE):
  if default_mode.switch_simplification_ei_ai:
    return a(c) + i()
  else:
    return e(c) + i()

def er(c=C_NONE, m=UNSTRESSED):
  if default_mode.switch_simplification_er_a and (m == UNSTRESSED):
    return a(c)
  else:
    return e(c)+r()

def eu(c=C_NONE):
  if default_mode.switch_simplification_eu_oi:
    return o(c) + i()
  else:
    return e(c) + u()

def f(c=C_NONE):
  return capitalize("f", c)

def ff():
  return double_consonant("f")

def g(c=C_NONE):
  return capitalize("g", c)

def h(c=C_NONE, m=0):
  if default_mode.switch_simplification_suppress_mute_h and m == MUTE:
    return ""
  else:
    return capitalize("h", c)

def i(c=C_NONE):
  return capitalize("i", c)
  
def ie(c=C_NONE):
  return elongation(i, c, ELONGATION_MODE_E)

def ih(c=C_NONE):
  return elongation(i, c, ELONGATION_MODE_H)

def j(c=C_NONE):
  return capitalize("j", c)
  
def k(c=C_NONE):
  return capitalize("k", c)

def l(c=C_NONE):
  return capitalize("l", c)
  
def ll():
  return double_consonant("l")
      
def m(c=C_NONE):
  return capitalize("m", c)
  
def mm():
  return double_consonant("m")
      
def n(c=C_NONE, m=0):
  if default_mode.switch_harmonization_homophony_terminating_consonants and (m == ACTUALLY_SHORT):
    return nn()
  else:
    return capitalize("n", c)
  
def nn():
  return double_consonant("n")
      
def o(c=C_NONE):
  return capitalize("o", c)
  
def ouml(c=C_NONE):
  if default_mode.switch_simplification_expand_umlaut:
    return capitalize("o", c) + capitalize("e")
  else:
    return capitalize("ö", c)

def oumlh(c=C_NONE):
  return elongation(ouml, c, ELONGATION_MODE_H)
  
def p(c=C_NONE):
  return capitalize("p", c)
  
def ph(c=C_NONE):
  if default_mode.switch_simplification_ph_f:
    return capitalize("f", c)
  else:
    return capitalize("p", c) + capitalize("h")

def qu(c=C_NONE):
  if default_mode.switch_simplification_qu_kw:
    return capitalize("k", c) + capitalize("w")
  else:
    return capitalize("q", c) + capitalize("u")
    

def r(c=C_NONE):
  return capitalize("r", c)

def s(c=C_NONE, m=0):
  if default_mode.switch_harmonization_homophony_terminating_consonants and (m == ACTUALLY_SHORT):
    return ss()
  else:
    return capitalize("s", c)

def sp(c=C_NONE):
  if default_mode.switch_simplification_sch_s:
    return capitalize("š", c) + p()
  else:
    return s(c) + p()

def ss(c=C_NONE):
  return double_consonant("s")
  
def sz(c=C_NONE, m=NEOW):
  if default_mode.switch_simplification_sz_ss or (m == EOW and not default_mode.switch_legacy_sz):
    return ss()
  else:
    return capitalize("ß", c)
      
def sch(c=C_NONE):
  if default_mode.switch_simplification_sch_s:
    return capitalize("š", c)
  else:
    return s(c) + capitalize("c") + capitalize("h")

def st(c=C_NONE):
  if default_mode.switch_simplification_sch_s:
    return capitalize("š", c) + t()
  else:
    return s(c) + t()

def t(c=C_NONE, m=0):
  if default_mode.switch_harmonization_homophony_terminating_consonants and (m == ACTUALLY_SHORT):
    return tt()
  else:
    return capitalize("t", c)

def tsch(c=C_NONE):
  if default_mode.switch_simplification_tsch_c:
    return capitalize("č", c)
  else:  
    return t(c) + sch()

def th(c=C_NONE):
  if default_mode.switch_simplification_th_t:
    return capitalize("t", c)
  else:
    return capitalize("t", c) + capitalize("h")

def tt():
  return double_consonant("t")
      
def u(c=C_NONE):
  return capitalize("u", c)
      
def uuml(c=C_NONE):
  if default_mode.switch_simplification_expand_umlaut:
    return u(c) + e()
  else:
    return capitalize("ü", c)
  
def uumlh(c=C_NONE):
  return elongation(uuml, c, ELONGATION_MODE_H)
  
def v(c=C_NONE, m=VOICELESS):
  if default_mode.switch_simplification_v_fw:
    if m == VOICELESS:
      return f(c)
    else:
      return w(c)
  else:
    return capitalize("v", c)
    
def w(c=C_NONE):
  return capitalize("w", c)
      
def x(c=C_NONE):
  if default_mode.switch_simplification_x_ks:
    return k(c) + s()
  else:
    return capitalize("x")
      

def y(c=C_NONE, m=Y_UE):
  if default_mode.switch_simplification_y_uej:
    if m == Y_UE:
      return uuml(c)
    elif m == Y_I:
      return i(c)
    else:
      return j(c)
  else:
    return capitalize("y", c)
        
def z(c=C_NONE):
  if default_mode.switch_simplification_z_ts:
    return t(c) + s()
  else:
    return capitalize("z", c)