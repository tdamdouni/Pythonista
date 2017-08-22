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

