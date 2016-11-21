#   This file is part of ssa.py.
#
#    ssa.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ssa.py is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ssa.py.  If not, see <http://www.gnu.org/licenses/>.
"""#-------------------------------------------------------------------------------
# Name:         ssa.py
# Purpose:      Perform Singular Spectrum Analysis using Python
# Context:      The root or primary ssa routines (in ssa_root.py) were
#                 originally developed in Matlab by Eric Breitenberger circa
#                 1995, and later extended with his permission by Tongying Shun
#                 circa 1997 and Karsten Sedmera circa 2002 under the direction
#                 of Dr. Christopher Duffy. Karsten Sedmera finished translating
#                 both the core functions and the wizard-like routine into
#                 Python in 2013. With the exception of functions that were not
#                 ideal for Python, the credits for each translated function are
#                 provided in each function's doc-string.
# Pythonista:   KSedmera
# Version:      2013/09, Python 2.7.5
# License:      GPLv3 (see COPYING txt file)
# Citation:     Eric Breitenberger (eric@gi.alaska.edu) for root ssa functions
#               Karsten Sedmera (70yxofzlivi74vhc@mailcatch.com) for ssa.py
#-------------------------------------------------------------------------------
General SSA Instructions (adapted from Tongying Shun):
    This script performs Singular Spectrum Analysis for one time series. It is
related to principal components analysis in that it identifies principal
components within a time series, i.e. similar to what you might expect from
Fourier analysis. There are many good textbooks that describe the pros and cons
and limitations of this technique that you need to read in order to apply the
results correctly.
    Before performing SSA on a time series, you ideally should select and try a
few values for the  embedding dimension, M. Usually, M should not be greater
than 1/3 of the length of the time series. The ratios of the principal
components are represented in a normalized eigenvalue spectrum to aid in
quantifying how "dominant" each empirically orthogonal function (EOF) is.
    The period or frequency of each EOF is estimated from the oscillatory pairs
(i.e. two phase-shifted eigenvectors). The usual goal of SSA is to use only a
small subset of the principal components from this analysis to reconstruct the
time series. Some excellent introductions to the SSA method include:

* Vautard, Yiou, and Ghil, Physica D 58, 95-126, 1992.
* J.B. Elsner and A.A. Tsonis book:
    Singular Spectrum Analysis: A New Tool in Time Series Analysis
    (e.g. via google ebook).
"""

import os, sys, time, Tkinter as Tk, tkFileDialog, math
try:
    from numpy import *
    import scipy
    import scipy.linalg as linalg
    import scipy.signal as sig
    from scipy.stats import chi2
    from scipy.optimize import leastsq
    import pylab as pl
    from matplotlib.ticker import AutoMinorLocator
    from ssa_root import *
except ImportError as exc:
    sys.stderr.write("Error: {}. Closing in 5 sec...\n".format(exc))
    print "Note: These tools require Python 2.6.5 - 2.7.5 (e.g. 2.6.5 comes with ArcGIS 10.0),"
    print "      AND several free science-related Python libraries. See which one your missing above."
    time.sleep(5);  sys.exit()

def TSplot((x, y), xl='Time (assumed uniform)', yl='y', logy=False, symb='b-', ts='TS plot', plot='pl.show()'):
    """ TSplot creates a basic time-series plot, unless plot is pointed to an additional plot function. """
    fig_ts = pl.figure(); fig_ts.patch.set_facecolor('white')
    fig_ts.canvas.set_window_title(ts+'; (Close to continue...)')
    if logy:    y=log(y)
    pl.plot(x,y,symb); ax_ts = pl.gca()
    ax_ts.xaxis.set_minor_locator(AutoMinorLocator())
    ax_ts.yaxis.set_minor_locator(AutoMinorLocator())
    pl.grid(b=True, which='major', color='0.4', linestyle='--')
    pl.grid(b=True, which='minor', color='0.4', linestyle=':')
    pl.xlabel(xl); pl.ylabel(yl)
    fig_ts.tight_layout()
    eval(plot)

