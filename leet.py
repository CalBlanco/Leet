import requests
from bs4 import BeautifulSoup
from news import newsScraper
import matplotlib.pyplot as plt
import numpy as np

#list of news scraper class objects
newsScrappers = []



yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo")
print(yf.word_count)
newsScrappers.append(yf)

usatoday = newsScraper('https://www.usatoday.com/money/investing/','market',20,'usa')
print(usatoday.news_links)

#just to turn of graphing
graph = False

if graph is True:
    for newsBoi in newsScrappers:
        count_dict = newsBoi.word_count
        keys = count_dict.keys()
        values = count_dict.values()
        plt.figure(figsize=(len(values),10))
        scat = plt.bar(keys,values)
        plt.savefig(newsBoi.nickname+".png")


