import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

class YahooFinanceSearch:
    def __init__(self,  filename, *Dictionaries):
        #
        self.filename = filename
        self.Dictionaries = Dictionaries

        ''' FINDSTONK is my shortcut to using the yfinance api. It uses the requests lib and beautifulsoup.

            @note : this function is only used by the symbolHandler function currently.

            @param: it takes one argument and that is a stock symbol like AAPL, or something.

            @return a list with the symbol itself, the current price, and the percentage change.

            str is the url that it is going to grab data from. the concatenation of the strings represent where in the link the.
            symbol must be placed in order for it to find the right page.

            There were some issues in finding info between NYSE listed stocks and other markets so to fix that.
            It finds a specific <div> element with id=quote-header-info.
            this div contains the stock pricing info.

            Then i convert the cur change to the percentage change by locating the numerical value after the first ( and before.
            the % sign. Cast that value to a float for graphing later.'''

        def findStonk(stonk):
            yahoo = 'http://finance.yahoo.com/quote/'
            url = yahoo + stonk.upper() + "?p=" + stonk.upper() + "&.tsrc=fin-srch"
            print(url)
            stonk_request = requests.get(url)
            if stonk_request.status_code == 200:
                stonk_soup = BeautifulSoup(stonk_request.content, 'html.parser')

                stonk_quote = stonk_soup.find('div', {'id': 'quote-header-info'})
                try:
                    stonk_subquote = stonk_quote.find('div', {'class': 'D(ib) Mend(20px)'})
                    stonk_data = stonk_subquote.find_all('span')

                    cur_price = stonk_data[-3].string
                    cur_change = stonk_data[-2].string
                    if cur_change:
                        perc_change = cur_change[cur_change.find('(') + 1:cur_change.find('%')]
                        perc_change = float(perc_change)
                        return [stonk, cur_price, perc_change]
                except AttributeError:
                    print('could not find quote for ' + stonk)
                    return [stonk, 0, 0]
                except IndexError:
                    print("Data not found for " + stonk)
                    return [stonk,0,0]

            else:
                print('no link available / connection failed')

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

        ScrapeTickerList = []
        # list of all found symbols
        symbolList = []
        cleanSymbols = []
        # set to true if you want the program to generate graphs for each site


        for dicts in Dictionaries:
            ScrapeTickerList.append(dicts)


        for scraper in ScrapeTickerList:
            # pull word count dicts
            count_items = scraper.word_count.items()
            new_count = {str(key): str(values) for key, values in count_items}
            keys = list(new_count.keys())
            for key in keys:
                symbolList.append(key)
        # remove duplicate entries from symbolList and turns into cleanSymbols
        for symbol in symbolList:
            if symbol not in cleanSymbols:
                cleanSymbols.append(symbol)

        # get stonk info
        # print(symbolList)
        handled = symbolHandler(cleanSymbols)

        self.handled_symbols = handled

        # graphing (not working atm)
        graph = True

        if graph is True:
            # This portion creates the graphs for frequency of symbols per news site
            for scraper in ScrapeTickerList:
                if scraper.p_data is not None:
                    current_count = scraper.word_count
                    keys = current_count.keys()
                    values = current_count.values()
                    plt.figure(figsize=(len(keys), 10))
                    plt.bar(keys, values)

                    plt.savefig(filename+'countchart.png')

            # This portion creates a graph of all the symbols with their respective percentage change
            company = []
            percent_change = []
            fig, ax = plt.subplots(figsize=(len(cleanSymbols), 10))
            for ticker in handled:
                try:
                    company.append(ticker[0])
                    percent_change.append(ticker[2])
                except TypeError:
                    print("None type found")

            # plt.figure(figsize=(len(company), 10))
            ax.scatter(company, percent_change, s=1000, c=percent_change, cmap='viridis')
            ax.set_xlabel('Symbol')
            ax.set_ylabel('% Change')
            ax.set_title('Symbols vs Their % Change')
            ax.grid(True)
            # fig.tight_layout()
            plt.savefig(f'{self.filename}.png')
            
