from bs4 import BeautifulSoup
from typing import Any, dict

""" takes an xml markup file as input and returns a dict with relation names as keys and text as values """

def scrape_rst_files(file: Any) --> dict:
    with open("abnb_lots_of_labels.xml","r") as rst, open("rel_dump.rst", "w") as sink:
        contents = rst.read()
        soup = BeautifulSoup(contents, "lxml")
        relation_tag = soup.find("segment")
        relation_tags = soup.find_all("segment") #tags
        data_dict = {}
        for relation_tag in relation_tags:
        #print(relation_tag)
            if len(relation_tag.attrs) == 3:
                data_dict[relation_tag["relname"]] = relation_tag.text
    return(data_dict)
