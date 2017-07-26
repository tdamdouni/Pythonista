# https://forum.omz-software.com/topic/3862/speech-sound-module-q-s

import speech, sound, time
rec = sound.Recorder("audio.m4a")
rec.record()
time.sleep(3)
rec.stop()
result = speech.recognize("audio.m4a")
print(result)
