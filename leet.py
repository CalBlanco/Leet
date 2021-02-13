import requests
from bs4 import BeautifulSoup
from news import newsScraper
import matplotlib.pyplot as plt
import numpy as np

#list of news scraper class objects
newsScrappers = []

# business news sources
# reuters https://www.reuters.com/business
# yahoo https://finance.yahoo.com/
# cnbc https://www.cnbc.com/economy/
# market watch https://www.marketwatch.com/column/financial-news

cnbc = newsScraper('https://www.cnbc.com/economy/','2021',8,"cnbc")
print(cnbc.word_count)
newsScrappers.append(cnbc)

yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo")
print(yf.word_count)
newsScrappers.append(yf)






for newsBoi in newsScrappers:
    count_dict = newsBoi.word_count
    keys = count_dict.keys()
    values = count_dict.values()
    plt.figure(figsize=(len(values),10))
    scat = plt.bar(keys,values)
    plt.savefig(newsBoi.nickname+".png")


