import requests
from bs4 import BeautifulSoup
import csv

class newsScraper:

    def __init__(self, url, sep, tol,nickname):
        self.url = url
        self.sep = sep
        self.tol = tol
        self.nickname = nickname


        # main request from website, content and then soup
        main_request = requests.get(url)
        main_content = main_request.content
        main_soup = BeautifulSoup(main_content, 'html.parser')

        # main links
        # get <a> elements from main content
        main_links = main_soup.find_all('a')

        # list for filtered links
        self.news_links = []
        self.p_data = ""
        self.word_count ={}


        # find the news related links
        for links in main_links:
            # get the href attribute from the <a> elements / from main_links
            href = links.get('href')
            if href is not None:
                if href not in self.news_links:
                    if href.find(self.sep) >= self.tol:
                        self.news_links.append(href)

        for news in self.news_links:
            # news request -> content -> soup : previously known as
            news_request = requests.get(news)
            news_content = news_request.content
            news_soup = BeautifulSoup(news_content,'html.parser')

            #find all p elements
            news_ps = news_soup.find_all('p')

            #convert all paragraphs to a single string
            for news_p in news_ps:
                news_string = news_p.string
                if news_string is not None:
                    self.p_data += news_string

        #lower case all string data
        #seperate each word and put into an array
        data_list = self.p_data.split()
        #filter array with the condition that the word is less than 5 characters (largest ticker length seemed to be 5)
        data_list = filter(lambda x: (len(x)<=5), data_list)
        #create dictionary with count
        #this portion takes the longest

        with open('StonkData.csv',mode='r') as infile:
            reader = csv.reader(infile)
            with open ('temp.csv',mode='w') as outfile:
                write = csv.writer(outfile)
                myDict = {rows[0]: rows[1] for rows in reader}

        count_dict = {}
        for data in data_list:
            if data in myDict:
                self.word_count[data] = self.p_data.count(data)




