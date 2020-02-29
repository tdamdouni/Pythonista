from __future__ import print_function
# https://forum.omz-software.com/topic/4214/urllib-request-python-2-vs-3/9

#!python2

import urllib
import time,datetime

class Quote(object):

	DATE_FMT = '%Y-%m-%d'
	TIME_FMT = '%H:%M:%S'
	
	def __init__(self):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		
	def append(self,dt,open_,high,low,close,volume):
		self.date.append(dt.date())
		self.time.append(dt.time())
		self.open_.append(float(open_))
		self.high.append(float(high))
		self.low.append(float(low))
		self.close.append(float(close))
		self.volume.append(int(volume))
		
	def to_csv(self):
		return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
		self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
		self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar])
		for bar in xrange(len(self.close))])
		
	def write_csv(self,filename):
		with open(filename,'w') as f:
			f.write(self.to_csv())
			
	def read_csv(self,filename):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		for line in open(filename,'r'):
			symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
			self.symbol = symbol
			dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
			self.append(dt,open_,high,low,close,volume)
		return True
		
	def __repr__(self):
		return self.to_csv()
		
		
class GoogleQuote(Quote):
	''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
	def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
		super(GoogleQuote,self).__init__()
		self.symbol = symbol.upper()
		start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
		url_string += "&startdate={0}&enddate={1}&output=csv".format(
		start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
		print(url_string)
		csv = urllib.urlopen(url_string).readlines()
		csv.reverse()
		for bar in xrange(0,len(csv)-1):
			ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
			open_,high,low,close = [float(x) for x in [open_,high,low,close]]
			dt = datetime.datetime.strptime(ds,'%d-%b-%y')
			self.append(dt,open_,high,low,close,volume)
			
if __name__ == '__main__':
	q = GoogleQuote('aapl','2011-01-01','2011-01-03')              # download year to date Apple data
	print(q)                                          # print it out

# --------------------

#!python3

import urllib.request
import time,datetime

class Quote(object):

	DATE_FMT = '%Y-%m-%d'
	TIME_FMT = '%H:%M:%S'
	
	def __init__(self):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		
	def append(self,dt,open_,high,low,close,volume):
		self.date.append(dt.date())
		self.time.append(dt.time())
		self.open_.append(float(open_))
		self.high.append(float(high))
		self.low.append(float(low))
		self.close.append(float(close))
		self.volume.append(int(volume))
		
	def to_csv(self):
		return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
		self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
		self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar])
		for bar in xrange(len(self.close))])
		
	def write_csv(self,filename):
		with open(filename,'w') as f:
			f.write(self.to_csv())
			
	def read_csv(self,filename):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		for line in open(filename,'r'):
			symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
			self.symbol = symbol
			dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
			self.append(dt,open_,high,low,close,volume)
		return True
		
	def __repr__(self):
		return self.to_csv()
		
		
class GoogleQuote(Quote):
	''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
	def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
		super(GoogleQuote,self).__init__()
		self.symbol = symbol.upper()
		start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
		url_string += "&startdate={0}&enddate={1}&output=csv".format(
		start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
		print(url_string)
		req = urllib.request.Request(url_string)
		csv = urllib.request.urlopen(req).readlines()
		csv.reverse()
		for bar in xrange(0,len(csv)-1):
			ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
			open_,high,low,close = [float(x) for x in [open_,high,low,close]]
			dt = datetime.datetime.strptime(ds,'%d-%b-%y')
			self.append(dt,open_,high,low,close,volume)
			
if __name__ == '__main__':
	q = GoogleQuote('aapl','2011-01-01','2011-01-03')              # download year to date Apple data
	print(q)                                          # print it out

# --------------------

#!python3

import urllib.request
import time,datetime

class Quote(object):

	DATE_FMT = '%Y-%m-%d'
	TIME_FMT = '%H:%M:%S'
	
	def __init__(self):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		
	def append(self,dt,open_,high,low,close,volume):
		self.date.append(dt.date())
		self.time.append(dt.time())
		self.open_.append(float(open_))
		self.high.append(float(high))
		self.low.append(float(low))
		self.close.append(float(close))
		self.volume.append(int(volume))
		
	def to_csv(self):
		return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
		self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
		self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar])
		for bar in range(len(self.close))])
		
	def write_csv(self,filename):
		with open(filename,'w') as f:
			f.write(self.to_csv())
			
	def read_csv(self,filename):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		for line in open(filename,'r'):
			symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
			self.symbol = symbol
			dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
			self.append(dt,open_,high,low,close,volume)
		return True
		
	def __repr__(self):
		return self.to_csv()
		
		
