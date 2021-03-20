import requests
from bs4 import BeautifulSoup
from collections import Counter


class YahooFinanceSearch:
    def __init__(self, headNum ,*Counters):
        #
        self.Counters = Counters
        self.headNum = headNum

        ''' FINDSTONK is my shortcut to using the yfinance api. It uses the requests lib and beautifulsoup.
            @note : this function is only used by the symbolHandler function currently.
            @param: it takes one argument and that is a list called stock_item, [symbol, count] ex:['AAPL',20].
            @return a list with the symbol itself, count on site, and the percentage change.
            str is the url that it is going to grab data from. the concatenation of the strings represent where in the link the.
            symbol must be placed in order for it to find the right page.
            There were some issues in finding info between NYSE listed stocks and other markets so to fix that.
            It finds a specific <div> element with id=quote-header-info.
            this div contains the stock pricing info.
            Then i convert the cur change to the percentage change by locating the numerical value after the first ( and before.
            the % sign. Cast that value to a float for graphing later.

            Changed this around this around to pass all the relevant graphing data in one spot 
            '''

        def addSubTicks(counters):
            final = Counter()
            for i in counters:
                final += i.org_freq
            return final.most_common(headNum)

        self.Counters = addSubTicks(Counter(self.Counters))

        print('\nFinal', self.Counters)


        def findStonk(stonk_item):
            # pull out symbol
            stonk = stonk_item[0]
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

                    cur_change = stonk_data[-2].string
                    if cur_change:
                        perc_change = cur_change[cur_change.find('(') + 1:cur_change.find('%')]
                        perc_change = float(perc_change)
                        return [stonk, stonk_item[1], perc_change]
                except AttributeError:
                    print('could not find quote for ' + stonk)
                    return [stonk, 0, 0]
                except IndexError:
                    print("Data not found for " + stonk)
                    return [stonk, 0, 0]

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
        mainDict = dict(self.Counters)
        # set to true if you want the program to generate graphs for each site

        #print("so Far",type(Dictionaries))

        # pull word count dicts
        count_items = mainDict.items()
        new_count = {str(key): int(values) for key, values in count_items}
        # changed the output here to return the symbol and the count for graphing later
        symbolList += list(map(list, new_count.items()))

        # remove duplicate entries from symbolList and turns into cleanSymbols
        for symbol in symbolList:
            if symbol not in cleanSymbols:
                cleanSymbols.append(symbol)

        # get stonk info
        # print(symbolList)
        handled = symbolHandler(symbolList)

        self.handled_symbols = handled
