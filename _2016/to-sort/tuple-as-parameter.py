# https://forum.omz-software.com/topic/3369/share-code-defensive-tuple-param-idea

def accept_a_tuple(tp):
	try:
		for v in tp:
			print(v)
	except:
		print('this fails')
		
def accept_a_tuple_better(tp):
	# headache saver when passing a single value tuple without a comma
	if not isinstance(tp, tuple):
		tp = (tp,)
	for v in tp:
		print(v)
		
		
accept_a_tuple((20,))           # is ok, we remember the comma
accept_a_tuple((10))            # this fails, is not a tuple
accept_a_tuple_better((10))     # i think this is a better way
# --------------------
def mega_accept_a_tuple(tp):
	try:
		print(tuple(tp))
	except TypeError:
		print(tuple((tp,)))
# --------------------

