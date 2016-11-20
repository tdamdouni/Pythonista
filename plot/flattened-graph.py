# coding: utf-8

# https://forum.omz-software.com/topic/3393/why-do-i-get-diffrent-graphs-running-this-code-with-python-2-7-or-3-5/2

import console
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml

# console.clear()
file_name = 'wc-cent-2.npy'
data = np.load(file_name)

fig_mag = plt.figure()
plt.psd(data[:, 0].flatten(), NFFT=256, Fs=80, window=ml.window_hanning, detrend = ml.detrend_none, scale_by_freq = True, noverlap = 0, pad_to = None, sides = 'onesided')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power/Frequency (dB/Hz)')
plt.title('PSD X')
plt.show()