def EOFplot(data, EOFsel=[], EOFpages=False, sid=0):
    """ EOFplot plots selected or pages of eigenvectors."""
    xvar = range(data.M)
    if not EOFpages:
        figeof = pl.figure(2); figeof.patch.set_facecolor('white')
        if EOFsel != []: ts = 'Selected Eigenvectors'
        else:   ts = 'Ordered Eigenvectors'
        figeof.canvas.set_window_title(ts+'; (Close to continue...)')
        for i,sel in enumerate(EOFsel):
            ax_e = figeof.add_subplot(5,4,i+1)
            ax_e.plot(xvar, data.E[:][:,sel])
            if data.fEp[sel]:    T = int(1./data.fEp[sel])
            else: T = 1
            pl.title(r'EOF#{0}:$\Delta$T={1}'.format(sel,T)) #EOF#[]: T=dominant period (1/f)
            pl.setp(pl.xticks()[-1], rotation=30)
        figeof.tight_layout()
    else:
        # Compensate for EOF-pages near end of M
        if sid+20 > data.M: eid = data.M
        else: eid = sid+20
        ts = 'Ranked Eigenvectors {0}-{1}; (Close to continue...)'.format(sid, eid)
        figeof = pl.figure(); figeof.patch.set_facecolor('white')
        figeof.canvas.set_window_title(ts)
        for i in range(eid-sid):
            ax_e = figeof.add_subplot(5,4,i+1)
            sel = sid + i
            ax_e.plot(xvar, data.E[:][:,sel])
            if data.fEp[sel]:    T = int(1./data.fEp[sel])
            else: T = 1
            pl.title(r'EOF#{0}:$\Delta$T={1}'.format(sel, T)) #EOF#[]: T=dominant period (1/f)
            pl.setp(pl.xticks()[-1], rotation=30)
        figeof.tight_layout()
        pl.show()

def ESplot(data, ts='', specfit = '', spts=[], ll=False):
    """ ESplot creates a log-linear eigenspectrum plot, unless plot is pointed to an additional plot function. """
    def plotcis(vf, fEf, M, E, specfit, N, spts):
        """ plot confidence intervals"""
        if spts == []:
            def rejvfs(ml, bl, vf, fEf): return [tup for k,tup in enumerate(zip(vf,fEf)) if tup[0] < bl*exp(ml*tup[1])]
            def selvfs(rejs, vf, fEf): return [tup for k,tup in enumerate(zip(vf,fEf)) if tup not in rejs]
            coords = []
            def drawline(event):
                coords.append((event.xdata, event.ydata))
                if len(coords) > 1:
                    x,y = zip(*coords)
                    #print 'xs: {0}, ys: {1}'.format(x,y)
                    axf = pl.gca()
                    line = pl.plot(x,y)
                    axf.figure.canvas.draw()
                    fig.canvas.mpl_disconnect(cid)
            fig = pl.gcf()
            cid = fig.canvas.mpl_connect('button_press_event', drawline)
            pl.show()
            if coords:
                xl,yl = zip(*coords)
                ml = (log(yl[1]/yl[0]))/(xl[1]-xl[0])
                bl= yl[1]*exp(-ml*xl[1])
                rejs = rejvfs(ml,bl,vf,fEf)
                if len(rejs) < data.M:
                    return [rejs, selvfs(rejs,vf,fEf)]
                else:
                    print "\nOops! You didn't select any points. The first 20 are selected for you."
                    return [zip(vf[20:],fEf[20:]), zip(vf[:20],fEf[:20])]
            else:
                print "\nOops! You didn't select any points. The first 20 are selected for you."
                return [zip(vf[20:],fEf[20:]), zip(vf[:20],fEf[:20])]
        else:
            def red(X, v, fE):  return v - X[0]/(X[1]+(2.*pi*X[2]*fE)**2)
            def powerlaw(X, v, fE): return v - X[0]*(fE**X[1])
            def selvfns(spts, vf, fEf): return [k for k,tup in enumerate(zip(vf,fEf)) if tup in spts]
            xvar=arange(0, 0.501, 0.001)
            nu=3.*N/len(vf)
            pupper=chi2.ppf(0.025,nu)
            plower=chi2.ppf(0.975,nu)
            vs,fs = zip(*spts[0])
            ax_es = pl.gca()
            if specfit == 'p':
                # fit power law relationship
                fit = leastsq(powerlaw,[1.0E-6,-2],args=(array(vs),array(fs)))
                yfit=[fit[0][0]*(i**fit[0][1]) for i in xvar]
                pl.fill_between(xvar, dot(nu/plower,yfit), dot(nu/pupper,yfit), alpha=0.2, facecolor='magenta')
                pl.plot(xvar,yfit,'m--')
                print ' v_fit = {0}*f^{1})'.format(*(fit[0][0], fit[0][1]))
            else:
                # fit red noise relationship
                fit=leastsq(red,[1.0E-1,1.0E1,1.0E1],args=(array(vs),array(fs)))
                yfit=[fit[0][0]/(fit[0][1]+(2.*pi*fit[0][2]*i)**2) for i in xvar]
                pl.fill_between(xvar, dot(nu/plower,yfit), dot(nu/pupper,yfit), alpha=0.2, facecolor='red')
                pl.plot(xvar,yfit,'r--')
                print u'\nv_fit = {0}/({1}+[2{2}*{3}*f]^2)'.format(*(fit[0][0], fit[0][1], u'\u03C0', fit[0][2]))
                if fit[0][0] == 1:
                    print 'Note that a constraint was forced.'
                    print 'You may want to try a power law relationship.'
            vl,fl = zip(*spts[1])
            pl.plot(fl,vl,'bo', mfc='none')
            selpts = selvfns(spts[1],vf,fEf)
            print 'Selected points: {0}\nExplain {1}% of the total variance.'.format(', '.join(str(i) for i in selpts), round(sum(vl)*100.,2))
            if len(selpts) > 20:
                print 'Warning: More than 20 were selected. Only plotting first 20. You can plot the rest in the next routine.'
                EOFplot(data, EOFsel=selpts[:20])
            else:   EOFplot(data, EOFsel=selpts)
            pl.show()
            return selpts
    fig_es = pl.figure(1); fig_es.patch.set_facecolor('white')
    fig_es.canvas.set_window_title('Eigenspectrum of '+ts+'; (Close to continue...)')
    pl.plot(data.fEp,data.vp,'k+'); ax_es = pl.gca()
    ax_es.set_yscale('log')
    if ll:  ax_es.set_xscale('log')
    pl.grid(b=True, which='major', color='0.4', linestyle='--')
    pl.grid(b=True, which='minor', color='0.4', linestyle=':')
    ax_es.xaxis.set_minor_locator(AutoMinorLocator())
    pl.xlabel('Frequency (cycle/$\Delta$T)')
    pl.ylabel('Normalized Eigenvalue')
    fig_es.tight_layout()
    if specfit == '':   pl.show()
    else:   return plotcis(data.vp,data.fEp,data.M,data.E,specfit,data.N,spts)

