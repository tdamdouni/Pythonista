#!/usr/bin/env python

from __future__ import print_function
maxsample=10
httpaddr="92.229.240.90"
httpmethod="OPTIONS"
httppath="/generate_204"
outfile="output"

enable_plot=True

verbose=0

import os, sys
import urllib
import argparse
import time
try:
  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib.backends.backend_pdf import PdfPages
  from itertools import cycle
  enable_plot=True
except ImportError:
  enable_plot=False

if enable_plot:
  linestyles = ["k-",":","k-.","--"]
  linecycler = cycle(linestyles)

# may work in multiple python versions
if sys.version_info[0] > 2:
  import http.client
else:
  import httplib

def urllib_parse_urlencode(*args):
  if sys.version_info[0] > 2: return urllib.parse.urlencode(args)
  return urllib.urlencode(*args)
  
def http_client_HTTPConnection(*args):
  if sys.version_info[0] > 2: return http.client.HTTPConnection(args)
  return httplib.HTTPConnection(*args)

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbosity', dest='verbose', help='enable verbose outout', action='store_true')
parser.add_argument('-f', '--filename',  dest='filename', help='.csv filename to update data', action='store')
parser.add_argument('-p', '--justplot',  dest='justplot', help='plot available .csv files', action='store_true')
args = parser.parse_args()

print("HTTPing Latency Plotter v0.9")
if not args.filename:
  if not args.justplot:
    parser.print_help()
    print('\nNo arguments provided... saving to '+outfile+'.csv\n')
    args.filename=outfile
#    sys.exit(0)

cy = [0] * maxsample
headers = {"Content-type": "application/x-www-form-urlencoded",
                 "Accept": "text/plain"}

filetitles=[]
y=[]
xlen=0

# send maxsample http requests
if not args.justplot:
  conn = http_client_HTTPConnection(httpaddr)
  for i in range(maxsample):
    params = urllib_parse_urlencode({'seq': i})
    starttime=time.time()
    conn.request(httpmethod, httppath, params, headers)
    response = conn.getresponse()
    elapsedtime=(time.time() - starttime) * 1000
    print("httping %s  time %.3f ms" % (httpaddr, elapsedtime))
    cy[i]=elapsedtime
    if verbose:
      print((response.status, response.reason))
    #data = response.read()
  conn.close()

  if not args.filename.endswith('.csv'):
    filetitles = [args.filename]
    args.filename = args.filename + '.csv'
  else:
    filetitles = [args.filename.split('.')[0]]

  if os.path.exists(args.filename):
    print("Updating "+args.filename+'...')
    f=open(args.filename, 'r')
    buffer=f.read()
    y=[[float(i)for i in buffer.split(',')]]
    y[0].extend(cy)
#  print y
    f.close()
  else: y=[cy]

  xlen=len(y[0])
  print('Writing to '+args.filename+'...')
  f=open(args.filename,'w')
  f.write(str(y[0][0]))
  f.write("".join([(","+str(i)) for i in y[0]]))
  f.close()
#endif justplot

if not enable_plot: sys.exit(0)

d=os.listdir('.')
for file in d:
  if os.path.isfile(file):
    if file.endswith('.csv'):
      if file != args.filename:
        print("Processing "+file)
        f=open(file, 'r')
        buffer=f.read()
        ry=[float(i)for i in buffer.split(',')]
        y.append(ry)
        if len(ry)>xlen: xlen=len(ry)
        filetitles.append(file.split('.')[0])
        f.close()

x=np.arange(xlen)
fig = plt.figure()
ax=plt.subplot(111)

for i in xrange(len(y)):
  if len(y[i]) < xlen: y[i].extend([0] * (xlen-len(y[i])))
  ax.plot(x, y[i], next(linecycler), label=filetitles[i])

leg = ax.legend(loc='upper center',# bbox_to_anchor=(0.5, 1.05),
                ncol=1, fancybox=True, shadow=True)

ax.set_ylim([-1,900])
ax.grid(True)
ax.set_xlabel('Time')
ax.set_ylabel('Round-Trip Time (ms)')
ax.set_title('HTTP Latency Req/Res')

#ax.set_yticklabels([])
#ax.set_xticklabels([])

frame  = leg.get_frame()
frame.set_facecolor('0.80')    # set the frame face color to light gray

# matplotlib.text.Text instances
for t in leg.get_texts():
    t.set_fontsize('small') 

print('Writing new file '+outfile+'.pdf/png')
fig.savefig(outfile+'.png')
pp = PdfPages(outfile+'.pdf')
pp.savefig(fig)
pp.close()

