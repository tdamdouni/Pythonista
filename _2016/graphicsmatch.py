import random

total = 100
run = True

graphics = ['T','TT','TTT','TTTT','TTTTT','TTTTTT']

while run == True:
	print('CURRENT TOTAL POINTS: ' + str(total))
	input('PRESS RETURN TO PLAY!:')
	graphic1 = random.choice(graphics)
	graphic2 = random.choice(graphics)
	graphic3 = random.choice(graphics)
	print()
	print(graphic1,graphic2,graphic3)

	if graphic1 == graphic2 == graphic3:
		print('JACKPOT--75 POINTS')
		total = total + 75
		
	elif (graphic1 == 'TT' or graphic1 == 'TTTT' or graphic1 == 'TTTTTT' ) and (graphic1 == graphic2):
		print('Bonus--40 POINTS')
		total = total + 40
	
	elif (graphic1 == 'T' or graphic1 == 'TTT' or graphic1 == 'TTTTT' ) and (graphic1 == graphic2):
		print('WIN 10 POINTS')
		total = total + 10
		
	elif graphic1 == graphic3:
		print('WIN 10 POINTS')
		total = total + 10

	else:
		print('LOSE 10 POINTS')
		total = total - 10

	print()
