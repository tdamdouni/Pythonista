# Vector Animations With Python

_Captured: 2016-02-29 at 11:05 from [zulko.github.io](http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/)_

I am a big fan of [Dave Whyte](https://dribbble.com/beesandbombs)'s vector animations, like this one:

![](https://d13yacurqjgara.cloudfront.net/users/583436/screenshots/1692659/spiral.gif)

It was generated using a special animation language called [Processing](http://www.processing.org/) (here is [Dave's code](https://dribbble.com/shots/1692659-Shell-Spiral/attachments/268926)). While it seems powerful, Processing it is not very elegant in my opinion ; this post shows how to do similar animations using two Python libraries, [Gizeh](https://github.com/Zulko/gizeh) (for the graphics) and [MoviePy](http://zulko.github.io/moviepy) (for the animations).

## Gizeh and Moviepy

Gizeh is a Python library I wrote on top of `cairocffi` ( a binding of the popular Cairo library) to make it more intuitive. To make a picture with Gizeh you create a _surface_, draw on it, and export it:
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    
    
    
    import gizeh
    surface = gizeh.Surface(width=320, height=260) # dimensions in pixel
    circle = gizeh.circle (r=40, # radius, in pixels
                           xy= [156, 200], # coordinates of the center
                           fill= (1,0,0)) # 'red' in RGB coordinates
    circle.draw( surface ) # draw the circle on the surface
    surface.get_npimage() # export as a numpy array (we will use that)
    surface.write_to_png("my_drawing.png") # export as a PNG
    

We obtain this magnificent Japanese flag:

![](http://zulko.github.io/images/vector_animations/my_drawing.png)

To make an animation with MoviePy, you write a function `make_frame` which, given some time `t`, returns the video frame at time `t`:
    
    
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
    
    
    
    from moviepy.editor import VideoClip
    def make_frame(t):
        """ returns a numpy array of the frame at time t """
        # ... here make a frame_for_time_t
        return frame_for_time_t
    clip = VideoClip(make_frame, duration=3) # 3-second clip
    clip.write_videofile("my_animation.mp4", fps=24) # export as video
    clip.write_gif("my_animation.gif", fps=24) # export as GIF
    

## Example 1

We start with an easy one. In `make_frame` we just draw a red circle, whose radius depends on the time `t`:
    
    
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
    
    
    
    import gizeh
    import moviepy.editor as mpy
    W,H = 128,128 # width, height, in pixels
    duration = 2 # duration of the clip, in seconds
    def make_frame(t):
        surface = gizeh.Surface(W,H)
        radius = W*(1+ (t*(duration-t))**2 )/6
        circle = gizeh.circle(radius, xy = (W/2,H/2), fill=(1,0,0))
        circle.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_gif("circle.gif",fps=15, opt="OptimizePlus", fuzz=10)
    

## Example 2

Now there are more circles, and we start to see the interest of making animations programmatically using `for` loops. The useful function `polar2cart` transforms polar coordinates (radius, angle) into cartesian coordinates (x,y).
    
    
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
    
    
    
    import numpy as np
    import gizeh
    import moviepy.editor as mpy
    W,H = 128,128
    duration = 2
    ncircles = 20 # Number of circles
    def make_frame(t):
        surface = gizeh.Surface(W,H)
        for i in range(ncircles):
            angle = 2*np.pi*(1.0*i/ncircles+t/duration)
            center = W*( 0.5+ gizeh.polar2cart(0.1,angle))
            circle = gizeh.circle(r= W*(1.0-1.0*i/ncircles),
                                  xy= center, fill= (i%2,i%2,i%2))
            circle.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=duration)
    clip.write_gif("circles.gif",fps=15, opt="OptimizePlus", fuzz=10)
    

## Example 3

Here we fill the circles with a slightly excentred radial gradient to give and impression of volume. The colors, initial positions and centers of rotations of the circles are chosen randomly at the beginning.
    
    
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
    
    
    
    import gizeh as gz
    import numpy as np
    import moviepy.editor as mpy
    W = H = 150
    D = 2 # duration
    nballs=60
    # generate random values of radius, color, center
    radii = np.random.randint(.1*W,.2*W, nballs)
    colors = np.random.rand(nballs,3)
    centers = np.random.randint(0,W, (nballs,2))
    def make_frame(t):
        surface = gz.Surface(W,H)
        for r,color, center in zip(radii, colors, centers):
            angle = 2*np.pi*(t/D*np.sign(color[0]-.5)+color[1])
            xy = center+gz.polar2cart(W/5,angle) # center of the ball
            gradient = gz.ColorGradient(type="radial",
                         stops_colors = [(0,color),(1,color/10)],
                         xy1=[0.3,-0.3], xy2=[0,0], xy3 = [0,1.4])
            ball = gz.circle(r=1, fill=gradient).scale(r).translate(xy)
            ball.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("balls.gif",fps=15,opt="OptimizePlus")
    

## Example 4

The shadow is done using a circle with radial fading black gradient whose intensity diminishes when the ball is higher, for more realism (?). The shadow is then squeezed vertically using `scale(r,r/2)`, so that its width is twice its height.
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 200,75
    D = 3
    r = 10 # radius of the ball
    DJ, HJ = 50, 35 # distance and height of the jumps
    ground = 0.75*H # y-coordinate of the ground
    gradient = gz.ColorGradient(type="radial",
                    stops_colors = [(0,(1,0,0)),(1,(0.1,0,0))],
                    xy1=[0.3,-0.3], xy2=[0,0], xy3 = [0,1.4])
    def make_frame(t):
        surface = gz.Surface(W,H, bg_color=(1,1,1))
        x = (-W/3)+(5*W/3)*(t/D)
        y = ground - HJ*4*(x % DJ)*(DJ-(x % DJ))/DJ**2
        coef = (HJ-y)/HJ
        shadow_gradient = gz.ColorGradient(type="radial",
                    stops_colors = [(0,(0,0,0,.2-coef/5)),(1,(0,0,0,0))],
                    xy1=[0,0], xy2=[0,0], xy3 = [0,1.4])
        shadow = (gz.circle(r=(1-coef/4), fill=shadow_gradient)
                   .scale(r,r/2).translate((x,ground+r/2)))
        shadow.draw(surface)
        ball = gz.circle(r=1, fill=gradient).scale(r).translate((x,y))
        ball.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("bouncingball.gif",fps=25, opt="OptimizePlus")
    

## Example 5

![](http://i.imgur.com/6rx7SUz.gif)

This is a derivative of the Dave Whyte animation shown in the introduction. It is made of stacked circles moving towards the picture's border, with carefully chosen sizes, starting times, and colors (I say _carefully chosen_ because it took me a few dozens random tries). The black around the picture is simply a big circle with no fill and a very very thick black border.
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 256, 256
    DURATION = 2.0
    NDISKS_PER_CYCLE = 8
    SPEED = .05
    def make_frame(t):
        dt = 1.0*DURATION/2/NDISKS_PER_CYCLE # delay between disks
        N = int(NDISKS_PER_CYCLE/SPEED) # total number of disks
        t0 = 1.0/SPEED # indicates at which avancement to start
        surface = gz.Surface(W,H)
        for i in range(1,N):
            a = (np.pi/NDISKS_PER_CYCLE)*(N-i-1)
            r = np.maximum(0, .05*(t+t0-dt*(N-i-1)))
            center = W*(0.5+ gz.polar2cart(r,a))
            color = 3*((1.0*i/NDISKS_PER_CYCLE) % 1.0,)
            circle = gz.circle(r=0.3*W, xy = center,fill = color,
                                  stroke_width=0.01*W)
            circle.draw(surface)
        contour1 = gz.circle(r=.65*W,xy=[W/2,W/2], stroke_width=.5*W)
        contour2 = gz.circle(r=.42*W,xy=[W/2,W/2], stroke_width=.02*W,
                                stroke=(1,1,1))
        contour1.draw(surface)
        contour2.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=DURATION)
    clip.write_gif("shutter.gif",fps=20, opt="OptimizePlus", fuzz=10)
    

## Example 6

You can draw more than circles ! And you can group different elements so that they will move together (here, a letter and a pentagon).
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 300, 75
    D = 2 # duration in seconds
    r = 22 # size of the letters / pentagons
    gradient= gz.ColorGradient("linear",((0,(0,.5,1)),(1,(0,1,1))),
                               xy1=(0,-r), xy2=(0,r))
    polygon = gz.regular_polygon(r, 5, stroke_width=3, fill=gradient)
    def make_frame(t):
        surface = gz.Surface(W,H, bg_color=(1,1,1))
        for i, letter in enumerate("GIZEH"):
            angle = max(0,min(1,2*t/D-1.0*i/5))*2*np.pi
            txt = gz.text(letter, "Amiri", 3*r/2, fontweight='bold')
            group = (gz.Group([polygon, txt])
                     .rotate(angle)
                     .translate((W*(i+1)/6,H/2)))
            group.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("gizeh.gif",fps=20, opt="OptimizePlus")
    

## Example 7

![](http://i.imgur.com/dfJ2Skz.gif)

We start with just a triangle. By rotating this triangle three time we obtain four triangles which fit nicely into a square. Then we copy this square following a checkerboard pattern. Finally we do the same with another color to fill the missing tiles. Now, if the original triangle is rotated, all the triangles on the picture will also be rotated.
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 200,200
    WSQ = W/4 # width of one 'square'
    D = 2 # duration
    a = np.pi/8 # small angle in one triangle
    points = [(0,0),(1,0),(1-np.cos(a)**2,np.sin(2*a)/2),(0,0)]
    def make_frame(t):
        surface = gz.Surface(W,H)
        for k, (c1,c2) in enumerate([[(.7,0.05,0.05),(1,0.5,0.5)],
                                    [(0.05,0.05,.7),(0.5,0.5,1)]]):
            grad = gz.ColorGradient("linear",xy1=(0,0), xy2 = (1,0),
                                   stops_colors= [(0,c1),(1,c2)])
            r = min(np.pi/2,max(0,np.pi*(t-D/3)/D))
            triangle = gz.polyline(points,xy=(-0.5,0.5), fill=grad,
                            angle=r, stroke=(1,1,1), stroke_width=.02)
            square = gz.Group([triangle.rotate(i*np.pi/2)
                                  for i in range(4)])
            squares = (gz.Group([square.translate((2*i+j+k,j))
                                for i in range(-3,4)
                                for j in range(-3,4)])
                       .scale(WSQ)
                       .translate((W/2-WSQ*t/D,H/2)))
            squares.draw(surface)
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame=make_frame).set_duration(D)
    clip.write_gif("blueradsquares.gif",fps=15, fuzz=30)
    

## Example 8

![](http://i.imgur.com/79tTac9.gif)

A nice thing to do with vector graphics is fractals. We first build a ying-yang, then we use this ying-yang as the dots of a bigger ying-yang, and we use the bigger ying-yang as the dots of an even bigger ying yang etc. In the end we go one level deep into the imbricated ying-yangs, and we start zooming.
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 256,256
    R=1.0*W/3
    D = 4
    yingyang = gz.Group( [
          gz.arc(R,0,np.pi, fill=(0,0,0)),
          gz.arc(R,-np.pi,0, fill=(1,1,1)),
          gz.circle(R/2,xy=(-R/2,0), fill=(0,0,0)),
          gz.circle(R/2,xy=(R/2,0), fill=(1,1,1))])
    fractal = yingyang
    for i in range(5):
        fractal = gz.Group([yingyang,
                    fractal.rotate(np.pi).scale(0.25).translate([R/2,0]),
                    fractal.scale(0.25).translate([-R/2,0]),
                    gz.circle(0.26*R, xy=(-R/2,0),
                        stroke=(1,1,1), stroke_width=1),
                    gz.circle(0.26*R, xy=(R/2,0),
                        stroke=(0,0,0), stroke_width=1)])
    # Go one level deep into the fractal
    fractal = fractal.translate([(R/2),0]).scale(4)
    def make_frame(t):
        surface = gz.Surface(W,H)
        G = 2**(2*(t/D)) # zoom coefficient
        (fractal.translate([R*2*(1-1.0/G)/3,0]).scale(G) # zoom
         .translate(W/2+gz.polar2cart(W/12,2*np.pi*t/D)) # spiral effect
         .draw(surface))
        return surface.get_npimage()
    clip = mpy.VideoClip(make_frame, duration=D)
    clip.write_gif("yingyang.gif",fps=15, fuzz=30, opt="OptimizePlus")
    

## Example 9

![](http://i.imgur.com/JanwSIf.gif)

That one is inspired by this [Dave Whyte animation](http://33.media.tumblr.com/ff988433be4970277349b0b57ae0abc6/tumblr_nb1fzsolQd1r2geqjo1_500.gif). We draw white-filled circles, each of these being almost completely transparent so that they only add 1 to the value of the pixels that they cover. Pixels with an even value, which are the pixels covered by an even number of circles, are then painted white, while the others will be black. To complexify and have a nicely-looping animation, we draw two circles in each direction, one being a time-shifted version of the other.
    
    
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
    
    
    
    import numpy as np
    import gizeh as gz
    import moviepy.editor as mpy
    W,H = 400,400
    D = 5 # duration, in seconds
    ncircles = 10
    def make_frame(t):
        surface = gz.Surface(W,H)
        for angle in np.linspace(0,2*np.pi,ncircles+1)[:-1]:
            center = np.array([W/2,H/2]) + gz.polar2cart(.2*W,angle)
            for i in [0,1]: # two circles belongin to two groups
                circle = gz.circle(W*.45*(i+t/D),xy=center,
                                      fill=(1,1,1,1.0/255))
                circle.draw(surface)
        return 255*((surface.get_npimage()+1) % 2)
    clip = mpy.VideoClip(make_frame, duration=D).resize(.5)
    clip.write_gif("rose.gif",fps=15, fuzz=30, opt="OptimizePlus")
    

## Example 10

![](http://i.imgur.com/2YdW9yf.gif)

A pentagon made of rotating squares ! Interestingly, making the squares rotate the other direction creates a very different-looking [animation](http://i.imgur.com/C8IKy28.gif). The squares are placed according to [this polar equation](http://math.stackexchange.com/a/41954/43338).

The difficulty in this animation is that the last square drawn will necessarily be on top of all the others, and not, as it should be, below the first square ! The solution is to draw each frame twice. The first time, we draw the squares starting from the right, so that the faulty square will also be on the right, and we only keep the left part of that picture. The second time we start drawing the squares from the left, so that the faulty square is on the left, and we keep the right part. By assembling the two valid parts we reconstitute a valid picture.
    
    
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
    
    
    
    import numpy as np
    import moviepy.editor as mpy
    import colorsys
    import gizeh as gz
    W,H = 256,256
    NFACES, R, NSQUARES, DURATION = 5, 0.3,  100, 2
    def half(t, side="left"):
        points = gz.geometry.polar_polygon(NFACES, R, NSQUARES)
        ipoint = 0 if side=="left" else NSQUARES/2
        points = (points[ipoint:]+points[:ipoint])[::-1]
        surface = gz.Surface(W,H)
        for (r, th, d) in points:
            center = W*(0.5+gz.polar2cart(r,th))
            angle = -(6*np.pi*d + t*np.pi/DURATION)
            color= colorsys.hls_to_rgb((2*d+t/DURATION)%1,.5,.5)
            square = gz.square(l=0.17*W, xy= center, angle=angle,
                       fill=color, stroke_width= 0.005*W, stroke=(1,1,1))
            square.draw(surface)
        im = surface.get_npimage()
        return (im[:,:W/2] if (side=="left") else im[:,W/2:])
    def make_frame(t):
        return np.hstack([half(t,"left"),half(t,"right")])
    clip = mpy.VideoClip(make_frame, duration=DURATION)
    clip.write_gif("pentagon.gif",fps=15, opt="OptimizePlus")
    

## Mixing videos and vector graphics

A nice advantage of combining Gizeh with MoviePy is that you can read actual video files (or gifs) and use the frames to fill shapes drawn with Gizeh.

We will use this [video](https://www.youtube.com/watch?v=t4gjl-uwUHc) from the Blender Foundation (it's under a Creative Common licence). Since you have read until there I'll show you a little unrelated trick: at _4:32_ the rabbit is jumping rope, so there is a potential for a well-looping GIF. We open the video around _4:32_, and let MoviePy automatically decide where to cut to have the best-looping GIF possible:
    
    
    1
    2
    3
    4
    5
    6
    
    
    
    from moviepy.editor import VideoFileClip
    import moviepy.video.tools.cuts as cuts
    clip = mpy.VideoFileClip("bunny.mp4").resize(0.2).subclip((4,32),(4,33))
    t_loop = cuts.find_video_period(clip) # gives t=0.56
    clip.subclip(0,t_loop).write_gif('jumping_bunny.gif')
    

![](http://i.imgur.com/MVp4TSx.gif)

Now we can feed the frames of this GIF to Gizeh, using MoviePy's `clip.fl(some_filter)`, which means _"I want a new clip made by transforming the frames of the current clip with some_filter"_.
    
    
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
    
    
    
    import moviepy.editor as mpy
    import numpy as np
    import gizeh as gz
    clip = mpy.VideoFileClip("jumping_bunny.gif")
    (w, h), d = clip.size, clip.duration
    center=  np.array([w/2, h/2])
    def my_filter(get_frame, t):
        """ Transforms a frame (given by get_frame(t)) into a different
        frame, using vector graphics."""
        surface = gz.Surface(w,h)
        fill = (gz.ImagePattern(get_frame(t), pixel_zero=center)
                .scale(1.5, center=center))
        for (nfaces,angle,f) in ([3, 0, 1.0/6],
                                  [5, np.pi/3, 3.0/6],
                                  [7, 2*np.pi/3, 5.0/6]):
            xy = (f*w, h*(.5+ .05*np.sin(2*np.pi*(t/d+f))))
            shape = gz.regular_polygon(w/6,nfaces, xy = xy,
                    fill=fill.rotate(angle, center))
            shape.draw(surface)
        return surface.get_npimage()
    clip.fl(my_filter).write_gif("jumping_bunny_shapes.gif")
    

![](http://i.imgur.com/ltArnnc.gif)

Finally, this function adds a zoom on some part of the video.
    
    
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
    
    
    
    import gizeh as gz
    import moviepy.editor as mpy
    import numpy as np
    def add_zoom(clip, target_center, zoom_center, zoom_radius, zoomx):
        w, h = clip.size
        def fl(im):
            """ transforms the image by adding a zoom """
            surface = gz.Surface.from_image(im)
            fill = gz.ImagePattern(im, pixel_zero=target_center,
                                   filter='best')
            line = gz.polyline([target_center, zoom_center],
                               stroke_width=3)
            circle_target= gz.circle(zoom_radius, xy=target_center,
                                     fill=fill, stroke_width=2)
            circle_zoom = gz.circle(zoom_radius, xy=zoom_center, fill=fill,
                           stroke_width=2).scale(zoomx, center=zoom_center)
            for e in line, circle_zoom, circle_target:
                e.draw(surface)
            return surface.get_npimage()
        return clip.fl_image(fl)
    clip = mpy.VideoFileClip("jumping_bunny.gif")
    w, h = clip.size
    clip_with_zoom = clip.fx(add_zoom, target_center = [w/2, h/3], zoomx=3,
                       zoom_center = [5*w/6, h/4], zoom_radius=15)
    clip_with_zoom.write_gif("jumping_bunnyt_zoom.gif")
    

![](http://i.imgur.com/VAvDKRN.gif)

## Your turn now !

I hope I have convinced you that Python is a nice language for making vector animations. If you give it a try, let me know of any difficulty you may meet installing or using MoviePy and Gizeh. And any feedback, improvement ideas, commits, etc. are also very appreciated.
