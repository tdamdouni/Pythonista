# coding: utf-8

# https://forum.omz-software.com/topic/1077/tex-rendering-via-matplotlib-tex/4 

import matplotlib.pyplot as plt
from matplotlib import rc

df_fig_sz = [1, 1]
formulas = [[r'$\alpha > \beta$', df_fig_sz, 0.2, 0.25, 'alpha beta'], 
[r'$\alpha_i > \beta_i$', df_fig_sz, 0.2, .25, 'ss_script'], 
[r'$\sqrt{2}$', df_fig_sz, 0.2, .25, 'radicals_01'], 
[r'$\sqrt[3]{x}$', df_fig_sz, 0.2, .25, 'radicals_02']
 ]
for f in formulas:
    params = {'figure.figsize': f[1],}
    plt.rcParams.update(params)
    fig = plt.figure()
    fig.text(f[2], f[3], f[0])
    plt.savefig(f[4] + '.png')

# --------------------
