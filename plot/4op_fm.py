# coding: utf-8

# https://gist.github.com/SpotlightKid/50c28ddc99bb27c98446
#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""A four-operator FM script generating a 64 wave 128 samples per cycle wavetable.

Requires the numpy and matplotlib third-party modules.

Ported from:

http://www.waldorf-music.info/kunena-en/blofeld-en/280-wavetable-script-for-blofeld-4-operator-fm

"""
# Author: Øystein Olsen
# Python conversion: Christopher Arndt

# V1: Adapted from a 2 operator FM script
# V2: Speed increase
# V3: Added FM feedback for operator 3
# V4: Added 1 precomputed frame for FM feedback
# V5: Correction of time-scale vector. Changed wavetable plot for better
#     readability
# V6: Added envelopes for operator amplitude
# V7: Renamed operators to correspond with DX-100 algorithms. Added envelope
#     and ratio for operator1 (aka carrier from V1-6). Added DX-100 algorithms
# V8: Python version, unified first and subsequent loop iterations

# Algorithms:

# 1) 1<2<3<4
# 2) 1<2<(3+4)
# 3) 1<(2<3)+4
# 4) 1<(2+3<4)
# 5) (1<2)+(3<4)
# 6) (1<4)+(2<4)+(3<4)
# 7) (1+2+(3<4))
# 8) (1+2+3+4)
#
# <  =  serial FM-stack
# +  =  parallell FM-stack
#
# Note,  operator 4 is the feedback operator for all algorithms.

# r1-r4    = ratios of operator 1 to 4
# feedback = strength of FM feedback for operator 4
# fm_algo  = FM algorithm,  see table above. Same as the algorithms for the
#            DX-100
# op1x     = x-coordinate (frame#) for operator envelope (zero based)
#            (1st always 0, last always wavetable length - 1)
# op1y     = amplitude for operator envelope (0 .. +1.0)
# fmwave   = the resulting wavetable
#
# The number of stages in each envelope can be as many as you like (up to the
# length of the wavetable), as long as  each pair (op1x/op1y etc.) has the
# same number of elements.
# The same applies to opxc/opcy, op2x/op2y and op3x/op3y. So you can have
# a different number of stages for each envelope.

# Modification notes:
#
# For other wavetable lengths, set 'wt_len' at the start of the script.
# If wt_len can not by evenly divided by four, the plot will not show the
# last wt_len modulo 4 entries.
# For other samples per cycle lengths, set 'spc' at the start of the script.

from __future__ import division, print_function, unicode_literals

from math import sin

from numpy import interp, linspace, pi, zeros
from matplotlib import pyplot as plt

# number of entries in wavetable
wt_len = 64
# samples per cycle resp. wavetable entry
spc = 128

# frequency ratios
r1 = 1
r2 = 2
r3 = 3
r4 = 4

# operator routing
feedback = 2
fm_algo = 8

# envelopes
op1x = [0, 31, wt_len-1]
op1y = [1, 1, 1]

op2x = [0, 11, wt_len-1]
op2y = [0, 0.75, 2]

op3x = [0, 21, wt_len-1]
op3y = [0, 0.25, 1.75]

op4x = [0, wt_len-1]
op4y = [0, 1]

op1 = interp(range(wt_len), op1x, op1y)
op2 = interp(range(wt_len), op2x, op2y)
op3 = interp(range(wt_len), op3x, op3y)
op4 = interp(range(wt_len), op4x, op4y)

x = linspace(0, wt_len * 2 * pi, spc * wt_len)
fmwave = zeros(wt_len * spc)

t = zeros(spc)
for i in range(spc):
    t[i] = sin(r4 * x[i] + feedback * t[i-1] if i else 0)

fb = zeros(wt_len * spc)
for n in range(spc * wt_len):
    index = n // spc # integer division <=> floor for positive n
    fb[n] = sin((r4 if i else r3) * x[n] + feedback * (fb[n-1] if i else t[spc-1]))

    if fm_algo == 1:
        fmwave[n] = op1[index] * sin(r1 * x[n] + op2[index] * sin(r2 * x[n] +
            op3[index] * sin(r3 * x[n] + op4[index] * fb[n])))
    elif fm_algo == 2:
        fmwave[n] = op1[index] * sin(r1*x[n] + op2[index] *
            sin(r2 * x[n] + op3[index] * sin(r3 * x[n]) + op4[index] * fb[n]))
    elif fm_algo == 3:
        fmwave[n] = op1[index] * sin(r1 * x[n] + op2[index] *
            sin(r2 * x[n] + op3[index] * sin(r3 * x[n])) + op4[index] * fb[n])
    elif fm_algo == 4:
        fmwave[n] = op1[index] * sin(r1 * x[n] + op2[index] *
            sin(r2 * x[n]) + op3[index] * sin(r3 * x[n] + op4[index] * fb[n]))
    elif fm_algo == 5:
        fmwave[n] = (op1[index] *
            sin(r1 * x[n] + op2[index] * sin(r2 * x[n])) +
            op3[index] * sin(r3 * x[n] + op4[index] * fb[n]))
    elif fm_algo == 6:
        fmwave[n] = (op1[index] * sin(r1* x[n] + op4[index] * fb[n]) +
            op2[index] * sin(r2 * x[n] + op4[index] * fb[n]) +
            op3[index] * sin(r3 * x[n] + op4[index] * fb[n]))
    elif fm_algo == 7:
        fmwave[n] = (op1[index] * sin(r1 * x[n]) + op2[index] *
            sin(r2 * x[n]) + op3[index] * sin(r3 * x[n] + op4[index] * fb[n]))
    elif fm_algo == 8:
        fmwave[n] = (op1[index] * sin(r1 * x[n]) +
            op2[index] * sin(r2 * x[n]) +
            op3[index] * sin(r3*x[n]) + op4[index] * fb[n])

# normalizing
for i in range(wt_len):
    index = i * spc
    frame = fmwave[index:index+spc]

    if abs(max(frame)) > 0:
        frame = (1 / max(frame)) * frame

    fmwave[index:index+spc] = frame


rows = 4
step = wt_len // rows
for i in range(rows):
    plt.subplot(rows, 1, i+1)
    plt.plot(fmwave[i*step*spc:step*(i+1)*spc], 'b-')

plt.show()