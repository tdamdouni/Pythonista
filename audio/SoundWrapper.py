import sound as soundOrig

class soundWrapper(object):
    def __init__(self, name = ''):
        self._l = list()
        soundOrig.__init__(name)

    def load_effect(self, name):
        soundOrig.load_effect(name)

    def play_effect(self, name, volume = 0.5, pitch = 1.0):
        iId = soundOrig.play_effect(name, volume, pitch)
        self._l.append(iId)
        return iId

    def stop_effect(self, effect_id):
        soundOrig.stop_effect(effect_id)
        self._l.remove(effect_id)

    def set_volume(self, vol):
        soundOrig.set_volume(vol)

    def stop_all_effects(self):
        for id in self._l:
            soundOrig.stop_effect(id)
        self._l = list()

sound = soundWrapper()
sound.play_effect('Beep')
sound.play_effect('Beep')
sound.stop_all_effects()
