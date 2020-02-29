from __future__ import print_function
# Makes Velveeta Cheesy Skillets
# Ready in about 20 minutes


# VARIABLES
#--------------------------------------------------
skillet_heat = 100
meat = (1,'lb.','ground beef')
water = (2,'cups','water')
pasta = ' pasta '
seasoning = ' seasoning '
cheese = 'VELVEETA'
skillet = [] #An array is a variable that contains other variables 
meal = None #Not yet at least ;)
#--------------------------------------------------


# FUNCTIONS
#--------------------------------------------------
# BROWN
#--------------------------------------------------
# Cooks/browns the meat and returns it
def brown(mt):
	# Inform the user
	print('Browning...' + str(mt))
	# Returns drained meat
	def drain(mt):
		return 'Drainined...' + str(mt)
	return drain(meat)

# Brown the meat
skillet.append(brown(meat))
print(skillet)
#--------------------------------------------------


# ADD
#--------------------------------------------------
# Returns stirred, boiled water,pasta, and seasoning at a reduced heat
def add(w,p,s):
	# Python string formatting to inform the user
	print('Adding {} {} {}'.format(w,p,s) + 'to skillet')
	
	# Returns stirred,water,pasta and seasoning
	def stir(w,p,s):
		return 'stiring ' + str(w) + p + s
	
	# Returns boiled stuff (the ingredients we add)
	def boil(stuff):
		return 'boiling ' + stuff
	
	# Reduces skillet_heat to 20
	def reduce():
		# Inform the user
		print('Reducing heat...')
		global skillet_heat
		# As long as skillet_heat is less than 20(degrees), decrement the heat
		while skillet_heat > 20:
			skillet_heat = skillet_heat - 1
	reduce()
	
	# Gets the global skillet_heat variable
	global skillet_heat
	
	# Inform the user
	print(('reduced heat to',skillet_heat))

	return boil(stir(w,p,s))

# Add to the skillet
skillet.append(add(water,pasta,seasoning))
#--------------------------------------------------


# COVER
#--------------------------------------------------
# Covers and simmers the skillet and removes it from the heat. 
def cover(sk):
	print('Covering skillet...')
	
	# Simmers a skillet for an amount of time(t)
	def simmer(sk,t):
		# Elapsed time(dt) is initially 0
		dt=0
		# As long as the elapsed time is less than 12(minutes) inform the user
		while dt<=t:
			print(str(dt)+' simmering... '+str(sk))
			# Don't forget to increment the time or else it will burn!
			dt+=1
	# Simmer away!
	simmer(skillet,12)
	
	# Removes the skillet from the heat
	def remove():
		# Inform the user
		print('Removing skillet...')
	remove()

# Cover the skillet
cover(skillet)
#--------------------------------------------------


# STIR
#--------------------------------------------------
def stir(ch):
	print('Stirring in cheese...')
	return ch

# Stir in cheese
skillet.append(stir(cheese))
#--------------------------------------------------


# SERVE
#--------------------------------------------------
def serve(m):
	print('Your meal is ...' + str(m) + ' ENJOY!')

meal = skillet

print() # just printing a new line

# Serve the meal
serve(meal)
#--------------------------------------------------


# CUSTOMIZE IT!
# Top with chopped fresh tomatoes and shredded lettuce before serving...

print()

# Nutrition Facts
nutri_facts={
'servings_per_container':5,
'calories':(230,380),
'calories_from_fat':(80,160),
'total_fat':(9,14,26),
'saturated_fat':(2,10,25),
'trans_fat':0,
'cholesterol':(10,3,23),
'sodium':(910,38,40),
'total_carb':(27,9,9),
'diet_fiber':(1,4,4),
'sugars':7,
'protein':8,
'VitaminA':(2,2),
'VitaminC':(0,0),
'Calcium':(15,15),
'Iron':(6,15),
}

# Package Ingredients
cheese_sauce_ingredients = []
seasoning_ingredients = []
ingredients = [cheese_sauce_ingredients,seasoning_ingredients]

for fact in nutri_facts:
	print(fact,str(nutri_facts[fact]))
	
#kraftfoods.com
#1-800-847-1997

