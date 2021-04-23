from StonkRedditAPI import StonkRedditAPI
from news import newsScraper
from DataTracker import FrameBuilder

from datetime import datetime


#start time
runtime = datetime.now()


#StonkReditAPI
'''
WSB = StonkRedditAPI('r/wallstreetbets', 'new', 'all', 100)
WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100)
WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100)
print('r/wallstreetbets', WSB.word_count)
print('r/Wallstreetbetsnew', WSBN.word_count)
print('r/WallStreetbetsELITE', WSBE.word_count)
R = YahooFinanceSearch( 'reddit', WSB, WSBN, WSBE,)
print(R.handled_symbols)

Graph(R.handled_symbols,'reddit')

'''
#newsScraper
yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",True)
print(yf.word_count)
cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',True)
print(cnbc.word_count)


#FrameBuilder Example
count_list = [yf.word_count,cnbc.word_count]

FrameBuilder(count_list,"temp1.csv")










#end time and time difference
endtime = datetime.now()
timedif = endtime - runtime
print(f'Runtime : {timedif.total_seconds()}s')