from bs4 import BeautifulSoup
from typing import Any, Dict


def scrape_rst_files():
    with open("pubmed_abstract.xml","r") as rst, open("rel_dump.rst", "w") as sink:
        contents = rst.read()
        soup = BeautifulSoup(contents, "lxml")
        segment_tags = soup.find_all("segment") # tags
        group_tag_list = soup.find_all("group")
        for segment in segment_tags:
            segment_tuples = [(segment.getText(),segment.get("relname"),segment.get("id"),segment.get("parent")) for segment in segment_tags]
        sorted_segment_tuples = sorted(segment_tuples,key=lambda tup: tup[2])
        print("segment labels: ",sorted_segment_tuples)
        for group in group_tag_list:
            group_tuples = [(group.get("relname"),group.get("id"),group.get("parent")) for group in group_tag_list]
        sorted_group_tuples = sorted(group_tuples,key=lambda tup: tup[2])
        print("group labels: ", sorted_group_tuples)
scrape_rst_files()
