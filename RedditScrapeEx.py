from StonkRedditAPI import StonkRedditAPI
from news import newsScraper
from DataTracker import Manager

from datetime import datetime


#start time
runtime = datetime.now()


#StonkReditAPI
WSB = StonkRedditAPI('r/wallstreetbets', 'new', 'all', 100)
WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100)
WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100)
print('r/wallstreetbets', WSB.word_count)
print('r/Wallstreetbetsnew', WSBN.word_count)
print('r/WallStreetbetsELITE', WSBE.word_count)



#newsScraper
yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",True)
print(yf.word_count)
cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',True)
print(cnbc.word_count)





manager = Manager('TrackedInfo')


wc_list = [yf.word_count,cnbc.word_count,WSB.word_count]

manager.storeDataSet(wc_list)



manager.readData('AMC')






#end time and time difference
endtime = datetime.now()
timedif = endtime - runtime
print(f'Runtime : {timedif.total_seconds()}s')