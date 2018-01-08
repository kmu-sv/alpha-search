import requests
from bs4 import BeautifulSoup
import json

url = input("[+} URL : ")

raw_code = requests.get(url).text

# Beautiful : Translate text to html
soup = BeautifulSoup(raw_code, "lxml")

data_dictionary = dict()

try:
    website = soup.select(".biz-website > a")[0].string
    data_dictionary["website"] = website
except Exception as ex: 
    data_dictionary["website"] = 'unknown'

moreinfo_dictionary = dict()

moreinfo = soup.select(".short-def-list > dl")
for info in moreinfo:
    attr_name, attr_content = "", ""
    for data in info.children:
        if data.name == "dt": #tag_name == dt
            attr_name = data.string.strip() # strip function removes contents in bracket.
        if data.name == "dd":
            attr_content = data.string.strip()
    moreinfo_dictionary[attr_name] = attr_content

data_dictionary["attributes"] = moreinfo_dictionary

print(json.dumps(data_dictionary, indent=4))


