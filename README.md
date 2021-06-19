# Leet
 The goal of this program is to track and utilize data found from the news/reddit about hot stocks. 
 End game is to have something trading for us that will just be reading posts on WSB and yFinance. Currently this program finds word counts of stocks (or what it believes are stocks) and tracks the data. 

---
 
## Important Classes
- news.py : newsScraper
- StonkRedditAPI.py : StonkRedditAPI
- DataTracker (lots of issues here)

---

## Class Descriptions

### newsScraper
- **Description** :
 `This class is used for finding word counts from news websites that do not have APIs. The flow of this class is as follows. Input a link to the root of a financial news site(Parent link). From that link find any additional links containing the seperator at or after the given tolerance. Visit each Child link and temporarily store all of the <p> tag data. Using the tag data and a CSV containing known symbols find and count every use of any symbol. Do this for every child link and then create a counter object called word_count that contains the final representation of the data found.`
- **Field Summary**

| Name       | Type    | Description                                                                                                                                    | Example                                                                                                                                   | Notes                                                                                                                                                          |
|------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| url        | string  | URL for the root of a news website                                                                                                             | https://finance.yahoo.com/                                                                                                                | Core variable, this class will not work without                                                                                                                |
| sep        | string  | Separating Value that helps the bot determine the structure of the news site                                                                   | Yahoo uses /news/ for all its articles so 'news' would be the separator                                                                   | Core Variable                                                                                                                                                  |
| tol        | int     | Short for tolerance. This determines how far into the URL it will look for the separating value                                                | https://finance.yahoo.com/news/were-changing-the-face-of-what-a-software-engineer-looks-like-google-diversity-officer-164158184.html. tol=10 | Will most likely be removed                                                                                                                                    |
| nickname   | string  | Used to determine the file name for a graph                                                                                                    | 'yahoo' or 'yf'                                                                                                                           | This variable is actually useless and I'm going to remove it                                                                                                   |
| debug      | bool    | If true news.py will print out its actions                                                                                                     |                                                                                                                                           | Handy for debugging. Pretty straight forward                                                                                                                   |
| news_links | list    | List of all news links found on the root site using the separator and tolerance variables                                                      | [link1,link2,link3,...,linkn]                                                                                                             | First BS4 use. Puts all found news links that meet the separator and tolerance requirements                                                                    |
| p_data     | string  | All the <p> tags from the links in news_links converted into strings                                                                           | "entire news article 1, entire news article 2, ... entire news article n"                                                                 | This is not a very useful field to view but it is relevant to the overall data produced and I used it a few times during debugging so it is not fully useless. |
| quotes     | list    | This is specific to YahooFinnances website structure. There are some random tickers included in the articles that are separate from the p_data | ["SYMB1, "SYMB2",... "SYMBN"]                                                                                                             | Only helpful for yahoo news links                                                                                                                              |
| word_count | Counter | Counts the amount of times a stock was mentioned in all of the articles.                                                                       | ("SYMB1" : 20, "SYMB2" : 3, ... "SYMBn" : k)                                                                                              |                                                                                                                                                                |

- **Constructor Summary**

| Constructor                                                | Description                                                                                                                                                        |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| newsScraper(url,sep,tol=10,nickname="example", debug=True) | url and separator must be set. While tol, nickname, and debug all have default values. The field summary is listed above but this constructor is straight forward. |
 
 
- **Method Summary**
`There are no methods in this class. Everything is done on initialization`
---
### StonkRedditAPI.py
- **Description** :
 This class uses the reddit API directly to find a word count for stocks. Adrien I would love if you edited this with more info.
- **Field Summary**
 
| Name         | Type    | Description                                                   | Example                          | Notes                                                             |
|--------------|---------|---------------------------------------------------------------|----------------------------------|-------------------------------------------------------------------|
| sub          | string  | Subreddit to be searched                                      | 'wsb'                            | Adrien im gonna ask you to do the notes for these                 |
| listing      | string  | The group of posts to be searched                             | 'hot', 'new', 'random', 'rising' | I think these are all the options for this field                  |
| dataType     | string  | Tag for the data we want to look at                           | 'title', 'selftext', 'all'       | Only look at titles, only look at the text, or look at everything |
| searchAmount | int     | number of searches to perform                                 | 100                              |                                                                   |
| p_data       | string  | Used to store raw string data from the searches               |                                  |                                                                   |
| word_count   | Counter | Used with p_data to determine what data is relevant to stonks |                                  |                                                                   | 

- **Constructor Summary**
- **Method Summary**
---
