import requests
import pandas as pd
import spacy
from collections import Counter

'''Reddit API class

    @params:
        sub - The subreddit searched. example: 'r/wallstreetbets'
        listing - The type of post searched. example: 'hot', 'new', 'random', or 'rising' posts
        dataType - The type of data searched. example: 'title', 'selftext', or 'all'
        searchAmount - The amount of searches for each post. example: '100'
        headNum - gets n number of tickers to view (Just like in pandas)

'''


class StonkRedditAPI:
    def __init__(self, sub, listing, dataType='all', searchAmount=100, headNum=10):
        #
        self.sub = sub
        self.listing = listing
        self.dataType = dataType
        self.searchAmount = searchAmount
        self.headNum = headNum

        self.final = []

        CLIENT_ID = 'kmLjEwV4QdbwUg'
        SECRET_KEY = 'S02BLYQZfxR5CXgRRrzTFOlz2Ru_xg'

        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

        login_data = {
            'grant_type': 'password',
            'username': 'DRIGONER',
            'password': '@Th3F0rc3'
        }

        headers = {'User-Agent': 'MyAPI/0.0.1'}

        res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=login_data, headers=headers)

        TOKEN = res.json()['access_token']

        headers['Authorization'] = f'bearer {TOKEN}'

        res = requests.get(f'https://oauth.reddit.com/{self.sub}/{self.listing}', headers=headers,
                           params={'limit': f'{self.searchAmount}'})

        df = pd.DataFrame()

        self.word_data = ''

        for post in res.json()['data']['children']:
            title = post['data']['title']
            selftext = post['data']['selftext']
            out_str = title + " " + selftext + " "
            self.word_data += out_str
            #df = df.append({
            #    'subreddit': post['data']['subreddit'],
            #    'title': post['data']['title'],
            #    'selftext': post['data']['selftext'],
            #    'upvote_ratio': post['data']['upvote_ratio']
            #}, ignore_index=True)
        # Prints all the keys we can use to search and put inside the data frame

        # Model being used from Spacy
        nlp = spacy.load('en_core_web_trf')

        # Simple Blacklist until we train our own model.
        BLACKLIST = ['🚀', '🚀 daily gme', 'repost', 'hf', 'keep going amc 2k', 'gme &', 'wsb']

        def get_orgs(text):
            # process the text with our SpaCy model to get named entities
            doc = nlp(text)
            # initialize list to store identified organizations
            org_list = []
            # loop through the identified entities and append ORG entities to org_list
            for entity in doc.ents:
                if entity.label_ == 'ORG' and entity.text.lower() not in BLACKLIST:
                    org_list.append(entity.text)
            # if organization is identified more than once it will appear multiple times in list
            # we use set() to remove duplicates then convert back to list
            org_list = list(set(org_list))
            return org_list

        if self.dataType == 'all':

            df['organizations'] = df['title'].apply(get_orgs)
            title = df['organizations'].to_list()
            title = [org for sublist in title for org in sublist]

            df['organizations'] = df['selftext'].apply(get_orgs)
            selftext = df['organizations'].to_list()
            selftext = [org for sublist in selftext for org in sublist]

            self.org_freq = Counter(title) + Counter(selftext)
            self.final = dict(self.org_freq.most_common(self.headNum))

            print(self.sub, self.final)

            # Use this when putting data found into a csv file
            # df.to_csv('reddit.csv', sep='|', index=False)

        else:
            df['organizations'] = df[f'{self.dataType}'].apply(get_orgs)
            search = df['organizations'].to_list()
            search = [org for sublist in search for org in sublist]

            self.org_freq = Counter(search)
            self.final = dict(self.org_freq.most_common(self.headNum))

            print(self.sub, self.final)
