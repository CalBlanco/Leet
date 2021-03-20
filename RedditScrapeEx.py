from StonkRedditAPI import StonkRedditAPI
from YahooFinanceSearch import YahooFinanceSearch
from news import newsScraper
from datetime import datetime
from DataTracker import Graph, DataTracker


#start time
runtime = datetime.now()

#StonkReditAPI
WSB = StonkRedditAPI('r/wallstreetbets', 'hot', 'all', 100, 10)
WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'hot', 'all', 100, 10)
WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'hot', 'all', 100, 10)

#Takes all the Counters of the subs and adds them into one Counter



R = YahooFinanceSearch(10, WSB, WSBN, WSBE)
print(R.handled_symbols)

symbs = R.handled_symbols

'''exDT = DataTracker(symbs,'example_datasheet')
exDT.writeTo()
print(exDT.readFrom())'''


'''
#newsScraper
yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",True)
print(yf.word_count)
cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',True)
print(cnbc.word_count)
News = YahooFinanceSearch('news',yf,cnbc)
print(News.handled_symbols)
Graph(News.handled_symbols,'News')
'''

#end time and time difference
endtime = datetime.now()
timedif = endtime - runtime
print(f'Runtime : {timedif.total_seconds()}')
