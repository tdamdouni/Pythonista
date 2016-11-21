import random
import ui
	
def get_score(sender):
	global home_score, away_score
	home_score = random.randint(0, 15)
	away_score = random.randint(0, 15)
	v['home_score'].text = str(home_score)
	v['opponents_score'].text = str(away_score)
	update_label()

def update_label():
	v['outcome'].font = ('DINCondensed-Bold', 25)
	if home_score == away_score: 
		v['outcome'].text = "It's A Tie!"
		v['outcome'].text_color = 'black'
	elif home_score > away_score:
		v['outcome'].text = 'Home Wins!'
		v['outcome'].text_color = '#1D76C8'
	else:
		v['outcome'].text = 'Away Wins!'
		v['outcome'].text_color = '#DB1F1F'

v = ui.load_view('scores')
v.present('sheet')
