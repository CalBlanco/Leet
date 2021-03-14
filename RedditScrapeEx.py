from StonkRedditAPI import StonkRedditAPI
from YahooFinanceSearch import YahooFinanceSearch
from news import newsScraper
from DataTracker import Graph



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
.'''

#newsScraper
yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",True)
print(yf.word_count)
cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',True)
print(cnbc.word_count)
News = YahooFinanceSearch('news',yf,cnbc)
print(News.handled_symbols)
Graph(News.handled_symbols,'News')

