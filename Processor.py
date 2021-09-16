import spacy
import math
from collections import Counter

# load spacey
nlp = spacy.load('en_core_web_trf')
nlp.max_length = 512
BLACKLIST = ['🚀', '🚀 daily gme', 'repost', 'hf', 'keep going amc 2k', 'gme &', 'wsb', 'yahoo finance',
             'the u.s. securities and exchange commission', 'sec', 'yahoo finance live', 'dow',
             'the commerce department\'s', 'the commerce department', 'the federal reserve'
             ]


def GenerateWordCount(word_data):
    '''
        @params:
            word_data : can be either string or a list of strings

        @return:
            word_count : counter object of found orgs

        @desc:
            Takes in a string or list of strings as input. Determine how many get_orgs() to run based on length of data.
            Iterate through the data and process it. Then use counters to determine a word count of found orgs.


    '''

    text_str = ''
    orgs = []

    if type(word_data) is str:
        text_str = word_data
    elif type(word_data) is list:
        for item in word_data:
            text_str += item
    else:
        print('Need a string or list of strings')

    if text_str:
        # get word count of string
        text_len = len(text_str.split(' '))
        maxW = nlp.max_length

        # calc number of iterations needed
        iterations = math.ceil(text_len / maxW)

        for i in range(iterations):
            # at the final iteration check from the last divisible position to the end of the string
            if i == iterations:
                orgs.append(get_orgs(text_str[(i * maxW):]))
            else:
                # calc lower and upper bound of string to meet word limit
                low_bound = i * maxW
                up_bound = (i + 1) * maxW
                orgs.append(get_orgs(text_str[low_bound:up_bound]))
    else:
        print('string not found in data')


    if orgs:

        word_count = Counter()
        for group in orgs:
            word_count += Counter(group)

        return word_count
    else:
        print('No orgs found in data')


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
