import requests
from bs4 import BeautifulSoup



# takes 3 args
# 1: url for website
# 2: the seperator (what distinguishes certain links)
# 3: the tolerance for the position of that seperator
# returns : a list of all paragraphs from articles found in the main website
def newsFilter(url, sep, tolerance):
    main_request = requests.get(url)
    main_content = main_request.content

    main_soup = BeautifulSoup(main_content, 'html.parser')
    links = main_soup.find_all('a')

    # seperate the men from the boys

    applicable_content = []
    para_content = []
    for link in links:
        url = link.get('href')

        if url.find(sep) >= tolerance:
            applicable_content.append(url)

    for content in applicable_content:
        child_request = requests.get(content)
        child_content = child_request.content
        child_soup = BeautifulSoup(child_content, 'html.parser')

        child_para = child_soup.find_all('p')

        micro_content = []
        for para_raw in child_para:
            para_str = para_raw.string #<p id=asdasda attr=>asdasdasd</p> into asdasdasd
            micro_content.append(para_str) # add that string to a list
        para_content.append(micro_content) # add ^ list to a parent list

    return para_content


def wordsFromFilter(parent_list):
    super = []
    super_str = []
    for child in parent_list:
        sub = []
        sub_str = ""
        for p_element in child:
            if p_element is not None:
                words = p_element.split()
                sub.append(words)
                for word in words:
                    sub_str += word + " "
        super.append(sub)
        super_str.append(sub_str)
    return super_str


test = newsFilter('https://finance.yahoo.com/','news',10)
print("Elements of main filter")
for t in test:
    print(t)

print("\n Word lists from main filter")
test_2 = wordsFromFilter(test)

for item in test_2:
    print(item)


some_str = "BOB EATS ALL THE BURGERS "




