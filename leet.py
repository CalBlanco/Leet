import requests
from bs4 import BeautifulSoup



# takes 3 args
# 1: url for website
# 2: the seperator (what distinguishes certain links)
# 3: the tolerance for the position of that seperator
# returns : a list of all paragraphs from articles found in the main website
def newsFilter(url, sep, tolerance):
    main_request = requests.get(url) #get content from main site
    main_content = main_request.content #create content variable

    main_soup = BeautifulSoup(main_content, 'html.parser') # turn to soup
    links = main_soup.find_all('a') # search soup for all <a> elements

    # seperate the men from the boys

    applicable_content = [] #creating empty lists for the data i want to output
    para_content = []
    for link in links:
        url = link.get('href') #get the href attributes from each <a>

        if url.find(sep) >= tolerance: #this line finds the seperating term and makes sure its position is greater than the tolerance
            applicable_content.append(url) #append to applicable list if meets conditions

    for content in applicable_content:
        child_request = requests.get(content) #make request to each link from applicable[]
        child_content = child_request.content #create variable for content from req
        child_soup = BeautifulSoup(child_content, 'html.parser') #create soup

        child_para = child_soup.find_all('p') #sort soup for <p> tags

        micro_content = [] # empty list
        for para_raw in child_para:
            para_str = para_raw.string # extract data from inside <p></p>
            micro_content.append(para_str) # add that string to a list
        para_content.append(micro_content) # add ^ list to a parent list

    return para_content #return the parent list


# this function can really only be used in tandem with newsFilter()
def wordsFromFilter(parent_list):
    super = [] #super list for the words
    super_str = "" #messing around with outputing this as a string
    for child in parent_list:
        sub = []
        sub_str = ""
        for p_element in child:
            if p_element is not None:
                words = p_element.lower().split()
                sub.append(words)
                for word in words:
                    sub_str += word + " "
        super.append(sub)
        super_str += sub_str + "\n"
    return super_str


# takes a count of each word and deposits it into a dict with the key being the word itself
# need to find a way to easily filter the strings
def wordListToDict(str):
    count_dict = {}
    str = str.lower()
    for words in str.split():
        if words != "a" and words != "the" and words != "on" and words !="of" and words !="an" and words!="we":
            count_dict[words] = str.count(words)

    return count_dict




test = newsFilter('https://finance.yahoo.com/','news',10)
print("Elements of main filter")
for t in test:
    print(t)

print("\n Word lists from main filter")
test_2 = wordsFromFilter(test)
print(test_2[0])

print("\n Word Counter Dictionaries")
test_3 = wordListToDict(test_2)
print(test_3)




