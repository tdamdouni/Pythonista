# Unlimited Backgrounding

I'm trying to follow [this tutorial](http://yifan.lu/2013/12/17/unlimited-backgrounding-on-ios/) to enable unlimited backgrounding on an app, using the new `objc_util` (in the beta).  
Do you think it will work? Is the tutorial still relevant with the latest iOS versions?

The code looks pretty simple:

    
        @property (nonatomic, strong) AVPlayer *player;
    
    
        NSError *sessionError = nil;
    [[AVAudioSession sharedInstance] setCategory:AVAudioSessionCategoryPlayback withOptions:AVAudioSessionCategoryOptionMixWithOthers error:&sessionError];
    
    AVPlayerItem *item = [AVPlayerItem playerItemWithURL:[[NSBundle mainBundle] URLForResource:@"silence" withExtension:@"mp3"]];
    
    [self setPlayer:[[AVPlayer alloc] initWithPlayerItem:item]];
    
    // this makes sure our player keeps working after the silence ends
    [[self player] setActionAtItemEnd:AVPlayerActionAtItemEndNone];
    
    [[self player] play];
    

I'm not able to fully implement it due to my lack of knowledges. In particular I'm not able to access a class' constant using `objc_util`.


__ ** [omz](/user/omz) ** [admin](/groups/administrators) 


You don't really need `objc_util` for this, it should work with the `sound` module as well.

    
        import sound
    import os
    import urllib
    
    # download a silent mp3 if it's not there yet:
    if not os.path.exists('silence.mp3'):
      urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
    player = sound.Player('silence.mp3')
    player.number_of_loops = -1 # repeat forever
    player.play()
    
    # do background stuff...
    
    # when you're done:
    player.stop()
    


__ ** [Obelisk](/user/obelisk) *

Background music play.

__ ** [jan4843](/user/jan4843) **

Thank you, **omz**! The code works for me. What does `sound.Player.number_of_loops = -1` mean? Is the sound played continuously? Does it consume CPU in background?

Also, I tried this:

    
        from sound import Player
    
    player = Player('')
    player.number_of_loops = -1
    player.play()
    

and it still works, even with files that doesn't exist.

* * *

Sorry, **Obelisk**, but I don't understand your comment. The idea is to play a silent sound to keep scripts running in the background, forever.

__ ** [Obelisk](/user/obelisk) **

Its a good idea，what background stuff to do normally？If use loop？

Other questions：how to play mp3 after turning off screen？why couldnt i put mp3 in a not current folder to play？

__ ** [jan4843](/user/jan4843) **

**Obelisk**, if you use a simple loop, iOS will stop it after 3 minutes because background activities have restrictions. It would also stop when iOS free up the RAM “killing” Pythonista.

__ ** [Obelisk](/user/obelisk) **

Theres a few apps with playing music that wont be stopped by ios in 3 minutes, i dont know why, do u mean iOS free up the RAM automatically?

__ ** [jan4843](/user/jan4843) **

That's the point, if an app is playing audio it doesn't get “killed”. If you try to run an endless script and meanwhile run some heavy games iOS will “kill” Pythonista and so your script to free up the RAM.  
The cool part is that the solution provided by **omz** does not interfere at all with playing audio in the system.

Meanwhile I got my hands back to my Mac and wrote the script I couldn't figure out:

    
        from objc_util import *
    from time import sleep
    from datetime import datetime
    
    # "Imports"
    AVAudioSession = ObjCClass('AVAudioSession')
    AVPlayer = ObjCClass('AVPlayer')
    AVPlayerItem = ObjCClass('AVPlayerItem')
    NSURL = ObjCClass('NSURL')
    
    # Set Pythonista app to play non-blocking, 'mixed with others' sounds
    audio_session = AVAudioSession.sharedInstance()
    audio_session.setCategory_withOptions_error_('AVAudioSessionCategoryPlayback', 1, None)
    
    # Create the item to play
    sound = NSURL.fileURLWithPath_('silence.mp3')
    item = AVPlayerItem.playerItemWithURL_(sound)
    
    # Play the sound (only once)
    player = AVPlayer.alloc().initWithPlayerItem_(item)
    player.setActionAtItemEnd_(2)
    player.play()
    
    while True:
        print 'Still running', datetime.now()
        sleep(1)
    

It does seem to work, as the **omz**’ solution, but I don't know if there is efficiency differences.

__ ** [hyshai](/user/hyshai) **

Hmmm I tested this by making a clipboard manager - Pythonista seems to still be killed after a couple of minutes.

EDIT: adding a `time.sleep(1)` seems to help....

    
        # coding: utf-8
    
    import sound
    import os
    import urllib
    import clipboard
    import time
    
    # download a silent mp3 if it's not there yet:
    if not os.path.exists('silence.mp3'):
      urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
    player = sound.Player('silence.mp3')
    player.number_of_loops = -1 # repeat forever
    player.play()
    
    # do background stuff...
    current = clipboard.get()
    print current
    while True:
        if current != clipboard.get():
                current = clipboard.get()
                print current
        #EDIT: this seems to help
        time.sleep(1)
    
    # when you're done:
    player.stop()
    
    

__ ** [smath](/user/smath) **

I'm working on a script that takes a long time to run, and I'd like to make an action menu item to allow running any script in the background, but the following isn't working:

    
        # coding: utf-8
    
    import editor
    import notification
    import sound
    import os
    import urllib
    
    # download a silent mp3 if it's not there yet:
    if not os.path.exists('silence.mp3'):
    urllib.urlretrieve('http://www.xamuel.com/blank-mp3-files/1sec.mp3', 'silence.mp3')
    player = sound.Player('silence.mp3')
    player.number_of_loops = -1 # repeat forever
    player.play()
    
    # run the currently open file. I know execfile isnt ideal, but the other option I found is os.system, which didn't work, I think because it uses subprocessing.'
    execfile(editor.get_path())
    
    # notify the user when the script is done.
    notification.schedule('Your script is done running', delay=0)
    
    

Thoughts?

__ ** [omz](/user/omz) ** [admin](/groups/administrators)

How exactly is it not working?

__ ** [smath](/user/smath) **

Pythonista is still killed after a couple minutes of running in the background.

__ ** [omz](/user/omz) ** [admin](/groups/administrators)

Maybe try doing a bit less work in your script, e.g. add some `time.sleep()` calls – this seems to have helped for [@hyshai](https://forum.omz-software.com/user/hyshai) (see post above), though I'm not exactly sure why. It could be that the system kills background processes that consume too much resources, even if they're playing audio.

