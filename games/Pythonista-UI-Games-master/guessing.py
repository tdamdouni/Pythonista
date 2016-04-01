import random
import ui

global rounds, player_wins, computer_wins

MINIMUM, MAXIMUM = (0, 1000)
player_wins = 0
computer_wins = 0
rounds = 0

def perform_guessing(number):
		player_guess = int(v['player_guess'].text)
		computer_guess = random.randint(MINIMUM, MAXIMUM)
		v['comp_guess'].text = str(computer_guess)
		v['the_number'].text = str(number)
		player_score = abs(player_guess - number)
		computer_score = abs(computer_guess - number)
		return player_score < computer_score
		
def guess(sender):
		v['label3'].text = 'The number was'
		global rounds, player_wins, computer_wins
		rounds += 1
		if perform_guessing(random.randint(MINIMUM, MAXIMUM)):
					player_wins += 1
					v['outcome'].text = 'Player Wins!'
					v['outcome'].text_color = 0.00, 0.50, 0.00
		else:
					computer_wins += 1
					v['outcome'].text = 'Computer Wins!'
					v['outcome'].text_color = 1.00, 0.00, 0.00
		v['comp_wins'].text = str(computer_wins)
		v['player_wins'].text = str(player_wins)

v = ui.load_view('guessing')
v['textview1'].text = str('Welcome to the guessing game! A number will be randomly chosen from %i to %i. The player will make a guess, and then the computer will guess. Whoever is closest wins that round!') % (MINIMUM, MAXIMUM)		
v.present('sheet')			
