from news import newsScraper
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

#FUNCTIONS

''' FINDSTONK is my shortcut to using the yfinance api. It uses the requests lib and beautifulsoup.
    
    @note : this function is only used by the symbolHandler function currently
    
    @param: it takes one argument and that is a stock symbol like AAPL, or something.
    
    @return a list with the symbol itself, the current price, and the percentage change
    
    str is the url that it is going to grab data from. the concatenation of the strings represent where in the link the.
    symbol must be placed in order for it to find the right page.
    
    after the request is made a BeautifulSoup object is made named stonk_soup.
    There were some issues in finding info between NYSE listed stocks and other markets so to fix that.
    It finds a specific <div> element with id=quote-header-info.
    this div contains the stock pricing info
    the reason for the negative indexing is that different symbols had different locations for the price.
    However they were always the second and third to last items.
    I turn these values into strings to get rid of all the html code in them
    
    Then i convert the cur change to the percentage change by locating the numerical value after the first ( and before.
    the % sign. Cast that value to a float for graphing later.'''

def findStonk(stonk):
    yahoo = 'http://finance.yahoo.com/quote/'
    url = yahoo + stonk.upper() + "?p=" + stonk.upper() + "&.tsrc=fin-srch"
    print(url)
    stonk_request = requests.get(url)
    stonk_soup = BeautifulSoup(stonk_request.content, 'html.parser')

    stonk_quote = stonk_soup.find('div',{'id':'quote-header-info'})
    stonk_data = stonk_quote.find_all('span')

    cur_price = stonk_data[-3].string
    cur_change = stonk_data[-2].string
    percent_change = cur_change[cur_change.find('(')+1:cur_change.find('%')]
    percent_change = float(percent_change)
    return [stonk,cur_price,percent_change]


# Symbol handler
''' SYMBOLHANDLER is a function for taking all of the found symbols and creating a list of values from the STONKFINDER
    method.
    
    @param: list of symbols we want information for
    
    @return : list of those symbols info 
    
    Super basic function. Just uses stonkFinder() and then appends that information to a list.
    Decided to split these into two separate functions to increase modularity of stonkFinder(). 

'''

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


yf = newsScraper('https://finance.yahoo.com/','news',10,"yahoo",False)
print(yf.word_count)
newsScrappers.append(yf)

cnbc = newsScraper('https://www.cnbc.com/economy/','2021',10,'cnbc',False)
print(cnbc.word_count)
newsScrappers.append(cnbc)

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
#print(symbolList)
handled = symbolHandler(cleanSymbols)
print(handled)

#graphing (not working atm)
if graph is True:
    #This portion creates the graphs for frequency of symbols per news site
    for scraper in newsScrappers:
        if scraper.p_data is not None:
            current_count = scraper.word_count
            keys = current_count.keys()
            values = current_count.values()
            plt.figure(figsize=(len(keys), 10))
            plt.bar(keys, values)

            plt.savefig(scraper.nickname + ".png")


    #This portion creates a graph of all the symbols with their respective percentage change
    company = []
    percent_change = []
    for ticker in handled:
        company.append(ticker[0])
        percent_change.append(ticker[2])

    plt.figure(figsize=(len(company), 10))
    plt.bar(company, percent_change)
    plt.savefig('stronk.png')




