from __future__ import absolute_import
from __future__ import print_function
import requests, urllib.parse
import time,datetime
from six.moves import range

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
	''' Daily quotes from Google. Date format='yyyymmdd' '''
	def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
		super(GoogleQuote,self).__init__()
		self.symbol = symbol.upper()
		#start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
		#end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
		url_string = "http://finance.google.com/finance/historical?"
		urldict={'q':self.symbol,'startdate':start_date,'enddate':end_date,'output':'csv'}
		url_string+=urllib.parse.urlencode(urldict)

		print(url_string)
		csv = requests.get(url_string).content.splitlines()
		csv.reverse()
		for bar in range(0,len(csv)-1):
			ds,open_,high,low,close,volume = csv[bar].decode('ascii').rstrip().split(',')
			open_,high,low,close = [float(x) for x in [open_,high,low,close]]
			dt = datetime.datetime.strptime(ds,'%d-%b-%y')
			self.append(dt,open_,high,low,close,volume)

if __name__ == '__main__':
	q = GoogleQuote('aapl','2011-01-01','2011-01-05') # download year to date Apple data
	print(q) # print it out

