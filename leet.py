from news import newsScraper
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

#FUNCTIONS
# stronk base info
def findStonk(stonk):
    yahoo = 'http://finance.yahoo.com/quote/'
    str = yahoo + stonk.upper() + "?p=" + stonk.upper() + "&.tsrc=fin-srch"

    stonk_request = requests.get(str)
    stonk_soup = BeautifulSoup(stonk_request.content, 'html.parser')

    cur_price = stonk_soup.find('span', attrs={'data-reactid': '50'}).string
    cur_change = stonk_soup.find('span', attrs={'data-reactid': '51'}).string
    today_volume = stonk_soup.find('span', attrs={'data-reactid': '126'}).string

    return [stonk,cur_price, cur_change, today_volume]


# Symbol handler

def symbolHandler(symbol_list):
    return_li = []
    for symbol in symbol_list:
        return_li.append(findStonk(symbol))

    return return_li

#list of news scraper class objects
newsScrappers = []
#list of all found symbols
symbolList = []
cleanSymbols = []
#set to true if you want the program to generate graphs for each site
graph = True

# added new parameter to newsScraper
# the final argurment is debug. Default it is true
# if debug = True it will print out if the connection was successful or not
yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",False)
print(yf.word_count)
newsScrappers.append(yf)

cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',False)
print(cnbc.word_count)
newsScrappers.append(yf)

yf_dict = yf.word_count
cnbc_dict = cnbc.word_count

#take the newscrappers word counts and get all of their symbols into a larger list
for scraper in newsScrappers:
    #pull word count di
    count_items = scraper.word_count.items()
    new_count = {str(key) : str(values) for key, values in count_items}
    keys = list(new_count.keys())
    for key in keys:
        symbolList.append(key)
#remove duplicate entries from symbolList and turns into cleanSymbols
for symbol in symbolList:
    if symbol not in cleanSymbols:
        cleanSymbols.append(symbol)


#get stonk info
print(symbolList)
print(symbolHandler(cleanSymbols))

#graphing (not working atm)
if graph is False:
    for scraper in newsScrappers:
        if scraper.p_data is not None:
            current_count = scraper.word_count
            keys = current_count.keys
            print(keys)
            values = current_count.values
            plt.figure(figsize=(len(keys), 10))
            scat = plt.bar(keys, values)
            plt.savefig(scraper.nickname + ".png")







