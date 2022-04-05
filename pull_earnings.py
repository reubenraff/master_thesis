#!/usr/bin/env python
import argparse
import concurrent.futures
from bs4 import BeautifulSoup
import multiprocessing
import time
from sec_edgar_downloader import Downloader
from unicodedata import normalize
import re
import requests
import string






def pull_earnings_call(seconds):
    url = "https://seekingalpha.com/article/4494623-airbnb-inc-abnb-ceo-brian-chesky-presents-morgan-stanley-2022-technology-media-and-telecom"
    request = requests.get(url)
    earnings_html = request #HTML
    #ABNB_html_page = "SEC_data/ABNB/ABNB/sec-edgar-filings/ABNB/10-K/0001559720-21-000010/filing-details.html"
    with open("earnings_text.html", "r") as source, open("earnings_text.doc","w+") as sink:
        soup = BeautifulSoup(source, 'html.parser', from_encoding="utf-8") #this encoding thing should get rid of all unicode
        conversation_spans = soup.select("p", {'class':"paywall-full-content"})
        paragraphs = []
        for paragraph in conversation_spans:
            paragraphs.append(str(paragraph))
        for element in paragraphs:
            string_convo = " ".join(element for element in paragraphs)
            span = '</span></strong></p> <p class="paywall-full-content">'
            split_string = string_convo.split(span)
            for line in split_string:
                print(line, file=sink)
pull_earnings_call(4)



#mulitprocessing
if __name__ == "__main__":
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        #secs = [5,4,3,2,1] #, secs
        results = executor.map(pull_earnings_call) # call the function that handles all the text here
        #for result in results:
        #    print(result)
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start, 2)} second(s)")