def PairedPlot(p1, p2, pptype='EOF', ts='a and b'):
    """ PairedPlot plots a pairs vectors againest one another."""
    fig_pp = pl.figure(1); fig_pp.patch.set_facecolor('white')
    fig_pp.canvas.set_window_title('Paired {0} plot of {1}; (Close to continue...)'.format(pptype, ts))
    pl.plot(p1,p2); ax_pp = pl.gca()
    pl.grid(b=True, which='major', color='0.4', linestyle='--')
    #pl.grid(b=True, which='minor', color='0.4', linestyle=':')
    ax_pp.xaxis.set_minor_locator(AutoMinorLocator())
    ax_pp.yaxis.set_minor_locator(AutoMinorLocator())
    xyl = ts.split(' and ')
    pl.xlabel(pptype+xyl[0])
    pl.ylabel(pptype+xyl[1])
    fig_pp.tight_layout()
    pl.show()

def ReconPlot(data, subp='t'):
    """ EOFplot plots selected or pages of eigenvectors."""
    fig_rp = pl.figure(2); fig_rp.patch.set_facecolor('white')
    fig_rp.canvas.set_window_title('Original and reconstructed time series for {0}; (Close to continue...)'.format(data.filename))
    def glines():
        pl.grid(b=True, which='major', color='0.4', linestyle='--')
        pl.grid(b=True, which='minor', color='0.4', linestyle=':')
        ax_rp.xaxis.set_minor_locator(AutoMinorLocator())
        ax_rp.yaxis.set_minor_locator(AutoMinorLocator())
    if subp == 't':
        ax_rp = fig_rp.add_subplot(2,1,1)
        ax_rp.plot(data.t,data.X,'g-', data.t, data.rx,'k--')
        pl.ylabel('Original, units')
        pl.title('Original and Reconstructed Time Series')
        glines()
        pl.legend(('Original','Reconstruction'),'best')
        ax_rp = fig_rp.add_subplot(2,1,2)
        ax_rp.plot(data.t, data.x_resid,'k')
        pl.ylabel('X-rx, residual')
        pl.xlabel('Time')
        glines()
    else:
        ax_rp = fig_rp.add_subplot(3,1,1)
        ax_rp.plot(data.t,data.X,'g-')
        pl.ylabel('Original, units')
        pl.title('Original and Reconstructed Time Series')
        glines()
        ax_rp = fig_rp.add_subplot(3,1,2)
        ax_rp.plot(data.t, data.rx,'k--')
        pl.ylabel('Reconstruction')
        glines()
        ax_rp = fig_rp.add_subplot(3,1,3)
        ax_rp.plot(data.t, data.x_resid,'k')
        pl.ylabel('X-rx, residual')
        pl.xlabel('Time')
        glines()
    fig_rp.tight_layout()
    pl.show()

