from bs4 import BeautifulSoup
from typing import Any, Dict


def scrape_rst_files():
    with open("earnings_airbnb.xml","r") as rst, open("rel_dump.rst", "w") as sink:
        contents = rst.read()
        soup = BeautifulSoup(contents, "lxml") #tags
        segment_tag = soup.find("segment")
        segment_tags = soup.find_all("segment") # tags #<class 'bs4.element.ResultSet'>
        group_tags = soup.find_all("group")
        #print(type(segment_tags[0]))
        """ segment_tags[0].text gets text"""
        segment_list = []
        rel_list = []
        for segment in segment_tags:
            segment_list.append(segment.text)
        for group in group_tags:
            rel_list.append(group.get("relname"))
    relations_dict = dict([(y,x+1) for x,y in enumerate(sorted(set(rel_list)))])
    num_labels = [relations_dict[x] for x in rel_list]