class GoogleQuote(Quote):
	''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
	def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
		super(GoogleQuote,self).__init__()
		self.symbol = symbol.upper()
		start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
		url_string += "&startdate={0}&enddate={1}&output=csv".format(
		start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
		print(url_string)
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
		headers = {'User-Agent': user_agent}
		req = urllib.request.Request(url_string,data=None,headers=headers)
		csv = urllib.request.urlopen(req).readlines()
		csv.reverse()
		for bar in range(0,len(csv)-1):
			ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
			open_,high,low,close = [float(x) for x in [open_,high,low,close]]
			dt = datetime.datetime.strptime(ds,'%d-%b-%y')
			self.append(dt,open_,high,low,close,volume)
			
if __name__ == '__main__':
	q = GoogleQuote('aapl','2011-01-01','2011-01-03')              # download year to date Apple data
	print(q)                                          # print it out
	
# --------------------

#!python2

import datetime
from collections import namedtuple

now = datetime.datetime.now()

# enhance the fmt string to avoid calls to strftime
FMT = '{},{:%Y-%m-%d},{:%H:%M:%S},{:.2f},{:.2f},{:.2f},{:.2f},{}'
print(FMT.format('AAPL', now, now, 1, 2, 3, 4, 5))

# Or define a namedtuple and a format to match
stock_info = namedtuple('stock_info', 'date time open high low close volume')
stock_record = stock_info(now, now, 1, 2, 3, 4, 5)
FMT = ('{},{date:%Y-%m-%d},{time:%H:%M:%S},{open:.2f},{high:.2f},{low:.2f},'
       '{close:.2f},{volume}')
print(FMT.format('AAPL', **stock_record._asdict()))

# --------------------

#!python2

import urllib,time,datetime

class Quote(object):

	DATE_FMT = '%Y-%m-%d'
	TIME_FMT = '%H:%M:%S'
	
	def __init__(self):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		
	def append(self,dt,open_,high,low,close,volume):
		self.date.append(dt.date())
		self.time.append(dt.time())
		self.open_.append(float(open_))
		self.high.append(float(high))
		self.low.append(float(low))
		self.close.append(float(close))
		self.volume.append(int(volume))
		
	def to_csv(self):
		return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
		self.date[bar].strftime('%Y-%m-%d'),self.time[bar].strftime('%H:%M:%S'),
		self.open_[bar],self.high[bar],self.low[bar],self.close[bar],self.volume[bar])
		for bar in xrange(len(self.close))])
		
	def write_csv(self,filename):
		with open(filename,'w') as f:
			f.write(self.to_csv())
			
	def read_csv(self,filename):
		self.symbol = ''
		self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
		for line in open(filename,'r'):
			symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
			self.symbol = symbol
			dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
			self.append(dt,open_,high,low,close,volume)
		return True
		
	def __repr__(self):
		return self.to_csv()
		
		
class GoogleQuote(Quote):
	''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
	def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
		super(GoogleQuote,self).__init__()
		self.symbol = symbol.upper()
		start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
		url_string += "&startdate={0}&enddate={1}&output=csv".format(
		start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
		csv = urllib.urlopen(url_string).readlines()
		csv.reverse()
		for bar in xrange(0,len(csv)-1):
			ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
			open_,high,low,close = [float(x) for x in [open_,high,low,close]]
			dt = datetime.datetime.strptime(ds,'%d-%b-%y')
			self.append(dt,open_,high,low,close,volume)
			
#if __name__ == '__main__':
q = GoogleQuote('vti','2017-09-08','2017-09-12')
print(q)

# --------------------

