# https://gist.github.com/anonymous/9a2cb564eaac2df3a71d

from time import time, sleep
from sound import play_effect
#from random import randint

# Drums array is set up like this:
# [[Drum_timer, drum_start, 'drum_sound'], [drum2_timer, etc..]]
# It increases drum_start each frame, and if drum_start==drum_timer
# then it plays the noise and resets drum_start

def play_beat(beat_speed=.1, loops=100,
              drums=[[3,0,'Drums_03'],
                     [5,0,'Drums_05'],
                     [7,0,'Drums_07'],
                     [8,0,'Drums_08']]):

	for loop in range(loops): #Repeats beat for every loop
		sleep(beat_speed) #pauses the program based on beat_speed
		for drum in drums:
			drum[1]+=1 #increase drum_start
			if drum[1]>=drum[0]: #if drum_start >= drum_timer
				drum[1]=0 #reset drum_start
				play_effect(drum[2]) #play sound
				
				
#BEGIN EXAMPLES

#Metronome.
play_beat(loops=32,drums=[[4,0,'Drums_01']])

#3/3 timing.  No wonder it sounds strange...
sleep(1)
play_beat(loops=243, beat_speed=.08,
          drums=[[3,0,'Drums_09'], #hihat
                 [9,3,'Drums_01'], #bass
                 [9,4.5,'Drums_01'], #bass
                 [9,0,'Drums_14'], #ride
                 [27,6,'Drums_14'], #tom
                 [27,3,'Drums_14'], #tom
                 #[9,3,'Drums_10'], #tom
                 #[9,6,'Drums_10'], #tom
                 [27,7.5,'Drums_01'], #bass
                 [27,0,'Drums_02'], #snare wood
                 [27,3,'Drums_11'], #crash
                 [81,72,'Drums_01'], #bass
                 [81,15,'Drums_01'], #bass
                 [81,12,'Drums_01'], #bass
                 [81,9,'Drums_01'], #bass
                 [81,6,'Drums_10'], #tom
                 [81,5.5,'Drums_10'], #tom
                 [81,5,'Drums_10'], #tom
                 [81,4,'Drums_08'], #tom
                 [81,3.5,'Drums_08'], #tom
                 [81,3,'Drums_08'], #tom
                 [81,2,'Drums_06'], #tom
                 [81,1.5,'Drums_06'], #tom
                 [81,1,'Drums_06'], #tom
                 [81,0,'Drums_13']]) #crash loud


#This beat uses a confusing timing that merges 2 and 3.
#I don't even know what to call this timing...
sleep(1)
play_beat(beat_speed=0.2, loops=144,
          drums=[[2,0,'Drums_09'], #hihat
                 [3,1,'Drums_09'], #hihat
                 [6,0,'Drums_02'], #snare wood
                 [6,2,'Drums_01'], #bass
                 [8,0,'Drums_01'], #bass
                 [8,4,'Drums_01'], #bass
                 [8,7,'Drums_01'], #bass
                 [9,6,'Drums_08'], #tom
                 [12,0,'Drums_14'], #ride
                 [16,6,'Drums_14'], #ride
                 [16,9,'Drums_14'], #ride
                 [16,12,'Drums_14'], #ride
                 [16,15,'Drums_14'], #ride
                 [18,0,'Drums_01'], #bass
                 [18,4,'Drums_01'], #bass
                 [18,8,'Drums_01'], #bass
                 [18,8,'Drums_10'], #tom
                 [48,0,'Drums_06'], #tom
                 [48,2,'Drums_08'], #tom
                 [48,4,'Drums_10'], #tom
                 [48,0,'Drums_06'], #tom
                 [48,1,'Drums_08'], #tom
                 [48,3,'Drums_10'], #tom
                 [48,5,'Drums_10'], #tom
                 [48,4,'Drums_14'], #ride
                 [48,6,'Drums_14'], #ride
                 [48,7,'Drums_11'], #crash
                 ])

