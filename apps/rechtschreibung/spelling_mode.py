# coding: utf-8
# This file is part of https://github.com/marcus67/rechtschreibung

# usage modes
VOWEL=1
CONS=2
MUTE=3
VOICEFULL=4
VOICELESS=5
EOW=6 # end of word
NEOW=7 # not end of word
C_K=8
C_Z=9
C_S=10
C_TSCH=11
Y_I=12
Y_J=13
Y_UE=14
CH_GREEK=15
CH_CK=16
CH_K=17
ACTUALLY_SHORT=18
ACTUALLY_ELONGATED=19
UNSTRESSED=20

ELONGATION_MODE_DEFAULT=0
ELONGATION_MODE_NONE=1
ELONGATION_MODE_E=2
ELONGATION_MODE_H=3
ELONGATION_MODE_DOUBLE=4
ELONGATION_MODE_MACRON=5

SZ_MODE_DEFAULT = 0
SZ_MODE_OLD_SPELLING = 1
SZ_MODE_NEW_SPELLING = 2
SZ_MODE_EXPAND = 3

# capitilization modes
C_NONE=0
C_NOUN=1
C_NAME=2
C_BOS=4 # beginning of sentence
C_ADDRESSING=8
C_BOS_AC=16 # beginning of sentence after colon

class SpellingModeCombinationControl(object):
  
  def __init__(self):

    self.name = u'[unbenannt]'
    self.comment = ''
    self.isImmutable = False
    self.isReference = False

class SpellingModeCombination(object):

  def __init__(self):
        
    # customization mode switches
    self.bitswitch_capitalization = C_NOUN | C_NAME | C_BOS | C_ADDRESSING | C_BOS_AC
    self.switch_capitalization_all_capital = False
    self.switch_capitalization_expand_sz = True
    self.switch_simplification_double_consonants = False
    self.switch_simplification_c_kz = False
    self.switch_simplification_ch_sch = False
    self.switch_simplification_ch_k = False
    self.switch_simplification_ck_kk = False
    self.switch_simplification_th_t = False
    self.switch_simplification_ph_f = False
    self.switch_simplification_qu_kw = False
    self.switch_simplification_v_fw = False
    self.switch_simplification_x_ks = False
    self.switch_simplification_y_uej = False
    self.switch_simplification_z_ts = False
    self.switch_simplification_sz_ss = False
    self.switch_simplification_tsch_c = False
    self.switch_simplification_sch_s = False
    self.switch_simplification_eu_oi = False
    self.switch_simplification_ei_ai = False
    self.switch_simplification_aumlu_oi = False
    self.switch_simplification_ch_ck = False    
    self.switch_simplification_expand_umlaut = False
    self.switch_simplification_suppress_mute_h = False
    self.switch_simplification_d_t = False
    self.switch_simplification_er_a = False
    self.switch_layout_word_separation = True
    self.switch_layout_paragraph_separation = True
    self.switch_punctuation_full_stop = True
    self.switch_punctuation_dot_abbr = True # Punkt bei Abkürzungen
    self.switch_punctuation_comma_sub_clause = True
    self.switch_punctuation_colon = True
    self.switch_legacy_sz = False
    self.segmented_control_harmonization_elongation = ELONGATION_MODE_DEFAULT
    self.switch_harmonization_homophony_terminating_consonants = False
    self.switch_harmonization_homophony_elongated_vowels = False

  def __eq__(self, other):
    
    return self.__dict__ == other.__dict__
    
        
class spelling_mode(object):
  
  def __init__(self):
    
    self.combination = SpellingModeCombination()
    self.control = SpellingModeCombinationControl()
    
  def __eq__(self, other):
    """
    :type other: spelling_mode
    """
    return self.combination == other.combination  
    
def compare_spelling_mode_combination_controls(mode1, mode2):
  """
  :type mode1: spelling_mode
  :type mode2: spelling_mode
  """
  return cmp(mode1.control.name.lower(), mode2.control.name.lower())
  
def test():
  
  mode = spelling_mode()
        
if __name__ == '__main__':
  test()
  