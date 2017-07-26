# https://twitter.com/keithohara/status/805548980750995457/photo/1

# SPELLINGB

c = {'n'}
h = c | set('ceiprx')
{w for w in [d.strip() for d in open("/usr/share/dict/words")] if len(w) > 4 and c < set(w) <= h} 