#4/4 timing.  Basic
sleep(1)
play_beat(loops=48,
          drums=[[3,0,'Drums_09'], #hihat
                 [6,0,'Drums_01'], #bass
                 [12,1.5,'Drums_02'], #snare wood
                 [12,3,'Drums_11']]) #crash


'''sleep(1)
rand=randint(1,10)
for i in range(10):
        play_beat(beat_speed=0.1, loops=1,
                drums=[[rand,randint(0,rand),'Drums_01'], #random
                     [rand,randint(0,rand),'Drums_0'+str(randint(1,9))], #random
                     [rand,randint(0,rand),'Drums_0'+str(randint(1,9))], #random
                   [rand*2,randint(0,rand*2),'Drums_1'+str(randint(0,6))], #random
                         [rand*4,randint(0,rand*4),'Drums_1'+str(randint(0,6))], #random
                         [rand*4,randint(0,rand*4),'Drums_1'+str(randint(0,6))], #random
                       ])'''

#Jungle beat.  Just mixed up a bunch of different timings.
sleep(1)
play_beat(loops=200,
          drums=[[2,0,'Drums_09'], #hihat
                 [3,0,'Drums_09'], #hihat
                 [4,0,'Drums_09'], #hihat
                 [5,0,'Drums_09'], #hihat
                 [6,0,'Drums_01'], #base
                 [7,0,'Drums_06'], #tom
                 [8,0,'Drums_08'], #tom
                 [9,0,'Drums_10'], #tom
                 [10.5,0,'Drums_10'], #tom
                 [12,1.5,'Drums_02'], #snare wood
                 [48,0,'Drums_15'], #crash loud - begins and ends this beat
                 ])

#4/8
sleep(1)
play_beat(beat_speed=.05, loops=288,
          drums=[[6,3,'Drums_09'], #hi hats
                 [9,3,'Drums_09'], #hi hats
                 [18,0,'Drums_11'], #crash
                 [36,0,'Drums_01'], #bass
                 [36,15,'Drums_01'], #bass
                 [72,3,'Drums_01'],
                 [72,12,'Drums_02'], #snare wood
                 [72,6,'Drums_02'], #snare wood
                 [144,12,'Drums_01'], #bass
                 [144,18,'Drums_01'], #bass
                 [144,7,'Drums_01'], #bass
                 [144,4,'Drums_01'],
                 [144,5,'Drums_01'],
                 [144,6,'Drums_01'],
                 [288,7,'Drums_14'], #ride
                 [288,8,'Drums_14'], #ride
                 [288,9,'Drums_14'], #ride
                 [288,0,'Drums_16'], #ride loud
                 [144,10,'Drums_01'], #bass
                 #[432,2,'Drums_01'], #bass
                 [144,0,'Drums_02'], #snare wood
                 [144,139,'Drums_02'], #snare wood
                 [144,136,'Drums_02'], #snare wood
                 [144,8,'Drums_14'], #ride
                 [144,7,'Drums_16'], #ride loud
                 [288,1,'Drums_01'], #bass
                 [288,2,'Drums_01'], #bass
                 [288,11,'Drums_01'], #bass
                 [288,5,'Drums_02'], #snare wood
                 [288,10,'Drums_02'], #snare wood
                 [288,15,'Drums_02'], #snare wood
                 [288,0,'Drums_15'], #crash loud
                 ])#[36,16,'Drums_10']])


#Simple 4/8 timing
sleep(1)
play_beat(loops=64,
          drums=[[2,2,'Drums_09'],
                 [8,5,'Drums_09'],
                 [8,7,'Drums_09'],
                 [32,2,'Drums_03'],
                 [64,5,'Drums_08'],
                 [64,6,'Drums_06'],
                 [64,4,'Drums_10'],
                 [8,4,'Drums_03'],
                 [8,8,'Drums_01'], #bass
                 [8,4,'Drums_01'], #bass
                 [16,0,'Drums_11']])

