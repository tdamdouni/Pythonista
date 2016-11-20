# coding: utf-8

# https://forum.omz-software.com/topic/2512/no-sound-when-i-run-a-script-at-all

import sound

sound.set_honors_silent_switch(False)
sound.set_volume(1)
sound.play_effect('piano:D3')