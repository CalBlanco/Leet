from StonkRedditAPI import StonkRedditAPI
from YahooFinanceSearch import YahooFinanceSearch

WSB = StonkRedditAPI('r/wallstreetbets', 'new', 'all', 100)
WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100)
WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100)
print('r/wallstreetbets', WSB.word_count)
print('r/Wallstreetbetsnew', WSBN.word_count)
print('r/WallStreetbetsELITE', WSBE.word_count)

YahooFinanceSearch( 'reddit', WSB, WSBN, WSBE,)
