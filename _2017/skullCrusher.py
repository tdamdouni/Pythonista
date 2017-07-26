# https://github.com/bjucha81/SkullCrusher/blob/master/skullCrusher.py

import random, ui, time, sys, sound



counter = 0
timme = 30



def GetRandom(sender): # Working


	global counter
	counter = counter + 1
	x = random.randint(10,680)
	y = random.randint(15,900)
	B1.frame = (x,y,95,50)
	L1.text = str((counter))
	
	z = random.randint(0,10)
	if z == 5: # Ghost appears
		main_view.add_subview(B3)
		a = random.randint(10,680)
		b = random.randint(15,900)
		main_view.add_subview(L5)
		main_view.background_color = '#d2629c'
		ui.delay(Ghosttime,1) # duration before Ghosttime is loaded
		
	elif z == 4: # Evil Pig appears
	
		main_view.add_subview(B5)
		q = random.randint(10,680)
		w = random.randint(15,900)
		main_view.add_subview(L6)
		main_view.background_color = '#ccd246'
		ui.delay(PiggyTime,1)
		
		
def Ghosttime(): # Working

	main_view.remove_subview(B3)
	main_view.remove_subview(L5)
	main_view.background_color = '56b0d2'
	
	
@ui.in_background
def Tdown(sender2): # Working
	main_view.remove_subview(Skull)
	main_view.remove_subview(BGhost)
	main_view.remove_subview(Bpig)
	main_view.remove_subview(HowTo)
	main_view.remove_subview(HowTo2)
	main_view.remove_subview(HowTo3)
	
	main_view.add_subview(B1)
	main_view.remove_subview(B2)
	main_view.remove_subview(Intro)
	global  timme
	while timme >= 0:
		L2.text = str(timme)
		timme = timme -1
		time.sleep(1)
		if L2.text <= '10':
			L2.text_color = 'red'
			L2.font = ('Helvetica',24)
			
	if L2.text <= '0':
		End()
		
		
def End(): # Working
	global timme, counter
	sound.play_effect('arcade:Powerup_1', 0.25, 0.8)
	timme = 30
	L2.text_color = 'black'
	L2.font = ('Helvetica',18)
	L2.text = str(timme)
	
	main_view.remove_subview(B1)
	main_view.add_subview(Utro)
	Utro.text = ( 'Game over, you got: ' + str(counter) + ' points')
	Utro.alignment = 1
	main_view.add_subview(B4)
	counter = 0
	
	
def Ghost(sender3): # Working
	global timme
	timme = timme + 5
	sound.play_effect('game:Ding_3', 0.25, 0.8)
	main_view.remove_subview(B3)
	main_view.remove_subview(L5)
	
	
@ui.in_background
def Retest(sender8): # Working

	main_view.add_subview(B1)
	main_view.remove_subview(Utro)
	main_view.remove_subview(B4)
	global  timme
	while timme >= 0:
		L2.text = str(timme)
		timme = timme -1
		time.sleep(1)
		if L2.text <= '10':
			L2.text_color = 'red'
			L2.font = ('Helvetica',24)
			
	if L2.text == '0':
		End()
		
		
def Piggy(sender9): # Working
	global timme
	timme = timme - 5
	sound.play_effect('game:Error', 0.25, 0.8)
	main_view.remove_subview(B5)
	main_view.remove_subview(L6)
	
def PiggyTime(): # Working
	main_view.remove_subview(B5)
	main_view.background_color = '56b0d2'
	main_view.remove_subview(L6)
	
main_view = ui.View(name = 'SkullCrusher!!!')
main_view.present(title_bar_color = 'grey')
main_view.background_color = '#56b0d2'
main_view.flex = 'WHBRL'

x = random.randint(10,680)
y = random.randint(15,900)

a = random.randint(10,680)
b = random.randint(15,900)

q = random.randint(10,680)
w = random.randint(15,900)

counter = 0
B1 = ui.Button()
B1.image = ui.Image.named('emj:Skull').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
B1.frame = (x,y,95,50)
B1.action = GetRandom


B2 = ui.Button(title = 'Ready to play?')
B2.border_width = 1
B2.corner_radius=15
B2.tint_color = 'black'
B2.frame = (295,390,190,50)
B2.background_color = '#975db0'
B2.action = Tdown

B3 = ui.Button(frame = (a,b,40,40))
B3.image =   ui.Image.named('emj:Ghost').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
B3.tint_color = 'white'
B3.action = Ghost

B4 = ui.Button (title = 'Play again?')
B4.frame = (295,390,190,50)
B4.action = Retest
B4.background_color = '#975db0'
B4.corner_radius = 15
B4.tint_color = 'black'

B5 = ui.Button(frame = (q,w,80,80))
B5.image =   ui.Image.named('emj:Pig_Face').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
B5.tint_color = 'white'
B5.action = Piggy

L1 = ui.Label(text = '0')
L1.frame = (-10,-15,50,50)
L1.alignment = 1

L2 = ui.Label(text = '30')
L2.frame = (730,-15,50,50)
L2.alignment = 1

L3 = ui.Label(text = 'Points')
L3.frame = (30,0,50,20)

L4 = ui.Label(text = 'Time:')
L4.frame = (700,0,45,20)

L5 = ui.Label(text = 'Ghost Time!!!')
L5.frame = (290,0,230,30)
L5.text_color = 'white'
L5.font = ('Helvetica',32)

L6 = ui.Label(text = 'Evil Piggy appears!')
L6.frame = (280,0,290,35)
L6.text_color = 'white'
L6.font = ('Helvetica',32)

Intro = ui.Label(text = 'The object of the game is to hit the Skull as many times possible before time runs out, Sometimes the TimeGhost will appear, if you hit him you will get +5 seconds. But look out for the evil Piggy, he will steal time from you')
Intro.frame = (287,440,210,200)
Intro.number_of_lines = 0
Intro.background_color = '#ffbb71'
Intro.alignment = 1

Utro = ui.Label()
Utro.frame = (260,450,250,50)
Utro.background_color = '#479dd4'
Utro.algnment = 1

Skull = ui.Button(image =   ui.Image.named('emj:Skull').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL),frame = (240,180,50,50))
BGhost = ui.Button(image =   ui.Image.named('emj:Ghost').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL),frame = (240,240,50,50))
Bpig = ui.Button(image =   ui.Image.named('emj:Pig_Face').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL),frame = (240,300,150,50))
HowTo = ui.Label(text = 'Hit him to get points',background_color = '#ffbb71', frame = (300,200,220,50) )
HowTo2 = ui.Label(text = 'Hit him to get +5 sec',background_color = '#ffbb71', frame = (300,250,220,50) )
HowTo3 = ui.Label(text = 'Hit him and you lose 5 sec',background_color = '#ffbb71', frame = (300,300,220,50) )

main_view.add_subview(L1)
main_view.add_subview(L2)
main_view.add_subview(B2)
main_view.add_subview(L3)
main_view.add_subview(L4)
main_view.add_subview(Skull)
main_view.add_subview(BGhost)
main_view.add_subview(Bpig)
main_view.add_subview(HowTo2)
main_view.add_subview(HowTo3)
main_view.add_subview(HowTo)
main_view.add_subview(Intro)

