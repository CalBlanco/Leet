# Leet
 The goal of this program is to track and utilize data found from the news/reddit about hot stocks. 
 End game is to have something trading for us that will just be reading posts on WSB and yFinance. Currently this program finds word counts of stocks (or what it believes are stocks) and tracks the data. 

# Use Main.py not RedditScrapeEx.py for main operation 
---
 
## Important Classes
- news.py : newsScraper
- StonkRedditAPI.py : StonkRedditAPI
- DataTracker : Manager 

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
 This class uses the reddit API directly and runs it through the Spacy model `en_core_web_trf`. We are using the 'organizations' entity to find tickers and important terminology within subs.
- **Field Summary**
 
| Name         | Type    | Description                                                   | Example                          | Notes                                                             |
|--------------|---------|---------------------------------------------------------------|----------------------------------|-------------------------------------------------------------------|
| sub          | string  | Subreddit to be searched                                      | 'r/Wallstreetbetsnew'                            | Choose a sub from reddit to view                 |
| listing      | string  | The group of posts to be searched                             | 'hot', 'new', 'random', 'rising' | Categories of searches within reddit API                  |
| dataType     | string  | Tag for the data we want to look at                           | 'title', 'selftext', 'all'       | Only look at titles, selftext of a posr only look (Default - 'all') |
| searchAmount | int     | Number of searches to perform                                 | 100                              | The amount of searches for the listing. (Default - 100)                                                                  |                                                                 |
| headNum   | int | Amount of data to view | 10   | (Default is 10)                                                                  | 

- **Constructor Summary**
 
| Constructor                                                | Description                                                                                                                                                        |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| StonkRedditAPI(sub, listing, dataType='all', searchAmount=100, headNum=10) | sub, and listing are required while dataType, searchAmount, and headNum have default values. Parameters are specified above. |
  
 
- **Method Summary**
 
| Name                                            | Description                                                                                                                                                        |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| get_orgs(text) | Loads Spacy model `en_core_web_trf` and processes all the data taken from the reddit API into a list to be filtered by the model. and returns the list of organizations found. |
---
 
### Manager
- **Description** :
 `This class is used to store our count data over longer periods of time. For each symbol that is found the Manager will first combine all lists of found symbols and counts, then create or append a file for each individual symbol. It is also able to read the count data for any symbols in our database`
- **Field Summary**
 
 | Name | Type   | Description                                      | Example                     | Notes                                                                                                                      |
|------|--------|--------------------------------------------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------|
| root | string | The root directory to store all of the data into | 'StockData' or 'DataFolder' | Create this folder before hand or there will be issues. The read method is only able to read from data in the root folder. |
 
 
- **Method Summary**
 
 
 | Name         | Return Type | Parameters  | Parameter Types    | Description                                                                                                                           | Example                                                                 | Notes                                                                                                                                              |
|--------------|-------------|-------------|--------------------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| storeDict(dict)    | void        | inDict      | Counter/Dictionary | Takes an input list of counters containing (symbol,count) and then appends the count data to a file for that symbol                   | let someCounter = {'a':2,'b':3,...'z':n}, storeDict(someCounter)        | Bread and butter of this class.                                                                                                                    |
| storeDataSet(list) | void        | listOfDicts | List               | Takes in a list of counter objects. Merges them together so there are no duplicates, and then runs storeDict() on the merged counter. | let li = [someCounter,someCounter1, ... someCounterN], storeDataSet(li) | Caller of the storeDict method                                                                                                                     |
| readData(str)     | List        | symbol      | string             | Looks through the root folder for the given symbols data. Then returns the tracked data.                                              | readData('AMC') or readData('GE')                                       | This only works if the files are in the root folder. If you are in a new root, or you have not tracked the symbol yet then it will return an error |

 
---
 
 ## Main.py
 
 - **Description**
 ``` Main driver for the application. Has a UI to run the scrapers and data collection, and also allows for viewing of the collected data```
 
 - **Method Summary**
 
 | Name             | Return   | Params | Param Type | Description                                                                                                       | Example                                                                         | Notes                                                                       |
|------------------|----------|--------|------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| runSingle()      | void     | none   | N.A        | Runs a single instance to collect data via news.py and StonkRedditAPI.py.                                         | N.A                                                                             | This function controls what is used in the runInBack function               |
| runInBack()      | void     | none   | N.A        | Runs a runSingle() over a specified time period and frequency                                                     | N.A                                                                             |                                                                             |
| look()           | void     | none   | N.A        | Allows user input to look at collected data                                                                       | N.A                                                                             | Going to improve this to show collected symbols and then let user pick      |
| changeSettings() | void     | none   | N.A        | Nothing yet, but plan is to let user add/change what scrapers are used to fine tune the data collection if wanted | N.A                                                                             |                                                                             |
| processCMD       | function | input  | str,char   | There is a command dictionary, the input is the key for the function to be executed in the dictionary             | let CMDS = {'a':doSomething,'b':doAnotherThing}, processInp('a') -> doSomething | Helpful and fun thing. Happy I found this and I want to use this style more |
| printMenu()      | void     | none   | N.A        | Prints all the available options, then based on input it will run one of the above functions                      |                                                                                 |                                                                             |
 
 
 
