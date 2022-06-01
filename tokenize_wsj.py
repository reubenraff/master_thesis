#!/usr/bin/env python
import csv
from transformers import BertTokenizer
#with open("wsj_tsv.tsv") as source:

#labels = []
#with open("wsj_data.tsv") as source:
    #tsv_file = csv.reader(source, delimiter="\t")
    #(label, sent1, sent2) = tsv_file

import csv
with open("wsj_tsv.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    all_pairs = []
    for line in tsvreader:
        sentence_pairs = line[1:]
        all_pairs.append(sentence_pairs)
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    input_ids = tokenizer(all_pairs[1], max_length=50, padding="max_length", truncation=True, return_tensors="tf")
    print("List of pairs", input_ids)
""" #TODO """

"""


input_ids = tokenizer([["hey hello there", "what is going on"], ["peter is in the", "what is going on"]], max_length=20, padding="max_length", truncation=True, return_tensors="tf")

print("List of pairs", input_ids)
"""
