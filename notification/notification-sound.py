# https://forum.omz-software.com/topic/2646/notification-sounds/5

import notification
notification.schedule('Test', delay=5, sound_name='Media/Sounds/drums/Drums_15')

# The same pattern ('Media/Sounds/<collection>/<name>') should work with any of the bundled sounds, not just the 'digital' and 'game' collections.
