import requests
from bs4 import BeautifulSoup
import csv
import random


class newsScraper:

    '''Main Scraping class.

        @params:
            url for finding main site, sep aka separating term, tol : find separator past certain point
            nickname for graph file name, debug : true = print connection status, false = no print.

        @important_variables:
            news_links(all the links that meet the sep and tolerance criteria
            p_data(the raw paragraph data from each link)
            word_count(symbols and their frequency in a dictionary) - main var

        @mechanics:
            this class takes in a main link(url) and finds related news links based on the sep and tol parameters.
            Individual requests are then made to each child link, with their <p> tags placed in a list called p_data
            That entire list is then filtered through the StonkData file and counted which then turns into word_count.

            @minor:
                There are somethings that might not make sense in here. Some websites require certain information
                or behavior in order to filter out bots and humans. Anything that has to do with timing, or header
                information is just for that. Do not touch them and ask me if you plan on making changes.
    '''

    def __init__(self, url, sep, tol=10,nickname="example",debug=True):
        # dont touch these
        self.headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer' : 'https://www.google.com/',
        }

        self.url = url
        self.sep = sep
        self.tol = tol
        self.nickname = nickname
        self.debug = debug

        # list for filtered links
        self.news_links = []
        self.p_data = ""
        self.word_count = {}

        main_session = requests.Session()
        print('session started : ' + self.url)

        # main request from website, content and then soup
        main_request = main_session.get(url,headers=self.headers)

        if main_request.status_code == 200:
            main_soup = BeautifulSoup(main_request.text, 'html.parser')
            if self.debug is True:
                print(main_request.headers)
            # main links
            # get <a> elements from main content
            main_links = main_soup.find_all('a')
            #main_p = main_soup.find_all('p')
            # find the news related links
            if main_links:
                for links in main_links:
                    # get the href attribute from the <a> elements / from main_links
                    href = links.get('href')
                    # make sure there is a value to look at
                    if href is not None:
                        # make sure it is not a duplicate with another link
                        if href not in self.news_links:
                            # if it can not find the base url in the news urls add the base to the news url
                            # noticed a problem where this actually pasted the url twice so watch out
                            # could use more work
                            if href.find(self.sep) >= self.tol and href.find(self.sep) != -1:
                                self.news_links.append(href)
            else:
                if debug is True:
                    print('no links found')
        else:
            if self.debug is True:
                print("connection failed STATUS CODE : " + str(main_request.status_code))
            main_session.close()

        if self.news_links:
            for news in self.news_links:
                main_session.cookies.clear()
                # news request -> content -> soup : previously known as

                #experimenting with delays on requests so that we don't get flagged
                wait_seed = random.seed()
                #wait_time = random.randrange(2,15)
                #time.sleep(wait_time)
                news_request = main_session.get(news,headers=self.headers)
                if self.debug is True:
                    print(news_request)
                if news_request.status_code == 200:
                    if self.debug is True:
                        print('Connected to : ' + news)
                    news_soup = BeautifulSoup(news_request.text,'html.parser')
                    # find all p elements
                    news_ps = news_soup.find_all('p')
                    # convert all paragraphs to a single string
                    for news_p in news_ps:
                        news_string = news_p.string
                        if news_string is not None:
                            self.p_data += news_string
                else:
                    if self.debug is True:
                        print('not found ' + news + " STATUS CODE: "+ str(news_request.status_code))

        main_session.close()
        print('ending session : ' + self.url)

        #lower case all string data
        #seperate each word and put into an array
        data_list = self.p_data.split()
        #filter array with the condition that the word is less than 5 characters (largest ticker length seemed to be 5)
        data_list = filter(lambda x: (len(x)<=5), data_list)
        #create dictionary with count
        #this portion takes the longest

        with open('StonkData.csv', mode='r') as infile:
            reader = csv.reader(infile)

            myDict = {}

            for rows in reader:
                myDict[rows[0]] = rows[1]


        for data in data_list:
            if data in myDict:
                self.word_count[data] = self.p_data.count(data)









