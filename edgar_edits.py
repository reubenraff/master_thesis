#!/usr/bin/env python
import argparse
import concurrent.futures
from bs4 import BeautifulSoup
import multiprocessing
import time
from sec_edgar_downloader import Downloader
from unicodedata import normalize
import re
import string





def pull_sec_data(seconds):
    downloader = Downloader("ABNB_S1")

    # downloader.get("S-1", "ABNB",include_amends=True)

    TGT_html_page = "sec-edgar-filings/TGT/10-K/0000027419-17-000008/filing-details.html"
    AMZN_html_page  = "sec-edgar-filings/AMZN/10-K/0001018724-17-000011/filing-details.html"
    WMT_html_page = "sec-edgar-filings/sec-edgar-filings/WMT/10-K/0000104169-20-000011/filing-details.html"
    ABNB_html_page = "SEC_data/ABNB/ABNB/sec-edgar-filings/ABNB/10-K/0001559720-21-000010/filing-details.html"
    ABNB_S1_html = "/Users/reubenraff/Projects/master_thesis/SEC_data/ABNB_S1/sec-edgar-filings/ABNB/S-1/0001193125-20-306257/filing-details.html"
    with open(TGT_html_page, "r") as source1, open("target_10K.doc","w+") as sink:
        pass
        #soup1 = BeautifulSoup(source1, 'html.parser')
        #tgt_text = soup1.find_all(text=True)
        #print(tgt_text, file=sink)

        #string1_text = " "
        #for words in tgt_text:
        #    string1_text += words
    #pattern = re.compile(r'x\.+')
    #clean_text1 = re.sub(pattern, "", string1_text)
    #print(clean_text1,file=sink1)

    ABNB_html_page = "/Users/reubenraff/Projects/master_thesis/SEC_data/ABNB_S1/sec-edgar-filings/ABNB/S-1/0001193125-20-306257/filing-details.html"
    #ABNB_html_page = "SEC_data/ABNB/ABNB/sec-edgar-filings/ABNB/10-K/0001559720-21-000010/filing-details.html"
    with open(ABNB_html_page, "r") as source1, open("abnb_stripper_hack.doc","w+") as sink1:
        soup = BeautifulSoup(source1, 'html.parser', from_encoding="utf-8") #this encoding thing should get rid of all unicode
        abnb_text = soup.find_all(text=True)
        for line in abnb_text:
            if re.search(r'\S', line):
                clean_str = " ".join(str(line).split())
                print(f"{''.join([word for word in clean_str]): <20}", file=sink1)
pull_sec_data(4)




#mulitprocessing
if __name__ == "__main__":
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [5,4,3,2,1] #, secs
        results = executor.map(pull_sec_data,secs) # call the function that handles all the text here
        #for result in results:
        #    print(result)
        finish = time.perf_counter()
        print(f"Finished in {round(finish-start, 2)} second(s)")
