# Making GIFs From Video Files With Python

_Captured: 2015-09-25 at 18:07 from [zulko.github.io](http://zulko.github.io/blog/2014/01/23/making-animated-gifs-from-video-files-with-python/)_

_Sometimes producing a good animated GIF requires a few advanced tweaks, for which scripting can help. So I added a GIF export feature to MoviePy, a Python package originally written for video editing._

For this demo we will make a few GIFs out of this trailer:

You can download it with this command if you have [Youtube-dl](http://rg3.github.io/youtube-dl/) installed:
    
    
    1
    
    
    
    youtube-dl 2Jw-AeaU5WI -o frozen_trailer.mp4

## Converting a video excerpt into a GIF

In what follows we import [MoviePy](http://zulko.github.io/moviepy/), we open the video file, we select the part between 1'22.65 (1 minute 22.65 seconds) and 1'23.2, reduce its size (to 30% of the original) and save it as a GIF:
    
    
    1
    2
    3
    4
    5
    6
    
    
    
    from moviepy.editor import *
    clip = (VideoFileClip("frozen_trailer.mp4")
            .subclip((1,22.65),(1,23.2))
            .resize(0.3))
    clip.write_gif("use_your_head.gif")
    

![](http://i.imgur.com/F1oOtnP.gif)

> _'Use Your Head - Hosted by imgur'_

## Cropping the image

For my next GIF I will only keep the center of the screen. If you intend to use MoviePy, note that you can preview a clip with `clip.preview()`. During the preview clicking on a pixel will print its position, which is convenient for cropping with precision.
    
    
    1
    2
    3
    4
    5
    
    
    
    kris_sven = (VideoFileClip("frozen_trailer.mp4")
                 .subclip((1,13.4),(1,13.9))
                 .resize(0.5)
                 .crop(x1=145,x2=400)) # remove left-right borders
    kris_sven.write_gif("kris_sven.gif")
    

![](http://i.imgur.com/CFFYEpd.gif)

> _'Kris and Sven - Hosted by imgur'_

## Freezing a region

Many GIF makers like to _freeze_ some parts of the GIF to reduce the file size and/or focus the attention on one part of the animation.

In the next GIF we freeze the left part of the clip. To do so we take a snapshot of the clip at t=0.2 seconds, we crop this snapshot to only keep the left half, then we make a composite clip which superimposes the cropped snapshot on the original clip:
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    
    
    
    anna_olaf = (VideoFileClip("frozen_trailer.mp4")
                 .subclip(87.9,88.1)
                 .speedx(0.5) # Play at half speed
                 .resize(.4))
    snapshot = (anna_olaf
                .crop(x2= anna_olaf.w/2) # remove right half
                .to_ImageClip(0.2) # snapshot of the clip at t=0.2s
                .set_duration(anna_olaf.duration))
    composition = CompositeVideoClip([anna_olaf, snapshot])
    composition.write_gif('anna_olaf.gif', fps=15)
    

![](http://i.imgur.com/Fc9Qc5f.gif)

> _'Anna and Olaf - Hosted by imgur'_

## Freezing a more complicated region

This time we will apply a custom mask to the snapshot to specify where it will be transparent (and let the animated part appear) .

![](http://zulko.github.io/images/gifs/mask.jpeg)

> _'That's what a mask is for.'_
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    
    
    
    import moviepy.video.tools.drawing as dw
    anna_kris = (VideoFileClip("frozen_trailer.mp4", audio=False)
                 .subclip((1,38.15),(1,38.5))
                 .resize(.5))
    # coordinates p1,p2 define the edges of the mask
    mask = dw.color_split(anna_kris.size, p1=(445, 20), p2=(345, 275),
                          grad_width=5) # blur the mask's edges
    snapshot = (anna_kris.to_ImageClip()
                .set_duration(anna_kris.duration)
                .set_mask(ImageClip(mask, ismask=True))
    composition = CompositeVideoClip([anna_kris,snapshot]).speedx(0.2)
    # 'fuzz' (0-100) below is for gif compression
    composition.write_gif('anna_kris.gif', fps=15, fuzz=3)
    

![](http://i.imgur.com/SBHkNqt.gif)

> _'Anna and Olaf - Hosted by imgur'_

## Time-symetrization

Surely you have noticed that in the previous GIFs, the end did not always look like the beginning. As a consequence, you could see a disruption every time the animation was restarted. A way to avoid this is to time-symetrize the clip, i.e. to make the clip play once forwards, then once backwards. This way the _end_ of the clip really _is_ the beginning of the clip. This creates a GIF that can loop fluidly, without a real beginning or end.
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    
    
    
    def time_symetrize(clip):
        """ Returns the clip played forwards then backwards. In case
        you are wondering, vfx (short for Video FX) is loaded by
        >>> from moviepy.editor import * """
        return concatenate([clip, clip.fx( vfx.time_mirror )])
    clip = (VideoFileClip("frozen_trailer.mp4", audio=False)
            .subclip(36.5,36.9)
            .resize(0.5)
            .crop(x1=189, x2=433)
            .fx( time_symetrize ))
    clip.write_gif('sven.gif', fps=15, fuzz=2)
    

![](http://i.imgur.com/fuqLsRG.gif)

> _'Sven - hosted on Imgur'_

Ok, this might be a bad example of time symetrization,it makes the snow flakes go upwards in the second half of the animation.

## Adding some text

In the next GIF there will be a text clip superimposed on the video clip.
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    
    
    
    olaf = (VideoFileClip("frozen_trailer.mp4", audio=False)
            .subclip((1,21.6),(1,22.1))
            .resize(.5)
            .speedx(0.5)
            .fx( time_symetrize ))
    # Many options are available for the text (requires ImageMagick)
    text = (TextClip("In my nightmares\nI see rabbits.",
                     fontsize=30, color='white',
                     font='Amiri-Bold', interline=-25)
            .set_pos((20,190))
            .set_duration(olaf.duration))
    composition = CompositeVideoClip( [olaf, text] )
    composition.write_gif('olaf.gif', fps=10, fuzz=2)
    

![](http://i.imgur.com/ZQzgNo6.gif)

> _'Olaf - Hosted by imgur'_

## Making the gif loopable

The following GIF features a lot of snow falling. Therefore it cannot be made loopable using time-symetrization (or you will snow floating upwards !). So we will make this animation loopable by having the beginning of the animation appear progressively (_fade in_) just before the end of the clip. The montage here is a little complicated, I cannot explain it better than with this picture:

![](http://zulko.github.io/images/gifs/castle_loopable.jpeg)

> _'I hope it's clear !' 400_
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    
    
    
    castle = (VideoFileClip("frozen_trailer.mp4", audio=False)
              .subclip(22.8,23.2)
              .speedx(0.2)
              .resize(.4))
    d = castle.duration
    castle = castle.crossfadein(d/2)
    composition = (CompositeVideoClip([castle,
                                       castle.set_start(d/2),
                                       castle.set_start(d)])
                   .subclip(d/2, 3*d/2))
    composition.write_gif('castle.gif', fps=5,fuzz=5)
    

![](http://i.imgur.com/VnoRpdq.gif)

> _'Disney Castle - Hosted by Imgur'_

## Another example of a GIF made loopable

The next clip (from the movie _Charade_) was almost loopable: you can see Carry Grant smiling, then making a funny face, then coming back to normal. The problem is that at the end of the excerpt Cary is not exactly in the same position, and he is not smiling as he was at the beginning. To correct this, we take a snapshot of the first frame and we make it appear progressively at the end. This seems to do the trick.
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    
    
    
    carry = (VideoFileClip("charade.mp4", audio=False)
             .subclip((1,51,18.3),(1,51,20.6))
             .crop(x1=102, y1=2, x2=297, y2=202))
    d = carry.duration
    snapshot = (carry.to_ImageClip()
                .set_duration(d/6)
                .crossfadein(d/6)
                .set_start(5*d/6))
    composition = CompositeVideoClip([carry, snapshot])
    composition.write_gif('carry.gif', fps=carry.fps, fuzz=3)
    

![](http://i.imgur.com/k1sz49h.gif)

> _'Carry Grant in Charade - Hosted by Imgur'_

## Big finish: background removal

Let's dive further into the scripting madness: we consider this video around 2'16 (_edit: not the video I originally used, it was removed by the Youtube user, I add to find another link_):

And we will remove the background to make this gif (with transparent background):

![](http://i.imgur.com/Fo2BxBK.gif)

> _'PigsPolka - Hosted by imgur'_

The main difficulty was to find what the background of the scene is. To do so, the script gathers a few images in which the little pigs are are different positions (so that every part part of the background is visible on at least several (actually most) of the slides, then it takes the pixel-per-pixel median of these pictures, which gives the background.
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
    32
    33
    34
    35
    36
    37
    38
    39
    40
    41
    42
    43
    44
    45
    46
    47
    48
    49
    50
    51
    52
    53
    54
    55
    56
    57
    58
    59
    60
    61
    62
    63
    64
    
    
    
    # Requires Scikit Images installed
    import numpy as np
    import skimage.morphology as skm
    import skimage.filter as skf
    from moviepy.editor import *
    ### LOAD THE CLIP
    pigsPolka =  (VideoFileClip("pigs_in_a_polka.mp4"))
                  .subclip((2,16.85),(2,35))
                  .resize(.5)
                  .crop(x1=140, y1=41, x2=454, y2=314))
    ### COMPUTE THE BACKGROUND
    # There is no single frame showing the background only (there
    # is always a little pig in the screen) so we use the median of
    # several carefully chosen frames to reconstitute the background.
    # I must have spent half an hour to find the right set of frames.
    times = (list(np.linspace(2.3,4.2,30))+
             list(np.linspace(6.0,7.1,30))+
             8*[6.2])
    frames_bg = [pigsPolka.get_frame(t) for t in times]
    background = np.percentile(np.array(frames_bg), 50,axis=0)
    ### MASK GENERATION
    def make_mask_frame(t):
        """ Computes the mask for the frame at time t """
        # THRESHOLD THE PIXEL-TO-PIXEL DIFFERENCE
        # BETWEEN THE FRAME AND THE BACKGROUND
        im = pigsPolka.get_frame(t)
        mask = ((im-background)**2).sum(axis=2) > 1500
        # REMOVE SMALL OBJECTS
        mask = skm.remove_small_objects(mask)
        # REMOVE SMALL HOLES (BY DILATIATION/EROSION)
        selem=np.array([[1,1,1],[1,1,1],[1,1,1]])
        for i in range(2):
            mask = skm.binary_dilation(mask,selem)
        for i in range(2):
            mask = skm.binary_erosion(mask,selem)
        # BLUR THE MASK A LITTLE
        mask = skf.gaussian_filter(mask.astype(float),1.5)
        return mask
    mask = (VideoClip( make_mask_frame, ismask=True,
                       duration= pigsPolka.duration)
    ### LAST EFFECTS AND GIF GENERATION
    final = (pigsPolka.set_mask(mask)
             .subclip(12.95,15.9)
             .fx(vfx.blackwhite) # black & white effect !
    final.write_gif('pigs_polka.gif', fps=10, fuzz=10)
    
