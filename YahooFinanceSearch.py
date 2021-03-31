import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter

class YahooFinanceSearch:
    def __init__(self,  filename, *Scrapers):
        #
        self.filename = filename
        self.Scrapers = Scrapers


        ''' FINDSTONK is my shortcut to using the yfinance api. It uses the requests lib and beautifulsoup.

            
            '''

        def findStonk(symbol):
            yahoo = 'http://finance.yahoo.com/quote/'
            url = yahoo + symbol.upper() + "?p=" + symbol.upper() + "&.tsrc=fin-srch"
            print(url)
            stonk_request = requests.get(url)
            if stonk_request.status_code == 200:
                stonk_soup = BeautifulSoup(stonk_request.content, 'html.parser')

                stonk_quote = stonk_soup.find('div', {'id': 'quote-header-info'})
                try:
                    stonk_subquote = stonk_quote.find('div', {'class': 'D(ib) Mend(20px)'})
                    stonk_data = stonk_subquote.find_all('span')

                    cur_change = stonk_data[-2].string
                    if cur_change:
                        perc_change = cur_change[cur_change.find('(') + 1:cur_change.find('%')]
                        perc_change = float(perc_change)
                        return perc_change
                except AttributeError:
                    print('could not find quote for ' + symbol)
                    return 0
                except IndexError:
                    print("Data not found for " + symbol)
                    return 0

            else:
                print('no link available / connection failed')



        # getChange
        ''' getChange is a function for taking all of the found symbols and creating a list of values from the STONKFINDER
            method.

            @param: list of symbols we want information for

            @return : list of those symbols info 

            Super basic function. Just uses stonkFinder() and then appends that information to a list.
            Decided to split these into two separate functions to increase modularity of stonkFinder(). 
        '''

        def getChange(symbol_list):
            perc = []
            for symbol in symbol_list:
                perc.append(findStonk(symbol))

            return perc


        #create main data frame from list of scrapers input
        agg_count = Counter()
        for scraper in Scrapers:
            agg_count += scraper.word_count
        self.main_frame = pd.DataFrame.from_dict(agg_count, orient="index", columns=["count"])

        #extract symbol list : index
        symbol_list =self.main_frame.index
        #run getChange to get change column
        self.main_frame['change'] = getChange(symbol_list)




