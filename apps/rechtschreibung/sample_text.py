import spelling_mode
import rulesets
import sentences

reload(spelling_mode)
reload(rulesets)
reload(sentences)

from sentences import *
from rulesets import *

def get_sample_text():
  return sentence001() + space() + sentence002() + space()+ sentence003() + space()+ sentence004() + space()+ sentence005() + para() + sentence006() + space() + sentence007() + space() + sentence008() + space() + sentence009() + space() + sentence010() + space() + sentence011() + space() + para() + sentence012() + space() + sentence013() + space() + sentence014() + space() + sentence015() + space() + sentence016() + space() + sentence017() + space() + sentence018() + space() + sentence019() + space() + sentence020() + space() + sentence021() + para() + para() + sentence1() + sentence2() + sentence3() + para() + sentence4() + para() + sentence5() 
  
def test():
  rulesets.set_default_mode(rulesets.spelling_mode().combination)
  sample_text = get_sample_text()
  print sample_text
  
  with open("doc/sample_text.txt", "w") as file:
    file.write(sample_text)
  
if __name__ == '__main__':
  test()