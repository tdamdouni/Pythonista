#coding: utf-8
import difflib
import string

DIFF_INSERT = u'i'
DIFF_DELETE = u'd'
DIFF_CHANGE = u'c'
DIFF_NONE = u' '

def compute_bit_value(state, old_value, state_bit):
  if state != bool(old_value & state_bit):
    return old_value ^ state_bit
  else:
    return old_value
          
def set_container_value(container, name, value):
  if getattr(container, name, None) != None:
    setattr(container, name, value)
  else:
    print "ERROR: name '%s' not found in container '%s'" % (name, type(container).__name__)
    
def get_change_control_strings(oldString, newString):

    enhancedString = unicode( oldString )
    controlString = unicode( " " * len(enhancedString) )
    
    for i,s in enumerate(difflib.ndiff(unicode(oldString), unicode(newString))):
      if s[0]==' ': 
        continue
        
      elif s[0]=='-':
        controlString = controlString[0:i] + DIFF_DELETE + controlString[i+1:]
        
      elif s[0]=='+':
        enhancedString = enhancedString[0:i] + unicode( s[-1] ) + enhancedString[i:]
        controlString = controlString[0:i] + DIFF_INSERT + controlString[i:]

    return ( enhancedString, controlString )    
  
  
def get_multi_token_change_control_strings(oldString, newString):
  
  oldTokens = string.split(oldString, ' ')
  newTokens = string.split(newString, ' ')
  if len(oldTokens) == len(newTokens):
    enhancedString = ''
    controlString = ''
    i = 0
    for oldToken in oldTokens:
      enhancedToken, tokenControlString = get_change_control_strings(oldToken,newTokens[i])
      if len(enhancedString) > 0:
        enhancedString = enhancedString + ' '
        controlString = controlString + ' '  
      enhancedString = enhancedString + enhancedToken
      controlString = controlString + tokenControlString
      i = i + 1
    return (enhancedString, controlString)
  else:  
    return get_change_control_strings(oldString, newString)  
  
def get_html_content(oldString, newString, show_changes):
  
  if oldString and show_changes:
    
    enhancedNewString, controlString = get_multi_token_change_control_strings(oldString, newString)
    
    newString = u''
    i = 0
    
    for c in controlString:
      #print i, c
      if c == DIFF_NONE:
        newString = newString + enhancedNewString[i]
      elif c == DIFF_INSERT:
        newString = newString + '<span id=''ins''>' + enhancedNewString[i] + '</span>'
      elif c == DIFF_DELETE:
        newString = newString + '<span id=''del''>' + enhancedNewString[i] + '</span>'
      i = i + 1
  
  # do some final replacements:
  # -) replace the surrogate characters used for those not found on the Apple keyboard by their HTML codes
  # -) replace the double quote character '"' bei &quot; so that the resultsing string can be used in JS.
  return newString.replace("\n","<BR/>").replace("ė","&#275;").replace("Ė","&#274;").replace('"','&quot;')
    
  
def add_missing_attributes(object, template):
  
  changes = 0
  for attr in template.__dict__:
    if not attr in object.__dict__:
      setattr(object, attr, getattr(template, attr))
      changes = changes + 1
  return changes
  
def test():
  print get_html_content("Zwei šBären","Eine Bäršin", True)
  
if __name__ == '__main__':
  test()