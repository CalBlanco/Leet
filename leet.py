import requests
from bs4 import BeautifulSoup
from news import newsScraper

#list of actual tickers
super_ = requests.get('https://stockanalysis.com/stocks/')
souper = BeautifulSoup(super_.content,'html.parser')
lis = souper.find_all('li')
lix = []
#only important thing here : super_dict contains all the tickers we are filtering the scraper for
super_dict = {}
for li in lis[10:-18]:
    li = li.string
    lix.append(li)

    li = li.split()

    super_dict[li[0]] = " ".join(li[2:])




