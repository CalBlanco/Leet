import requests
import pandas as pd
import csv


'''Reddit API class

    @params:
        sub - The subreddit wanted to be searched example: 'r/wallstreetbets'
        listing - The type of data that is wanting to be searches. example: 'hot', 'new', 'random', or 'rising' posts
        dataType - The type of data that is wanting to be searched example: 'title', 'selftext', or 'all'
        searchAmount - The amount of searches you want to search in the specific category in the listings argument example: '100'
            
'''

class StonkRedditAPI:
    def __init__(self, sub, listing, dataType,searchAmount):
        #
        self.sub = sub
        self.listing = listing
        self.dataType = dataType
        self.searchAmount = searchAmount

        #for data processing and comparrison
        self.p_data = ''
        self.word_count = {}

        #adds the items from the data fram into a string
        def addToString():
            for redd_p in search:
                redd_string = redd_p
                if redd_string is not None:
                    self.p_data += redd_string

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

        res = requests.get(f'https://oauth.reddit.com/{self.sub}/{self.listing}', headers=headers, params={'limit': f'{self.searchAmount}'})

        df = pd.DataFrame()
        for post in res.json()['data']['children']:
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio']
            }, ignore_index=True)
        #Prints all the keys we can use to search and put inside the data frame
        print(post['data'].keys())


        print(df,'\n')

        #search both title and selftext of the post, otherwise only the specific part of the post
        if self.dataType == 'all':
            search = df['title']
            addToString()
            search = df['selftext']
            addToString()
        else:
            search = df[f'{self.dataType}']
            addToString()



        # separate each word and put into an array
        data_list = self.p_data.split()
        # filter array with the condition that the word is less than 5 characters (largest ticker length seemed to be 5)
        data_list = filter(lambda x: (len(x) <= 5), data_list)

        #compares the the string to the data in the dictionary
        with open('StonkData.csv', mode='r') as infile:
            reader = csv.reader(infile)
            with open('temp.csv', mode='w') as outfile:
                write = csv.writer(outfile)
                myDict = {rows[0]: rows[1] for rows in reader}

        for data in data_list:
            if data in myDict:
                self.word_count[data] = self.p_data.count(data)

