from StonkRedditAPI import StonkRedditAPI
from YahooFinanceSearch import YahooFinanceSearch

test1 = StonkRedditAPI('r/wallstreetbets', 'hot', 'all', 100)
test2 = StonkRedditAPI('r/Wallstreetbetsnew', 'hot', 'all', 100)
test3 = StonkRedditAPI('r/WallStreetbetsELITE', 'hot', 'all', 100)
print('r/wallstreetbets', test1.word_count)
print('r/Wallstreetbetsnew', test2.word_count)
print('r/WallStreetbetsELITE', test3.word_count)

yahoo_test = YahooFinanceSearch( 'reddit', test1, test2, test3,)
