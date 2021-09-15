from StonkRedditAPI import StonkRedditAPI
from news import NewsScraper
from DataTracker import Manager

from datetime import datetime


#start time
runtime = datetime.now()








#newsScraper
yf = NewsScraper('https://finance.yahoo.com/',['finance.yahoo.com','news'],"scraper",True)
print(yf.word_count)
cnbc = NewsScraper('https://www.cnbc.com/economy/',['www.cnbc.com','2021'])
print(cnbc.word_count)





manager = Manager('TrackedInfo')


wc_list = [yf.word_count,cnbc.word_count]
print(wc_list)






#end time and time difference
endtime = datetime.now()
timedif = endtime - runtime
print(f'Runtime : {timedif.total_seconds()}s')