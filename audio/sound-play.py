# https://forum.omz-software.com/topic/3641/sound-effect-not-stopping

import sound, time
y = "room_One.mp3"
x = sound.play_effect(y)
#sound.play_effect(y)  # <- This call can be removed
time.sleep(5)
sound.stop_effect(x)

