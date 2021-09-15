from StonkRedditAPI import StonkRedditAPI
from news import NewsScraper,RedditInterface
from DataTracker import Manager
import Processor

from datetime import datetime


#start time
runtime = datetime.now()



WSB = RedditInterface('r/wallstreetbets','new')
#print(WSB.word_data)


#

#newsScraper
yf = NewsScraper('https://finance.yahoo.com/',['finance.yahoo.com','news'],"scraper",True)
#print(yf.word_count)
cnbc = NewsScraper('https://www.cnbc.com/economy/',['www.cnbc.com','2021'])
#print(cnbc.word_count)





#manager = Manager('TrackedInfo')


#wc_list = [yf.word_count,cnbc.word_count]
#print(wc_list)


out = Processor.GenerateWordCount([yf.word_data,cnbc.word_data,WSB.word_data])
print(out)


#end time and time difference
endtime = datetime.now()
timedif = endtime - runtime
print(f'Runtime : {timedif.total_seconds()}s')