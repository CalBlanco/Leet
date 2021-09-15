import spacy
from collections import Counter

#load spacey
nlp = spacy.load('en_core_web_trf')
nlp.max_length = 1000
BLACKLIST = ['🚀', '🚀 daily gme', 'repost', 'hf', 'keep going amc 2k', 'gme &', 'wsb']

def GenerateWordCount(word_count):
    text_str = ''

    if type(word_count) is str:
        text_str = word_count
    elif type(word_count) is list:
        for item in word_count:
            text_str += item
    else:
        print('Need a string or list of strings')
        return None

    if text_str:
        processes = get_orgs(text_str)
        return Counter(processes)




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