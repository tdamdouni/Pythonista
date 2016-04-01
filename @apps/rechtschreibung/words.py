import rulesets
import spelling_mode

reload(rulesets)
reload(spelling_mode)

from rulesets import *
from spelling_mode import *

def abbrechen(c=0):
  return a(c)+bb()+r()+e()+ch()+e()+n()

def aus(c=0):
  return au(c)+s()
  
def bei(c=0):
  return b(c)+ei()

def casimir(c=0):
  return rulesets.c(c=C_NAME|c)+a()+s()+i()+m()+i()+r()

def dass(c=0):
  return d(c)+a()+sz(m=EOW)
  
def das(c=0):
  return d(c)+a()+s(m=ACTUALLY_SHORT)

def dem(c=0):
  return d(c)+e(m=ACTUALLY_ELONGATED)+m()

def den(c=0):
  return d(c)+e(m=ACTUALLY_ELONGATED)+n()
  
def der(c=0):
  return d(c)+e()+r()
  
def die(c=0):
  return d(c)+ie()

def ein(c=0):
  return ei(c) + n()
  
def end(c=0):
  return e(c)+n()+d(m=VOICELESS)

def fuer(c=0):
  return f()+uuml()+r()
  
def ist(c=0):
  return i(c)+s()+t()
  
def hat(c=0):
  return h(c)+a()+t()
  
def man(c=0):
  return m(c)+a()+n(m=ACTUALLY_SHORT)
    
def mit(c=0):
  return m(c)+i()+t(m=ACTUALLY_SHORT)
    
def schlieszen(c):
  return sch(c)+l()+ie()+sz()+e()+n()
  
def sich(c=0):
  return s(c)+i()+ch()
  
def sie(c=0):
  return s(c)+ie()
  
def sind(c=0):
  return s(c)+i()+n()+d(m=VOICELESS)
  
def speichern(c=0):
  return sp(c)+ei()+ch()+e()+r()+n()

def ueberschreiben(c=0):
  return uuml(c)+b()+er()+sch()+r()+ei()+b()+e()+n()
  
def und(c=0):
  return u(c)+n()+d(m=VOICELESS)
  
def viel(c=0):
  return v(c, m=VOICELESS)+ie()+l()
  
def von(c=0):
  return v(c, m=VOICELESS)+o()+n()
  
def wie(c=0):
  return w(c)+ie()
  
def wendy(c=0):
  return w(c=C_NAME|c)+e()+n()+d()+y(m=Y_I)
  
def test():
  rulesets.set_default_mode(rulesets.spelling_mode())
  print casimir()+das()+der()+die()+ist()+sind()+und()+wendy()
  
if __name__ == '__main__':
  test()

  

