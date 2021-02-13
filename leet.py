import requests
from bs4 import BeautifulSoup
from news import newsScraper
import matplotlib.pyplot as plt

#list of news scraper class objects
newsScrappers = []



yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo")
print(yf.word_count)
newsScrappers.append(yf)

#this is misnamed but i didnt want it to make another graph so
usatoday = newsScraper('https://www.cnbc.com/economy/','2021',10,'usa')
print(usatoday.word_count)
newsScrappers.append(usatoday)

# this one aint working
#reut = newsScraper('https://www.reuters.com/business','article',10,'reut')
#print(reut.word_count)
#newsScrappers.append(reut)


#just to turn of graphing
graph = True

if graph is True:
    for newsBoi in newsScrappers:
        if newsBoi.p_data is not None:
            count_dict = newsBoi.word_count
            keys = count_dict.keys()
            values = count_dict.values()
            plt.figure(figsize=(len(values),10))
            scat = plt.bar(keys,values)
            plt.savefig(newsBoi.nickname+".png")



def combineData():
    print('asd')
