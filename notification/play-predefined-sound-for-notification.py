# http://stackoverflow.com/questions/39049011/how-come-pythonistas-notification-module-wont-honor-my-sound-choice

import notification
import sound

notification.schedule("Hello World!",5,'digital:PhaserUp7','http://apple.com')

sound.play_effect('digital:PhaserUp7')
