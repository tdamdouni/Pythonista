import sound

class SoundManager(object):
    def __init__(self, name = ''):
        self._playing = dict()

    def load_effect(self, name):
        sound.load_effect(name)

    def play_effect(self, name, volume=0.5, pitch=1.0):
        sound_id = sound.play_effect(name, volume, pitch)
        self._playing[sound_id] = 1
        return sound_id

    def stop_effect(self, sound_id):
        sound.stop_effect(sound_id)
        del self._playing[sound_id]

    def set_volume(self, vol):
        sound.set_volume(vol)

    def stop_all_effects(self):
        for sound_id in self._playing:
            sound.stop_effect(sound_id)
        self._playing.clear()