class ssa_data(object):
    """Purpose: store SSA results for a time-series file."""
    def __init__(self, filename='', fpath=''):
        """Function: intiate the data object and assign filename, if given."""
        object.__init__(self)
        self.filename = filename
        self.fpath = fpath
    def describe(self, data=None):
        """Function: accept a time series, then store and report its basic stats."""
        self.X = data
        self.N = len(self.X)
        self.t = range(self.N)
        print 'SSA analysis for {0}:\n time-series length = {1}'.format(self.filename, self.N)
        self.mean = mean(self.X)
        print ' Mean = {}'.format(self.mean)
        self.variance = std(self.X)**2
        print ' Variance = {}'.format(self.variance)
        self.Y = self.X - self.mean
        TSplot((self.t,self.X), yl='Original Units',ts='TS plot of '+self.filename)
        #return (N,t,xm,xv)

class LBParams(object):
    def __init__(self, title='', txt_instruct='', but_command='', but_lbl='', lbl_list=[]):
        object.__init__(self)
        self.title = title
        self.txt_instruct = txt_instruct
        self.but_command = but_command
        self.but_lbl = but_lbl
        self.lbl_list = lbl_list
    def open_lb(self):
        master = Tk.Tk()
        master.title(self.title)
        F1 = Tk.Frame(master)
        lab = Tk.Label(F1)
        lab.config(text=self.txt_instruct)
        lab.pack()
        s = Tk.Scrollbar(F1)
        L = Tk.Listbox(F1, width=30)
        s.pack(side=Tk.RIGHT, fill=Tk.Y)
        L.pack(side=Tk.LEFT, fill=Tk.Y)
        s['command'] = L.yview
        L['yscrollcommand'] = s.set
        for id in self.lbl_list:  L.insert(Tk.END, id)
        F1.pack(side=Tk.TOP)
        F2 = Tk.Frame(master)
        def run_command():
            rid = L.get(Tk.ACTIVE)
            eval(self.but_command.format(rid))
            print '\n{0}: {1} {2} successful.'.format(self.title, self.but_lbl, rid)
        b2 = Tk.Button(F2, text=self.but_lbl, command=run_command)
        b2.pack(side=Tk.LEFT)
        F2.pack(side=Tk.TOP)
        Tk.mainloop()

def FileSelect(req = 'Please select a file:'):
    """ Tk file-selector. Returns [full path, root path, and filename]"""
    try:
        root = Tk.Tk(); root.withdraw(); fname = tkFileDialog.askopenfilename(title=req); root.destroy()
        return [fname]+list(os.path.split(fname))
    except:
        print "Error in file selection:", sys.exc_info()[1]; time.sleep(5);  sys.exit()

for line in __doc__.split('#')[:-1]:
    if line:    print line.strip('\n')
# SELECT the time series
fname = FileSelect('Please select a time series txt-file:')
data = ssa_data(fname[2], fname[0])
try:    data.describe(array([float(line.strip()) for line in open(data.fpath, 'r')]))
except: print "Error:", sys.exc_info()[1]; time.sleep(5);  sys.exit()

# Offer to resample or average the original time series and print directions
ra = raw_input('Want to resample or average the time series (r/a/[n assumed])?')
if ra == 'r':
   re_interval=int(raw_input('Input the TIME-INTERVAL for resampling (e.g. 30 for daily -> monthly):'))
   data.describe(data.X[::re_interval])
