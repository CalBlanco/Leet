from StonkRedditAPI import StonkRedditAPI


test = StonkRedditAPI('r/wallstreetbets', 'hot', 'all', 100)
print('Results', test.word_count)
