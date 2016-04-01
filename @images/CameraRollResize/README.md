camera_roll_resize
==================

Pythonista-script to modify resolution, mode and quality of a camera roll picture and save a copy


Example:
========

Picture-Information: resolution = 1936 x 2592 (5.0 MP), mode = RGBA

!!! Changing the resolution is time-consuming !!! Resolution higher 6000 x 4000 (24MP) can cause a abend!

0 = Auto processing (Resolution = 1936 x 2592, quality = 95%, mode = RGBA)<br />
1 = Same resolution (1936 x 2592)<br />
2 = Define resolution<br />
3 = 3MP (2048 x 1536)<br />
5 = 5MP (2592 x 1936)<br />
Resolution: 2

Changing the ratio causes picture deformation!<br />
Width: 800<br />
Height: 600

Quality (0 - 100): 90

0 = no change (RGBA)<br />
1 = black/white<br />
2 = grey<br />
3 = RGB no transparency<br />
4 = RGB with transparency<br />
5 = CMYK<br />
6 = YCbCr<br />
7 = 32bit Pixel<br />
Mode: 0

Picture is in process ...<br />
Completed!<br />
Resolution = 800 x 600, quality = 90%, mode = RGBA