elif ra == 'a':
   intrvl = int(raw_input('Enter the desired averaging INTERVAL (e.g. 30 for daily -> monthly):'))
   data.describe(array([mean(j) for j in [data.X[i:i+intrvl] for i in xrange(0, data.N, intrvl)]]))
yorn = raw_input('Do you want SSA instructions? (y/[n assumed])')
if yorn:
    for line in __doc__.split('#')[-2:]:
        if line:    print line.strip('\n')

#------------------------ Begining main SSA method--------------------------
#  Input the 'embedding dimension' or lag, M
M = raw_input('Enter the EMBEDDING DIMENSION, M\n\n+ e.g. Enter 240 for 20-yrs of monthly data.\n+ Default/blank M = 0.33 * ts-length.\n+ M must be < 0.5 * ts-length.\n')
if not M:   data.M = int(0.33*data.N)
else:       data.M = int(M)
print ' M = {} observations.'.format(data.M)

#------------------Beginning of basic SSA------------------------
#  Originally written by Eric Breitenberger. Version date 5/22/95
[data.E, data.V, data.C] = ssaeig(data.Y, data.M)
data.A = pc(data.X, data.E)
data.R = rc(data.A, data.E)
#----------------End of basic SSA------------------------

# Normalize the eigenvalues (% variance)
v = data.V/sum(data.V)
M2 = data.M - len(nonzero(v<0.)[0])
if M2 != data.M: print ' Note: %i negative eigenvalue(s).' % (data.M-M2)
yorn = raw_input('Want to plot the eigenvalues by variance-rank? (y/[n assumed])')
if yorn == 'y':
    en = raw_input('How many ranked eigenvalues do you want to plot?')
    try: en = int(en)
    except: en = int(data.M/0.33)
    TSplot((range(en), v[:en]), 'Ordered, k=1:{}'.format(en), yl='Normalized Eigenvalue',logy=True, symb='x', ts='Ranked Eigenvalue Plot of '+data.filename)
    print '\nPlotting the ranked eigenvalues. (Close to continue)'

# Display the eigenspectra versus frequency
#
# WARNING: the frequency of the eigenvectors is often difficult to estimate since
# SSA does not guarantee that each extracted EOF has a single frequency. The
# following routine tries to fit a sinusoid to each EOF and reports the fitted
# frequency, which is not always feasible or accurate.
[mE, fE] = eoffreq(data.E)    # calculate the dominant frequency for the test data
#v = V./sum(V)
data.vp = v[:M2]
data.fEp = fE[:M2]

print '\nPlotting the raw log-linear eigenspectrum. (Close to continue)'
ESplot(data, ts=data.filename)
yorn = raw_input("Want to select EOFs from the eigenspectrum plot? ([y assumed]/n)")
if not yorn:    yorn = 'y'
while yorn == 'y':
    print '\n### Starting EOF selection and exploration ###'
    specfit = raw_input('Fit EOFs with a POWER-LAW or RED-NOISE filter? (p/[r, assumed])')
    speclabel = 'red' if specfit == 'r' else 'power-law'
    if not specfit: specfit = 'r'
    print ' Click 2 points in the next plot to draw a line to select EOFs (i.e. above your line).'
    print ' Close this initial plot to view the eigenspectrum with your selected EOFs circled and'
    print '       shaded 95% confidence intervals for the fitted {} noise floor.'.format(speclabel)
    spts = ESplot(data, ts=data.filename+" Draw a selection line below, then", specfit=specfit)
    data.sel_EOFs = ESplot(data, ts=data.filename+" with selected EOFs", specfit=specfit, spts=spts)
    yorn = raw_input(' Want to vew the LOG-LOG version of this plot, or apply a DIFFERENT filter (y/[n assumed]/d)?')
    if yorn == 'y':
        ESplot(data, ts=fname[2]+" with selected EOFs", specfit=specfit, spts=spts, ll=True)
        yorn = 'n'
    elif yorn == 'd': yorn='y'

yorn = raw_input('Want to plot EOF-pages? (y/[n assumed])')
if yorn == 'y':
    idlist = range(data.M)
    print '\n Opening a ListBox selection window. Plot as many EOF pages as you\n  wish, and then close the plots and ListBox to continue.'
    EOF_listbox = LBParams('EOF-Pages', 'Select 1st EOF,\nclick Plot 20.',
         "EOFplot(data, EOFpages=True, sid=int({0}))", "Plot next 20 EOFs beginning with", idlist)
    EOF_listbox.open_lb()

# Now offer to plot two eigenvectors against each other
yorn = raw_input('Want to plot a Eigenvector Pair against each other (y/n)?')
while yorn == 'y':
    pair = raw_input('Enter ranks of desired pair (e.g. 1,2):')
    if not pair: yorn = 'n'
    else:
        v_num = [int(i) for i in pair.split(',')]
        if len(v_num) > 2 or len(v_num) < 2:
            raise Warning("You didn't specify 2 ranks properly. Try again.")
            pair = raw_input('Please enter the ranks for the desired eigenvector pair (e.g. 1,2):')
            v_num = [int(i) for i in pair.split(',')]
            if len(v_num) > 2 or len(v_num) < 2:
                raise Warning("You didn't specify 2 ranks properly. Moving on...")
                yorn = 'n'
            else:
                print '\nEOF pair, {0}, explain {1}% of the total variance.'.format(v_num, round(sum(data.vp[k] for k in v_num)*100.,2))
                PairedPlot(data.E[:][:,v_num[0]],data.E[:][:,v_num[1]], ts='{0} and {1}'.format(*v_num))
        else:
            print '\nEOF pair, {0}, explain {1}% of the total variance.'.format(v_num, round(sum(data.vp[k] for k in v_num)*100.,2))
            PairedPlot(data.E[:][:,v_num[0]],data.E[:][:,v_num[1]], ts='{0} and {1}'.format(*v_num))
    yorn = raw_input('Want to plot another pair (y/n)?')

# Reconstruct the signal based on the SSA analysis
yorn = raw_input('Want to plot a reconstructed time series (y/n)?')
while yorn == 'y' or yorn == 'r':
    r_sel = raw_input('Enter the desired EOF-#s (e.g. 1,2,3,4... or blank for selected):')
    if not r_sel:
        if 'sel_EOFs' in dir(data):    r_sel = ','.join(str(i) for i in data.sel_EOFs)
        else:   r_sel = ','.join(str(i) for i in xrange(0,int(data.M)))
    r_sel = [int(i) for i in r_sel.split(',')]
    nr = len(r_sel)
    yorn2 = raw_input('Do you want to scale the reconstruction mean by the explained variance? ([y assumed]/n)?')
    scaled_mean = data.mean if yorn2 == 'n' else data.mean*sum(data.vp[r_sel])
    yorn2 = raw_input('Plot the original against the RESIDUAL or the RECONSTRUCTION? (rs, [rc assumed])')
    if yorn2 == 'rs':
        data.x_resid = [i+scaled_mean for i in sum(data.R[:][:,r_sel], axis=1)]
        data.rx = [data.X[i]-data.x_resid[i] for i in range(data.N)]
    else:
        yorn2 = raw_input('Plot original and reconstruction SEPARATELY or TOGETHER (s/[t assumed])?')
        data.rx = [i+scaled_mean for i in sum(data.R[:][:,r_sel], axis=1)]
        data.x_resid = [data.X[i]-data.rx[i] for i in range(data.N)]
    if nr == data.M: print '\nPlotted reconstruction for all {} EOFS.'.format(data.M)
    else:   print '\nThe plotted reconstruction for EOFS: {0}\nExplain {1}% of the total variance.'.format(', '.join(str(i) for i in r_sel), round(sum(data.vp[k] for k in r_sel)*100.,2))
    if yorn2 == 's':
        ReconPlot(data, subp='s')
    else:
        ReconPlot(data, subp='t')
    yorn = raw_input(' Would you like to consider a different reconstruction (y/[n assumed])?')

yorn = raw_input('Would you like to save any SSA data to disk (y/n)?')
if yorn == 'y':
    print '\n Your working directory is: {}.\n Select a variable from the next ListBox window, then close it when finished.'.format(fname[1])
    var_nms = [i for i in data.__dict__.keys() if i[:1] != '_']
    vname_lb = LBParams('SSA Variables', 'Select variable,\nclick Save.',
         "savetxt(data.fpath.replace('.txt','_{0}.txt'), data.{0}, delimiter=',', newline='\\n')",
         "Save to csv:", var_nms)
    vname_lb.open_lb()
print '\nClosing ssa.py.'